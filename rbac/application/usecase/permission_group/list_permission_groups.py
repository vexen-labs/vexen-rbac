from dataclasses import dataclass

from rbac.application.dto.base import BaseResponse
from rbac.application.dto.permission_group_dto import PermissionGroupResponse
from rbac.domain.ports.permission_group_repository_port import (
	IPermissionGroupRepositoryPort,
)


@dataclass
class ListPermissionGroups:
	repository: IPermissionGroupRepositoryPort

	async def __call__(self) -> BaseResponse[list[PermissionGroupResponse]]:
		try:
			groups = await self.repository.list()

			response_data = [
				PermissionGroupResponse(
					id=g.id,
					name=g.name,
					display_name=g.display_name,
					description=g.description,
					icon=g.icon,
					order=g.order,
					permissions=g.permissions if g.permissions else [],
					permission_count=len(g.permissions) if g.permissions else 0,
					created_at=g.created_at,
				)
				for g in groups
			]

			return BaseResponse.ok(response_data)

		except Exception as e:
			return BaseResponse.fail(f"Error listing permission groups: {str(e)}")
