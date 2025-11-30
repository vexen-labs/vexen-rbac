"""
Mapper for Role entity and RoleModel.

Mappers are pure functions that only convert between domain entities
and ORM models. They should NOT contain any database logic.
"""

from rbac.domain.entity.role import Role
from rbac.infraestructure.output.persistence.sqlalchemy.models.role import RoleModel


class RoleMapper:
	"""Converts between Role entity and RoleModel."""

	@staticmethod
	def to_entity(model: RoleModel) -> Role:
		"""
		Convert RoleModel to Role entity.

		Args:
			model: SQLAlchemy model instance (should be loaded with relationships)

		Returns:
			Role: Domain entity
		"""
		permission_ids = [p.id for p in model.permissions]
		permission_group_ids = [pg.id for pg in model.permission_groups]

		return Role(
			id=model.id,
			name=model.name,
			display_name=model.display_name,
			description=model.description,
			permissions=permission_ids,
			permission_groups=permission_group_ids,
			user_count=0,  # This is calculated, not persisted
			created_at=model.created_at,
			updated_at=model.updated_at,
		)

	@staticmethod
	def to_model(entity: Role) -> RoleModel:
		"""
		Convert Role entity to RoleModel.

		Note: This creates the model but does NOT set M2M relationships.
		Use repository methods to handle relationships.

		Args:
			entity: Domain entity

		Returns:
			RoleModel: SQLAlchemy model instance (not persisted)
		"""
		return RoleModel(
			id=entity.id if hasattr(entity, "id") and entity.id else None,
			name=entity.name,
			display_name=entity.display_name,
			description=entity.description,
		)

	@staticmethod
	def update_model_from_entity(model: RoleModel, entity: Role) -> RoleModel:
		"""
		Update existing model instance with entity data.

		Only updates scalar fields, not relationships.
		Use repository methods to handle M2M relationships.

		Args:
			model: Existing model instance
			entity: Source entity with updated data

		Returns:
			RoleModel: Updated model instance (same object, modified in place)
		"""
		model.name = entity.name
		model.display_name = entity.display_name
		model.description = entity.description
		return model
