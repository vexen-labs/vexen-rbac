"""
RBAC - Role-Based Access Control Library

This module provides the main entry point for the RBAC library,
following hexagonal architecture principles.
"""

from dataclasses import dataclass
from typing import Literal

from rbac.application.service.rbac_service import RBACService
from rbac.domain.ports import (
	IPermissionGroupRepositoryPort,
	IPermissionRepositoryPort,
	IRoleRepositoryPort,
)


@dataclass
class RBACConfig:
	"""Configuration for RBAC initialization."""

	database_url: str
	adapter: Literal["sqlalchemy"] = "sqlalchemy"
	echo: bool = False
	pool_size: int = 5
	max_overflow: int = 10


class RBAC:
	"""
	Main RBAC class - Entry point for the library.

	This class acts as a facade and factory, following the hexagonal architecture.
	It initializes the appropriate adapters and provides access to RBAC services.

	Example:
		>>> rbac = RBAC(
		...     database_url="postgresql+asyncpg://user:pass@localhost/db",
		...     adapter="sqlalchemy"
		... )
		>>> await rbac.init()
		>>> role = await rbac.roles.create_role(role_data)
	"""

	def __init__(
		self,
		database_url: str | None = None,
		adapter: Literal["sqlalchemy"] = "sqlalchemy",
		echo: bool = False,
		pool_size: int = 5,
		max_overflow: int = 10,
		config: RBACConfig | None = None,
	):
		"""
		Initialize RBAC with database configuration.

		Args:
			database_url: Database connection URL
			adapter: Database adapter to use (currently only "sqlalchemy")
			echo: Enable SQL echo for debugging
			pool_size: Database connection pool size
			max_overflow: Maximum overflow for connection pool
			config: Alternative way to pass configuration as an object

		Raises:
			ValueError: If neither database_url nor config is provided
			ValueError: If adapter is not supported
		"""
		if config:
			self._config = config
		elif database_url:
			self._config = RBACConfig(
				database_url=database_url,
				adapter=adapter,
				echo=echo,
				pool_size=pool_size,
				max_overflow=max_overflow,
			)
		else:
			raise ValueError("Either 'database_url' or 'config' must be provided")

		if self._config.adapter != "sqlalchemy":
			raise ValueError(f"Unsupported adapter: {self._config.adapter}")

		self._initialized = False
		self._service: RBACService | None = None
		self._repositories: dict[
			str, IPermissionGroupRepositoryPort | IPermissionRepositoryPort | IRoleRepositoryPort
		] = {}

	async def init(self) -> None:
		"""
		Initialize the RBAC system.

		This method:
		1. Creates the database engine and session factory
		2. Initializes the database schema (creates tables if they don't exist)
		3. Instantiates repositories
		4. Creates the RBAC service

		Raises:
			RuntimeError: If already initialized
		"""
		if self._initialized:
			raise RuntimeError("RBAC is already initialized")

		if self._config.adapter == "sqlalchemy":
			await self._init_sqlalchemy()

		self._initialized = True

	async def _init_sqlalchemy(self) -> None:
		"""Initialize SQLAlchemy adapter."""
		import os

		from rbac.infraestructure.output.persistence.sqlalchemy.database import (
			DatabaseConfig,
			init_db,
		)

		# Set environment variables for DatabaseConfig
		os.environ["DATABASE_URL"] = self._config.database_url
		os.environ["DB_ECHO"] = str(self._config.echo)
		os.environ["DB_POOL_SIZE"] = str(self._config.pool_size)
		os.environ["DB_MAX_OVERFLOW"] = str(self._config.max_overflow)

		# Initialize database (creates tables)
		await init_db()

		# Store session factory for creating sessions per operation
		self._session_factory = DatabaseConfig.get_session_factory()

		# Create repository wrappers that manage sessions
		from rbac.infraestructure.output.persistence.sqlalchemy.adapters import (
			PermissionGroupRepositoryAdapter,
			PermissionRepositoryAdapter,
			RoleRepositoryAdapter,
		)

		self._repositories["role"] = RoleRepositoryAdapter(self._session_factory)
		self._repositories["permission"] = PermissionRepositoryAdapter(self._session_factory)
		self._repositories["permission_group"] = PermissionGroupRepositoryAdapter(
			self._session_factory
		)

		# Initialize service
		self._service = RBACService(
			_role_repository=self._repositories["role"],
			_permission_repository=self._repositories["permission"],
			_permission_group_repository=self._repositories["permission_group"],
		)

	async def close(self) -> None:
		"""
		Close all database connections and cleanup resources.

		This should be called when shutting down the application.
		"""
		if not self._initialized:
			return

		if self._config.adapter == "sqlalchemy":
			from rbac.infraestructure.output.persistence.sqlalchemy.database import close_db

			await close_db()

		self._initialized = False
		self._service = None
		self._repositories = {}

	@property
	def roles(self):
		"""
		Access to role use cases.

		Returns:
			Role use case factory with methods like create_role, get_role, etc.

		Raises:
			RuntimeError: If RBAC is not initialized
		"""
		self._ensure_initialized()
		return self._service.roles

	@property
	def permissions(self):
		"""
		Access to permission use cases.

		Returns:
			Permission use case factory with methods like create_permission, etc.

		Raises:
			RuntimeError: If RBAC is not initialized
		"""
		self._ensure_initialized()
		return self._service.permissions

	@property
	def permission_groups(self):
		"""
		Access to permission group use cases.

		Returns:
			Permission group use case factory with methods like create_permission_group, etc.

		Raises:
			RuntimeError: If RBAC is not initialized
		"""
		self._ensure_initialized()
		return self._service.permission_groups

	@property
	def service(self) -> RBACService:
		"""
		Access to the underlying RBAC service.

		This provides direct access to all service methods if needed.

		Returns:
			RBACService: The main service instance

		Raises:
			RuntimeError: If RBAC is not initialized
		"""
		self._ensure_initialized()
		return self._service

	def _ensure_initialized(self) -> None:
		"""
		Ensure RBAC is initialized.

		Raises:
			RuntimeError: If not initialized
		"""
		if not self._initialized or self._service is None:
			raise RuntimeError("RBAC is not initialized. Call 'await rbac.init()' first.")

	async def health_check(self) -> bool:
		"""
		Perform a health check of the RBAC system.

		Returns:
			True if the system is healthy, False otherwise

		Raises:
			RuntimeError: If RBAC is not initialized
		"""
		self._ensure_initialized()
		return await self._service.health_check()

	async def __aenter__(self):
		"""Async context manager entry."""
		await self.init()
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb):  # noqa: ANN001
		"""Async context manager exit."""
		await self.close()
		return False
