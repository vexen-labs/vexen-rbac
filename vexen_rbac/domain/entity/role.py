from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Role:
	"""
	Rol del sistema.

	Agrupa permisos y se asigna a usuarios.
	Ejemplos: admin, supervisor, operator, viewer
	"""

	id: int
	name: str  # slug: admin, supervisor
	display_name: str  # Administrador, Supervisor
	description: str | None = None
	permissions: list[int] = field(default_factory=list)  # IDs de Permission
	permission_groups: list[int] = field(default_factory=list)  # IDs de PermissionGroup
	user_count: int = 0  # Calculado, no persistido
	created_at: datetime = field(default_factory=datetime.now)
	updated_at: datetime | None = None

	def has_permission(self, permission_name: str) -> bool:
		"""Verifica si este rol tiene un permiso específico"""
		# En implementación real, se haría JOIN con tabla permissions
		# Aquí es solo la interfaz del dominio
		raise NotImplementedError("Debe implementarse en el repositorio")
