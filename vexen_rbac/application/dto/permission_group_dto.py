"""
DTOs for PermissionGroup use cases.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class PermissionGroupResponse:
	"""Response DTO for PermissionGroup."""

	id: int
	name: str
	display_name: str
	description: str | None
	icon: str | None
	order: int
	permissions: list[int]
	permission_count: int
	created_at: datetime


@dataclass
class CreatePermissionGroupRequest:
	"""Request DTO for creating a PermissionGroup."""

	name: str
	display_name: str
	description: str | None = None
	icon: str | None = None
	order: int = 0
	permissions: list[int] | None = None


@dataclass
class UpdatePermissionGroupRequest:
	"""Request DTO for updating a PermissionGroup."""

	name: str | None = None
	display_name: str | None = None
	description: str | None = None
	icon: str | None = None
	order: int | None = None
	permissions: list[int] | None = None
