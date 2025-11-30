from dataclasses import dataclass
from datetime import datetime

from rbac.application.dto.base import BaseResponse
from rbac.application.dto.role_dto import CreateRoleRequest, RoleResponse
from rbac.domain.entity.role import Role
from rbac.domain.ports.role_repository_port import IRoleRepositoryPort


@dataclass
class CreateRole:
	repository: IRoleRepositoryPort

	async def __call__(self, request: CreateRoleRequest) -> BaseResponse[RoleResponse]:
		try:
			role = Role(
				id=0,
				name=request.name,
				display_name=request.display_name,
				description=request.description,
				permissions=request.permissions or [],
				permission_groups=request.permission_groups or [],
				user_count=0,
				created_at=datetime.now(),
			)

			saved_role = await self.repository.save(role)

			response = RoleResponse(
				id=saved_role.id,
				name=saved_role.name,
				display_name=saved_role.display_name,
				description=saved_role.description,
				permissions=saved_role.permissions,
				permission_groups=saved_role.permission_groups,
				user_count=saved_role.user_count,
				created_at=saved_role.created_at,
				updated_at=saved_role.updated_at,
			)

			return BaseResponse.ok(response)

		except Exception as e:
			return BaseResponse.fail(f"Error creating role: {str(e)}")
