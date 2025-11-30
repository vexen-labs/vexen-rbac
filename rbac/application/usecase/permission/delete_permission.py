from dataclasses import dataclass

from rbac.application.dto.base import BaseResponse
from rbac.domain.ports.permission_repository_port import IPermissionRepositoryPort


@dataclass
class DeletePermission:
	repository: IPermissionRepositoryPort

	async def __call__(self, permission_id: int) -> BaseResponse[bool]:
		try:
			permission = await self.repository.get_by_id(permission_id)

			if permission is None:
				return BaseResponse.fail(f"Permission with ID {permission_id} not found")

			await self.repository.delete(permission_id)

			return BaseResponse.ok(True)

		except Exception as e:
			return BaseResponse.fail(f"Error deleting permission: {str(e)}")
