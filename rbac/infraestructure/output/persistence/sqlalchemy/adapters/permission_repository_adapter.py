from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from rbac.domain.entity import Permission
from rbac.domain.ports import IPermissionRepositoryPort
from rbac.infraestructure.output.persistence.sqlalchemy.repositories import (
	PermissionRepository,
)


class PermissionRepositoryAdapter(IPermissionRepositoryPort):
	def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
		self._session_factory = session_factory

	async def get_by_id(self, permission_id: int) -> Permission | None:
		async with self._session_factory() as session:
			repository = PermissionRepository(session)
			result = await repository.get_by_id(permission_id)
			await session.commit()
			return result

	async def save(self, permission: Permission) -> Permission:
		async with self._session_factory() as session:
			repository = PermissionRepository(session)
			result = await repository.save(permission)
			await session.commit()
			return result

	async def delete(self, permission_id: int) -> None:
		async with self._session_factory() as session:
			repository = PermissionRepository(session)
			await repository.delete(permission_id)
			await session.commit()

	async def group_by_category(self) -> dict[str, list[Permission]]:
		async with self._session_factory() as session:
			repository = PermissionRepository(session)
			result = await repository.group_by_category()
			await session.commit()
			return result

	async def list(self) -> list[Permission]:
		async with self._session_factory() as session:
			repository = PermissionRepository(session)
			result = await repository.list()
			await session.commit()
			return result
