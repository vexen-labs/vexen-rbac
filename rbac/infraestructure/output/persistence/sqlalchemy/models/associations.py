"""
Association models for many-to-many relationships.

These are declarative models instead of Table objects for better
type safety and potential future extension.
"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from rbac.infraestructure.output.persistence.sqlalchemy.models.base import Base


class RolePermissionAssociation(Base):
	"""
	Association model for Role ↔ Permission relationship.

	This represents the many-to-many relationship between roles and permissions.
	"""

	__tablename__ = "role_permissions"

	role_id: Mapped[int] = mapped_column(
		ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
	)
	permission_id: Mapped[int] = mapped_column(
		ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True
	)

	def __repr__(self) -> str:
		return f"<RolePermission(role_id={self.role_id}, permission_id={self.permission_id})>"


class RolePermissionGroupAssociation(Base):
	"""
	Association model for Role ↔ PermissionGroup relationship.

	This represents the many-to-many relationship between roles and permission groups.
	"""

	__tablename__ = "role_permission_groups"

	role_id: Mapped[int] = mapped_column(
		ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
	)
	permission_group_id: Mapped[int] = mapped_column(
		ForeignKey("permission_groups.id", ondelete="CASCADE"), primary_key=True
	)

	def __repr__(self) -> str:
		return (
			f"<RolePermissionGroup(role_id={self.role_id}, "
			f"permission_group_id={self.permission_group_id})>"
		)


class PermissionGroupPermissionAssociation(Base):
	"""
	Association model for PermissionGroup ↔ Permission relationship.

	This represents the many-to-many relationship between permission groups
	and permissions.
	"""

	__tablename__ = "permission_group_permissions"

	permission_group_id: Mapped[int] = mapped_column(
		ForeignKey("permission_groups.id", ondelete="CASCADE"), primary_key=True
	)
	permission_id: Mapped[int] = mapped_column(
		ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True
	)

	def __repr__(self) -> str:
		return (
			f"<PermissionGroupPermission("
			f"permission_group_id={self.permission_group_id}, "
			f"permission_id={self.permission_id})>"
		)
