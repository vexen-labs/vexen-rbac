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
		"""Elimina un rol por su ID"""
		pass
