#  these are the webhooks routes for integration with woocommerce
from fastapi import FastAPI, Depends, HTTPException, Request,APIRouter
from sqlalchemy.orm import Session
from ..database import database  # Your database connection
from ..models import User,Integration,Broadcast
import json # Your models
import requests
from ..Schemas import user,integration,woocommerce
from ..oauth2 import get_current_user
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import httpx
from datetime import datetime, timedelta
import pytz
from ..services import tasks
from pydantic import BaseModel
import requests
from urllib.parse import urlparse
import base64



router=APIRouter(tags=['woocommerce'])

# Function to verify API key from request headers or query params
async def verify_api_key(request: Request, db: AsyncSession ):
    api_key = request.headers.get("Authorization")
    
    # If the API key is passed as a query parameter
    if not api_key:
        api_key = request.query_params.get("api_key")
        
    # Remove "Bearer " if passed in the Authorization header
    if api_key and api_key.startswith("Bearer"):
        api_key = api_key[7:]
    
    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    # Check if API key exists in the database
    result =await db.execute(select(User.User).filter(User.User.api_key == api_key))

    user=result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    print(user)
    return user


async def send_order_confirmation_message(order_data, whatsapp_token, phone_id, db: AsyncSession,user_id):
    """
    Sends a user-specific message template when a new order is created in WooCommerce.
    """
    product_id = order_data["line_items"][0]["product_id"]

    
    # Fetch the integration details from the database
    result=await db.execute(select(Integration.WooIntegration).filter((Integration.WooIntegration.user_id==user_id)&(Integration.WooIntegration.type=="woo/order_confirmation")&(Integration.WooIntegration.product_id==product_id)))
    integration=result.scalars().first()
    if not integration:
        raise ValueError("No WooCommerce order confirmation integration found")

    template_name = integration.template
    parameters = integration.parameters
    template_data= json.loads(integration.template_data)
    TemplateLanguage = template_data.get("language")
    image_id=integration

    customer_phone = order_data["billing"]["phone"]
    customer_name = order_data["billing"]["first_name"]
    order_id = order_data["id"]
    order_total = order_data["total"]

    success_count = 0
    failed_count = 0

    # Make list of contacts (expected format by database)
    contacts_list=[customer_phone]
    

    # Map parameters to values from order_data
    parameter_values = {
        "customer_name": customer_name,
        "order_id": order_id,
        "order_total": order_total
    }

    # Define the message components
    components = [
        {
            "type": "body",
            "parameters": []
        }
    ]
    


    data = {
        "messaging_product": "whatsapp",
        "to": customer_phone,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": TemplateLanguage},
        }
    }

    if integration.image_id:
        data["template"]["components"] = [
            {
                "type": "header",
                "parameters": [
                    {
                        "type": "image",
                        "image": {"id": integration.image_id}
                    }
                ]
            }
        ]

    if integration.parameters:
        for param in parameters:
            param_key = param["key"]
            
            # Map parameter keys to specific values
            if param_key == "billing.first_name":
                value = customer_name
            # elif param_key == "id":
            #     value = order_id
            # elif param_key == "total":
            #     value = order_total
            else:
                value = ""  # Default for unknown parameters


            body_params = [{"type": "text", "text": f"{value}"}] 
            # Ensure the components list exists
            if "components" not in data["template"]:
                data["template"]["components"] = []
                
            data["template"]["components"].append({
                    "type": "body",
                    "parameters": body_params
                })
        

 
    # WhatsApp API endpoint and headers
    API_URL = f"https://graph.facebook.com/v20.0/{phone_id}/messages"
    API_HEADERS = {
        "Authorization": f"Bearer {whatsapp_token}",  # Use user-specific token
        "Content-Type": "application/json"
    }
    
    # Send message to WhatsApp API
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, headers=API_HEADERS, json=data)

    if response.status_code == 200:
        print(f"Message sent successfully to {customer_phone}")
        success_count += 1
        confirmation_status="Successful"
    else:
        print(f"Failed to send message. Response: {response.text}")
        failed_count += 1
        confirmation_status="Failed"

    # log to the broadcast to daatbase
    
    

    db_broadcastList=Broadcast.BroadcastList(
        user_id=user_id,
        name=customer_name,
        template=template_name,
        contacts=contacts_list,
        type="woo/integration",
        success=success_count,
        failed=failed_count,
        status= confirmation_status,
        
    )
    db.add(db_broadcastList)
    await db.commit()
    await db.refresh(db_broadcastList)

# webhook for the order cofirmation
@router.post("/webhook/woocommerce")
async def handle_woocommerce_webhook(request: Request, db: AsyncSession = Depends(database.get_db)):
    # Verify API key
    user = await verify_api_key(request, db)

    body = await request.body()
    print(f"Webhook received: {body.decode('utf-8')},user id is {user.id}")  # Log the raw body for debugging
    
    # Try to parse the body as JSON
    try:
        
        payload = await request.json()
        await send_order_confirmation_message(payload,user.PAccessToken,user.Phone_id,db,user.id)
    except Exception as e:
        return {"error": "Invalid JSON", "detail": str(e)}

    # Continue processing the webhook data

    print(payload)
    return {"status": "success"}
    

# route for fetchapi key
@router.get("/webhooklink")
async def apikey(request:Request,get_current_user: user.newuser=Depends(get_current_user)):
    apikey=get_current_user.api_key

    base_url = request.url.scheme + "://" + request.url.netloc

    webhooklink=f"{base_url}/webhook/woocommerce?api_key={apikey}"

    return{"webkook_link":webhooklink}
    

@router.post("/integrate/woo_order_cnf")
async def saveWooIntegartion(request:integration.wooIntegration,get_current_user: user.newuser=Depends(get_current_user),db: AsyncSession = Depends(database.get_db)):
    parameters_list = [{"key": param.key} for param in request.parameters]
    
    result=await db.execute(select(Integration.WooIntegration).filter((Integration.WooIntegration.user_id==get_current_user.id)
                            &(Integration.WooIntegration.type=="woo/order_confirmation")
                            &(Integration.WooIntegration.product_id==request.product_id)))
    exixsting=result.scalars().first()
    if exixsting:
        raise HTTPException(status_code=400, detail="Integration for the product already exists")
   
   # Create the WooIntegrationDB model instance
    integration=Integration.Integration(
        user_id=get_current_user.id,
        type=request.type,
        api_key=get_current_user.api_key,
        app="woocommerce",
        
        
    )
    # Add and commit the data to the database
    db.add(integration)
    await db.commit()
    await db.refresh(integration)

    result2=await db.execute(select(Integration.Integration).filter((Integration.Integration.user_id==get_current_user.id)&(Integration.Integration.type==request.type)))
    integration_search=result2.scalars().first()
    woo_integration = Integration.WooIntegration(
        integration_id=integration_search.id,
        parameters=parameters_list,
        api_key=get_current_user.api_key,
        type=request.type,
        template=request.template_id,
        template_data=request.template_data,
        user_id=get_current_user.id,
        product_id=request.product_id,
        description=request.description,
        image_id=request.image_id

    )

    # Add and commit the data to the database
    db.add(woo_integration)
    await db.commit()
    await db.refresh(woo_integration)

    # Create the WooIntegrationDB model instance
   

    return {"template": request.template_id, "parameters": request.parameters}




from datetime import datetime, timedelta
import pytz



def calculate_next_execution_time(repeat_days, time_str):
    """
    Calculate the next execution time based on repeat_days and time in IST.
    """
    # Define IST and UTC timezones
    ist = pytz.timezone('Asia/Kolkata')
    utc = pytz.utc

    # Map days of the week to integers
    days_mapping = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
                    "Friday": 4, "Saturday": 5, "Sunday": 6}

    # Ensure repeat_days is not empty
    if not repeat_days:
        raise ValueError("repeat_days cannot be empty")

    repeat_days = sorted([days_mapping[day] for day in repeat_days])  # Sort for easier lookup

    # Current time in IST
    now_ist = datetime.now(ist)
    current_day = now_ist.weekday()
    current_time = now_ist.time()

    # Convert target time string to a datetime object in IST
    today_date = now_ist.strftime("%Y-%m-%d")
    target_time_ist = datetime.strptime(f"{today_date} {time_str}", "%Y-%m-%d %H:%M")
    target_time_ist = ist.localize(target_time_ist)
    target_time_utc = target_time_ist.astimezone(utc).time()  # Convert to UTC time format

    # If today is a repeat day AND the current time is before the target time → Execute today
    if current_day in repeat_days and current_time < target_time_ist.time():
        next_execution_date = now_ist
    else:
        # Find the next available repeat day
        days_until_next = min(
            [(day - current_day) % 7 for day in repeat_days if (day - current_day) % 7 > 0],
            default=7  # Default to next week's first repeat day if all have passed
        )

        # Compute next execution date
        next_execution_date = now_ist + timedelta(days=days_until_next)

    # Combine date and UTC time in required format
    next_execution = datetime.combine(next_execution_date.date(), target_time_utc, tzinfo=utc)

    return next_execution


@router.post("/integrate/woo_pwn")
async def saveWooIntegartion(request:integration.wooIntegration,get_current_user: user.newuser=Depends(get_current_user),db: AsyncSession = Depends(database.get_db)):
    parameters_list = [{"key": param.key} for param in request.parameters]
    
    # result=await db.execute(select(Integration.WooIntegration).filter((Integration.WooIntegration.user_id==get_current_user.id)&(Integration.WooIntegration.type=="woo/pwn")))
    # exixsting=result.scalars().first()
    # if exixsting:
    #     raise HTTPException(status_code=400, detail="Integration already exists")
   
   # Create the WooIntegrationDB model instance
    integration=Integration.Integration(
        user_id=get_current_user.id,
        type=request.type,
        api_key=get_current_user.api_key,
        app="woocommerce"
    )
    # Add and commit the data to the database
    db.add(integration)
    await db.commit()
    await db.refresh(integration)

    query = await db.execute(
        select(Integration.Integration_credentials)
        .filter(Integration.Integration_credentials.user_id==get_current_user.id,
                Integration.Integration_credentials.app=="WooCommerce")
    )

    integration_credentials = query.scalars().first()

    # result2=await db.execute(select(Integration.Integration).filter((Integration.Integration.id==integration.id)&(Integration.Integration.type==request.type)))
    # integration_search=result2.scalars().first()
    woo_integration = Integration.WooIntegration(
        integration_id=integration.id,
        parameters=parameters_list,
        api_key=get_current_user.api_key,
        type=request.type,
        template=request.template_id,
        template_data=request.template_data,
        user_id=get_current_user.id,
        contacts_start_date=request.contacts_start_date.replace(tzinfo=None),
        contacts_end_date=request.contacts_end_date.replace(tzinfo=None),
        repeat_days=request.repeat_days,
        time=request.time,
        rest_key=integration_credentials.client_key,
        rest_secret=integration_credentials.client_secret,
        product_id=request.product_id,
        status=request.status,
        base_url=integration_credentials.base_url,
        description=request.description,
        image_id=request.image_id
    )

    # Add and commit the data to the database
    db.add(woo_integration)
    await db.commit()
    await db.refresh(woo_integration)
 

    next_execution_time = calculate_next_execution_time(request.repeat_days, request.time)
    delay_seconds = (next_execution_time - datetime.now(pytz.utc)).total_seconds()
    print(f"This the delay time {delay_seconds/(60)}")

    # Schedule the task
    tasks.schedule_woo_task.send_with_options(args=(woo_integration.id,), delay=delay_seconds*1000) #delay in miliseconds


    return {"template": request.template_id, "parameters": request.parameters}




def test_woocommerce_connection(base_url: str, consumer_key: str, consumer_secret: str,store_name:str):
    try:
        # WooCommerce API endpoint
        url = f"{base_url}/wp-json/wc/v3/"
        # Perform a GET request to fetch store data

        # Set up authentication and headers
        credentials = f"{consumer_key}:{consumer_secret}"
        token = base64.b64encode(credentials.encode()).decode()

        # Parse the URL and extract the hostname
        parsed_url = urlparse(base_url)
        hostname = parsed_url.hostname

        headers = {
                "Authorization": f"Basic {token}",
                "Accept": "*/*",
                "Cache-Control": "no-cache",
                "User-Agent": "PostmanRuntime/7.28.0",
                "Host": hostname
            }
        response = requests.get(f"{base_url}/wp-json/wc/v3/", headers=headers)

        store_info={
            "store_name":f"{store_name}",
            "consumer_key":f"{consumer_key}",
            "consumer_secret":f"{consumer_secret}",
            "base_url":f"{base_url}"
        }

        # Check if the response is valid
        if response.status_code == 200:
            return {"status": "connected", "store_info": store_info}
        else:
            return {"status": "error", "message": response.json().get("message", "Connection failed")}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Endpoint to validate connection with WooCommerce
@router.post("/test-woocommerce")
async def validate_woocommerce_connection(
    credentials: woocommerce.WooCommerceCredentials,
    get_current_user: user.newuser = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db),
):
    # Test the WooCommerce connection
    result = test_woocommerce_connection(
        base_url=credentials.base_url,
        consumer_key=credentials.consumer_key,
        consumer_secret=credentials.consumer_secret,
        store_name=credentials.store_name,
    )

    if result["status"] == "connected":
        # Check if the integration already exists
        query = select(Integration.Integration_credentials).where(
            Integration.Integration_credentials.user_id == get_current_user.id,
            Integration.Integration_credentials.app == "WooCommerce"
        )
        existing_integration = await db.execute(query)
        existing_integration = existing_integration.scalar_one_or_none()

        if existing_integration:
            # Raise an exception if the integration already exists
            raise HTTPException(
                status_code=400, 
                detail="WooCommerce integration already exists"
            )

        # Add a new integration if it doesn't exist
        new_credentials = Integration.Integration_credentials(
            user_id=get_current_user.id,
            app="WooCommerce",
            client_key=credentials.consumer_key,
            client_secret=credentials.consumer_secret,
            base_url=credentials.base_url,
            store_name=credentials.store_name
        )
        db.add(new_credentials)
        await db.commit()
        await db.refresh(new_credentials)

        return {"message": "Connection successful", "store_info": result["store_info"]}
    else:
        raise HTTPException(status_code=400, detail=result["message"])


@router.get("/check-integration")
async def check_integration(   
    get_current_user: user.newuser = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)):

    # Fetch the integration details for the logged-in user
    query = await db.execute(
        select(Integration.Integration_credentials)
        .filter(Integration.Integration_credentials.user_id==get_current_user.id,
                Integration.Integration_credentials.app=="WooCommerce")
    )

    integration = query.scalars().first()

    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found.")


    # Test the integration
    result = test_woocommerce_connection(integration.base_url,integration.client_key, integration.client_secret,integration.store_name)

    return result


# @router.get("/woo_products")
# async def get_products(
#     get_current_user: user.newuser = Depends(get_current_user),
#     db: AsyncSession = Depends(database.get_db)):

#     # Fetch the integration details for the logged-in user
#     query = await db.execute(
#         select(Integration.Integration_credentials)
#         .filter(Integration.Integration_credentials.user_id==get_current_user.id,
#                 Integration.Integration_credentials.app=="WooCommerce")
#     )

#     integration = query.scalars().first()

#     if not integration:
#         raise HTTPException(status_code=404, detail="Integration not found.")

#     credentials = f"{integration.client_key}:{integration.client_secret}"
#     token = base64.b64encode(credentials.encode()).decode()

#     # Headers
#     headers = {
#         "Authorization": f"Basic {token}",
#         "Accept": "*/*",  # Ensures JSON response
#         "Cache-Control": "no-cache",   # Mimics Postman's Cache-Control
#         "User-Agent": "PostmanRuntime/7.28.0",  # Mimics Postman's User-Agent header
#         # "Host": hostname  # Add Host header manually
#     }

#     params = {

#     }

#     WC_API_URL = f"{integration.base_url}/wp-json/wc/v3/products"

#     async with httpx.AsyncClient() as client:
#         try:
#             # Fetch products from WooCommerce API
#             response = await client.get(WC_API_URL,headers=headers)
#             # response.raise_for_status()  # Raise error for bad status code

#             products = response.json()  # Parse the JSON response
#             # Optional: Clean the data if you need only specific fields
#             product_list = [{"id": product["id"], "name": product["name"]} for product in products]

#             return product_list

#         except httpx.HTTPStatusError as e:
#             raise HTTPException(status_code=e.response.status_code, detail="Error fetching products from WooCommerce")
#         except httpx.RequestError as e:
#             raise HTTPException(status_code=500, detail="An error occurred while requesting the WooCommerce API")

@router.get("/woo_products")
async def get_products(
    get_current_user: user.newuser = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)):

    # Fetch the integration details for the logged-in user
    query = await db.execute(
        select(Integration.Integration_credentials)
        .filter(Integration.Integration_credentials.user_id == get_current_user.id,
                Integration.Integration_credentials.app == "WooCommerce")
    )

    integration = query.scalars().first()

    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found.")

    credentials = f"{integration.client_key}:{integration.client_secret}"
    token = base64.b64encode(credentials.encode()).decode()

    # Headers
    headers = {
        "Authorization": f"Basic {token}",
        "Accept": "application/json",
        "User-Agent": "WooCommerceAPI",
    }

    WC_API_URL = f"{integration.base_url}/wp-json/wc/v3/products"

    # Pagination setup
    per_page = 50  # Adjust the number of products per request as needed
    page = 1
    all_products = []

    async with httpx.AsyncClient() as client:
        try:
            while True:
                # Fetch products from WooCommerce API with pagination
                response = await client.get(
                    WC_API_URL,
                    headers=headers,
                    params={"per_page": per_page, "page": page}
                )
                response.raise_for_status()  # Raise error for bad status code

                products = response.json()
                if not products:
                    break  # Break the loop if no more products are returned

                all_products.extend(products)
                page += 1

            # Optional: Filter the product data if only specific fields are needed
            product_list = [
                {"id": product["id"], "name": product["name"], "price": product.get("price")}
                for product in all_products
            ]

            return product_list

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Error fetching products: {e.response.text}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")



@router.delete("/disconnect-woocommerce")
async def disconnect_woocommerce(
    get_current_user: user.newuser = Depends(get_current_user),
    db: AsyncSession = Depends(database.get_db)):

    query = await db.execute(
        select(Integration.Integration_credentials)
        .filter(Integration.Integration_credentials.user_id==get_current_user.id,
                Integration.Integration_credentials.app=="WooCommerce")
    )

    integration = query.scalars().first()

    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found.")

    await db.delete(integration)
    await db.commit()

    # Perform necessary disconnection logic
    # For example, clear WooCommerce API credentials from the database
    return {"status": "success", "message": "WooCommerce disconnected"}


@router.get("/woo-integration-list")
async def integrationlist(
    db: AsyncSession = Depends(database.get_db),
    get_current_user: user.newuser = Depends(get_current_user)
):
    # Fetch the list of integrations asynchronously
    result = await db.execute(
        select(Integration.WooIntegration).filter(Integration.WooIntegration.user_id == get_current_user.id)
        .order_by(Integration.WooIntegration.created_at.desc())
    )
    integrationList = result.scalars().all()

    if not integrationList:
        raise HTTPException(status_code=404, detail="No integration exists for the current user")

    return integrationList

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select