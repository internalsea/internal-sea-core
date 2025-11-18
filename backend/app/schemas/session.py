from pydantic import BaseModel
from typing import Optional

class OrganizationInfo(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserInfo(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class SessionResponse(BaseModel):
    organization: OrganizationInfo
    user: UserInfo
    configuration: Optional[str] = None
    version_of_software: Optional[str] = None
    session_info: Optional[str] = None

    class Config:
        from_attributes = True