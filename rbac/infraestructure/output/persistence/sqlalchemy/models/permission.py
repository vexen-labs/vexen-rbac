"""
SQLAlchemy model for Permission entity.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rbac.infraestructure.output.persistence.sqlalchemy.models.associations import (
	PermissionGroupPermissionAssociation,
	RolePermissionAssociation,
)
from rbac.infraestructure.output.persistence.sqlalchemy.models.base import Base

if TYPE_CHECKING:
	from rbac.infraestructure.output.persistence.sqlalchemy.models.permission_group import (
		PermissionGroupModel,
	)
	from rbac.infraestructure.output.persistence.sqlalchemy.models.role import (
		RoleModel,
	)


class PermissionModel(Base):
	"""
	SQLAlchemy model for Permission.

	Represents a specific action that can be granted to a role.
	Examples: 'users.read', 'tickets.write', 'roles.delete'
	"""

	__tablename__ = "permissions"

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
	display_name: Mapped[str] = mapped_column(String(200), nullable=False)
	description: Mapped[str | None] = mapped_column(Text, nullable=True)
	category: Mapped[str] = mapped_column(String(50), default="general", nullable=False)
	created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)

	# Relationships using declarative association models
	roles: Mapped[list["RoleModel"]] = relationship(
		"RoleModel",
		secondary=RolePermissionAssociation.__table__,
		back_populates="permissions",
		lazy="selectin",
	)
	permission_groups: Mapped[list["PermissionGroupModel"]] = relationship(
		"PermissionGroupModel",
		secondary=PermissionGroupPermissionAssociation.__table__,
		back_populates="permissions",
		lazy="selectin",
	)

	def __repr__(self) -> str:
		return f"<PermissionModel(id={self.id}, name={self.name})>"

	def __str__(self) -> str:
		return f"{self.name} - {self.display_name}"
