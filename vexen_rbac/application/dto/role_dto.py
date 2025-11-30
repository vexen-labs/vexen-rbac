from dataclasses import dataclass
from datetime import datetime

from vexen_rbac.application.dto.permission_dto import PermissionSimpleResponse


@dataclass
class RoleResponse:
	id: int
	name: str
	display_name: str
	description: str | None
	permissions: list[int]
	permission_groups: list[int]
	user_count: int
	created_at: datetime
	updated_at: datetime | None


@dataclass
class RoleExpandedResponse:
	id: int
	name: str
	display_name: str
	description: str | None
	permissions: list[PermissionSimpleResponse]
	user_count: int
	created_at: datetime
	updated_at: datetime | None


@dataclass
class CreateRoleRequest:
	"""Request DTO for creating a Role."""

	name: str
	display_name: str
	description: str | None = None
	permissions: list[int] | None = None
	permission_groups: list[int] | None = None


@dataclass
class UpdateRoleRequest:
	"""Request DTO for updating a Role."""

	name: str | None = None
	display_name: str | None = None
	description: str | None = None
	permissions: list[int] | None = None
	permission_groups: list[int] | None = None
