from dataclasses import dataclass

from rbac.application.dto import (
	BaseResponse,
	PermissionGroupByCategoryResponse,
	PermissionSimpleResponse,
)
from rbac.domain.ports.permission_repository_port import IPermissionRepositoryPort


@dataclass
class GetPermissionsGrouped:
	repository: IPermissionRepositoryPort

	async def __call__(self) -> BaseResponse[list[PermissionGroupByCategoryResponse]]:
		try:
			grouped = await self.repository.group_by_category()

			category_map = {
				"users": "Usuarios",
				"roles": "Roles",
				"tickets": "Tickets",
				"dashboard": "Dashboard",
				"reports": "Reportes",
				"settings": "Configuración",
			}

			result = []
			for category, permissions in grouped.items():
				simple_permissions = [
					PermissionSimpleResponse(
						id=p.id, name=p.name, display_name=p.display_name, category=p.category
					)
					for p in permissions
				]

				group = PermissionGroupByCategoryResponse(
					category=category,
					display_name=category_map.get(category, category.capitalize()),
					permissions=simple_permissions,
				)
				result.append(group)

			return BaseResponse(success=True, data=result)

		except Exception as e:
			return BaseResponse(success=False, error=str(e))
