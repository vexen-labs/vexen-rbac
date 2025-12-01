# RBAC API Examples

La API pública de RBAC devuelve información en formato JSON compatible con APIs REST.

## Inicialización

La API pública soporta dos formas de uso:

### Forma 1: Instanciación directa (Recomendado para aplicaciones)

```python
from rbac import RBAC

rbac = RBAC(database_url="postgresql+asyncpg://...")
await rbac.init()

result = await rbac.service.list_roles_paginated(page=1, page_size=20)

await rbac.close()
```

### Forma 2: Context Manager (Recomendado para scripts)

```python
from rbac import RBAC

async with RBAC(database_url="postgresql+asyncpg://...") as rbac:
    result = await rbac.service.list_roles_paginated(page=1, page_size=20)
```

## 1. Listar Roles con Paginación

```python
from rbac import RBAC

rbac = RBAC(database_url="postgresql+asyncpg://...")
await rbac.init()

result = await rbac.service.list_roles_paginated(page=1, page_size=20)

if result.success:
    print(f"Total roles: {result.pagination.total_items}")
    for role in result.data:
        print(f"- {role.display_name}: {role.permissions}")
```

**Formato de respuesta:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "admin",
      "displayName": "Administrador",
      "description": "Acceso total al sistema",
      "permissions": [1, 2, 3],
      "userCount": 5,
      "createdAt": "2025-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalPages": 1,
    "totalItems": 8,
    "hasNext": false,
    "hasPrev": false
  }
}
```

## 2. Obtener Rol por ID (Expandido)

```python
result = await rbac.service.get_role_expanded(role_id=1)

if result.success:
    role = result.data
    print(f"Role: {role.display_name}")
    print(f"Permissions: {len(role.permissions)}")
    for perm in role.permissions:
        print(f"  - {perm.display_name} ({perm.name})")
```

**Formato de respuesta:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "admin",
    "displayName": "Administrador",
    "description": "Acceso total al sistema",
    "permissions": [
      {
        "id": 1,
        "name": "users.read",
        "displayName": "Ver Usuarios",
        "category": "users"
      },
      {
        "id": 2,
        "name": "users.write",
        "displayName": "Gestionar Usuarios",
        "category": "users"
      }
    ],
    "userCount": 5,
    "createdAt": "2025-01-01T00:00:00Z",
    "updatedAt": "2025-01-15T10:00:00Z"
  }
}
```

## 3. Crear Rol

```python
from vexen_rbac.application.dto import CreateRoleRequest

request = CreateRoleRequest(
    name="analista",
    display_name="Analista",
    description="Acceso de lectura y análisis",
    permissions=[1, 2, 3]
)

result = await rbac.roles.create_role(request)

if result.success:
    print(f"Created role: {result.data.display_name}")
```

**Formato de respuesta:**
```json
{
  "success": true,
  "data": {
    "id": 5,
    "name": "analista",
    "displayName": "Analista",
    "description": "Acceso de lectura y análisis",
    "permissions": [1, 2, 3],
    "userCount": 0,
    "createdAt": "2025-01-20T16:00:00Z"
  }
}
```

## 4. Actualizar Rol

```python
from vexen_rbac.application.dto import UpdateRoleRequest

request = UpdateRoleRequest(
    display_name="Analista Senior",
    description="Acceso de lectura, análisis y reportes",
    permissions=[1, 2, 3, 4, 5]
)

result = await rbac.roles.update_role(role_id=5, role_data=request)
```

## 5. Eliminar Rol

```python
result = await rbac.roles.delete_role(role_id=5)

if result.success:
    print("Role deleted successfully")
```

## 6. Listar Permisos

```python
result = await rbac.permissions.list_permissions()

if result.success:
    for perm in result.data:
        print(f"{perm.name}: {perm.display_name}")
```

**Formato de respuesta:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "users.read",
      "displayName": "Ver Usuarios",
      "description": "Permite ver la lista de usuarios",
      "category": "users"
    },
    {
      "id": 2,
      "name": "users.write",
      "displayName": "Gestionar Usuarios",
      "description": "Permite crear, editar y eliminar usuarios",
      "category": "users"
    }
  ]
}
```

## 7. Obtener Grupos de Permisos

```python
result = await rbac.service.get_permissions_grouped()

if result.success:
    for group in result.data:
        print(f"\n{group.display_name} ({group.category}):")
        for perm in group.permissions:
            print(f"  - {perm.display_name}")
```

**Formato de respuesta:**
```json
{
  "success": true,
  "data": [
    {
      "category": "users",
      "displayName": "Usuarios",
      "permissions": [
        {
          "id": 1,
          "name": "users.read",
          "displayName": "Ver Usuarios"
        },
        {
          "id": 2,
          "name": "users.write",
          "displayName": "Gestionar Usuarios"
        }
      ]
    },
    {
      "category": "tickets",
      "displayName": "Tickets",
      "permissions": [
        {
          "id": 3,
          "name": "tickets.read",
          "displayName": "Ver Tickets"
        }
      ]
    }
  ]
}
```

## Ejemplo Completo (Uso en Aplicación)

```python
import asyncio
import json
from rbac import RBAC
from vexen_rbac.application.dto import CreateRoleRequest, CreatePermissionRequest

async def main():
    rbac = RBAC(database_url="postgresql+asyncpg://...")
    await rbac.init()

    try:
        perm1 = await rbac.permissions.create_permission(
            CreatePermissionRequest(
                name="reports.read",
                display_name="Ver Reportes",
                category="reports"
            )
        )

        role = await rbac.roles.create_role(
            CreateRoleRequest(
                name="reporter",
                display_name="Reporteador",
                permissions=[perm1.data.id]
            )
        )

        roles_paginated = await rbac.service.list_roles_paginated(page=1, page_size=10)

        role_expanded = await rbac.service.get_role_expanded(role.data.id)

        permissions_grouped = await rbac.service.get_permissions_grouped()

        response = {
            "roles": {
                "total": roles_paginated.pagination.total_items,
                "data": [
                    {
                        "id": r.id,
                        "name": r.name,
                        "displayName": r.display_name,
                    }
                    for r in roles_paginated.data
                ]
            },
            "roleDetail": {
                "id": role_expanded.data.id,
                "name": role_expanded.data.name,
                "permissions": [
                    {"name": p.name, "displayName": p.display_name}
                    for p in role_expanded.data.permissions
                ]
            },
            "permissionGroups": [
                {
                    "category": g.category,
                    "count": len(g.permissions)
                }
                for g in permissions_grouped.data
            ]
        }

        print(json.dumps(response, indent=2))

    finally:
        await rbac.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Métodos Disponibles

### Roles
- `list_roles_paginated(page, page_size)` - Lista roles con paginación
- `get_role_expanded(role_id)` - Obtiene rol con permisos expandidos
- `create_role(request)` - Crea un nuevo rol
- `update_role(role_id, request)` - Actualiza un rol
- `delete_role(role_id)` - Elimina un rol
- `add_permissions_to_role(role_id, permission_ids)` - Agrega permisos a rol
- `remove_permissions_from_role(role_id, permission_ids)` - Quita permisos de rol
- `count_roles()` - Cuenta total de roles
- `count_role_permissions(role_id)` - Cuenta permisos en un rol

### Permisos
- `list_permissions()` - Lista todos los permisos
- `get_permissions_grouped()` - Obtiene permisos agrupados por categoría
- `create_permission(request)` - Crea un nuevo permiso
- `update_permission(permission_id, request)` - Actualiza un permiso
- `delete_permission(permission_id)` - Elimina un permiso

### Grupos de Permisos
- `list_permission_groups()` - Lista grupos de permisos
- `create_permission_group(request)` - Crea un grupo
- `update_permission_group(group_id, request)` - Actualiza un grupo
- `delete_permission_group(group_id)` - Elimina un grupo
- `add_permissions_to_group(group_id, permission_ids)` - Agrega permisos a grupo
- `remove_permissions_from_group(group_id, permission_ids)` - Quita permisos de grupo
- `count_group_permissions(group_id)` - Cuenta permisos en grupo
