from dataclasses import dataclass

from rbac.domain.ports.permission_repository_port import IPermissionRepositoryPort

from .create_permission import CreatePermission
from .delete_permission import DeletePermission
from .get_permission import GetPermission
from .list_permissions import ListPermissions
from .update_permission import UpdatePermission


@dataclass
class PermissionUseCaseFactory:
	repository: IPermissionRepositoryPort

	def __post_init__(self):
		self.create_permission = CreatePermission(self.repository)
		self.get_permission = GetPermission(self.repository)
		self.delete_permission = DeletePermission(self.repository)
		self.update_permission = UpdatePermission(self.repository)
		self.list_permissions = ListPermissions(self.repository)
