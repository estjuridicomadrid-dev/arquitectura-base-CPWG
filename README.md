# arquitectura-base-CPWG

Base de análisis de discontinuidades para diseños CPWG en KiCad y paquete
publicable con KiCad Plugin and Content Manager (PCM).

## Contenido

- `rf_discontinuity_analyzer.py`: estimación cuasiestática de la impedancia de una
  CPWG y de la reflexión en una transición entre dos geometrías.
- `architecture_base_cpwg.py`: acción del editor PCB de KiCad para introducir las
  dos geometrías y mostrar los resultados del analizador.
- `generate_icons.py`: genera `resources/icon.svg`, incluido en el paquete.
- `metadata.json`: metadatos PCM del paquete, versión inicial `1.3.0`.
- `.github/workflows/pcm_release.yml`: pruebas y publicación automática al enviar
  una etiqueta `v*`.

La acción aparece en el menú de herramientas del editor PCB de KiCad. La estimación
usa una aproximación CPW de plano de masa infinito y la permitividad
efectiva `(εr + 1) / 2`; no sustituye una simulación electromagnética de onda
completa ni las comprobaciones DRC de KiCad.

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

El workflow `.github/workflows/pcm_release.yml` se ejecuta con etiquetas `v*`.
La versión de la etiqueta (sin la `v`) debe coincidir con `versions[0].version`
en `metadata.json`. Para publicar la versión `1.3.0`, después de integrar los
archivos en la rama principal:

```bash
git tag v1.3.0
git push origin v1.3.0
```

El workflow ejecuta las pruebas, valida `metadata.json`, genera el icono y crea
`arquitectura_base_cpwg_pcm.zip`. El release de GitHub incluye ese ZIP y el
`metadata.json` actualizado con la URL, el SHA-256 y el tamaño del paquete. Para
publicar, GitHub Actions requiere permiso de escritura de contenidos en la
configuración del repositorio.
