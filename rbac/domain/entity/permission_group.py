from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class PermissionGroup:
    """
    Grupo de permisos.

    Agrupa permisos relacionados para facilitar la gestión en la UI.
    Ejemplos: 'Gestión de Usuarios', 'Gestión de Tickets', 'Administración del Sistema'
    """

    id: int
    name: str  # slug: users_management, tickets_management
    display_name: str  # Gestión de Usuarios, Gestión de Tickets
    description: Optional[str] = None
    icon: Optional[str] = None  # Nombre del ícono para la UI
    order: int = 0  # Orden de presentación en la UI
    permissions: List[int] = field(default_factory=list)  # IDs de Permission
    created_at: datetime = field(default_factory=datetime.now)

    def has_permissions(self) -> bool:
        """Verifica si el grupo tiene permisos asignados"""
        return len(self.permissions) > 0

    def permission_count(self) -> int:
        """Retorna la cantidad de permisos en el grupo"""
        return len(self.permissions)
