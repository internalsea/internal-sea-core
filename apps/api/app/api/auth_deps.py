"""Shared auth dependency type aliases for routers."""

from typing import Annotated

from fastapi import Depends

from app.models.identity import User
from app.modules.auth.dependencies import require_admin, require_editor, require_viewer

ViewerUser = Annotated[User, Depends(require_viewer)]
EditorUser = Annotated[User, Depends(require_editor)]
AdminUser = Annotated[User, Depends(require_admin)]
