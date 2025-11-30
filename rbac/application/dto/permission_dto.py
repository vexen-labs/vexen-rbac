"""
DTOs for Permission use cases.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class PermissionResponse:
	"""Response DTO for Permission."""

	id: int
	name: str
	display_name: str
	description: str | None
	category: str
	created_at: datetime


@dataclass
class CreatePermissionRequest:
	"""Request DTO for creating a Permission."""

	name: str
	display_name: str
	description: str | None = None
	category: str = "general"


@dataclass
class UpdatePermissionRequest:
	"""Request DTO for updating a Permission."""

	name: str | None = None
	display_name: str | None = None
	description: str | None = None
	category: str | None = None
