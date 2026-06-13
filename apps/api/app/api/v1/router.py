from fastapi import APIRouter

from app.api.v1.endpoints import health
from app.modules.activity.router import router as activity_router
from app.modules.auth.router import router as auth_router
from app.modules.automation.router import router as automation_router
from app.modules.capabilities.router import router as capabilities_router
from app.modules.comments.router import router as comments_router
from app.modules.compliance.router import router as compliance_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.data_products.router import router as data_products_router
from app.modules.files.router import router as files_router
from app.modules.internal_projects.router import router as internal_projects_router
from app.modules.notifications.router import router as notifications_router
from app.modules.people.router import router as people_router
from app.modules.performance.router import router as performance_router
from app.modules.projects.router import router as projects_router
from app.modules.relationships.router import router as relationships_router
from app.modules.search.router import router as search_router
from app.modules.teams.router import router as teams_router
from app.modules.tenancy.router import router as tenancy_router
from app.modules.work_items.router import router as work_items_router
from app.modules.worker.router import router as worker_router

api_v1_router = APIRouter()
api_v1_router.include_router(health.router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(tenancy_router)
api_v1_router.include_router(data_products_router)
api_v1_router.include_router(work_items_router)
api_v1_router.include_router(projects_router)
api_v1_router.include_router(internal_projects_router)
api_v1_router.include_router(people_router)
api_v1_router.include_router(teams_router)
api_v1_router.include_router(capabilities_router)
api_v1_router.include_router(performance_router)
api_v1_router.include_router(compliance_router)
api_v1_router.include_router(dashboard_router)
api_v1_router.include_router(search_router)
api_v1_router.include_router(comments_router)
api_v1_router.include_router(activity_router)
api_v1_router.include_router(relationships_router)
api_v1_router.include_router(files_router)
api_v1_router.include_router(automation_router)
api_v1_router.include_router(notifications_router)
api_v1_router.include_router(worker_router)
