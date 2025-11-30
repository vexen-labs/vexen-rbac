"""
SQLAlchemy model for PermissionGroup entity.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.associations import (
	PermissionGroupPermissionAssociation,
	RolePermissionGroupAssociation,
)
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.base import Base

if TYPE_CHECKING:
	from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.permission import (
		PermissionModel,
	)
	from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.role import (
		RoleModel,
	)


class PermissionGroupModel(Base):
	"""
	SQLAlchemy model for PermissionGroup.

	Groups related permissions for easier UI management.
	Examples: 'User Management', 'Ticket Management', 'System Administration'
	"""

	__tablename__ = "permission_groups"

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
	display_name: Mapped[str] = mapped_column(String(200), nullable=False)
	description: Mapped[str | None] = mapped_column(Text, nullable=True)
	icon: Mapped[str | None] = mapped_column(String(50), nullable=True)
	order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
	created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)

	# Relationships using declarative association models
	permissions: Mapped[list["PermissionModel"]] = relationship(
		"PermissionModel",
		secondary=PermissionGroupPermissionAssociation.__table__,
		back_populates="permission_groups",
		lazy="selectin",
	)
	roles: Mapped[list["RoleModel"]] = relationship(
		"RoleModel",
		secondary=RolePermissionGroupAssociation.__table__,
		back_populates="permission_groups",
		lazy="selectin",
	)

	def __repr__(self) -> str:
		return f"<PermissionGroupModel(id={self.id}, name={self.name})>"

	def __str__(self) -> str:
		return self.display_name
