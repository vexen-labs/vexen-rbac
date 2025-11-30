from dataclasses import dataclass

from vexen_rbac.application.dto.base import BaseResponse
from vexen_rbac.domain.ports.role_repository_port import IRoleRepositoryPort


@dataclass
class CountRoles:
	repository: IRoleRepositoryPort

	async def __call__(self) -> BaseResponse[int]:
		try:
			count = await self.repository.count()
			return BaseResponse(success=True, data=count)

		except Exception as e:
			return BaseResponse(success=False, error=str(e))
