"""
Repository adapters that manage session lifecycle.

These adapters wrap the actual repository implementations and handle
AsyncSession creation/cleanup for each operation, providing a cleaner
API for the public library interface.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from rbac.domain.entity import Permission, PermissionGroup, Role
from rbac.domain.ports import (
	IPermissionGroupRepositoryPort,
	IPermissionRepositoryPort,
	IRoleRepositoryPort,
)
from rbac.infraestructure.output.persistence.sqlalchemy.repositories import (
	PermissionGroupRepository,
	PermissionRepository,
	RoleRepository,
)


class RoleRepositoryAdapter(IRoleRepositoryPort):
	"""
	Adapter for RoleRepository that manages AsyncSession lifecycle.

	This adapter creates a new session for each operation and ensures
	proper cleanup, making it safe to use across the application lifecycle.
	"""

	def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
		"""
		Initialize adapter with session factory.

		Args:
			session_factory: SQLAlchemy async session factory
		"""
		self._session_factory = session_factory

	async def get_by_id(self, role_id: int) -> Role | None:
		"""Get role by ID, managing session internally."""
		async with self._session_factory() as session:
			repository = RoleRepository(session)
			result = await repository.get_by_id(role_id)
			await session.commit()
			return result

	async def save(self, role: Role) -> Role:
		"""Save role, managing session internally."""
		async with self._session_factory() as session:
			repository = RoleRepository(session)
			result = await repository.save(role)
			await session.commit()
			return result

	async def delete(self, role_id: int) -> None:
		"""Delete role, managing session internally."""
		async with self._session_factory() as session:
			repository = RoleRepository(session)
			await repository.delete(role_id)
			await session.commit()


class PermissionRepositoryAdapter(IPermissionRepositoryPort):
	"""
	Adapter for PermissionRepository that manages AsyncSession lifecycle.
	"""

	def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
		"""
		Initialize adapter with session factory.

		Args:
			session_factory: SQLAlchemy async session factory
		"""
		self._session_factory = session_factory

	async def get_by_id(self, permission_id: int) -> Permission | None:
		"""Get permission by ID, managing session internally."""
		async with self._session_factory() as session:
			repository = PermissionRepository(session)
			result = await repository.get_by_id(permission_id)
			await session.commit()
			return result

	async def save(self, permission: Permission) -> Permission:
		"""Save permission, managing session internally."""
		async with self._session_factory() as session:
			repository = PermissionRepository(session)
			result = await repository.save(permission)
			await session.commit()
			return result

	async def delete(self, permission_id: int) -> None:
		"""Delete permission, managing session internally."""
		async with self._session_factory() as session:
			repository = PermissionRepository(session)
			await repository.delete(permission_id)
			await session.commit()


class PermissionGroupRepositoryAdapter(IPermissionGroupRepositoryPort):
	"""
	Adapter for PermissionGroupRepository that manages AsyncSession lifecycle.
	"""

	def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
		"""
		Initialize adapter with session factory.

		Args:
			session_factory: SQLAlchemy async session factory
		"""
		self._session_factory = session_factory

	async def get_by_id(self, permission_group_id: int) -> PermissionGroup | None:
		"""Get permission group by ID, managing session internally."""
		async with self._session_factory() as session:
			repository = PermissionGroupRepository(session)
			result = await repository.get_by_id(permission_group_id)
			await session.commit()
			return result

	async def save(self, permission_group: PermissionGroup) -> PermissionGroup:
		"""Save permission group, managing session internally."""
		async with self._session_factory() as session:
			repository = PermissionGroupRepository(session)
			result = await repository.save(permission_group)
			await session.commit()
			return result

	async def delete(self, permission_group_id: int) -> None:
		"""Delete permission group, managing session internally."""
		async with self._session_factory() as session:
			repository = PermissionGroupRepository(session)
			await repository.delete(permission_group_id)
			await session.commit()
