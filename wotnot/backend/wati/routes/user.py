from fastapi import APIRouter,Depends,HTTPException,UploadFile,Request
from ..models import User
from ..Schemas import user
from ..database import database
from sqlalchemy.orm import Session
from .. import hashing
import secrets   
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import secrets
from ..oauth2 import get_current_user
import httpx
import requests
import json

router=APIRouter(tags=['User'])


# Define the schemas for the request body
# Endpoint to process the responses
@router.post("/subscribe_customer")
async def process_responses(
    payload: dict,
    db: AsyncSession = Depends(database.get_db),
    get_current_user: user.newuser = Depends(get_current_user),
):
    sessionInfoResponse = payload.get("sessionInfoResponse")
    sdkResponse = payload.get("sdkResponse")

    if not sessionInfoResponse or not sdkResponse:
        raise HTTPException(status_code=400, detail="Missing required fields")

    try:
        # Parse the JSON strings
        session_info = json.loads(sessionInfoResponse)
        sdk_info = json.loads(sdkResponse)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")

    # Extract necessary data
    waba_id = session_info.get("data", {}).get("waba_id")
    # phone_id = session_info.get("data", {}).get("phone_id")
    code = sdk_info.get("authResponse", {}).get("code")

    if not waba_id or not code:
        raise HTTPException(status_code=400, detail="Invalid data received")

 
   

    current_user= await db.execute(
        select(User.User).filter(
            User.User.id == get_current_user.id
        )
    )
    current_user = current_user.scalars().first()

    if not current_user:
        raise HTTPException(
            status_code=400, detail="user not found"
        )
    



    # Exchange the code for a business token
    token_url = "https://graph.facebook.com/v20.0/oauth/access_token"  # Use the correct version
    client_id = "2621821927998797"  # Replace with your app's client ID
    client_secret = "70f8ff2327df71cf505b853f0fdc4a20"  # Replace with your app's client secret
    redirect_uri = "https://2f4d-2405-201-3004-d09d-700c-69d4-6511-ab75.ngrok-free.app/broadcast/broadcast2"  # Replace with your app's redirect URI

    try:
        response = requests.post(
            token_url,
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
            },
        )
        response.raise_for_status()
        token_data = response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to exchange code: {e}")
    

    # Save waba_id and phone_id to the database for the current user

    current_user.WABAID=int(waba_id)
    current_user.PAccessToken=token_data.get("access_token")
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    # Permanent access token
    Paccess_token=token_data.get("access_token")

    # Setup webhooks for the customers
    url = f"https://graph.facebook.com/v21.0/{waba_id}/subscribed_apps"
    headers = {
        "Authorization": f"Bearer {Paccess_token}",
    }
    response = requests.post(url, headers=headers)
    response.raise_for_status()

    # # Register the customer's phone_no id
    # pin="123456"

    # url = f"https://graph.facebook.com/v21.0/{phone_number_id}/register"
    # headers = {
    #     "Authorization": f"Bearer {Paccess_token}",
    #     "Content-Type": "application/json",
    # }
    # data = {
    #     "messaging_product": "whatsapp",
    #     "pin": pin,
    # }
    # response = requests.post(url, headers=headers, json=data)
    # response.raise_for_status()
    # return response.json()


    # Return the business access token to the frontend
    return {"access_token": token_data.get("access_token"), "expires_in": token_data.get("expires_in")}

# Notes:
# - Replace placeholders like YOUR_CLIENT_ID, YOUR_CLIENT_SECRET, and YOUR_REDIRECT_URI with actual values.
# - Ensure your database schema and models (e.g., User) have `waba_id` and `phone_id` fields.
# - Ensure your authentication dependency `get_current_user` returns the logged-in user object.
# - Install necessary libraries (e.g., requests) if not already installed.
    


import httpx
import os

  # Replace with your actual Turnstile secret key

async def verify_turnstile_token(token: str, remoteip: str = None) -> dict:
    data = {
        "secret": os.getenv("TURNSTILE_SECRET_KEY"),
        "response": token,
    }
    if remoteip:
        data["remoteip"] = remoteip

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data=data
        )
        result = response.json()
        return result

@router.post('/register')
async def new_user(
    request: user.register_user,
    db: AsyncSession = Depends(database.get_db)):

    # verify_turnstile = await verify_turnstile_token(request.turnstile_token, request.remote_ip)
    remote_ip = request.client.host
    result = await verify_turnstile_token(request.cf_token, remoteip=remote_ip)

    if result.get("success"):
    
        # Check for existing user
        result = await db.execute(
            select(User.User).filter(
                (User.User.email == request.email) 
            )
        )
        existing_user = result.scalars().first()
        
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Account with this email or phone number already exists"
            )
        
        # Create a new user
        api_key = secrets.token_hex(32)
        registeruser = User.User( 
            username=request.username,
            email=request.email,
            password_hash=hashing.Hash.bcrypt(request.password),  # Decode the hash to store it as a string
            # WABAID=request.WABAID,
            # PAccessToken=request.PAccessToken,
            # Phone_id=request.Phone_id,
            api_key=api_key
        )
        
        db.add(registeruser)
        await db.commit()  # Commit the transaction asynchronously
        await db.refresh(registeruser)  # Refresh the instance asynchronously

        return {"success": True, "message": "Account created successfully"}


# @router.post("/update-profile", status_code=200)
# async def update_profile(
#     request: user.UpdateProfileRequest,
#     get_current_user: user.newuser = Depends(get_current_user)
# ):
#     # Log request body to see its structure
#     print(request.dict())  # or logging for better handling

#     # ... the rest of your code
@router.post("/update-profile", status_code=200)
def update_profile(
    request: user.BusinessProfile, 
    get_current_user: user.newuser = Depends(get_current_user)
):
    """
    Updates the WhatsApp Business Profile using the provided JSON payload.
    """

    WHATSAPP_API_URL = f"https://graph.facebook.com/v20.0/{get_current_user.Phone_id}/whatsapp_business_profile"

    # Prepare the request payload by dumping the model and ensuring all fields are serializable
    payload = {
        "messaging_product": request.messaging_product,
        "address": request.address,
        "description": request.description,
        "vertical": request.vertical,
        "about": request.about,
        "email": str(request.email),
        "websites": [str(url) for url in request.websites],
        "profile_picture_handle": request.profile_picture_handle or None,
    }

    headers = {
        "Authorization": f"Bearer {get_current_user.PAccessToken}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(WHATSAPP_API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            return {"message": "Business profile updated successfully", "data": response.json()}
        else:
            if response.headers.get("Content-Type") == "application/json":
                error_message = response.json().get("error", {}).get("message", "Unknown error occurred")
            else:
                error_message = response.text or "Unknown error occurred"

            raise HTTPException(
                status_code=response.status_code,
                detail=f"{error_message}",
            )

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {e}")




from fastapi import FastAPI, HTTPException, UploadFile
import requests
import mimetypes






@router.post("/resumable-upload/")
async def resumable_upload(file: UploadFile,get_current_user: user.newuser = Depends(get_current_user)):
    # Calculate file parameters
    BASE_URL = "https://graph.facebook.com/v20.0"
    ACCESS_TOKEN = get_current_user.PAccessToken
    file_content = await file.read()
    file_length = len(file_content)  # File size in bytes
    file_type = mimetypes.guess_type(file.filename)[0] or "application/octet-stream"
    file_name = file.filename

    # Step 1: Create Upload Session
    create_session_url = f"{BASE_URL}/app/uploads/"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    params = {
        "file_length": file_length,
        "file_type": file_type,
        "file_name": file_name
    }

    create_session_response = requests.post(create_session_url, headers=headers, params=params)
    if create_session_response.status_code != 200:
        raise HTTPException(status_code=create_session_response.status_code, detail=create_session_response.json())

    upload_session_data = create_session_response.json()
    upload_id = upload_session_data["id"]
    print(upload_id)

    # Step 2: Upload File Chunk
    upload_url = f"{BASE_URL}/{upload_id}&access_token={ACCESS_TOKEN}"
    upload_headers = {
        'Content-Type': 'image/jpeg',
        'Accept': '*/*',
        'file_offset': str(0)
    }
    
    payload = file_content

    upload_response = requests.post(upload_url, headers=upload_headers, data=payload)
    if upload_response.status_code != 200:
        raise HTTPException(status_code=upload_response.status_code, detail=upload_response.json())
    

    url = f"https://graph.facebook.com/v20.0/{upload_id}&access_token={ACCESS_TOKEN}"

    payload = file_content
    headers = {
    'Content-Type': 'image/jpeg',
    'file_offset': '0'
    }

    upload_response = requests.request("POST", url, headers=headers, data=payload)

    if upload_response.status_code != 200:
        raise HTTPException(status_code=upload_response.status_code, detail=upload_response.json())


    # Step 3: Query Upload Status
    query_url = f"{BASE_URL}/{upload_id}&access_token={ACCESS_TOKEN}"
    query_response = requests.get(query_url, headers=headers)
    if query_response.status_code != 200:
        raise HTTPException(status_code=query_response.status_code, detail=query_response.json())

    # Combine all results
    return {
        "upload_session": upload_session_data,
        "upload_response": upload_response.json(),
        "query_status": query_response.json()
    }









@router.get("/get-business-profile/")
def get_business_profile(get_current_user: user.newuser = Depends(get_current_user)):
    """
    Fetch the WhatsApp Business Profile details.
    """
    
    BASE_URL = "https://graph.facebook.com/v17.0"
    ACCESS_TOKEN = get_current_user.PAccessToken
    PHONE_NUMBER_ID = get_current_user.Phone_id
    url = f"{BASE_URL}/{PHONE_NUMBER_ID}/whatsapp_business_profile?fields=about,address,description,email,profile_picture_url,websites,vertical"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()
