from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.future import select
from datetime import datetime, timedelta

# Import your own modules
from .database import database
from .routes import user, broadcast, contacts, auth, woocommerce, integration, wallet, analytics
from .services import dramatiq_router
from . import oauth2
from .models import ChatBox  # ChatBox model is assumed here

# Initialize FastAPI app
app = FastAPI(title="WotNot Backend")

# Allow frontend access (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
async def create_db_and_tables():
    async with database.engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)

# Include API routes
app.include_router(broadcast.router)
app.include_router(contacts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(wallet.router)
app.include_router(oauth2.router)
app.include_router(dramatiq_router.router)
app.include_router(woocommerce.router)
app.include_router(integration.router)
app.include_router(analytics.router)

# APScheduler for background jobs
scheduler = AsyncIOScheduler()
scheduler_started = False


async def close_expired_chats():
    """
    Closes chats that are inactive for more than 24 hours.
    """
    try:
        async for session in database.get_db():
            now = datetime.now()

            result = await session.execute(
                select(ChatBox.Last_Conversation).where(
                    ChatBox.Last_Conversation.active == True,
                    now - ChatBox.Last_Conversation.last_chat_time > timedelta(minutes=1440)
                )
            )
            expired_conversations = result.scalars().all()

            for conversation in expired_conversations:
                conversation.active = False

            await session.commit()
            print(f"Closed {len(expired_conversations)} expired chats.")
            break
    except Exception as e:
        print(f"Error in close_expired_chats: {e}")


# ------------------------------
# NEW FEATURE: Predefined Messages API
# ------------------------------

@app.get("/predefined-messages")
async def get_predefined_messages():
    """
    Returns a list of predefined chatbot messages.
    """
    messages = [
        {"id": 1, "text": "Hello! 👋 How can I assist you today?"},
        {"id": 2, "text": "Would you like to know about our products?"},
        {"id": 3, "text": "Please provide your contact details."},
        {"id": 4, "text": "Thank you for reaching out! We'll get back soon."}
    ]
    return {"status": "success", "messages": messages}


# ------------------------------
# Startup & Shutdown Events
# ------------------------------

@app.on_event("startup")
async def startup_event():
    global scheduler_started
    await create_db_and_tables()
    if not scheduler_started:
        scheduler.add_job(close_expired_chats, 'interval', minutes=1)
        scheduler.start()
        scheduler_started = True
        print("Scheduler started.")


@app.on_event("shutdown")
async def shutdown_event():
    global scheduler_started
    if scheduler_started:
        scheduler.shutdown(wait=False)
        scheduler_started = False
        print("Scheduler shut down.")
