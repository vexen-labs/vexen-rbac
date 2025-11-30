from dataclasses import dataclass

from rbac.domain.ports.permission_group_repository_port import IPermissionGroupRepositoryPort

from .create_permission_group import CreatePermissionGroup
from .delete_permission_group import DeletePermissionGroup
from .get_permission_group import GetPermissionGroup
from .list_permission_groups import ListPermissionGroups
from .update_permission_group import UpdatePermissionGroup


@dataclass
class PermissionGroupUseCaseFactory:
	repository: IPermissionGroupRepositoryPort

	def __post_init__(self):
		self.create_permission_group = CreatePermissionGroup(self.repository)
		self.get_permission_group = GetPermissionGroup(self.repository)
		self.delete_permission_group = DeletePermissionGroup(self.repository)
		self.update_permission_group = UpdatePermissionGroup(self.repository)
		self.list_permission_groups = ListPermissionGroups(self.repository)
