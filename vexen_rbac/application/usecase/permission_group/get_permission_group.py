from dataclasses import dataclass

from vexen_rbac.application.dto.base import BaseResponse
from vexen_rbac.application.dto.permission_group_dto import PermissionGroupResponse
from vexen_rbac.domain.ports.permission_group_repository_port import (
	IPermissionGroupRepositoryPort,
)


@dataclass
class GetPermissionGroup:
	repository: IPermissionGroupRepositoryPort

	async def __call__(self, permission_group_id: int) -> BaseResponse[PermissionGroupResponse]:
		try:
			permission_group = await self.repository.get_by_id(permission_group_id)

			if permission_group is None:
				return BaseResponse.fail(
					f"Permission group with ID {permission_group_id} not found"
				)

			response = PermissionGroupResponse(
				id=permission_group.id,
				name=permission_group.name,
				display_name=permission_group.display_name,
				description=permission_group.description,
				icon=permission_group.icon,
				order=permission_group.order,
				permissions=permission_group.permissions,
				permission_count=permission_group.permission_count(),
				created_at=permission_group.created_at,
			)

			return BaseResponse.ok(response)

		except Exception as e:
			return BaseResponse.fail(f"Error getting permission group: {str(e)}")
