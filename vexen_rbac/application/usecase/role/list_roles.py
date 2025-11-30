from dataclasses import dataclass

from vexen_rbac.application.dto.base import BaseResponse
from vexen_rbac.application.dto.role_dto import RoleResponse
from vexen_rbac.domain.ports.role_repository_port import IRoleRepositoryPort


@dataclass
class ListRoles:
	repository: IRoleRepositoryPort

	async def __call__(self) -> BaseResponse[list[RoleResponse]]:
		try:
			roles = await self.repository.list()

			response_data = [
				RoleResponse(
					id=r.id,
					name=r.name,
					display_name=r.display_name,
					description=r.description,
					permissions=r.permissions if r.permissions else [],
					permission_groups=r.permission_groups if r.permission_groups else [],
					user_count=0,  # Not available in simple list
					created_at=r.created_at,
					updated_at=None,  # Role entity doesn't have updated_at
				)
				for r in roles
			]

			return BaseResponse.ok(response_data)

		except Exception as e:
			return BaseResponse.fail(f"Error listing roles: {str(e)}")
