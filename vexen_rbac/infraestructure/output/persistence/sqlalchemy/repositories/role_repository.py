"""
SQLAlchemy 2.0 implementation of Role repository with async sessions.
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from vexen_rbac.domain.entity.role import Role
from vexen_rbac.domain.ports.role_repository_port import IRoleRepositoryPort
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.mappers.role_mapper import (
	RoleMapper,
)
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.permission import (
	PermissionModel,
)
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.permission_group import (
	PermissionGroupModel,
)
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.role import RoleModel


class RoleRepository(IRoleRepositoryPort):
	"""SQLAlchemy 2.0 async implementation of role repository."""

	def __init__(self, session: AsyncSession):
		"""
		Initialize repository with async session.

		Args:
			session: SQLAlchemy async session
		"""
		self.session = session

	async def get_by_id(self, role_id: int) -> Role | None:
		"""
		Retrieve a role by its ID.

		Args:
			role_id: ID of the role to retrieve

		Returns:
			Role entity if found, None otherwise
		"""
		stmt = select(RoleModel).where(RoleModel.id == role_id)
		result = await self.session.execute(stmt)
		model = result.scalar_one_or_none()

		if model is None:
			return None

		return RoleMapper.to_entity(model)

	async def save(self, role: Role) -> Role:
		"""
		Save (create or update) a role.

		Args:
			role: Role entity to save

		Returns:
			Saved role entity with updated data
		"""
		# Check if role exists
		stmt = select(RoleModel).where(RoleModel.id == role.id)
		result = await self.session.execute(stmt)
		existing_model = result.scalar_one_or_none()

		if existing_model:
			# Update existing role
			model = RoleMapper.update_model_from_entity(existing_model, role)
			# Update M2M relationships
			await self._update_relationships(model, role)
		else:
			# Create new role
			model = RoleMapper.to_model(role)
			self.session.add(model)
			await self.session.flush()
			await self.session.refresh(model)
			# Set M2M relationships
			await self._update_relationships(model, role)

		await self.session.flush()
		await self.session.refresh(model)

		return RoleMapper.to_entity(model)

	async def delete(self, role_id: int) -> None:
		"""
		Delete a role by its ID.

		Args:
			role_id: ID of the role to delete
		"""
		stmt = select(RoleModel).where(RoleModel.id == role_id)
		result = await self.session.execute(stmt)
		model = result.scalar_one_or_none()

		if model:
			await self.session.delete(model)
			await self.session.flush()

	async def _update_relationships(self, model: RoleModel, entity: Role) -> None:
		"""
		Update M2M relationships for the role.

		This is repository logic, not mapper logic.

		Args:
			model: Existing model instance (must be saved to DB)
			entity: Source entity with relationship data
		"""
		# Clear existing relationships
		model.permissions.clear()
		model.permission_groups.clear()

		# Add new permission relationships
		if entity.permissions:
			stmt = select(PermissionModel).where(PermissionModel.id.in_(entity.permissions))
			result = await self.session.execute(stmt)
			permissions = result.scalars().all()
			model.permissions.extend(permissions)

		# Add new permission group relationships
		if entity.permission_groups:
			stmt = select(PermissionGroupModel).where(
				PermissionGroupModel.id.in_(entity.permission_groups)
			)
			result = await self.session.execute(stmt)
			permission_groups = result.scalars().all()
			model.permission_groups.extend(permission_groups)

	async def add_permissions(self, role_id: int, permission_ids: list[int]) -> Role:
		stmt = select(RoleModel).where(RoleModel.id == role_id)
		result = await self.session.execute(stmt)
		model = result.scalar_one_or_none()

		if not model:
			raise ValueError(f"Role with id {role_id} not found")

		perm_stmt = select(PermissionModel).where(PermissionModel.id.in_(permission_ids))
		perm_result = await self.session.execute(perm_stmt)
		permissions = perm_result.scalars().all()

		existing_ids = {p.id for p in model.permissions}
		for permission in permissions:
			if permission.id not in existing_ids:
				model.permissions.append(permission)

		await self.session.flush()
		await self.session.refresh(model)

		return RoleMapper.to_entity(model)

	async def remove_permissions(self, role_id: int, permission_ids: list[int]) -> Role:
		stmt = select(RoleModel).where(RoleModel.id == role_id)
		result = await self.session.execute(stmt)
		model = result.scalar_one_or_none()

		if not model:
			raise ValueError(f"Role with id {role_id} not found")

		model.permissions = [p for p in model.permissions if p.id not in permission_ids]

		await self.session.flush()
		await self.session.refresh(model)

		return RoleMapper.to_entity(model)

	async def count(self) -> int:
		stmt = select(func.count()).select_from(RoleModel)
		result = await self.session.execute(stmt)
		return result.scalar_one()

	async def count_permissions(self, role_id: int) -> int:
		stmt = select(RoleModel).where(RoleModel.id == role_id)
		result = await self.session.execute(stmt)
		model = result.scalar_one_or_none()

		if not model:
			return 0

		return len(model.permissions)

	async def list_paginated(self, page: int, page_size: int) -> tuple[list[Role], int]:
		offset = (page - 1) * page_size

		count_stmt = select(func.count()).select_from(RoleModel)
		total_result = await self.session.execute(count_stmt)
		total = total_result.scalar_one()

		stmt = (
			select(RoleModel).offset(offset).limit(page_size).order_by(RoleModel.created_at.desc())
		)
		result = await self.session.execute(stmt)
		models = result.scalars().all()

		roles = [RoleMapper.to_entity(model) for model in models]
		return roles, total

	async def get_by_id_with_permissions(self, role_id: int) -> tuple[Role, list] | None:
		stmt = select(RoleModel).where(RoleModel.id == role_id)
		result = await self.session.execute(stmt)
		model = result.scalar_one_or_none()

		if model is None:
			return None

		role = RoleMapper.to_entity(model)
		permissions = [
			{
				"id": p.id,
				"name": p.name,
				"display_name": p.display_name,
				"category": p.category,
			}
			for p in model.permissions
		]

		return role, permissions

	async def list(self) -> list[Role]:
		"""
		Retrieve all roles.

		Returns:
			List of all role entities
		"""
		stmt = select(RoleModel).order_by(RoleModel.name)
		result = await self.session.execute(stmt)
		models = result.scalars().all()

		return [RoleMapper.to_entity(model) for model in models]
