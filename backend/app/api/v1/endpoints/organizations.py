from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[OrganizationResponse])
async def get_organizations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    organizations = db.query(Organization).offset(skip).limit(limit).all()
    return organizations

@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    organization = db.query(Organization).filter(Organization.id == org_id).first()
    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.post("/", response_model=OrganizationResponse)
async def create_organization(
    organization: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_organization = Organization(**organization.dict())
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization

@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: int,
    organization: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_organization = db.query(Organization).filter(Organization.id == org_id).first()
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    update_data = organization.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_organization, field, value)
    
    db.commit()
    db.refresh(db_organization)
    return db_organization
