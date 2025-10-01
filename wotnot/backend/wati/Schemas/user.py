from pydantic import BaseModel
from pydantic import BaseModel
from typing import List, Optional



class newuser(BaseModel):
    id:int
    username:str
    email:str
    password:str
    WABAID:int
    PAccessToken:str
    Phone_id:int
    api_key:Optional[str]


class register_user(BaseModel):
    username:str
    email:str
    password:str
    WABAID:Optional[int]=None
    PAccessToken:Optional[str]=None
    Phone_id:Optional[int]=None
    cf_token:Optional[str]=None

# login user model

class LoginUser(BaseModel):
    username:str
    password:str


# User Business Profile Update 
class BusinessProfile(BaseModel):
    messaging_product: str = "whatsapp"  # Fixed value
    address: str
    description: str
    vertical: str
    about: str
    email: str
    websites: List[str]
    profile_picture_handle: Optional[str]

