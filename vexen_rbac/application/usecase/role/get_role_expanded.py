from dataclasses import dataclass

from vexen_rbac.application.dto import (
	BaseResponse,
	PermissionSimpleResponse,
	RoleExpandedResponse,
)
from vexen_rbac.domain.ports.role_repository_port import IRoleRepositoryPort


@dataclass
class GetRoleExpanded:
	repository: IRoleRepositoryPort

	async def __call__(self, role_id: int) -> BaseResponse[RoleExpandedResponse]:
		try:
			result = await self.repository.get_by_id_with_permissions(role_id)

			if result is None:
				return BaseResponse(success=False, error=f"Role with id {role_id} not found")

			role, permissions_data = result

			permissions = [
				PermissionSimpleResponse(
					id=p["id"],
					name=p["name"],
					display_name=p["display_name"],
					category=p["category"],
				)
				for p in permissions_data
			]

			response = RoleExpandedResponse(
				id=role.id,
				name=role.name,
				display_name=role.display_name,
				description=role.description,
				permissions=permissions,
				user_count=role.user_count,
				created_at=role.created_at,
				updated_at=role.updated_at,
			)

			return BaseResponse(success=True, data=response)

		except Exception as e:
			return BaseResponse(success=False, error=str(e))
