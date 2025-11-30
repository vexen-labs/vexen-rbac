from dataclasses import dataclass

from vexen_rbac.domain.ports.role_repository_port import IRoleRepositoryPort

from .add_permissions_to_role import AddPermissionsToRole
from .count_role_permissions import CountRolePermissions
from .count_roles import CountRoles
from .create_role import CreateRole
from .delete_role import DeleteRole
from .get_role import GetRole
from .get_role_expanded import GetRoleExpanded
from .list_roles import ListRoles
from .list_roles_paginated import ListRolesPaginated
from .remove_permissions_from_role import RemovePermissionsFromRole
from .update_role import UpdateRole


@dataclass
class RoleUseCaseFactory:
	repository: IRoleRepositoryPort

	def __post_init__(self):
		self.create_role = CreateRole(self.repository)
		self.get_role = GetRole(self.repository)
		self.get_role_expanded = GetRoleExpanded(self.repository)
		self.update_role = UpdateRole(self.repository)
		self.delete_role = DeleteRole(self.repository)
		self.list_roles = ListRoles(self.repository)
		self.list_roles_paginated = ListRolesPaginated(self.repository)
		self.add_permissions = AddPermissionsToRole(self.repository)
		self.remove_permissions = RemovePermissionsFromRole(self.repository)
		self.count_roles = CountRoles(self.repository)
		self.count_permissions = CountRolePermissions(self.repository)
