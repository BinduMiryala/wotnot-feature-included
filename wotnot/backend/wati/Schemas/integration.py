from pydantic import BaseModel,Json
from datetime import datetime
from typing import List,Optional



class Parameter(BaseModel):
    key: str

class wooIntegration(BaseModel):
    template_id:str
    template_data:str
    parameters:List[Parameter]
    type:str
    contacts_start_date:Optional[datetime]= None
    contacts_end_date:Optional[datetime]= None
    repeat_days:Optional[List[str]]= None
    time:Optional[str]= None
    rest_key:Optional[str]= None
    rest_secret:Optional[str]= None
    product_id:Optional[int]= None
    status:Optional[str]= None
    base_url:Optional[str]= None
    description:Optional[str]=None
    image_id:Optional[str]=None
