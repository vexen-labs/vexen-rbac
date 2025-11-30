from dataclasses import dataclass

from vexen_rbac.application.dto.base import BaseResponse
from vexen_rbac.application.dto.permission_dto import PermissionResponse
from vexen_rbac.domain.ports.permission_repository_port import IPermissionRepositoryPort


@dataclass
class ListPermissions:
	repository: IPermissionRepositoryPort

	async def __call__(self) -> BaseResponse[list[PermissionResponse]]:
		try:
			permissions = await self.repository.list()

			response_data = [
				PermissionResponse(
					id=p.id,
					name=p.name,
					display_name=p.display_name,
					description=p.description,
					category=p.category,
					created_at=p.created_at,
				)
				for p in permissions
			]

			return BaseResponse.ok(response_data)

		except Exception as e:
			return BaseResponse.fail(f"Error listing permissions: {str(e)}")
