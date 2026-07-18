<div align="center">
  <h3>UNIVERSIDAD NACIONAL DE SAN AGUSTÍN</h3>
  <h4>FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS</h4>
  <h4>ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS</h4>
  <br>
  <img src="/tests-docs/logo-unsa.png" alt="Logo UNSA" width="200"/>
  <br><br>
  <b>Curso:</b> Pruebas de Software <br>
  <b>Docente:</b> Ing. Robert Edison Arisaca Mamani <br>
  <b>Semestre:</b> VII <br>
  <b>Proyecto:</b> HOT Tasking Manager — Reporte de EjecuciÃ³n: Pruebas de Sistema (DesempeÃ±o y Carga) <br>
  <b>Fecha de Elaboración:</b> 19/07/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Reporte de EjecuciÃ³n: Pruebas de Sistema (DesempeÃ±o y Carga)

**Atributo de Calidad:** DesempeÃ±o y Carga (Performance Testing)
**Responsable de EjecuciÃ³n:** Alexandra
**Fecha de EjecuciÃ³n:** 19 de Julio de 2026
**Herramienta:** K6
**MÃ©trica Objetivo (Libro de Myers):** Latencia `p(95) < 2000ms`, Tasa de Error `rate < 5%`

## 1. Resumen Ejecutivo de Resultados

La prueba de desempeÃ±o y carga fue ejecutada exitosamente simulando **50 usuarios concurrentes (VUs)** interactuando simultÃ¡neamente con la API de Tareas (bloqueo y desbloqueo de tareas de mapeo).

El sistema cumpliÃ³ satisfactoriamente con los Criterios de AceptaciÃ³n definidos en el Plan de Pruebas:

*   **Regla 1 â€” Velocidad (Latencia):** El 95% de las peticiones fueron respondidas en **1.76 segundos** (`p(95) = 1.76s`), manteniÃ©ndose por debajo del umbral mÃ¡ximo exigido de 2 segundos.
*   **Regla 2 â€” Tasa de Error:** Solo el **0.04%** de las peticiones fallaron, cumpliendo holgadamente el criterio de aceptaciÃ³n que toleraba hasta un 5% de error. (De cada 10,000 peticiones, solo 5 presentaron timeout).

## 2. Evidencia de EjecuciÃ³n

![Resultados K6 en Consola](./k6-results.jpg)

## 3. AnÃ¡lisis de DesempeÃ±o y ContenciÃ³n de Base de Datos

Durante los 12 minutos de ejecuciÃ³n sostenida, se completaron 4,665 ciclos completos (iteraciones). En estos ciclos, 50 usuarios virtuales intentaron adquirir el bloqueo (*lock*) sobre la misma tarea simultÃ¡neamente. 

El desglose de cÃ³digos de respuesta demuestra un manejo de concurrencia impecable por parte del backend y la base de datos (PostGIS):

*   **`lock_200_ok` (1033 peticiones):** Representa las veces en las que un usuario virtual logrÃ³ adquirir el bloqueo exitosamente.
*   **`lock_403_conflict_or_state` (3632 peticiones):** Representa los rechazos correctos del sistema. Cuando mÃºltiples usuarios intentaron bloquear una tarea que ya habÃ­a sido asignada milisegundos antes al usuario ganador, el sistema los rechazÃ³ apropiadamente (HTTP 403). **Esto demuestra la integridad transaccional**, asegurando que dos usuarios nunca pueden apropiarse de la misma tarea simultÃ¡neamente (Race Condition evitada). 
*   **`checks_succeeded: 100.00% (9330 de 9330)`**: Demuestra que el 100% de las respuestas del servidor fueron las esperadas (Ã©xitos o rechazos controlados), sin presentar comportamientos anÃ³malos o corrupciones de estado.

## 4. ConclusiÃ³n

El sistema backend de Tasking Manager **soporta exitosamente 50 usuarios concurrentes** intentando bloquear tareas simultÃ¡neamente. Mantiene una tasa de error inferior al 0.1% y responde al 95% de las peticiones en menos de 1.8 segundos. Se da por **APROBADO** el Atributo 1 de Pruebas de Sistema (DesempeÃ±o y Carga).


