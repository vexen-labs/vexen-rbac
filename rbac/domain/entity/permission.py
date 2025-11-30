from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Permission:
	"""
	Permiso del sistema.

	Representa una acción específica que puede ser otorgada a un rol.
	Ejemplos: 'users.read', 'tickets.write', 'roles.delete'
	"""

	id: int | None
	name: str  # formato: "resource.action" (ej: "users.read")
	display_name: str
	description: str | None = None
	category: str = "general"  # users, tickets, roles, system
	created_at: datetime = field(default_factory=datetime.now)

	def __post_init__(self):
		"""Validación básica"""
		if not self.name or "." not in self.name:
			raise ValueError("Permission name must follow format 'resource.action'")
