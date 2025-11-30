from dataclasses import dataclass

from rbac.application.dto.base import BaseResponse
from rbac.application.dto.role_dto import RoleResponse
from rbac.domain.ports.role_repository_port import IRoleRepositoryPort


@dataclass
class RemovePermissionsFromRole:
	repository: IRoleRepositoryPort

	async def __call__(self, role_id: int, permission_ids: list[int]) -> BaseResponse[RoleResponse]:
		try:
			role = await self.repository.remove_permissions(role_id, permission_ids)

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

			return BaseResponse(success=True, data=response)

		except Exception as e:
			return BaseResponse(success=False, error=str(e))
