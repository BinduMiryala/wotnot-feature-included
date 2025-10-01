
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean,BIGINT
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from ..database import database

Base = declarative_base()

class Conversation(database.Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True, index=True)
    wa_id = Column(String, index=True)  # WhatsApp ID of the user
    message_id = Column(String)  # Unique message ID
    phone_number_id = Column(BIGINT)  # Phone number ID
    message_content = Column(Text)  # Message body
    media_id=Column(String,nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)  # Message timestamp
    context_message_id = Column(String, nullable=True,default= None)  # ID of the message that this is replying to
    message_type = Column(String)  # Type of message (e.g., text, image)
    is_first_message = Column(Boolean, default=False)  # Indicates if it's the first message in the conversation
    direction = Column(String, nullable=False)  # Track message direction


class Last_Conversation(database.Base):
    __tablename__ = 'last_conversations'

    
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String)  # Unique message ID
    message_content = Column(Text)  # Message body
    business_account_id = Column(String, nullable=False)  # ID of the business account
    sender_wa_id = Column(String, nullable=False)
    sender_name= Column(String, nullable=False)# WhatsApp Profile name of the sender
    receiver_wa_id = Column(String, nullable=False)  # WhatsApp ID of the recipient
    last_chat_time = Column(DateTime,default=datetime.utcnow)  # Timestamp for the first chat
    active = Column(Boolean, default=True)  # Status of the conversation

    def __init__(self, business_account_id, sender_wa_id,sender_name, receiver_wa_id, last_chat_time=None, message_content= None ,message_id = None, active=True):
        self.business_account_id = business_account_id
        self.message_id = message_id
        self.message_content = message_content
        self.sender_wa_id = sender_wa_id
        self.sender_name = sender_name
        self.receiver_wa_id = receiver_wa_id
        self.last_chat_time = last_chat_time or datetime.now()
        self.active = active
