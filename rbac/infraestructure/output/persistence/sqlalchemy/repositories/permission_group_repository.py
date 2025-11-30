"""
SQLAlchemy 2.0 implementation of PermissionGroup repository with async sessions.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from rbac.domain.entity.permission_group import PermissionGroup
from rbac.domain.ports.permission_group_repository_port import (
	IPermissionGroupRepositoryPort,
)
from rbac.infraestructure.output.persistence.sqlalchemy.mappers.permission_group_mapper import (
	PermissionGroupMapper,
)
from rbac.infraestructure.output.persistence.sqlalchemy.models.permission import (
	PermissionModel,
)
from rbac.infraestructure.output.persistence.sqlalchemy.models.permission_group import (
	PermissionGroupModel,
)


class PermissionGroupRepository(IPermissionGroupRepositoryPort):
	"""SQLAlchemy 2.0 async implementation of permission group repository."""

	def __init__(self, session: AsyncSession):
		"""
		Initialize repository with async session.

		Args:
			session: SQLAlchemy async session
		"""
		self.session = session

	async def get_by_id(self, permission_group_id: int) -> PermissionGroup | None:
		"""
		Retrieve a permission group by its ID.

		Args:
			permission_group_id: ID of the permission group to retrieve

		Returns:
			PermissionGroup entity if found, None otherwise
		"""
		stmt = select(PermissionGroupModel).where(PermissionGroupModel.id == permission_group_id)
		result = await self.session.execute(stmt)
		model = result.scalar_one_or_none()

		if model is None:
			return None

		return PermissionGroupMapper.to_entity(model)

	async def save(self, permission_group: PermissionGroup) -> PermissionGroup:
		"""
		Save (create or update) a permission group.

		Args:
			permission_group: PermissionGroup entity to save

		Returns:
			Saved permission group entity with updated data
		"""
		# Check if permission group exists
		stmt = select(PermissionGroupModel).where(PermissionGroupModel.id == permission_group.id)
		result = await self.session.execute(stmt)
		existing_model = result.scalar_one_or_none()

		if existing_model:
			# Update existing permission group
			model = PermissionGroupMapper.update_model_from_entity(existing_model, permission_group)
			# Update M2M relationships
			await self._update_permissions_relationship(model, permission_group)
		else:
			# Create new permission group
			model = PermissionGroupMapper.to_model(permission_group)
			self.session.add(model)
			await self.session.flush()
			await self.session.refresh(model)
			# Set M2M relationships
			await self._update_permissions_relationship(model, permission_group)

		await self.session.flush()
		await self.session.refresh(model)

		return PermissionGroupMapper.to_entity(model)

	async def delete(self, permission_group_id: int) -> None:
		"""
		Delete a permission group by its ID.

		Args:
			permission_group_id: ID of the permission group to delete
		"""
		stmt = select(PermissionGroupModel).where(PermissionGroupModel.id == permission_group_id)
		result = await self.session.execute(stmt)
		model = result.scalar_one_or_none()

		if model:
			await self.session.delete(model)
			await self.session.flush()

	async def _update_permissions_relationship(
		self, model: PermissionGroupModel, entity: PermissionGroup
	) -> None:
		"""
		Update M2M relationship between permission group and permissions.

		This is repository logic, not mapper logic.

		Args:
			model: Existing model instance (must be saved to DB)
			entity: Source entity with relationship data
		"""
		# Clear existing relationships
		model.permissions.clear()

		# Add new relationships
		if entity.permissions:
			stmt = select(PermissionModel).where(PermissionModel.id.in_(entity.permissions))
			result = await self.session.execute(stmt)
			permissions = result.scalars().all()
			model.permissions.extend(permissions)

	async def add_permissions(self, group_id: int, permission_ids: list[int]) -> PermissionGroup:
		stmt = select(PermissionGroupModel).where(PermissionGroupModel.id == group_id)
		result = await self.session.execute(stmt)
		model = result.scalar_one_or_none()

		if not model:
			raise ValueError(f"Permission group with id {group_id} not found")

		perm_stmt = select(PermissionModel).where(PermissionModel.id.in_(permission_ids))
		perm_result = await self.session.execute(perm_stmt)
		permissions = perm_result.scalars().all()

		existing_ids = {p.id for p in model.permissions}
		for permission in permissions:
			if permission.id not in existing_ids:
				model.permissions.append(permission)

		await self.session.flush()
		await self.session.refresh(model)

		return PermissionGroupMapper.to_entity(model)

	async def remove_permissions(self, group_id: int, permission_ids: list[int]) -> PermissionGroup:
		stmt = select(PermissionGroupModel).where(PermissionGroupModel.id == group_id)
		result = await self.session.execute(stmt)
		model = result.scalar_one_or_none()

		if not model:
			raise ValueError(f"Permission group with id {group_id} not found")

		model.permissions = [p for p in model.permissions if p.id not in permission_ids]

		await self.session.flush()
		await self.session.refresh(model)

		return PermissionGroupMapper.to_entity(model)

	async def count_permissions(self, group_id: int) -> int:
		stmt = select(PermissionGroupModel).where(PermissionGroupModel.id == group_id)
		result = await self.session.execute(stmt)
		model = result.scalar_one_or_none()

		if not model:
			return 0

		return len(model.permissions)
