from ..database import database
from sqlalchemy import Integer,Column,String,ARRAY,JSON,Date
from . import User

from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, func



class Integration(database.Base):
    __tablename__="Integration"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey(User.User.id))
    api_key=Column(String)
    app=Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    type=Column(String)

# Integration Credentials
class Integration_credentials(database.Base):
    __tablename__="integration_credentials"
    id=Column(Integer,primary_key=True)
    user_id= Column(Integer,ForeignKey(User.User.id))
    app=Column(String) #"WooCommerce", "Shopify", etc.
    store_name=Column(String)
    client_key= Column(String)
    client_secret =Column(String)
    base_url=Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

# WooCommerce
class WooIntegration(database.Base):
    __tablename__="Woo_Integration"
    id=Column(Integer,primary_key=True)
    integration_id=Column(Integer,ForeignKey(Integration.id))
    description=Column(String,nullable=True)
    user_id=Column(Integer,ForeignKey(User.User.id))
    api_key=Column(String,nullable=True)
    rest_key=Column(String,nullable=True) 
    rest_secret=Column(String,nullable=True)
    type=Column(String)
    template=Column(String)
    template_data=Column(String)
    parameters=Column(JSON)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    contacts_start_date=Column(TIMESTAMP,nullable=True)
    contacts_end_date=Column(TIMESTAMP,nullable=True)
    repeat_days=Column(ARRAY(String),nullable=True)
    time=Column(String,nullable=True)
    product_id=Column(Integer,nullable=True)
    status=Column(String,nullable=True)
    base_url=Column(String,nullable=True)
    image_id=Column(String,nullable=True)


