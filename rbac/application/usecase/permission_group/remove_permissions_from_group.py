from dataclasses import dataclass

from rbac.application.dto.base import BaseResponse
from rbac.application.dto.permission_group_dto import PermissionGroupResponse
from rbac.domain.ports.permission_group_repository_port import (
	IPermissionGroupRepositoryPort,
)


@dataclass
class RemovePermissionsFromGroup:
	repository: IPermissionGroupRepositoryPort

	async def __call__(
		self, group_id: int, permission_ids: list[int]
	) -> BaseResponse[PermissionGroupResponse]:
		try:
			group = await self.repository.remove_permissions(group_id, permission_ids)

			response = PermissionGroupResponse(
				id=group.id,
				name=group.name,
				display_name=group.display_name,
				description=group.description,
				icon=group.icon,
				order=group.order,
				permissions=group.permissions,
				permission_count=len(group.permissions),
				created_at=group.created_at,
			)

			return BaseResponse(success=True, data=response)

		except Exception as e:
			return BaseResponse(success=False, error=str(e))
