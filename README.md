# RBAC - Role-Based Access Control Library

A flexible and extensible Role-Based Access Control (RBAC) library built with hexagonal architecture principles, designed to be as simple to use as FastAPI.

## Features

- **Clean Architecture**: Built with hexagonal architecture (ports and adapters)
- **Simple API**: FastAPI-like interface for ease of use
- **Async Support**: Fully asynchronous using SQLAlchemy 2.0+ with asyncpg
- **Type Safe**: Complete type hints for better IDE support
- **Flexible**: Easy to extend and customize
- **Production Ready**: Session management, connection pooling, and error handling

## Installation

```bash
pip install rbac
```

Or with uv:

```bash
uv pip install rbac
```

## Quick Start

```python
from rbac import RBAC
from rbac.application.dto import CreateRoleRequest

# Initialize RBAC
rbac = RBAC(database_url="postgresql+asyncpg://user:pass@localhost/db")
await rbac.init()

# Create a role
role = await rbac.roles.create_role(
    CreateRoleRequest(
        name="admin",
        display_name="Administrator",
        permissions=[1, 2, 3]
    )
)

# List roles with pagination
result = await rbac.service.list_roles_paginated(page=1, page_size=20)

# Get role with expanded permissions
role_detail = await rbac.service.get_role_expanded(role_id=1)

# Close when done
await rbac.close()
```

## Usage with FastAPI

```python
from fastapi import FastAPI
from rbac import RBAC

app = FastAPI()
rbac = RBAC(database_url="postgresql+asyncpg://...")

@app.on_event("startup")
async def startup():
    await rbac.init()

@app.on_event("shutdown")
async def shutdown():
    await rbac.close()

@app.get("/roles")
async def list_roles(page: int = 1, page_size: int = 20):
    result = await rbac.service.list_roles_paginated(page, page_size)
    return result
```

## Features

### Roles

- Create, read, update, delete roles
- List roles with pagination
- Add/remove permissions from roles
- Count roles and permissions

### Permissions

- Create, read, update, delete permissions
- List permissions
- Group permissions by category

### Permission Groups

- Create, read, update, delete permission groups
- Add/remove permissions from groups
- Organize permissions hierarchically

## Architecture

This library follows hexagonal architecture principles:

- **Domain Layer**: Pure business logic (entities, value objects)
- **Application Layer**: Use cases and DTOs
- **Infrastructure Layer**: Database adapters (SQLAlchemy)
- **Public API**: Clean facade hiding complexity

## Requirements

- Python 3.11+
- PostgreSQL (with asyncpg)
- SQLAlchemy 2.0+

## Documentation

- [Usage Guide](USAGE.md) - Complete usage documentation
- [API Examples](API_EXAMPLES.md) - API response formats
- [Integration Guide](INTEGRATION_GUIDE.md) - Framework integration examples
- [New Features](NEW_FEATURES.md) - Recently added features

## Development

```bash
# Clone repository
git clone https://github.com/yourusername/rbac.git
cd rbac

# Install with development dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Format code
ruff format .

# Lint code
ruff check .
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on GitHub.
