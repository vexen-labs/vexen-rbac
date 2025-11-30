from dataclasses import dataclass

from vexen_rbac.application.dto.base import BaseResponse
from vexen_rbac.application.dto.permission_dto import (
	PermissionResponse,
	UpdatePermissionRequest,
)
from vexen_rbac.domain.ports.permission_repository_port import IPermissionRepositoryPort


@dataclass
class UpdatePermission:
	repository: IPermissionRepositoryPort

	async def __call__(
		self, permission_id: int, request: UpdatePermissionRequest
	) -> BaseResponse[PermissionResponse]:
		try:
			permission = await self.repository.get_by_id(permission_id)

			if permission is None:
				return BaseResponse.fail(f"Permission with ID {permission_id} not found")

			if request.name is not None:
				permission.name = request.name
			if request.display_name is not None:
				permission.display_name = request.display_name
			if request.description is not None:
				permission.description = request.description
			if request.category is not None:
				permission.category = request.category

			permission.__post_init__()

			updated_permission = await self.repository.save(permission)

			response = PermissionResponse(
				id=updated_permission.id,
				name=updated_permission.name,
				display_name=updated_permission.display_name,
				description=updated_permission.description,
				category=updated_permission.category,
				created_at=updated_permission.created_at,
			)

			return BaseResponse.ok(response)

		except ValueError as e:
			return BaseResponse.fail(f"Validation error: {str(e)}")
		except Exception as e:
			return BaseResponse.fail(f"Error updating permission: {str(e)}")
