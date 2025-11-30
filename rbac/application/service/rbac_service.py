from dataclasses import dataclass

from rbac.application.usecase import (
	PermissionGroupUseCaseFactory,
	PermissionUseCaseFactory,
	RoleUseCaseFactory,
)
from rbac.domain.ports import (
	IPermissionGroupRepositoryPort,
	IPermissionRepositoryPort,
	IRoleRepositoryPort,
)


@dataclass
class RBACService:
	_role_repository: IRoleRepositoryPort
	_permission_repository: IPermissionRepositoryPort
	_permission_group_repository: IPermissionGroupRepositoryPort

	def __post_init__(self):
		self.roles = RoleUseCaseFactory(self._role_repository)
		self.permissions = PermissionUseCaseFactory(self._permission_repository)
		self.permission_groups = PermissionGroupUseCaseFactory(self._permission_group_repository)

	async def health_check(self) -> bool:
		"""
		Perform a health check of the RBAC service.

		Returns:
			True if the service is healthy, False otherwise
		"""
		# Implement actual health check logic here (e.g., database connectivity)
		return True

	async def get_role_by_id(self, role_id: int):
		return await self.roles.get_role(role_id)

	async def get_list_of_roles(self):
		return await self.roles.list_roles()

	async def get_permission_by_id(self, permission_id: int):
		return await self.permissions.get_permission(permission_id)

	async def get_list_of_permissions(self):
		return await self.permissions.list_permissions()

	async def get_permission_group_by_id(self, permission_group_id: int):
		return await self.permission_groups.get_permission_group(permission_group_id)

	async def get_list_of_permission_groups(self):
		return await self.permission_groups.list_permission_groups()

	async def create_role(self, role_data):
		return await self.roles.create_role(role_data)

	async def create_permission(self, permission_data):
		return await self.permissions.create_permission(permission_data)

	async def create_permission_group(self, permission_group_data):
		return await self.permission_groups.create_permission_group(permission_group_data)

	async def update_role(self, role_id: int, role_data):
		return await self.roles.update_role(role_id, role_data)

	async def update_permission(self, permission_id: int, permission_data):
		return await self.permissions.update_permission(permission_id, permission_data)

	async def update_permission_group(self, permission_group_id: int, permission_group_data):
		return await self.permission_groups.update_permission_group(
			permission_group_id, permission_group_data
		)

	async def delete_role(self, role_id: int):
		return await self.roles.delete_role(role_id)

	async def delete_permission(self, permission_id: int):
		return await self.permissions.delete_permission(permission_id)

	async def delete_permission_group(self, permission_group_id: int):
		return await self.permission_groups.delete_permission_group(permission_group_id)

	async def add_permissions_to_role(self, role_id: int, permission_ids: list[int]):
		return await self.roles.add_permissions(role_id, permission_ids)

	async def remove_permissions_from_role(self, role_id: int, permission_ids: list[int]):
		return await self.roles.remove_permissions(role_id, permission_ids)

	async def add_permissions_to_group(self, group_id: int, permission_ids: list[int]):
		return await self.permission_groups.add_permissions(group_id, permission_ids)

	async def remove_permissions_from_group(self, group_id: int, permission_ids: list[int]):
		return await self.permission_groups.remove_permissions(group_id, permission_ids)

	async def count_roles(self):
		return await self.roles.count_roles()

	async def count_role_permissions(self, role_id: int):
		return await self.roles.count_permissions(role_id)

	async def count_group_permissions(self, group_id: int):
		return await self.permission_groups.count_permissions(group_id)

	async def list_roles_paginated(self, page: int = 1, page_size: int = 20):
		from rbac.application.dto import PaginationRequest

		request = PaginationRequest(page=page, page_size=page_size)
		return await self.roles.list_roles_paginated(request)

	async def get_role_expanded(self, role_id: int):
		return await self.roles.get_role_expanded(role_id)

	async def get_permissions_grouped(self):
		return await self.permissions.get_permissions_grouped()
