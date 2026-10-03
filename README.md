# arquitectura-base-CPWG

Base de análisis de discontinuidades para diseños CPWG en KiCad y paquete
publicable con KiCad Plugin and Content Manager (PCM).

## Contenido

- `rf_discontinuity_analyzer.py`: estimación cuasiestática de la impedancia de una
  CPWG y de la reflexión en una transición entre dos geometrías.
- `architecture_base_cpwg.py`: acción del editor PCB de KiCad para introducir las
  dos geometrías y mostrar los resultados del analizador.
- `generate_icons.py`: genera `resources/icon.svg` y `resources/icon.png` de 64×64.
- `package_pcm.py`: genera el icono del paquete, construye y comprueba la
  estructura del archivo PCM.
- `metadata.json`: metadatos PCM del paquete, versión inicial `1.3.0`.
- `.github/workflows/pcm_release.yml`: pruebas y publicación automática al enviar
  una etiqueta `v*`, o ejecución manual desde Actions.

La acción aparece en el menú de herramientas del editor PCB de KiCad. La estimación
usa una aproximación CPW de plano de masa infinito y la permitividad
efectiva `(εr + 1) / 2`; no sustituye una simulación electromagnética de onda
completa ni las comprobaciones DRC de KiCad.

## Alcance y preparación comercial

La versión actual es un estimador exploratorio de una transición entre dos
geometrías CPWG introducidas manualmente. No modifica placas, no enruta ni coloca
vías automáticamente y no ejecuta DRC. No debe utilizarse como única base para
fabricar un diseño RF.

El estado de la validación electromagnética, la compatibilidad real con KiCad,
la validación de mercado y las consideraciones de comercialización se documentan
en [`COMMERCIAL_READINESS.md`](COMMERCIAL_READINESS.md). Esos puntos incluyen
pruebas pendientes que requieren simuladores, instalaciones de KiCad, usuarios
potenciales y asesoramiento legal; no se consideran demostrados por las pruebas
unitarias o por una publicación exitosa.

## Pruebas y uso local

Requiere Python 3.10 o posterior; las pruebas y el analizador solo usan la
biblioteca estándar.

```bash
python -m unittest discover -s tests -v
python rf_discontinuity_analyzer.py \
  --width-before 0.30 --gap-before 0.20 \
  --width-after 0.25 --gap-after 0.20 \
  --epsilon-r 4.2
python generate_icons.py
```

El analizador imprime en JSON las impedancias antes y después de la transición,
el coeficiente de reflexión, la pérdida de retorno y la ROE. Las dimensiones de
ancho y separación se expresan en milímetros.

## Publicar un release PCM

El workflow `.github/workflows/pcm_release.yml` se ejecuta con etiquetas `v*`
o manualmente desde Actions en la rama `main`, indicando `tag_name` (por defecto,
`v1.3.0`). La versión de la etiqueta (sin la `v`) debe coincidir con
`versions[0].version` en `metadata.json`. Para publicar la versión `1.3.0`
mediante una etiqueta, después de integrar los archivos en la rama principal:

```bash
git tag v1.3.0
git push origin v1.3.0
```

El workflow ejecuta las pruebas, valida `metadata.json` y crea
`arquitectura_base_cpwg_pcm.zip` con el manifiesto en la raíz, los módulos bajo
`plugins/` y `resources/icon.png` de 64×64. El release de GitHub incluye ese ZIP y el
`metadata.json` actualizado con la URL, el SHA-256 y el tamaño del paquete. Para
publicar, GitHub Actions requiere permiso de escritura de contenidos en la
configuración del repositorio.
