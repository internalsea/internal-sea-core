import os
import json
import sys
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from app.models import (
    Organization,
    User,
    Role,
    OrganizationMembership,
    Team,
    TeamUserRole,
)

# --- Helper functions ---
def get_engine():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ DATABASE_URL not set in environment.")
        sys.exit(1)
    return create_engine(db_url, future=True)

def get_or_create(session, model, defaults=None, **by):
    obj = session.scalar(select(model).filter_by(**by))
    if obj:
        return obj, False
    obj = model(**by, **(defaults or {}))
    session.add(obj)
    session.flush()
    return obj, True

def maybe_hash(password=None, hashed=None):
    if hashed:
        return hashed
    if password:
        import bcrypt
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    return None


# --- Core seeding functions ---
def seed_user(session, user_data):
    email = user_data["email"]
    hashed = maybe_hash(user_data.get("password"), user_data.get("hashed_password"))
    defaults = {
        "first_name": user_data.get("first_name", ""),
        "last_name": user_data.get("last_name"),
        "hashed_password": hashed or "CHANGE_ME_HASH",
        "is_active": user_data.get("is_active", True),
        "is_superuser": user_data.get("is_superuser", False),
    }
    user, created = get_or_create(session, User, email=email, defaults=defaults)
    if not created and hashed and user.hashed_password != hashed:
        user.hashed_password = hashed
    return user


def seed_organization(session, org_data):
    org, _ = get_or_create(
        session,
        Organization,
        name=org_data["name"],
        defaults={"description": org_data.get("description"), "is_active": True},
    )

    # Org admin
    admin_data = org_data.get("admin_user")
    if admin_data:
        admin_user = seed_user(session, admin_data)
        org_role = session.scalar(select(Role).where(Role.name == "org_admin"))
        get_or_create(
            session,
            OrganizationMembership,
            organization_id=org.id,
            user_id=admin_user.id,
            defaults={"role_id": org_role.id, "is_default": True},
        )

    # Teams
    for team_data in org_data.get("teams", []):
        team, _ = get_or_create(
            session,
            Team,
            organization_id=org.id,
            name=team_data["name"],
            defaults={"description": team_data.get("description")},
        )

        for member_data in team_data.get("members", []):
            user = seed_user(session, member_data["user"])
            for role_name in member_data.get("roles", []):
                role = session.scalar(select(Role).where(Role.name == role_name))
                get_or_create(
                    session,
                    TeamUserRole,
                    team_id=team.id,
                    user_id=user.id,
                    role_id=role.id,
                )

    return org


def main():
    if len(sys.argv) < 3 or sys.argv[1] != "--file":
        print("Usage: python scripts/seed.py --file /path/to/json")
        sys.exit(1)

    json_path = sys.argv[2]
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    engine = get_engine()
    with Session(engine) as session:
        for org_data in data.get("organizations", []):
            seed_organization(session, org_data)
        session.commit()
        print(f"✅ Seed complete from {json_path}")


if __name__ == "__main__":
    main()
