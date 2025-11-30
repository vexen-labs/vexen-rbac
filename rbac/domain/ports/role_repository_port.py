from abc import ABC, abstractmethod

from rbac.domain.entity.role import Role


class IRoleRepositoryPort(ABC):
	"""Interfaz del repositorio para la entidad Role"""

	@abstractmethod
	async def get_by_id(self, role_id: int) -> Role | None:
		"""Obtiene un rol por su ID"""
		pass

	@abstractmethod
	async def save(self, role: Role) -> Role:
		"""Guarda un rol en el repositorio"""
		pass

	@abstractmethod
	async def delete(self, role_id: int) -> None:
		pass

	@abstractmethod
	async def add_permissions(self, role_id: int, permission_ids: list[int]) -> Role:
		pass

	@abstractmethod
	async def remove_permissions(self, role_id: int, permission_ids: list[int]) -> Role:
		pass

	@abstractmethod
	async def count(self) -> int:
		pass

	@abstractmethod
	async def count_permissions(self, role_id: int) -> int:
		pass

	@abstractmethod
	async def list_paginated(self, page: int, page_size: int) -> tuple[list[Role], int]:
		pass

	@abstractmethod
	async def get_by_id_with_permissions(self, role_id: int) -> tuple[Role, list] | None:
		pass

	@abstractmethod
	async def list(self) -> list[Role]:
		"""Obtiene todos los roles"""
		pass
