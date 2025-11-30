from dataclasses import dataclass

from rbac.application.dto.base import BaseResponse
from rbac.domain.ports.role_repository_port import IRoleRepositoryPort


@dataclass
class CountRolePermissions:
	repository: IRoleRepositoryPort

	async def __call__(self, role_id: int) -> BaseResponse[int]:
		try:
			count = await self.repository.count_permissions(role_id)
			return BaseResponse(success=True, data=count)

		except Exception as e:
			return BaseResponse(success=False, error=str(e))
