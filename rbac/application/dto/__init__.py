"""
Data Transfer Objects for the application layer.
"""

from rbac.application.dto.base import BaseResponse
from rbac.application.dto.permission_dto import (
	CreatePermissionRequest,
	PermissionResponse,
	UpdatePermissionRequest,
)
from rbac.application.dto.permission_group_dto import (
	CreatePermissionGroupRequest,
	PermissionGroupResponse,
	UpdatePermissionGroupRequest,
)
from rbac.application.dto.role_dto import (
	CreateRoleRequest,
	RoleResponse,
	UpdateRoleRequest,
)

__all__ = [
	"BaseResponse",
	# Permission DTOs
	"PermissionResponse",
	"CreatePermissionRequest",
	"UpdatePermissionRequest",
	# PermissionGroup DTOs
	"PermissionGroupResponse",
	"CreatePermissionGroupRequest",
	"UpdatePermissionGroupRequest",
	# Role DTOs
	"RoleResponse",
	"CreateRoleRequest",
	"UpdateRoleRequest",
]
