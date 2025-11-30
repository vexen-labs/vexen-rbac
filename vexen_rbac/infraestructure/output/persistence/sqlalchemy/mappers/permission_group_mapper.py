"""
Mapper for PermissionGroup entity and PermissionGroupModel.

Mappers are pure functions that only convert between domain entities
and ORM models. They should NOT contain any database logic.
"""

from vexen_rbac.domain.entity.permission_group import PermissionGroup
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.permission_group import (
	PermissionGroupModel,
)


class PermissionGroupMapper:
	"""Converts between PermissionGroup entity and PermissionGroupModel."""

	@staticmethod
	def to_entity(model: PermissionGroupModel) -> PermissionGroup:
		"""
		Convert PermissionGroupModel to PermissionGroup entity.

		Args:
			model: SQLAlchemy model instance (should be loaded with permissions)

		Returns:
			PermissionGroup: Domain entity
		"""
		permission_ids = [p.id for p in model.permissions]

		return PermissionGroup(
			id=model.id,
			name=model.name,
			display_name=model.display_name,
			description=model.description,
			icon=model.icon,
			order=model.order,
			permissions=permission_ids,
			created_at=model.created_at,
		)

	@staticmethod
	def to_model(entity: PermissionGroup) -> PermissionGroupModel:
		"""
		Convert PermissionGroup entity to PermissionGroupModel.

		Note: This creates the model but does NOT set M2M relationships.
		Use repository methods to handle relationships.

		Args:
			entity: Domain entity

		Returns:
			PermissionGroupModel: SQLAlchemy model instance (not persisted)
		"""
		return PermissionGroupModel(
			id=entity.id if hasattr(entity, "id") and entity.id else None,
			name=entity.name,
			display_name=entity.display_name,
			description=entity.description,
			icon=entity.icon,
			order=entity.order,
		)

	@staticmethod
	def update_model_from_entity(
		model: PermissionGroupModel, entity: PermissionGroup
	) -> PermissionGroupModel:
		"""
		Update existing model instance with entity data.

		Only updates scalar fields, not relationships.
		Use repository methods to handle M2M relationships.

		Args:
			model: Existing model instance
			entity: Source entity with updated data

		Returns:
			PermissionGroupModel: Updated model instance (same object, modified in place)
		"""
		model.name = entity.name
		model.display_name = entity.display_name
		model.description = entity.description
		model.icon = entity.icon
		model.order = entity.order
		return model
