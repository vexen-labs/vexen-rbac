"""
Shared database models for vexen-rbac.

This module re-exports all SQLAlchemy models from their original locations
for centralized import. This facilitates future migration management with
tools like Alembic.

Usage:
    from vexen_rbac.shared.models import (
        Base,
        RoleModel,
        PermissionModel,
        PermissionGroupModel,
        RolePermissionAssociation,
        RolePermissionGroupAssociation,
        PermissionGroupPermissionAssociation,
    )
"""

from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.associations import (
	PermissionGroupPermissionAssociation,
	RolePermissionAssociation,
	RolePermissionGroupAssociation,
)
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.base import Base
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.permission import (
	PermissionModel,
)
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.permission_group import (
	PermissionGroupModel,
)
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.role import RoleModel

__all__ = [
	"Base",
	"RoleModel",
	"PermissionModel",
	"PermissionGroupModel",
	"RolePermissionAssociation",
	"RolePermissionGroupAssociation",
	"PermissionGroupPermissionAssociation",
]
