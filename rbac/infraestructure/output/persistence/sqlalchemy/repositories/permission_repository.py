"""
SQLAlchemy 2.0 implementation of Permission repository with async sessions.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from rbac.domain.entity.permission import Permission
from rbac.domain.ports.permission_repository_port import IPermissionRepositoryPort
from rbac.infraestructure.output.persistence.sqlalchemy.mappers.permission_mapper import (
	PermissionMapper,
)
from rbac.infraestructure.output.persistence.sqlalchemy.models.permission import (
	PermissionModel,
)


class PermissionRepository(IPermissionRepositoryPort):
	"""SQLAlchemy 2.0 async implementation of permission repository."""

	def __init__(self, session: AsyncSession):
		"""
		Initialize repository with async session.

		Args:
			session: SQLAlchemy async session
		"""
		self.session = session

	async def get_by_id(self, permission_id: int) -> Permission | None:
		"""
		Retrieve a permission by its ID.

		Args:
			permission_id: ID of the permission to retrieve

		Returns:
			Permission entity if found, None otherwise
		"""
		stmt = select(PermissionModel).where(PermissionModel.id == permission_id)
		result = await self.session.execute(stmt)
		model = result.scalar_one_or_none()

		if model is None:
			return None

		return PermissionMapper.to_entity(model)

	async def save(self, permission: Permission) -> Permission:
		"""
		Save (create or update) a permission.

		Args:
			permission: Permission entity to save

		Returns:
			Saved permission entity with updated data
		"""
		# Check if permission exists
		stmt = select(PermissionModel).where(PermissionModel.id == permission.id)
		result = await self.session.execute(stmt)
		existing_model = result.scalar_one_or_none()

		if existing_model:
			# Update existing permission
			model = PermissionMapper.update_model_from_entity(existing_model, permission)
		else:
			# Create new permission
			model = PermissionMapper.to_model(permission)
			self.session.add(model)

		await self.session.flush()
		await self.session.refresh(model)

		return PermissionMapper.to_entity(model)

	async def delete(self, permission_id: int) -> None:
		"""
		Delete a permission by its ID.

		Args:
			permission_id: ID of the permission to delete
		"""
		stmt = select(PermissionModel).where(PermissionModel.id == permission_id)
		result = await self.session.execute(stmt)
		model = result.scalar_one_or_none()

		if model:
			await self.session.delete(model)
			await self.session.flush()

	async def group_by_category(self) -> dict[str, list[Permission]]:
		from rbac.infraestructure.output.persistence.sqlalchemy.mappers.permission_mapper import (
			PermissionMapper,
		)

		stmt = select(PermissionModel).order_by(PermissionModel.category, PermissionModel.name)
		result = await self.session.execute(stmt)
		models = result.scalars().all()

		grouped = {}
		for model in models:
			permission = PermissionMapper.to_entity(model)
			if permission.category not in grouped:
				grouped[permission.category] = []
			grouped[permission.category].append(permission)

		return grouped
