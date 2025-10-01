from fastapi import APIRouter, HTTPException
from datetime import datetime
import requests
import os

from fastapi import APIRouter,Depends,HTTPException, File, UploadFile,Request
from ..models import Broadcast,Contacts,Integration
from ..Schemas import broadcast,user
from ..database import database
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from pydantic import BaseModel
import requests
import json
from fastapi.responses import JSONResponse
import csv
import io
from ..oauth2 import get_current_user
from dramatiq import get_broker
from dramatiq import Message
from ..crud.template import send_template_to_whatsapp
from ..services import tasks




router=APIRouter(tags=["Integration"])


from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter()

# Read from .env or secure vault in production
# 



@router.get("/get-analytics")
async def get_analytics(start: str, end: str,get_current_user: user.newuser = Depends(get_current_user)):
    try:
        start_ts = int(datetime.strptime(start, "%Y-%m-%d").timestamp())
        end_ts = int(datetime.strptime(end, "%Y-%m-%d").timestamp())

        API_VERSION = "v20.0"

        url = f"https://graph.facebook.com/{API_VERSION}/{get_current_user.WABAID}?fields=analytics.start({start_ts}).end({end_ts}).granularity(DAY).country_codes([\"IN\"])&access_token={get_current_user.PAccessToken}"


        print("Fetching Meta analytics...")
        print("URL:", url)
        print("Start:", start_ts, "End:", end_ts)

        response = requests.get(url, timeout=10)
        print("Meta response:", response.status_code)
        print("Response content:", response.text)

        data = response.json()

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=data)

        # if not data.get("analytics", {}).get("data"):
        #     return {"message": "No analytics data found."}

        return data
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
