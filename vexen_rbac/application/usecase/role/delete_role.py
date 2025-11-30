from dataclasses import dataclass

from vexen_rbac.application.dto.base import BaseResponse
from vexen_rbac.domain.ports.role_repository_port import IRoleRepositoryPort


@dataclass
class DeleteRole:
	repository: IRoleRepositoryPort

	async def __call__(self, role_id: int) -> BaseResponse[bool]:
		try:
			role = await self.repository.get_by_id(role_id)

			if role is None:
				return BaseResponse.fail(f"Role with ID {role_id} not found")

			await self.repository.delete(role_id)

			return BaseResponse.ok(True)

		except Exception as e:
			return BaseResponse.fail(f"Error deleting role: {str(e)}")
