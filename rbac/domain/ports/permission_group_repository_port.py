from abc import ABC, abstractmethod

from rbac.domain.entity.permission_group import PermissionGroup


class IPermissionGroupRepositoryPort(ABC):
	"""Interfaz del repositorio para la entidad PermissionGroup"""

	@abstractmethod
	async def get_by_id(self, permission_group_id: int) -> PermissionGroup | None:
		"""Obtiene un grupo de permisos por su ID"""
		pass

	@abstractmethod
	async def save(self, permission_group: PermissionGroup) -> PermissionGroup:
		"""Guarda un grupo de permisos en el repositorio"""
		pass

	@abstractmethod
	async def delete(self, permission_group_id: int) -> None:
		pass

	@abstractmethod
	async def add_permissions(self, group_id: int, permission_ids: list[int]) -> PermissionGroup:
		pass

	@abstractmethod
	async def remove_permissions(self, group_id: int, permission_ids: list[int]) -> PermissionGroup:
		pass

	@abstractmethod
	async def count_permissions(self, group_id: int) -> int:
		pass

	@abstractmethod
	async def list(self) -> list[PermissionGroup]:
		"""Obtiene todos los grupos de permisos"""
		pass
