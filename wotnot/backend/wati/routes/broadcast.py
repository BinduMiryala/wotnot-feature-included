from fastapi import APIRouter, Depends, HTTPException, Request, Query, status
from fastapi.responses import PlainTextResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc, cast, String
from datetime import datetime
from typing import AsyncGenerator
import httpx
import json
import asyncio
import logging

from ..models import Broadcast, ChatBox
from ..models.ChatBox import Last_Conversation, Conversation
from ..Schemas import chatbox, user
from ..database import database
from ..oauth2 import get_current_user

router = APIRouter(tags=['Broadcast'])

WEBHOOK_VERIFY_TOKEN = "12345"  # Replace with your verification token


# --------------------- Meta Webhook ---------------------
@router.get("/meta-webhook")
async def verify_webhook(request: Request):
    """Verify WhatsApp webhook subscription"""
    verify_token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    hubmode = request.query_params.get("hub.mode")

    if verify_token == WEBHOOK_VERIFY_TOKEN and hubmode == "subscribe":
        return PlainTextResponse(content=challenge, status_code=200)
    raise HTTPException(status_code=403, detail="Verification token mismatch")


@router.post("/meta-webhook")
async def receive_meta_webhook(request: Request, db: AsyncSession = Depends(database.get_db)):
    """Receive WhatsApp webhook events"""
    try:
        body = await request.json()
        if "entry" not in body:
            raise HTTPException(status_code=400, detail="Invalid webhook format")

        for event in body.get("entry", []):
            for change in event.get("changes", []):
                value = change.get("value")
                if not value:
                    continue

                # Process message statuses
                for status_msg in value.get("statuses", []):
                    await process_status(status_msg, db)

                # Process incoming messages
                if "messages" in value:
                    await handle_incoming_messages(value, db)

        return {"message": "Webhook data processed successfully"}
    except Exception as e:
        logging.error(f"Error processing webhook: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


# --------------------- Process Message Status ---------------------
async def process_status(status_msg: dict, db: AsyncSession):
    wamid = status_msg.get("id")
    message_status = status_msg.get("status")
    message_read = message_delivered = message_sent = False
    error_reason = None

    if message_status == "read":
        message_read = message_delivered = message_sent = True
    elif message_status == "delivered":
        message_delivered = message_sent = True
    elif message_status == "sent":
        message_sent = True
    elif message_status == "failed":
        if status_msg.get("errors"):
            err = status_msg["errors"][0]
            details = err.get("error_data", {}).get("details", "No details")
            error_reason = f"Error Code: {err.get('code','N/A')}, Title: {err.get('title','N/A')}, Details: {details}"

    if wamid:
        result = await db.execute(select(Broadcast.BroadcastAnalysis).filter(Broadcast.BroadcastAnalysis.message_id == wamid))
        broadcast_report = result.scalars().first()
        if broadcast_report:
            broadcast_report.read = message_read
            broadcast_report.delivered = message_delivered
            broadcast_report.sent = message_sent
            broadcast_report.status = message_status
            if error_reason:
                broadcast_report.error_reason = error_reason
            db.add(broadcast_report)
            await db.commit()


# --------------------- Handle Incoming Messages ---------------------
async def handle_incoming_messages(value: dict, db: AsyncSession):
    name = value["contacts"][0]["profile"]["name"]
    phone_number_id = value["metadata"]["phone_number_id"]

    for message in value["messages"]:
        wa_id = message["from"]
        message_id = message["id"]
        message_content = message.get("text", {}).get("body", "")
        timestamp = int(message["timestamp"])
        message_type = message["type"]
        context_message_id = message.get("context", {}).get("id")
        utc_time = datetime.utcfromtimestamp(timestamp)

        # Remove old Last_Conversation
        result = await db.execute(select(Last_Conversation).filter(
            Last_Conversation.sender_wa_id == wa_id,
            Last_Conversation.receiver_wa_id == phone_number_id
        ))
        last_conversation = result.scalars().first()
        if last_conversation:
            await db.delete(last_conversation)
            await db.commit()

        # Insert new Last_Conversation
        last_conv = Last_Conversation(
            business_account_id=value["metadata"].get("business_account_id", "unknown"),
            message_id=message_id,
            message_content=message_content,
            sender_wa_id=wa_id,
            sender_name=name,
            receiver_wa_id=phone_number_id,
            last_chat_time=utc_time,
            active=True
        )
        db.add(last_conv)
        await db.commit()

        # Insert into Conversation
        conversation = Conversation(
            wa_id=wa_id,
            message_id=message_id,
            phone_number_id=int(phone_number_id),
            message_content=message_content,
            timestamp=utc_time,
            context_message_id=context_message_id,
            message_type=message_type,
            direction="Receive"
        )
        db.add(conversation)
        await db.commit()


# --------------------- Helpers ---------------------
def convert_to_dict(instance):
    if instance is None:
        return None
    data = {}
    for key, value in instance.__dict__.items():
        if not key.startswith("_"):
            data[key] = value.isoformat() if isinstance(value, datetime) else value
    return data


# --------------------- SSE Conversations ---------------------
@router.get("/sse/conversations/{contact_number}")
async def event_stream(contact_number: str, request: Request, token: str = Query(...), db: AsyncSession = Depends(database.get_db)) -> StreamingResponse:
    current_user = await get_current_user(token, db)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    async def get_conversations() -> AsyncGenerator[str, None]:
        last_data = None
        while True:
            result = await db.execute(
                select(Conversation)
                .filter(Conversation.wa_id == contact_number)
                .filter(Conversation.phone_number_id == current_user.Phone_id)
                .order_by(Conversation.timestamp)
            )
            conversations = result.scalars().all()
            conversation_data = [convert_to_dict(c) for c in conversations]
            if conversation_data != last_data:
                yield f"data: {json.dumps(conversation_data)}\n\n"
                last_data = conversation_data
            if await request.is_disconnected():
                break
            await asyncio.sleep(2)

    return StreamingResponse(get_conversations(), media_type="text/event-stream")


# --------------------- SSE Active Conversations ---------------------
@router.get("/active-conversations")
async def get_active_conversations(request: Request, token: str = Query(...), db: AsyncSession = Depends(database.get_db)) -> StreamingResponse:
    current_user = await get_current_user(token, db)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    async def get_active_chats() -> AsyncGenerator[str, None]:
        last_active_chats = None
        while True:
            if await request.is_disconnected():
                break
            result = await db.execute(
                select(Last_Conversation)
                .filter(cast(Last_Conversation.receiver_wa_id, String) == str(current_user.Phone_id))
                .order_by(desc(Last_Conversation.last_chat_time))
            )
            active_chat_data = [convert_to_dict(c) for c in result.scalars().all()]
            if active_chat_data != last_active_chats:
                last_active_chats = active_chat_data
                yield f"data: {json.dumps(active_chat_data)}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(get_active_chats(), media_type="text/event-stream")


# --------------------- Send Text Message ---------------------
@router.post("/send-text-message/")
async def send_message(payload: chatbox.MessagePayload, db: AsyncSession = Depends(database.get_db), current_user: user.newuser = Depends(get_current_user)):
    whatsapp_url = f"https://graph.facebook.com/v20.0/{current_user.Phone_id}/messages"
    headers = {"Authorization": f"Bearer {current_user.PAccessToken}", "Content-Type": "application/json"}
    data = {"messaging_product": "whatsapp", "to": payload.wa_id, "type": "text", "text": {"body": payload.body}}

    async with httpx.AsyncClient() as client:
        response = await client.post(whatsapp_url, headers=headers, json=data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    response_data = response.json()
    conversation = Conversation(
        wa_id=payload.wa_id,
        message_id=response_data.get("messages", [{}])[0].get("id", "unknown"),
        phone_number_id=current_user.Phone_id,
        message_content=payload.body,
        timestamp=datetime.utcnow(),
        context_message_id=None,
        message_type="text",
        direction="Sent"
    )
    db.add(conversation)
    await db.commit()
    return {"status": "Message sent", "response": response_data}
