"""
Mapper for Permission entity and PermissionModel.

Mappers are pure functions that only convert between domain entities
and ORM models. They should NOT contain any database logic.
"""

from vexen_rbac.domain.entity.permission import Permission
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.permission import (
	PermissionModel,
)


class PermissionMapper:
	"""Converts between Permission entity and PermissionModel."""

	@staticmethod
	def to_entity(model: PermissionModel) -> Permission:
		"""
		Convert PermissionModel to Permission entity.

		Args:
			model: SQLAlchemy model instance

		Returns:
			Permission: Domain entity
		"""
		return Permission(
			id=model.id,
			name=model.name,
			display_name=model.display_name,
			description=model.description,
			category=model.category,
			created_at=model.created_at,
		)

	@staticmethod
	def to_model(entity: Permission) -> PermissionModel:
		"""
		Convert Permission entity to PermissionModel.

		Args:
			entity: Domain entity

		Returns:
			PermissionModel: SQLAlchemy model instance (not persisted)
		"""
		return PermissionModel(
			id=entity.id if hasattr(entity, "id") and entity.id else None,
			name=entity.name,
			display_name=entity.display_name,
			description=entity.description,
			category=entity.category,
		)

	@staticmethod
	def update_model_from_entity(model: PermissionModel, entity: Permission) -> PermissionModel:
		"""
		Update existing model instance with entity data.

		Only updates scalar fields, not relationships.

		Args:
			model: Existing model instance
			entity: Source entity with updated data

		Returns:
			PermissionModel: Updated model instance (same object, modified in place)
		"""
		model.name = entity.name
		model.display_name = entity.display_name
		model.description = entity.description
		model.category = entity.category
		return model
