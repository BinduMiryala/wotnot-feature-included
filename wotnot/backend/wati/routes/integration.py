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



@router.get("/integration/list")
async def integrationlist(
    db: AsyncSession = Depends(database.get_db),
    get_current_user: user.newuser = Depends(get_current_user)
):
    # Fetch the list of integrations asynchronously
    result = await db.execute(
        select(Integration.Integration).filter(Integration.Integration.user_id == get_current_user.id)
        .order_by(Integration.Integration.user_id.desc())
    )
    integrationList = result.scalars().all()

    if not integrationList:
        raise HTTPException(status_code=404, detail="No integration exists for the current user")

    return integrationList

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select





@router.delete("/integration/{id}")
async def delete_integration(
    id: int,
    db: AsyncSession = Depends(database.get_db),
    get_current_user: user.newuser = Depends(get_current_user),
):
    # Find the WooIntegration object asynchronously
    woo_integration_result = await db.execute(
        select(Integration.WooIntegration).filter(
            (Integration.WooIntegration.integration_id == id) &
            (Integration.WooIntegration.user_id == get_current_user.id)
        )
    )
    woo_integration = woo_integration_result.scalars().first()

    if woo_integration:
        # Delete WooIntegration object
        await db.delete(woo_integration)
        await db.commit()
    else:
        raise HTTPException(status_code=404, detail="WooCommerce Integration not found")

    # Find the Integration object asynchronously
    integration_result = await db.execute(
        select(Integration.Integration).filter(
            (Integration.Integration.id == id) &
            (Integration.Integration.user_id == get_current_user.id)
        )
    )
    integration = integration_result.scalars().first()

    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")

    # Delete the Integration object
    await db.delete(integration)
    await db.commit()

    return {"detail": f"Successfully deleted Integration with id: {id}"}


