from dataclasses import dataclass

from rbac.domain.ports.role_repository_port import IRoleRepositoryPort

from .create_role import CreateRole
from .delete_role import DeleteRole
from .get_role import GetRole
from .list_roles import ListRoles
from .update_role import UpdateRole


@dataclass
class RoleUseCaseFactory:
	repository: IRoleRepositoryPort

	def __post_init__(self):
		self.create_role = CreateRole(self.repository)
		self.get_role = GetRole(self.repository)
		self.update_role = UpdateRole(self.repository)
		self.delete_role = DeleteRole(self.repository)
		self.list_roles = ListRoles(self.repository)
