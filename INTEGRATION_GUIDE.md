# RBAC Integration Guide

Guía de integración de RBAC en diferentes tipos de aplicaciones.

## Uso General

RBAC está diseñado para usarse como una instancia global en tu aplicación, similar a FastAPI:

```python
from rbac import RBAC

# Instanciar una vez
rbac = RBAC(database_url="postgresql+asyncpg://...")

# Inicializar al arrancar la aplicación
await rbac.init()

# Usar durante toda la vida de la aplicación
result = await rbac.service.list_roles_paginated()

# Cerrar al apagar la aplicación
await rbac.close()
```

## Integración con FastAPI

```python
from fastapi import FastAPI, Depends
from rbac import RBAC
from vexen_rbac.application.dto import CreateRoleRequest, PaginationRequest

app = FastAPI()

# Instancia global de RBAC
rbac = RBAC(
    database_url="postgresql+asyncpg://hexa:hexa@localhost:5432/rbac",
    pool_size=10,
    max_overflow=20
)

@app.on_event("startup")
async def startup():
    await rbac.init()
    print("✅ RBAC initialized")

@app.on_event("shutdown")
async def shutdown():
    await rbac.close()
    print("✅ RBAC closed")

# Endpoints
@app.get("/api/roles")
async def list_roles(page: int = 1, page_size: int = 20):
    result = await rbac.service.list_roles_paginated(page, page_size)

    if not result.success:
        return {"error": result.error}

    return {
        "success": True,
        "data": [
            {
                "id": role.id,
                "name": role.name,
                "displayName": role.display_name,
                "permissions": role.permissions,
                "userCount": role.user_count,
            }
            for role in result.data
        ],
        "pagination": {
            "page": result.pagination.page,
            "pageSize": result.pagination.page_size,
            "totalPages": result.pagination.total_pages,
            "totalItems": result.pagination.total_items,
            "hasNext": result.pagination.has_next,
            "hasPrev": result.pagination.has_prev,
        }
    }

@app.get("/api/roles/{role_id}")
async def get_role(role_id: int):
    result = await rbac.service.get_role_expanded(role_id)

    if not result.success:
        return {"error": result.error}

    return {
        "success": True,
        "data": {
            "id": result.data.id,
            "name": result.data.name,
            "displayName": result.data.display_name,
            "permissions": [
                {
                    "id": p.id,
                    "name": p.name,
                    "displayName": p.display_name,
                    "category": p.category,
                }
                for p in result.data.permissions
            ],
            "userCount": result.data.user_count,
        }
    }

@app.post("/api/roles")
async def create_role(request: CreateRoleRequest):
    result = await rbac.roles.create_role(request)

    if not result.success:
        return {"error": result.error}

    return {"success": True, "data": result.data}

@app.get("/api/permissions/groups")
async def get_permissions_grouped():
    result = await rbac.service.get_permissions_grouped()

    if not result.success:
        return {"error": result.error}

    return {
        "success": True,
        "data": [
            {
                "category": group.category,
                "displayName": group.display_name,
                "permissions": [
                    {
                        "id": p.id,
                        "name": p.name,
                        "displayName": p.display_name,
                    }
                    for p in group.permissions
                ]
            }
            for group in result.data
        ]
    }
```

## Integración con Dependency Injection

```python
from typing import Annotated
from fastapi import Depends

# Crear dependency
def get_rbac_service():
    return rbac.service

RBACService = Annotated[object, Depends(get_rbac_service)]

@app.get("/api/roles")
async def list_roles(
    service: RBACService,
    page: int = 1,
    page_size: int = 20
):
    result = await service.list_roles_paginated(page, page_size)
    return result
```

## Integración con Django (Async Views)

```python
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from rbac import RBAC

# Instancia global
rbac = RBAC(database_url="postgresql+asyncpg://...")

# Inicializar en apps.py
class MyAppConfig(AppConfig):
    def ready(self):
        import asyncio
        asyncio.run(rbac.init())

# Usar en views
async def list_roles(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('pageSize', 20))

    result = await rbac.service.list_roles_paginated(page, page_size)

    return JsonResponse({
        "success": result.success,
        "data": [...],  # Serializar result.data
        "pagination": {...}  # Serializar result.pagination
    })
```

## Integración con Litestar (antes Starlite)

```python
from litestar import Litestar, get
from rbac import RBAC

rbac = RBAC(database_url="postgresql+asyncpg://...")

@get("/roles")
async def list_roles(page: int = 1, page_size: int = 20) -> dict:
    result = await rbac.service.list_roles_paginated(page, page_size)
    return {"success": result.success, "data": result.data}

async def on_startup():
    await rbac.init()

async def on_shutdown():
    await rbac.close()

app = Litestar(
    route_handlers=[list_roles],
    on_startup=[on_startup],
    on_shutdown=[on_shutdown]
)
```

## Integración con Scripts/CLI

Para scripts o CLI, usar context manager es más conveniente:

```python
import asyncio
from rbac import RBAC

async def create_admin_role():
    async with RBAC(database_url="postgresql+asyncpg://...") as rbac:
        result = await rbac.roles.create_role(...)
        print(f"Created: {result.data.display_name}")

if __name__ == "__main__":
    asyncio.run(create_admin_role())
```

## Manejo de Configuración

### Usando Variables de Entorno

```python
import os
from rbac import RBAC

rbac = RBAC(
    database_url=os.getenv("DATABASE_URL"),
    echo=os.getenv("DB_ECHO", "false").lower() == "true",
    pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
)
```

### Usando RBACConfig

```python
from rbac import RBAC, RBACConfig

config = RBACConfig(
    database_url="postgresql+asyncpg://...",
    adapter="sqlalchemy",
    echo=False,
    pool_size=10,
    max_overflow=20
)

rbac = RBAC(config=config)
```

## Mejores Prácticas

### 1. Instancia Global
```python
# ✅ BIEN - Una instancia para toda la aplicación
rbac = RBAC(database_url="...")
await rbac.init()

# ❌ MAL - Crear nueva instancia en cada request
async def handle_request():
    rbac = RBAC(database_url="...")  # No hacer esto
    await rbac.init()
```

### 2. Inicialización
```python
# ✅ BIEN - Inicializar en startup
@app.on_event("startup")
async def startup():
    await rbac.init()

# ❌ MAL - Inicializar en cada request
async def handle_request():
    await rbac.init()  # No hacer esto
```

### 3. Cierre de Conexiones
```python
# ✅ BIEN - Cerrar en shutdown
@app.on_event("shutdown")
async def shutdown():
    await rbac.close()

# ✅ TAMBIÉN BIEN - Usar context manager para scripts
async with RBAC(...) as rbac:
    # Cierra automáticamente
    pass
```

## Testing

Para tests, usar context manager o fixtures:

```python
import pytest
from rbac import RBAC

@pytest.fixture
async def rbac_instance():
    rbac = RBAC(database_url="postgresql+asyncpg://test_db")
    await rbac.init()
    yield rbac
    await rbac.close()

async def test_create_role(rbac_instance):
    result = await rbac_instance.roles.create_role(...)
    assert result.success
```
