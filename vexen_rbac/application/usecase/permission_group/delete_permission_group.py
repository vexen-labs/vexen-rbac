from dataclasses import dataclass

from vexen_rbac.application.dto.base import BaseResponse
from vexen_rbac.domain.ports.permission_group_repository_port import (
	IPermissionGroupRepositoryPort,
)


@dataclass
class DeletePermissionGroup:
	repository: IPermissionGroupRepositoryPort

	async def __call__(self, permission_group_id: int) -> BaseResponse[bool]:
		try:
			permission_group = await self.repository.get_by_id(permission_group_id)

			if permission_group is None:
				return BaseResponse.fail(
					f"Permission group with ID {permission_group_id} not found"
				)

			await self.repository.delete(permission_group_id)

			return BaseResponse.ok(True)

		except Exception as e:
			return BaseResponse.fail(f"Error deleting permission group: {str(e)}")
