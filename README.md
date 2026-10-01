# arquitectura-base-CPWG

KiCad CPWG Auto-Stitcher, Closed-Loop DRC & Capacitive Tapering Engine.

## Configuración del repositorio y CI/CD

### 1. Vinculación del entorno local

```bash
git branch -M main
git remote add origin https://github.com/estjuridicomadrid-dev/arquitectura-base-CPWG.git
# o por SSH: git@github.com:estjuridicomadrid-dev/arquitectura-base-CPWG.git
git push -u origin main
```

El archivo `.gitignore` excluye `__pycache__/`, bytecode de Python, archivos `*.zip`
(p. ej. `rf_via_stitcher_package.zip`, generado por el pipeline), `.DS_Store` y `.vscode/`.

### 2. Permisos de GitHub Actions

Para que el workflow `.github/workflows/pcm_release.yml` pueda publicar releases con `GITHUB_TOKEN`:

1. **Settings → Actions → General → Workflow permissions**.
2. Seleccionar **Read and write permissions**.
3. (Opcional, recomendado) Marcar **Allow GitHub Actions to create and approve pull requests**.
4. Pulsar **Save**.

### 3. Primer release automático

Crear el tag semántico correspondiente a la versión de `metadata.json`:

```bash
git tag v1.3.0
git push origin v1.3.0
```

En la pestaña **Actions** se ejecutarán los jobs `test-and-validate` (flake8 y
`rf_discontinuity_analyzer.py`) y `build-and-release` (`generate_icons.py`, empaquetado ZIP,
SHA-256 e inyección en `metadata.json`). El release quedará publicado en **Releases** con
`rf_via_stitcher_package.zip` y `metadata.json`.
