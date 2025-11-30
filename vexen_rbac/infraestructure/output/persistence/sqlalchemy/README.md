# SQLAlchemy 2.0 Persistence Layer

Esta carpeta contiene la implementación de persistencia usando SQLAlchemy 2.0 con sesiones asíncronas y PostgreSQL.

## Estructura

```
sqlalchemy/
├── database.py              # Configuración de AsyncEngine y AsyncSession
├── models/                  # Modelos ORM usando DeclarativeBase
│   ├── base.py              # Base declarativa y tablas de asociación M2M
│   ├── permission.py        # PermissionModel
│   ├── permission_group.py  # PermissionGroupModel
│   └── role.py              # RoleModel (con relaciones M2M)
├── mappers/                 # Conversión Entity ↔ Model
│   ├── permission_mapper.py
│   ├── permission_group_mapper.py
│   └── role_mapper.py
└── repositories/            # Implementación de puertos con AsyncSession
    ├── permission_repository.py
    ├── permission_group_repository.py
    └── role_repository.py
```

## Características de SQLAlchemy 2.0

- **AsyncEngine y AsyncSession**: Soporte completo para operaciones asíncronas
- **Typed Annotations**: Usa `Mapped` y `mapped_column` para type hints
- **DeclarativeBase**: Nueva sintaxis declarativa de SQLAlchemy 2.0
- **Lazy loading**: Configurado como `selectin` para evitar N+1 queries
- **Connection pooling**: Configuración optimizada de pool de conexiones

## Relaciones Many-to-Many

### Tablas de Asociación (en `models/base.py`):

1. **role_permissions** (roles ↔ permissions)
   - role_id → roles.id
   - permission_id → permissions.id

2. **role_permission_groups** (roles ↔ permission_groups)
   - role_id → roles.id
   - permission_group_id → permission_groups.id

3. **permission_group_permissions** (permission_groups ↔ permissions)
   - permission_group_id → permission_groups.id
   - permission_id → permissions.id

## Uso

### 1. Inicializar la base de datos

```python
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.database import (
    init_db,
    close_db
)

# Al inicio de la aplicación
await init_db()

# Al cerrar la aplicación
await close_db()
```

### 2. Usar con context manager (recomendado)

```python
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.database import get_async_session
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.repositories import RoleRepository
from vexen_rbac.domain.entity import Role

async def create_role():
    async with get_async_session() as session:
        # Crear repositorio con la sesión
        repo = RoleRepository(session)

        # Crear un rol
        role = Role(
            id=1,
            name="admin",
            display_name="Administrator",
            description="Full system access",
            permissions=[1, 2, 3],
            permission_groups=[1]
        )

        # Guardar (commit automático al salir del context manager)
        saved_role = await repo.save(role)
        print(f"Created role: {saved_role.display_name}")
```

### 3. Uso manual de sesiones

```python
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.database import DatabaseConfig
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.repositories import (
    RoleRepository,
    PermissionRepository
)

# Obtener factory de sesiones
session_factory = DatabaseConfig.get_session_factory()

# Crear sesión
async with session_factory() as session:
    try:
        # Crear repositorios
        role_repo = RoleRepository(session)
        permission_repo = PermissionRepository(session)

        # Realizar operaciones
        role = await role_repo.get_by_id(1)

        # Commit manual
        await session.commit()
    except Exception:
        await session.rollback()
        raise
```

### 4. Operaciones CRUD

```python
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.database import get_async_session
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.repositories import (
    RoleRepository,
    PermissionRepository,
    PermissionGroupRepository
)
from vexen_rbac.domain.entity import Role, Permission, PermissionGroup

async def crud_examples():
    async with get_async_session() as session:
        role_repo = RoleRepository(session)

        # CREATE
        new_role = Role(
            id=1,
            name="admin",
            display_name="Administrator",
            permissions=[1, 2],
            permission_groups=[1]
        )
        created_role = await role_repo.save(new_role)

        # READ
        role = await role_repo.get_by_id(1)
        print(f"Found: {role.display_name}")

        # UPDATE
        role.description = "Updated description"
        updated_role = await role_repo.save(role)

        # DELETE
        await role_repo.delete(1)
```

## Variables de Entorno

Configurar en archivo `.env`:

```env
# Database URL (formato: postgresql+asyncpg://user:password@host:port/database)
DATABASE_URL=postgresql+asyncpg://rbac_user:rbac_password@localhost:5432/rbac_db

# Database settings
DB_ECHO=False                # True para ver SQL queries en consola
DB_POOL_SIZE=5               # Tamaño del pool de conexiones
DB_MAX_OVERFLOW=10           # Máximo de conexiones extra
```

## Migraciones con Alembic

### Instalación

```bash
uv add alembic
```

### Inicialización

```bash
# Crear estructura de Alembic
alembic init migrations

# Editar alembic.ini - cambiar sqlalchemy.url
sqlalchemy.url = postgresql+asyncpg://rbac_user:rbac_password@localhost:5432/rbac_db
```

### Configurar `migrations/env.py`

```python
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models import Base
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.database import DatabaseConfig

# En target_metadata
target_metadata = Base.metadata

# En run_migrations_offline()
url = DatabaseConfig.get_database_url()

# En run_migrations_online() usar async
from sqlalchemy.ext.asyncio import create_async_engine

async def run_async_migrations():
    connectable = create_async_engine(
        DatabaseConfig.get_database_url(),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
```

### Comandos de Alembic

```bash
# Crear migración automática
alembic revision --autogenerate -m "Initial migration"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1

# Ver historial
alembic history

# Ver estado actual
alembic current
```

## Configuración del Engine

El `AsyncEngine` está configurado con:

- **pool_size**: 5 conexiones en pool
- **max_overflow**: 10 conexiones adicionales máximas
- **pool_pre_ping**: Verifica conexiones antes de usar
- **pool_recycle**: Recicla conexiones cada hora
- **echo**: Logs de SQL (controlado por env var)

## Patrones Avanzados

### 1. Transacciones Explícitas

```python
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.database import get_async_session

async def complex_operation():
    async with get_async_session() as session:
        role_repo = RoleRepository(session)
        permission_repo = PermissionRepository(session)

        # Todas las operaciones en la misma transacción
        role = await role_repo.get_by_id(1)
        permission = await permission_repo.get_by_id(1)

        # Modificar ambos
        role.description = "Updated"
        await role_repo.save(role)

        permission.category = "admin"
        await permission_repo.save(permission)

        # Commit automático al salir si no hay errores
        # Rollback automático si hay excepción
```

### 2. Queries Personalizadas

```python
from sqlalchemy import select
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models import RoleModel

async def custom_query():
    async with get_async_session() as session:
        # Query personalizada
        stmt = select(RoleModel).where(RoleModel.name.like("admin%"))
        result = await session.execute(stmt)
        roles = result.scalars().all()

        return roles
```

### 3. Eager Loading de Relaciones

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.models import RoleModel

async def get_role_with_permissions():
    async with get_async_session() as session:
        # Cargar rol con todas sus relaciones en una query
        stmt = (
            select(RoleModel)
            .options(
                selectinload(RoleModel.permissions),
                selectinload(RoleModel.permission_groups)
            )
            .where(RoleModel.id == 1)
        )
        result = await session.execute(stmt)
        role_model = result.scalar_one()

        return RoleMapper.to_entity(role_model)
```

## Ejemplo Completo de Aplicación

```python
import asyncio
from contextlib import asynccontextmanager

from vexen_rbac.infraestructure.output.persistence.sqlalchemy.database import (
    init_db,
    close_db,
    get_async_session
)
from vexen_rbac.infraestructure.output.persistence.sqlalchemy.repositories import (
    RoleRepository,
    PermissionRepository
)
from vexen_rbac.domain.entity import Role, Permission


@asynccontextmanager
async def lifespan():
    """Application lifespan manager."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


async def main():
    async with lifespan():
        # Crear permission
        async with get_async_session() as session:
            perm_repo = PermissionRepository(session)

            permission = Permission(
                id=1,
                name="users.read",
                display_name="Read Users",
                category="users"
            )
            await perm_repo.save(permission)

        # Crear role
        async with get_async_session() as session:
            role_repo = RoleRepository(session)

            role = Role(
                id=1,
                name="admin",
                display_name="Administrator",
                permissions=[1]
            )
            saved_role = await role_repo.save(role)
            print(f"Created: {saved_role}")

        # Obtener role
        async with get_async_session() as session:
            role_repo = RoleRepository(session)
            role = await role_repo.get_by_id(1)
            print(f"Retrieved: {role}")


if __name__ == "__main__":
    asyncio.run(main())
```

## Comparación con TortoiseORM

| Aspecto | SQLAlchemy 2.0 | TortoiseORM |
|---------|----------------|-------------|
| **Madurez** | Muy maduro, estándar de la industria | Más reciente |
| **Type hints** | Excelente (Mapped, mapped_column) | Bueno |
| **Migraciones** | Alembic (robusto, flexible) | Aerich (más simple) |
| **Queries** | Muy potente, flexible | Más simple, menos flexible |
| **Documentación** | Extensa | Buena pero menos completa |
| **Ecosistema** | Enorme | Más pequeño |
| **Curva de aprendizaje** | Media-Alta | Baja |
| **Performance** | Excelente | Excelente |

## Notas Importantes

1. **Sesiones asíncronas**: Todos los métodos de repositorio son async
2. **Lazy loading**: Configurado como `selectin` para evitar N+1 queries
3. **Relaciones M2M**: Se actualizan mediante `update_model_relationships()`
4. **IDs auto-incrementales**: PostgreSQL genera IDs automáticamente
5. **Context manager**: Maneja commit/rollback automáticamente
6. **Pool de conexiones**: Reutiliza conexiones para mejor performance
7. **Type safety**: Usa Mapped[T] para type checking completo

## Troubleshooting

### Error: "greenlet_spawn has not been called"

Asegúrate de tener instalado `greenlet`:
```bash
uv add greenlet
```

### Error: "Could not locate column in row"

Verifica que las relaciones estén cargadas. Usa `selectinload()` o configura `lazy="selectin"`.

### Performance lento en M2M

Considera usar `selectinload()` para cargar relaciones en una sola query:
```python
stmt = select(RoleModel).options(selectinload(RoleModel.permissions))
```
