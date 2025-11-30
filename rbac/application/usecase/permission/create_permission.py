from dataclasses import dataclass

from rbac.application.dto.base import BaseResponse
from rbac.application.dto.permission_dto import (
	CreatePermissionRequest,
	PermissionResponse,
)
from rbac.domain.entity.permission import Permission
from rbac.domain.ports.permission_repository_port import IPermissionRepositoryPort


@dataclass
class CreatePermission:
	repository: IPermissionRepositoryPort

	async def __call__(self, request: CreatePermissionRequest) -> BaseResponse[PermissionResponse]:
		try:
			permission = Permission(
				id=None,
				name=request.name,
				display_name=request.display_name,
				description=request.description,
				category=request.category,
			)

			saved_permission = await self.repository.save(permission)

			response = PermissionResponse(
				id=saved_permission.id,
				name=saved_permission.name,
				display_name=saved_permission.display_name,
				description=saved_permission.description,
				category=saved_permission.category,
				created_at=saved_permission.created_at,
			)

			return BaseResponse.ok(response)

		except Exception as e:
			return BaseResponse.fail(f"Validation error: {str(e)}")
