from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.core.database import get_db
from app.models.organization import OrganizationMembership
from app.models.user import User
from app.schemas.session import SessionResponse

router = APIRouter()

@router.get("/", response_model=List[SessionResponse])
async def get_sessions(
    skip: int = 0,
    limit: int = 100,
    organization_id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    """Get organization-user combinations with related data."""
    # If no parameters provided, return hardcoded first one
    if organization_id is None and user_id is None:
        query = db.query(OrganizationMembership).options(
            joinedload(OrganizationMembership.organization),
            joinedload(OrganizationMembership.user)
        ).limit(1)
        
        membership = query.first()
        
        if membership is None:
            return []
        
        return [{
            "organization": membership.organization,
            "user": membership.user,
            "configuration": "configuration",
            "version_of_software": "v0.1",
            "session_info": "test session"
        }]
    
    # If parameters provided, use normal filtering
    query = db.query(OrganizationMembership).options(
        joinedload(OrganizationMembership.organization),
        joinedload(OrganizationMembership.user)
    )
    
    if organization_id:
        query = query.filter(OrganizationMembership.organization_id == organization_id)
    if user_id:
        query = query.filter(OrganizationMembership.user_id == user_id)
    
    memberships = query.offset(skip).limit(limit).all()
    
    return [
        {
            "organization": membership.organization,
            "user": membership.user,
            "configuration": None,
            "version_of_software": None,
            "session_info": None
        }
        for membership in memberships
    ]