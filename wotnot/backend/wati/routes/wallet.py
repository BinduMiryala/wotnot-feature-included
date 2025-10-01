from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
import requests
from datetime import datetime
from ..oauth2 import get_current_user
from ..Schemas import user  
from ..database import database 
import logging
from ..models import User
from typing import Optional
router = APIRouter(tags=['Wallet'])
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
import requests
import logging

 # Ensure `get_async_db` provides AsyncSession

 # Assuming you have this dependency

router = APIRouter()

@router.get("/conversation-analytics/{account_id}")
async def get_conversation_analytics(account_id: int, db: AsyncSession = Depends(database.get_db), get_current_user: user.newuser = Depends(get_current_user)):
    ACCESS_TOKEN = get_current_user.PAccessToken

    # Fetch account creation time asynchronously
    result = await db.execute(select(User.User).filter(User.User.WABAID == account_id))
    account_creation_time = result.scalars().first()
    
    if not account_creation_time:
        raise HTTPException(status_code=404, detail="Account not found")

    since = int(account_creation_time.created_at.timestamp())
    until = int(datetime.now().timestamp())

    url = f"https://graph.facebook.com/v20.0/{account_id}?fields=conversation_analytics.start({since}).end({until}).granularity(DAILY).phone_numbers([]).dimensions([\"CONVERSATION_CATEGORY\",\"CONVERSATION_TYPE\",\"COUNTRY\",\"PHONE\"])"

    response = requests.get(url, params={"access_token": ACCESS_TOKEN})
    logging.info(response)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("error", "Error fetching data"))

    return response.json()


@router.get("/conversation-cost-history/")
async def get_conversation_cost_history(
    
    start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format"),
    db: AsyncSession = Depends(database.get_db),
    get_current_user: user.newuser = Depends(get_current_user),
):
    ACCESS_TOKEN = get_current_user.PAccessToken

    # Fetch account creation time asynchronously
    result = await db.execute(select(User.User).filter(User.User.WABAID == get_current_user.WABAID))
    account_creation_time = result.scalars().first()
    
    if not account_creation_time:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Default date range to account creation time and current time if not provided
    since = int(account_creation_time.created_at.timestamp())
    until = int(datetime.now().timestamp())

    if start_date:
        try:
            since = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format, expected YYYY-MM-DD")
    
    if end_date:
        try:
            until = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format, expected YYYY-MM-DD")
    
    if since > until:
        raise HTTPException(status_code=400, detail="start_date cannot be after end_date")

    # Build the URL for the API request
    url = f"https://graph.facebook.com/v20.0/{get_current_user.WABAID}?fields=conversation_analytics.start({since}).end({until}).granularity(DAILY).phone_numbers([]).dimensions([\"CONVERSATION_CATEGORY\",\"CONVERSATION_TYPE\",\"COUNTRY\",\"PHONE\"])"
    
    # Make the request to the external API
    response = requests.get(url, params={"access_token": ACCESS_TOKEN})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("error", "Error fetching data"))
    
    conversation_data = response.json().get("conversation_analytics", {}).get("data", [])
    processed_data = []

    # Process the data
    for data_entry in conversation_data:
        data_points = data_entry.get("data_points", [])
        for point in data_points:
            start_time = datetime.utcfromtimestamp(point["start"]).strftime('%Y-%m-%d %H:%M:%S')
            end_time = datetime.utcfromtimestamp(point["end"]).strftime("%Y-%m-%d %H:%M:%S")
            cost = point.get("cost")
            conversation_type = point.get("conversation_type")
            conversation_category = point.get("conversation_category")

            processed_data.append({
                "start_time": start_time,
                "end_time": end_time,
                "cost": cost,
                "conversation_type": conversation_type,
                "conversation_category": conversation_category
            })

    return {"conversation_analytics": processed_data}


@router.get("/conversations-cost/{account_id}")
async def get_conversation_costs(account_id: int, db: AsyncSession = Depends(database.get_db), get_current_user: user.newuser = Depends(get_current_user)):
    ACCESS_TOKEN = get_current_user.PAccessToken

    # Fetch account details asynchronously
    result = await db.execute(select(User.User).filter(User.User.WABAID == account_id))
    account_details = result.scalars().first()
    
    if not account_details:
        raise HTTPException(status_code=404, detail="Account not found")

    since = int(account_details.created_at.timestamp())
    until = int(datetime.now().timestamp())

    url = f"https://graph.facebook.com/v20.0/{account_id}?fields=conversation_analytics.start({since}).end({until}).granularity(DAILY).phone_numbers([]).dimensions([\"CONVERSATION_CATEGORY\",\"CONVERSATION_TYPE\",\"COUNTRY\",\"PHONE\"])"
    
    response = requests.get(url, params={"access_token": ACCESS_TOKEN})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("error", "Error fetching data"))

    data = response.json()
    conversation_data_points = data.get("conversation_analytics", {}).get("data", [])
    
    total_cost = sum(
        data_point.get("cost", 0)
        for entry in conversation_data_points
        for data_point in entry.get("data_points", [])
    )

    paid_amount = account_details.paid_amount

    return paid_amount - total_cost





@router.get("/conversation-cost-history/")
async def get_conversation_cost_history(
    
    start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format"),
    db: AsyncSession = Depends(database.get_db),
    get_current_user: user.newuser = Depends(get_current_user),
):
    ACCESS_TOKEN = get_current_user.PAccessToken

    # Fetch account creation time asynchronously
    result = await db.execute(select(User.User).filter(User.User.WABAID == get_current_user.WABAID))
    account_creation_time = result.scalars().first()
    
    if not account_creation_time:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Default date range to account creation time and current time if not provided
    since = int(account_creation_time.created_at.timestamp())
    until = int(datetime.now().timestamp())

    if start_date:
        try:
            since = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format, expected YYYY-MM-DD")
    
    if end_date:
        try:
            until = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format, expected YYYY-MM-DD")
    
    if since > until:
        raise HTTPException(status_code=400, detail="start_date cannot be after end_date")

    # Build the URL for the API request
    url = f"https://graph.facebook.com/v20.0/{get_current_user.WABAID}?fields=conversation_analytics.start({since}).end({until}).granularity(DAILY).phone_numbers([]).dimensions([\"CONVERSATION_CATEGORY\",\"CONVERSATION_TYPE\",\"COUNTRY\",\"PHONE\"])"
    
    # Make the request to the external API
    response = requests.get(url, params={"access_token": ACCESS_TOKEN})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json().get("error", "Error fetching data"))
    
    conversation_data = response.json().get("conversation_analytics", {}).get("data", [])
    processed_data = []

    # Process the data
    for data_entry in conversation_data:
        data_points = data_entry.get("data_points", [])
        for point in data_points:
            start_time = datetime.utcfromtimestamp(point["start"]).strftime('%Y-%m-%d %H:%M:%S')
            end_time = datetime.utcfromtimestamp(point["end"]).strftime("%Y-%m-%d %H:%M:%S")
            cost = point.get("cost")
            conversation_type = point.get("conversation_type")
            conversation_category = point.get("conversation_category")

            processed_data.append({
                "start_time": start_time,
                "end_time": end_time,
                "cost": cost,
                "conversation_type": conversation_type,
                "conversation_category": conversation_category
            })

    return {"conversation_analytics": processed_data}