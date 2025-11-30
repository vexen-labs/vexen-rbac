# Guía de Publicación Automática en PyPI

Este documento explica cómo configurar la publicación automática del paquete `rbac` en PyPI usando GitHub Actions.

## ¿Cómo funciona?

El workflow `.github/workflows/python-publish.yml` automatiza todo el proceso:

1. **Trigger**: Se ejecuta automáticamente cuando creas un **Release** en GitHub
2. **Build**: Construye el paquete usando `uv build` (más rápido que `python -m build`)
3. **Publish**: Publica en PyPI usando **Trusted Publishing** (sin necesidad de tokens manuales)

## Configuración Inicial (Una sola vez)

### 1. Configurar Trusted Publishing en PyPI

Trusted Publishing es el método más seguro recomendado por PyPI. No requiere guardar tokens en GitHub.

**Pasos:**

1. Ve a https://pypi.org/manage/account/publishing/
2. Haz clic en "Add a new pending publisher"
3. Completa el formulario:
   ```
   PyPI Project Name: vexen-rbac
   Owner: vexen-labs
   Repository name: vexen-rbac
   Workflow name: python-publish.yml
   Environment name: pypi
   ```
4. Haz clic en "Add"

**Importante**: Debes hacer esto ANTES de crear tu primer release. PyPI necesita verificar que el workflow existe.

### 2. Configurar Environment en GitHub (Opcional pero Recomendado)

Los environments permiten agregar protecciones adicionales antes de publicar.

**Pasos:**

1. Ve a: `https://github.com/vexen-labs/rbac/settings/environments`
2. Haz clic en "New environment"
3. Nombre: `pypi`
4. (Opcional) Configura protecciones:
   - **Required reviewers**: Agrega usuarios que deben aprobar antes de publicar
   - **Wait timer**: Tiempo de espera antes de publicar (ej: 5 minutos para cancelar si es necesario)
   - **Deployment branches**: Limitar a `main` branch solamente

## Flujo de Publicación

### Publicar una nueva versión

```bash
# 1. Actualizar versión en pyproject.toml
# Edita manualmente o usa un script
version = "0.2.0"

# 2. Commit y push cambios
git add pyproject.toml
git commit -m "Bump version to 0.2.0"
git push origin main

# 3. Crear tag
git tag v0.2.0
git push origin v0.2.0

# 4. Crear Release en GitHub
# Ve a: https://github.com/vexen-labs/rbac/releases/new
# - Tag: v0.2.0 (selecciona el tag que creaste)
# - Release title: v0.2.0 o "RBAC v0.2.0"
# - Description: Escribe el changelog (qué cambió en esta versión)
# - Haz clic en "Publish release"

# 5. El workflow se ejecuta automáticamente
# - Construye el paquete con uv
# - Publica en PyPI
# - Puedes ver el progreso en la pestaña "Actions" de GitHub
```

### Crear Release desde GitHub CLI

Si prefieres hacerlo desde la terminal:

```bash
# Instalar gh si no lo tienes
# https://cli.github.com/

# Crear release
gh release create v0.2.0 \
  --title "v0.2.0" \
  --notes "
## Cambios
- Feature: Nueva funcionalidad X
- Fix: Corrección de bug Y
- Docs: Actualización de documentación
"

# El workflow se ejecutará automáticamente
```

## Verificar Publicación

1. **GitHub Actions**: Ve a `https://github.com/vexen-labs/rbac/actions`
   - Verás el workflow "Publish to PyPI" en ejecución
   - Haz clic para ver logs detallados

2. **PyPI**: Ve a `https://pypi.org/project/rbac/`
   - La nueva versión debería aparecer en unos minutos

3. **Probar instalación**:
   ```bash
   # Crear un ambiente virtual nuevo
   uv venv test-env
   source test-env/bin/activate

   # Instalar desde PyPI
   uv pip install rbac

   # Verificar versión
   python -c "import rbac; print(rbac.__version__)"
   ```

## Troubleshooting

### Error: "Trusted publishing exchange failure"

**Causa**: PyPI no tiene configurado el trusted publisher.

**Solución**:
1. Verifica que configuraste el pending publisher en PyPI (paso 1)
2. Verifica que los valores sean exactamente:
   - Owner: `vexen-labs`
   - Repository: `rbac`
   - Workflow: `python-publish.yml`
   - Environment: `pypi`

### Error: "version already exists"

**Causa**: Intentas publicar una versión que ya existe en PyPI.

**Solución**:
1. Incrementa la versión en `pyproject.toml`
2. Crea un nuevo tag y release con la nueva versión

### Error: "Build failed"

**Causa**: Error al construir el paquete.

**Solución**:
1. Prueba el build localmente: `uv build`
2. Verifica que `pyproject.toml` esté correcto
3. Revisa los logs del workflow en GitHub Actions

### El workflow no se ejecuta

**Causa**: El trigger no se activó.

**Solución**:
1. Verifica que creaste un **Release**, no solo un tag
2. El workflow solo se ejecuta con releases publicados (no drafts)
3. Verifica que el archivo esté en `.github/workflows/python-publish.yml`

## Alternativa: Publicación Manual con Token

Si no quieres usar Trusted Publishing, puedes usar un token de PyPI:

1. **Generar token en PyPI**:
   - Ve a https://pypi.org/manage/account/token/
   - Crea un token con scope para el proyecto `rbac`

2. **Agregar secret en GitHub**:
   - Ve a `https://github.com/vexen-labs/rbac/settings/secrets/actions`
   - Crea un secret llamado `PYPI_API_TOKEN` con tu token

3. **Actualizar workflow**:
   ```yaml
   - name: Publish to PyPI
     uses: pypa/gh-action-pypi-publish@release/v1
     with:
       user: __token__
       password: ${{ secrets.PYPI_API_TOKEN }}
   ```

Pero **Trusted Publishing es más seguro** y no requiere guardar tokens.

## Mejoras del Workflow

El workflow actualizado incluye:

- ✅ **uv build**: 10x más rápido que `python -m build`
- ✅ **Trusted Publishing**: Sin tokens, más seguro
- ✅ **Environment protection**: Opción de requerir aprobación antes de publicar
- ✅ **URL del proyecto**: Link directo a la versión publicada en PyPI
- ✅ **Comentarios en español**: Más fácil de entender

## Referencias

- [Trusted Publishing - PyPI](https://docs.pypi.org/trusted-publishers/)
- [GitHub Actions - Publishing](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python#publishing-to-package-registries)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Creating Releases - GitHub](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
