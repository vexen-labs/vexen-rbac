"""
Database configuration for SQLAlchemy 2.0 with async sessions.
"""

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.ext.asyncio import (
	AsyncEngine,
	AsyncSession,
	async_sessionmaker,
	create_async_engine,
)


class DatabaseConfig:
	"""Configuration for async SQLAlchemy database connection."""

	_engine: AsyncEngine | None = None
	_session_factory: async_sessionmaker[AsyncSession] | None = None

	@classmethod
	def get_database_url(cls) -> str:
		"""
		Get database URL from environment variables.

		Returns:
			str: PostgreSQL async database URL
		"""
		return os.getenv(
			"DATABASE_URL",
			"postgresql+asyncpg://rbac_user:rbac_password@localhost:5432/rbac_db",
		)

	@classmethod
	def get_engine_config(cls) -> dict[str, Any]:
		"""
		Get engine configuration.

		Returns:
			dict: Configuration for create_async_engine
		"""
		return {
			"echo": os.getenv("DB_ECHO", "False").lower() == "true",
			"pool_size": int(os.getenv("DB_POOL_SIZE", "5")),
			"max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "10")),
			"pool_pre_ping": True,
			"pool_recycle": 3600,
		}

	@classmethod
	def get_engine(cls) -> AsyncEngine:
		"""
		Get or create the async engine singleton.

		Returns:
			AsyncEngine: SQLAlchemy async engine
		"""
		if cls._engine is None:
			database_url = cls.get_database_url()
			engine_config = cls.get_engine_config()
			cls._engine = create_async_engine(database_url, **engine_config)
		return cls._engine

	@classmethod
	def get_session_factory(cls) -> async_sessionmaker[AsyncSession]:
		"""
		Get or create the async session factory.

		Returns:
			async_sessionmaker: Factory for creating async sessions
		"""
		if cls._session_factory is None:
			engine = cls.get_engine()
			cls._session_factory = async_sessionmaker(
				engine,
				class_=AsyncSession,
				expire_on_commit=False,
				autocommit=False,
				autoflush=False,
			)
		return cls._session_factory

	@classmethod
	async def close(cls) -> None:
		"""Close the database engine and cleanup resources."""
		if cls._engine is not None:
			await cls._engine.dispose()
			cls._engine = None
			cls._session_factory = None


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
	"""
	Context manager for async database sessions.

	Yields:
		AsyncSession: SQLAlchemy async session

	Example:
		async with get_async_session() as session:
			result = await session.execute(select(RoleModel))
	"""
	session_factory = DatabaseConfig.get_session_factory()
	session = session_factory()
	try:
		yield session
		await session.commit()
	except Exception:
		await session.rollback()
		raise
	finally:
		await session.close()


async def init_db() -> None:
	"""
	Initialize database connection and create tables.

	This should be called at application startup.
	"""
	from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models.base import Base

	engine = DatabaseConfig.get_engine()

	async with engine.begin() as conn:
		# Create all tables
		await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
	"""
	Close database connections.

	This should be called at application shutdown.
	"""
	await DatabaseConfig.close()
