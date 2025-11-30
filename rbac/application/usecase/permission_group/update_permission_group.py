from dataclasses import dataclass

from rbac.application.dto.base import BaseResponse
from rbac.application.dto.permission_group_dto import (
	PermissionGroupResponse,
	UpdatePermissionGroupRequest,
)
from rbac.domain.ports.permission_group_repository_port import (
	IPermissionGroupRepositoryPort,
)


@dataclass
class UpdatePermissionGroup:
	repository: IPermissionGroupRepositoryPort

	async def __call__(
		self, permission_group_id: int, request: UpdatePermissionGroupRequest
	) -> BaseResponse[PermissionGroupResponse]:
		try:
			permission_group = await self.repository.get_by_id(permission_group_id)

			if permission_group is None:
				return BaseResponse.fail(
					f"Permission group with ID {permission_group_id} not found"
				)

			if request.name is not None:
				permission_group.name = request.name
			if request.display_name is not None:
				permission_group.display_name = request.display_name
			if request.description is not None:
				permission_group.description = request.description
			if request.icon is not None:
				permission_group.icon = request.icon
			if request.order is not None:
				permission_group.order = request.order
			if request.permissions is not None:
				permission_group.permissions = request.permissions

			updated_group = await self.repository.save(permission_group)

			response = PermissionGroupResponse(
				id=updated_group.id,
				name=updated_group.name,
				display_name=updated_group.display_name,
				description=updated_group.description,
				icon=updated_group.icon,
				order=updated_group.order,
				permissions=updated_group.permissions,
				permission_count=updated_group.permission_count(),
				created_at=updated_group.created_at,
			)

			return BaseResponse.ok(response)

		except Exception as e:
			return BaseResponse.fail(f"Error updating permission group: {str(e)}")
