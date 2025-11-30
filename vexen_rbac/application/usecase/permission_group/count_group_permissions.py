from dataclasses import dataclass

from vexen_rbac.application.dto.base import BaseResponse
from vexen_rbac.domain.ports.permission_group_repository_port import (
	IPermissionGroupRepositoryPort,
)


@dataclass
class CountGroupPermissions:
	repository: IPermissionGroupRepositoryPort

	async def __call__(self, group_id: int) -> BaseResponse[int]:
		try:
			count = await self.repository.count_permissions(group_id)
			return BaseResponse(success=True, data=count)

		except Exception as e:
			return BaseResponse(success=False, error=str(e))
