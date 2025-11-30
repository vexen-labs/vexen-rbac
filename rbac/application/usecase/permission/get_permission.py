from dataclasses import dataclass

from rbac.application.dto.base import BaseResponse
from rbac.application.dto.permission_dto import PermissionResponse
from rbac.domain.ports.permission_repository_port import IPermissionRepositoryPort


@dataclass
class GetPermission:
	repository: IPermissionRepositoryPort

	async def __call__(self, permission_id: int) -> BaseResponse[PermissionResponse]:
		try:
			permission = await self.repository.get_by_id(permission_id)

			if permission is None:
				return BaseResponse.fail(f"Permission with ID {permission_id} not found")

			response = PermissionResponse(
				id=permission.id,
				name=permission.name,
				display_name=permission.display_name,
				description=permission.description,
				category=permission.category,
				created_at=permission.created_at,
			)

			return BaseResponse.ok(response)

		except Exception as e:
			return BaseResponse.fail(f"Error getting permission: {str(e)}")
