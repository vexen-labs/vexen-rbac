from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from rbac.domain.entity import PermissionGroup
from rbac.domain.ports import IPermissionGroupRepositoryPort
from rbac.infraestructure.output.persistence.sqlalchemy.repositories import (
	PermissionGroupRepository,
)


class PermissionGroupRepositoryAdapter(IPermissionGroupRepositoryPort):
	def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
		self._session_factory = session_factory

	async def get_by_id(self, permission_group_id: int) -> PermissionGroup | None:
		async with self._session_factory() as session:
			repository = PermissionGroupRepository(session)
			result = await repository.get_by_id(permission_group_id)
			await session.commit()
			return result

	async def save(self, permission_group: PermissionGroup) -> PermissionGroup:
		async with self._session_factory() as session:
			repository = PermissionGroupRepository(session)
			result = await repository.save(permission_group)
			await session.commit()
			return result

	async def delete(self, permission_group_id: int) -> None:
		async with self._session_factory() as session:
			repository = PermissionGroupRepository(session)
			await repository.delete(permission_group_id)
			await session.commit()

	async def add_permissions(self, group_id: int, permission_ids: list[int]) -> PermissionGroup:
		async with self._session_factory() as session:
			repository = PermissionGroupRepository(session)
			result = await repository.add_permissions(group_id, permission_ids)
			await session.commit()
			return result

	async def remove_permissions(self, group_id: int, permission_ids: list[int]) -> PermissionGroup:
		async with self._session_factory() as session:
			repository = PermissionGroupRepository(session)
			result = await repository.remove_permissions(group_id, permission_ids)
			await session.commit()
			return result

	async def count_permissions(self, group_id: int) -> int:
		async with self._session_factory() as session:
			repository = PermissionGroupRepository(session)
			result = await repository.count_permissions(group_id)
			await session.commit()
			return result
