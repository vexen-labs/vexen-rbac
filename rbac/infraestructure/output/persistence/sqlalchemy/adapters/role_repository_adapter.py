from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from rbac.domain.entity import Role
from rbac.domain.ports import IRoleRepositoryPort
from rbac.infraestructure.output.persistence.sqlalchemy.repositories import (
	RoleRepository,
)


class RoleRepositoryAdapter(IRoleRepositoryPort):
	def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
		self._session_factory = session_factory

	async def get_by_id(self, role_id: int) -> Role | None:
		async with self._session_factory() as session:
			repository = RoleRepository(session)
			result = await repository.get_by_id(role_id)
			await session.commit()
			return result

	async def save(self, role: Role) -> Role:
		async with self._session_factory() as session:
			repository = RoleRepository(session)
			result = await repository.save(role)
			await session.commit()
			return result

	async def delete(self, role_id: int) -> None:
		async with self._session_factory() as session:
			repository = RoleRepository(session)
			await repository.delete(role_id)
			await session.commit()

	async def add_permissions(self, role_id: int, permission_ids: list[int]) -> Role:
		async with self._session_factory() as session:
			repository = RoleRepository(session)
			result = await repository.add_permissions(role_id, permission_ids)
			await session.commit()
			return result

	async def remove_permissions(self, role_id: int, permission_ids: list[int]) -> Role:
		async with self._session_factory() as session:
			repository = RoleRepository(session)
			result = await repository.remove_permissions(role_id, permission_ids)
			await session.commit()
			return result

	async def count(self) -> int:
		async with self._session_factory() as session:
			repository = RoleRepository(session)
			result = await repository.count()
			await session.commit()
			return result

	async def count_permissions(self, role_id: int) -> int:
		async with self._session_factory() as session:
			repository = RoleRepository(session)
			result = await repository.count_permissions(role_id)
			await session.commit()
			return result

	async def list_paginated(self, page: int, page_size: int) -> tuple[list[Role], int]:
		async with self._session_factory() as session:
			repository = RoleRepository(session)
			result = await repository.list_paginated(page, page_size)
			await session.commit()
			return result

	async def get_by_id_with_permissions(self, role_id: int) -> tuple[Role, list] | None:
		async with self._session_factory() as session:
			repository = RoleRepository(session)
			result = await repository.get_by_id_with_permissions(role_id)
			await session.commit()
			return result
