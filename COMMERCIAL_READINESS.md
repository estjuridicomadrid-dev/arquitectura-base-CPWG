# Preparación para comercialización

Este documento separa lo que el repositorio ya acredita de lo que aún exige
pruebas externas. No se han realizado ni se presuponen mediciones, entrevistas
con clientes o revisiones jurídicas.

## 1. Paquete PCM

El workflow genera el archivo con `metadata.json` en la raíz, los módulos del
plugin bajo `plugins/`, la licencia y `resources/icon.png` en formato PNG de
64×64. La
validación automática comprueba los archivos requeridos y algunos campos del
manifiesto; la aceptación final debe comprobarse instalando el ZIP desde PCM en
una instalación real de KiCad.

## 2. Validación electromagnética

El analizador actual usa una aproximación cuasiestática CPW con plano de masa
infinito y permitividad efectiva `(εr + 1) / 2`. Las pruebas unitarias verifican
propiedades básicas e invariantes; no validan precisión frente a un solver ni
frente a hardware.

Antes de presentar resultados como fiables para diseño, crear un conjunto
reproducible de casos que abarque rangos de ancho, gap, permitividad, espesor,
frecuencia y variaciones geométricas relevantes. Para cada caso, registrar
geometría, propiedades del stackup, configuración del solver, versión del
solver, impedancia o S-parameters de referencia, salida del plugin y error
absoluto/relativo. Comparar geometrías rectas primero y después transiciones;
fijar umbrales de aceptación con un especialista RF y publicar limitaciones.
No anunciar precisión ni uso apto para fabricación hasta completar esa
comparación con simulación electromagnética y, cuando sea posible, mediciones.

## 3. Compatibilidad KiCad

`metadata.json` declara KiCad 8.0 como versión mínima, pero las pruebas
automatizadas actuales no cargan `pcbnew` ni `wx`; por ello no acreditan
compatibilidad efectiva. Registrar en una matriz por sistema operativo y
versión de KiCad: instalación PCM, carga del plugin, apertura del diálogo,
entrada válida e inválida, resultados, cierre y reinstalación/actualización.
Ejecutar y registrar cada celda en instalaciones reales antes de ampliar la
compatibilidad declarada.

| Plataforma | KiCad 8.0 (mínimo declarado) |
| --- | --- |
| Windows | Pendiente de prueba manual |
| macOS | Pendiente de prueba manual |
| Linux | Pendiente de prueba manual |

## 4. Alcance del producto

La propuesta inicial es un **estimador CPWG de escritorio integrado en KiCad**:
entrada manual de dos geometrías y presentación de estimaciones de impedancia,
reflexión, pérdida de retorno y ROE. Es deliberadamente una herramienta
exploratoria. El auto-stitching de vías, la edición de placa, la optimización
automática y la ejecución de DRC quedan fuera del alcance actual y requerirían
requisitos, diseño y validación propios.

## 5. Validación de mercado

Realizar entrevistas exploratorias con diseñadores de PCB RF, ingenieros de
hardware y usuarios de KiCad que trabajen con líneas CPW/CPWG. No presentar
estas entrevistas como realizadas hasta registrar fecha, perfil y consentimiento.
Preguntar, sin inducir una respuesta:

1. ¿Cómo verifica hoy una transición CPWG y qué herramientas usa?
2. ¿Qué errores o tareas repetitivas le cuestan más tiempo?
3. ¿Qué decisiones tomaría con una estimación rápida dentro de KiCad y cuáles
   seguiría verificando con simulación?
4. ¿Qué precisión, informes, geometrías y compatibilidad exigiría?
5. ¿Qué solución alternativa usa actualmente y cuánto cuesta en tiempo/licencia?
6. ¿Qué formato de compra preferiría: soporte, formación, integración o
   personalización? ¿Quién aprueba el gasto?

Documentar patrones y objeciones, separar opiniones de compromisos de compra y
validar interés con un piloto y una oferta/precio concretos antes de invertir en
funciones adicionales. No hay evidencia de demanda comercial aportada aún.

## 6. Modelo de oferta y licencia

El repositorio declara GPL-3.0. La licencia permite cobrar por copias, pero la
distribución queda sujeta a las obligaciones de GPL-3.0, incluidos los derechos
de los destinatarios sobre el código fuente y la redistribución conforme a la
licencia. No ofrecer exclusividad sobre esta versión ni imponer restricciones
adicionales incompatibles con la licencia.

Como hipótesis que se debe contrastar con clientes, evaluar ingresos por
integración, soporte, formación, personalización o servicios profesionales
alrededor del plugin. Revisar cualquier modelo de doble licencia o cambio de
licencia con titulares de derechos y asesoramiento jurídico antes de ofrecerlo.
Este resumen no es asesoramiento legal ni sustituye una revisión de la licencia,
titularidad, dependencias y obligaciones aplicables a la distribución concreta.
