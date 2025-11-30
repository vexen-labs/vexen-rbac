"""
SQLAlchemy model for Role entity.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.associations import (
	RolePermissionAssociation,
	RolePermissionGroupAssociation,
)
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.base import Base

if TYPE_CHECKING:
	from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.permission import (
		PermissionModel,
	)
	from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.permission_group import (
		PermissionGroupModel,
	)


class RoleModel(Base):
	"""
	SQLAlchemy model for Role.

	Groups permissions and is assigned to users.
	Examples: admin, supervisor, operator, viewer
	"""

	__tablename__ = "roles"

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
	display_name: Mapped[str] = mapped_column(String(200), nullable=False)
	description: Mapped[str | None] = mapped_column(Text, nullable=True)
	created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
	updated_at: Mapped[datetime | None] = mapped_column(
		default=datetime.now, onupdate=datetime.now, nullable=True
	)

	# Relationships using declarative association models
	permissions: Mapped[list["PermissionModel"]] = relationship(
		"PermissionModel",
		secondary=RolePermissionAssociation.__table__,
		back_populates="roles",
		lazy="selectin",
	)
	permission_groups: Mapped[list["PermissionGroupModel"]] = relationship(
		"PermissionGroupModel",
		secondary=RolePermissionGroupAssociation.__table__,
		back_populates="roles",
		lazy="selectin",
	)

	def __repr__(self) -> str:
		return f"<RoleModel(id={self.id}, name={self.name})>"

	def __str__(self) -> str:
		return self.display_name
