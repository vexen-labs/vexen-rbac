# RBAC - Public API Usage

A Role-Based Access Control library built with hexagonal architecture, designed to be as simple to use as FastAPI.

## Installation

```bash
# Install from source
pip install -e .

# Or with uv
uv pip install -e .
```

## Quick Start

### Basic Usage

```python
from rbac import RBAC
from rbac.application.dto import CreateRoleRequest

# Initialize RBAC
rbac = RBAC(
    database_url="postgresql+asyncpg://user:pass@localhost/db"
)

# Initialize database
await rbac.init()

# Use the services
role_request = CreateRoleRequest(
    name="admin",
    display_name="Administrator"
)
result = await rbac.roles.create_role(role_request)

# Always close when done
await rbac.close()
```

### Recommended: Context Manager

```python
from rbac import RBAC

# Automatically handles init/close
async with RBAC(database_url="postgresql+asyncpg://...") as rbac:
    # Create roles
    role_result = await rbac.roles.create_role(role_data)

    # Create permissions
    perm_result = await rbac.permissions.create_permission(perm_data)

    # Create permission groups
    group_result = await rbac.permission_groups.create_permission_group(group_data)
```

## Configuration

### Simple Configuration

```python
rbac = RBAC(
    database_url="postgresql+asyncpg://user:pass@localhost/db",
    echo=True,          # Enable SQL logging
    pool_size=10,       # Connection pool size
    max_overflow=20     # Max overflow connections
)
```

### Using RBACConfig

```python
from rbac import RBAC, RBACConfig

config = RBACConfig(
    database_url="postgresql+asyncpg://user:pass@localhost/db",
    adapter="sqlalchemy",  # Currently only SQLAlchemy is supported
    echo=False,
    pool_size=5,
    max_overflow=10
)

rbac = RBAC(config=config)
```

## Available Services

### Roles

```python
# Create role
from rbac.application.dto import CreateRoleRequest

role_request = CreateRoleRequest(
    name="admin",
    display_name="Administrator",
    description="Full system access",
    permissions=[1, 2, 3],           # Permission IDs
    permission_groups=[1]             # Permission Group IDs
)
result = await rbac.roles.create_role(role_request)

# Get role
result = await rbac.roles.get_role(role_id=1)

# List all roles
result = await rbac.roles.list_roles()

# Update role
from rbac.application.dto import UpdateRoleRequest

update_request = UpdateRoleRequest(
    display_name="Super Administrator"
)
result = await rbac.roles.update_role(role_id=1, role_data=update_request)

# Delete role
result = await rbac.roles.delete_role(role_id=1)
```

### Permissions

```python
# Create permission
from rbac.application.dto import CreatePermissionRequest

perm_request = CreatePermissionRequest(
    name="users.read",
    display_name="Read Users",
    category="users",
    description="Can view user information"
)
result = await rbac.permissions.create_permission(perm_request)

# Get permission
result = await rbac.permissions.get_permission(permission_id=1)

# List all permissions
result = await rbac.permissions.list_permissions()

# Update permission
from rbac.application.dto import UpdatePermissionRequest

update_request = UpdatePermissionRequest(
    display_name="View All Users"
)
result = await rbac.permissions.update_permission(
    permission_id=1,
    permission_data=update_request
)

# Delete permission
result = await rbac.permissions.delete_permission(permission_id=1)
```

### Permission Groups

```python
# Create permission group
from rbac.application.dto import CreatePermissionGroupRequest

group_request = CreatePermissionGroupRequest(
    name="user_management",
    display_name="User Management",
    description="All user-related permissions",
    permissions=[1, 2, 3]  # Permission IDs
)
result = await rbac.permission_groups.create_permission_group(group_request)

# Get permission group
result = await rbac.permission_groups.get_permission_group(group_id=1)

# List all permission groups
result = await rbac.permission_groups.list_permission_groups()

# Update permission group
from rbac.application.dto import UpdatePermissionGroupRequest

update_request = UpdatePermissionGroupRequest(
    display_name="Complete User Management"
)
result = await rbac.permission_groups.update_permission_group(
    group_id=1,
    group_data=update_request
)

# Delete permission group
result = await rbac.permission_groups.delete_permission_group(group_id=1)
```

## Response Format

All operations return a result object with the following structure:

```python
class Result:
    success: bool        # True if operation succeeded
    data: Any | None    # The result data (entity or list of entities)
    error: str | None   # Error message if failed
```

Usage example:

```python
result = await rbac.roles.get_role(1)

if result.success:
    print(f"Role: {result.data.display_name}")
    print(f"Permissions: {result.data.permissions}")
else:
    print(f"Error: {result.error}")
```

## Health Check

```python
is_healthy = await rbac.health_check()

if is_healthy:
    print("✅ RBAC system is healthy")
else:
    print("❌ RBAC system has issues")
```

## Direct Service Access

If you need direct access to the underlying service:

```python
# Access the RBACService directly
service = rbac.service

# All service methods are available
result = await service.create_role(role_data)
result = await service.get_role_by_id(role_id)
```

## Environment Variables

You can also configure via environment variables (read by DatabaseConfig):

```bash
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db
DB_ECHO=True
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
```

## Complete Example

```python
import asyncio
from rbac import RBAC
from rbac.application.dto import (
    CreatePermissionRequest,
    CreateRoleRequest,
)


async def main():
    async with RBAC(
        database_url="postgresql+asyncpg://rbac_user:rbac_password@localhost/rbac_db"
    ) as rbac:
        # Create permissions
        read_perm = await rbac.permissions.create_permission(
            CreatePermissionRequest(
                name="users.read",
                display_name="Read Users",
                category="users"
            )
        )

        write_perm = await rbac.permissions.create_permission(
            CreatePermissionRequest(
                name="users.write",
                display_name="Write Users",
                category="users"
            )
        )

        # Create role with permissions
        if read_perm.success and write_perm.success:
            role = await rbac.roles.create_role(
                CreateRoleRequest(
                    name="user_manager",
                    display_name="User Manager",
                    permissions=[read_perm.data.id, write_perm.data.id]
                )
            )

            if role.success:
                print(f"✅ Created role: {role.data.display_name}")
                print(f"   With {len(role.data.permissions)} permissions")


if __name__ == "__main__":
    asyncio.run(main())
```

## Architecture

This library follows hexagonal architecture (ports and adapters):

- **Domain Layer**: Pure business logic (entities, value objects)
- **Application Layer**: Use cases and DTOs
- **Infrastructure Layer**: Database adapters (SQLAlchemy)
- **Public API**: The `RBAC` class that orchestrates everything

The `RBAC` class acts as a facade, hiding the complexity and providing a clean, simple API similar to FastAPI.
