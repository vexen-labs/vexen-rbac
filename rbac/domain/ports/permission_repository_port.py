from abc import ABC, abstractmethod

from rbac.domain.entity.permission import Permission


class IPermissionRepositoryPort(ABC):
	"""Interfaz del repositorio para la entidad Permission"""

	@abstractmethod
	async def get_by_id(self, permission_id: int) -> Permission | None:
		"""Obtiene un permiso por su ID"""
		pass

	@abstractmethod
	async def save(self, permission: Permission) -> Permission:
		"""Guarda un permiso en el repositorio"""
		pass

	@abstractmethod
	async def delete(self, permission_id: int) -> None:
		pass

	@abstractmethod
	async def group_by_category(self) -> dict[str, list[Permission]]:
		pass
