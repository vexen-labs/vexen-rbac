"""
Data Transfer Objects for the application layer.
"""

from vexen_rbac.application.dto.base import BaseResponse
from vexen_rbac.application.dto.pagination import (
	PaginatedResponse,
	PaginationRequest,
	PaginationResponse,
)
from vexen_rbac.application.dto.permission_dto import (
	CreatePermissionRequest,
	PermissionGroupByCategoryResponse,
	PermissionResponse,
	PermissionSimpleResponse,
	UpdatePermissionRequest,
)
from vexen_rbac.application.dto.permission_group_dto import (
	CreatePermissionGroupRequest,
	PermissionGroupResponse,
	UpdatePermissionGroupRequest,
)
from vexen_rbac.application.dto.role_dto import (
	CreateRoleRequest,
	RoleExpandedResponse,
	RoleResponse,
	UpdateRoleRequest,
)

__all__ = [
	"BaseResponse",
	"PermissionResponse",
	"PermissionSimpleResponse",
	"CreatePermissionRequest",
	"UpdatePermissionRequest",
	"PermissionGroupByCategoryResponse",
	"PermissionGroupResponse",
	"CreatePermissionGroupRequest",
	"UpdatePermissionGroupRequest",
	"RoleResponse",
	"RoleExpandedResponse",
	"CreateRoleRequest",
	"UpdateRoleRequest",
	"PaginationRequest",
	"PaginationResponse",
	"PaginatedResponse",
]
