from dataclasses import dataclass

from rbac.application.dto.base import BaseResponse
from rbac.application.dto.role_dto import RoleResponse, UpdateRoleRequest
from rbac.domain.ports.role_repository_port import IRoleRepositoryPort


@dataclass
class UpdateRole:
	repository: IRoleRepositoryPort

	async def __call__(
		self, role_id: int, request: UpdateRoleRequest
	) -> BaseResponse[RoleResponse]:
		try:
			role = await self.repository.get_by_id(role_id)

			if role is None:
				return BaseResponse.fail(f"Role with ID {role_id} not found")

			if request.name is not None:
				role.name = request.name
			if request.display_name is not None:
				role.display_name = request.display_name
			if request.description is not None:
				role.description = request.description
			if request.permissions is not None:
				role.permissions = request.permissions
			if request.permission_groups is not None:
				role.permission_groups = request.permission_groups

			updated_role = await self.repository.save(role)

			response = RoleResponse(
				id=updated_role.id,
				name=updated_role.name,
				display_name=updated_role.display_name,
				description=updated_role.description,
				permissions=updated_role.permissions,
				permission_groups=updated_role.permission_groups,
				user_count=updated_role.user_count,
				created_at=updated_role.created_at,
				updated_at=updated_role.updated_at,
			)

			return BaseResponse.ok(response)

		except Exception as e:
			return BaseResponse.fail(f"Error updating role: {str(e)}")
