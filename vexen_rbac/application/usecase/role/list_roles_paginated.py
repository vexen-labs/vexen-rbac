from dataclasses import dataclass
from math import ceil

from vexen_rbac.application.dto import (
	PaginatedResponse,
	PaginationRequest,
	PaginationResponse,
	RoleResponse,
)
from vexen_rbac.domain.ports.role_repository_port import IRoleRepositoryPort


@dataclass
class ListRolesPaginated:
	repository: IRoleRepositoryPort

	async def __call__(self, request: PaginationRequest) -> PaginatedResponse[RoleResponse]:
		try:
			roles, total = await self.repository.list_paginated(request.page, request.page_size)

			total_pages = ceil(total / request.page_size) if total > 0 else 1

			role_responses = [
				RoleResponse(
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
				for role in roles
			]

			pagination = PaginationResponse(
				page=request.page,
				page_size=request.page_size,
				total_pages=total_pages,
				total_items=total,
				has_next=request.page < total_pages,
				has_prev=request.page > 1,
			)

			return PaginatedResponse(success=True, data=role_responses, pagination=pagination)

		except Exception as e:
			return PaginatedResponse(
				success=False,
				data=[],
				pagination=PaginationResponse(
					page=1,
					page_size=20,
					total_pages=0,
					total_items=0,
					has_next=False,
					has_prev=False,
				),
				error=str(e),
			)
