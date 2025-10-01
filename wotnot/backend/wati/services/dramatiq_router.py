from fastapi import APIRouter, HTTPException, Depends
from dramatiq import Message
from ..models import Broadcast
from ..Schemas import broadcast, user
from ..oauth2 import get_current_user
from .tasks import send_broadcast
from datetime import datetime
from dramatiq import Message
from ..database import database
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter()

@router.post("/schedule-template-message/")
async def schedule_template_message(
    request: broadcast.input,
    db: AsyncSession = Depends(database.get_db),
    get_current_user: user.newuser = Depends(get_current_user)
):
    contacts = [{"name": contact.name, "phone": contact.phone} for contact in request.recipients]

    # Convert scheduled_time to a timezone-naive datetime object
    scheduled_datetime = datetime.fromisoformat(request.scheduled_time.replace("Z", "")).replace(tzinfo=None)

    # Get current time in UTC (timezone-naive)
    now = datetime.utcnow()

    # Calculate delay in seconds
    delay = (scheduled_datetime - now).total_seconds()

    if delay < 0:
        raise HTTPException(status_code=400, detail="Scheduled time must be in the future.")

    # Create a new broadcast list entry
    broadcast_list = Broadcast.BroadcastList(
        user_id=get_current_user.id,
        name=request.name,
        template=request.template,
        contacts=[contact.phone for contact in request.recipients],
        type=request.type,
        success=0,
        failed=0,
        status="Scheduled",
        scheduled_time=scheduled_datetime  # Store timezone-naive datetime
    )

    # Add broadcast list entry asynchronously
    db.add(broadcast_list)
    await db.commit()
    await db.refresh(broadcast_list)

    saved_broadcast_id = broadcast_list.id

    # API details
    API_url = f"https://graph.facebook.com/v20.0/{get_current_user.Phone_id}/messages"
    headers = {
        "Authorization": f"Bearer {get_current_user.PAccessToken}",
        "Content-Type": "application/json"
    }

    # Schedule the task with the calculated delay
    task: Message = send_broadcast.send_with_options(
        args=[request.template, request.template_data, contacts, saved_broadcast_id, API_url, headers, get_current_user.id, request.image_id, request.body_parameters,get_current_user.Phone_id],
        delay=delay * 1000  # delay in milliseconds
    )

    # Update the broadcast list entry with the task ID asynchronously
    result = await db.execute(
        select(Broadcast.BroadcastList).filter(Broadcast.BroadcastList.id == saved_broadcast_id)
    )
    broadcast_log_task_id = result.scalars().first()

    if not broadcast_log_task_id:
        raise HTTPException(status_code=404, detail="Broadcast not found")

    broadcast_log_task_id.task_id = task.message_id
    db.add(broadcast_log_task_id)
    await db.commit()
    await db.refresh(broadcast_log_task_id)

    # Return success message
    return {
        "message": f"Message {saved_broadcast_id} scheduled to be sent at {request.scheduled_time}.",
        "task_id": task.message_id
    }
