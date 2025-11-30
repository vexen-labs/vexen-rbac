"""
RBAC - Role-Based Access Control Library

A flexible and extensible RBAC library built with hexagonal architecture.

Basic usage:
    >>> from rbac import RBAC
    >>>
    >>> rbac = RBAC(database_url="postgresql+asyncpg://user:pass@localhost/db")
    >>> await rbac.init()
    >>>
    >>> # Use the services
    >>> role = await rbac.roles.create_role(role_data)
    >>> permissions = await rbac.permissions.list_permissions()
    >>>
    >>> await rbac.close()

Context manager usage:
    >>> async with RBAC(database_url="postgresql+asyncpg://...") as rbac:
    ...     role = await rbac.roles.create_role(role_data)
"""

from .core import RBAC, RBACConfig

__version__ = "0.1.0"
__all__ = ["RBAC", "RBACConfig"]
