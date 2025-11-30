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
			return BaseResponse.fail("List all permission groups not yet implemented in repository")

		except Exception as e:
			return BaseResponse.fail(f"Error listing permission groups: {str(e)}")
