from dataclasses import dataclass

from rbac.application.dto.base import BaseResponse
from rbac.application.dto.role_dto import RoleResponse
from rbac.domain.ports.role_repository_port import IRoleRepositoryPort


@dataclass
class GetRole:
	repository: IRoleRepositoryPort

	async def __call__(self, role_id: int) -> BaseResponse[RoleResponse]:
		try:
			role = await self.repository.get_by_id(role_id)

			if role is None:
				return BaseResponse.fail(f"Role with ID {role_id} not found")

			response = RoleResponse(
				id=role.id,
				name=role.name,
				display_name=role.display_name,
				description=role.description,
				permissions=role.permissions,
				permission_groups=role.permission_groups,
				user_count=role.user_count,
				created_at=role.created_at,
				updated_at=role.updated_at,
			)

			return BaseResponse.ok(response)

		except Exception as e:
			return BaseResponse.fail(f"Error getting role: {str(e)}")
