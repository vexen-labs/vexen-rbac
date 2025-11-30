from dataclasses import dataclass

from rbac.application.dto.base import BaseResponse
from rbac.application.dto.permission_dto import PermissionResponse
from rbac.domain.ports.permission_repository_port import IPermissionRepositoryPort


@dataclass
class ListPermissions:
	repository: IPermissionRepositoryPort

	async def __call__(self) -> BaseResponse[list[PermissionResponse]]:
		try:
			return BaseResponse.fail("List all permissions not yet implemented in repository")

		except Exception as e:
			return BaseResponse.fail(f"Error listing permissions: {str(e)}")
