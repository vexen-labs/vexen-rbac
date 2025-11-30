from dataclasses import dataclass

from rbac.application.dto.base import BaseResponse
from rbac.application.dto.role_dto import RoleResponse
from rbac.domain.ports.role_repository_port import IRoleRepositoryPort


@dataclass
class ListRoles:
	repository: IRoleRepositoryPort

	async def __call__(self) -> BaseResponse[list[RoleResponse]]:
		try:
			return BaseResponse.fail("List all roles not yet implemented in repository")

		except Exception as e:
			return BaseResponse.fail(f"Error listing roles: {str(e)}")
