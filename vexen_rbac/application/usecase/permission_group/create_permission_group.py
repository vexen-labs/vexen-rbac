from dataclasses import dataclass
from datetime import datetime

from vexen_rbac.application.dto.base import BaseResponse
from vexen_rbac.application.dto.permission_group_dto import (
	CreatePermissionGroupRequest,
	PermissionGroupResponse,
)
from vexen_rbac.domain.entity.permission_group import PermissionGroup
from vexen_rbac.domain.ports.permission_group_repository_port import (
	IPermissionGroupRepositoryPort,
)


@dataclass
class CreatePermissionGroup:
	repository: IPermissionGroupRepositoryPort

	async def __call__(
		self, request: CreatePermissionGroupRequest
	) -> BaseResponse[PermissionGroupResponse]:
		try:
			permission_group = PermissionGroup(
				id=0,
				name=request.name,
				display_name=request.display_name,
				description=request.description,
				icon=request.icon,
				order=request.order,
				permissions=request.permissions or [],
				created_at=datetime.now(),
			)

			saved_group = await self.repository.save(permission_group)

			response = PermissionGroupResponse(
				id=saved_group.id,
				name=saved_group.name,
				display_name=saved_group.display_name,
				description=saved_group.description,
				icon=saved_group.icon,
				order=saved_group.order,
				permissions=saved_group.permissions,
				permission_count=saved_group.permission_count(),
				created_at=saved_group.created_at,
			)

			return BaseResponse.ok(response)

		except Exception as e:
			return BaseResponse.fail(f"Error creating permission group: {str(e)}")
