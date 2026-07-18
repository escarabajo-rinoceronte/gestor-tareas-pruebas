<div align="center">
  <h3>UNIVERSIDAD NACIONAL DE SAN AGUSTÍN</h3>
  <h4>FACULTAD DE INGENIERÍA DE PRODUCCIÓN Y SERVICIOS</h4>
  <h4>ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS</h4>
  <br>
  <img src="/tests-docs/img/logo-unsa.png" alt="Logo UNSA" width="200"/>
  <br><br>
  <b>Curso:</b> Pruebas de Software <br>
  <b>Docente:</b> Ing. Robert Edison Arisaca Mamani <br>
  <b>Semestre:</b> VII <br>
  <b>Proyecto:</b> HOT Tasking Manager — Plan Maestro de Pruebas: Estrategia Organizacional <br>
  <b>Fecha de Elaboración:</b> 11/06/2026 <br>
  <b>Arequipa — Perú</b>
</div>

---

# Plan Maestro de Pruebas: Estrategia Organizacional

**Proyecto:** HOT OSM Tasking Manager  
**EstÃ¡ndar de Referencia:** ISO/IEC/IEEE 29119-2 (Procesos de Pruebas) y 29119-3  

## 1. Estrategia General de Pruebas
El proyecto adopta un enfoque de pruebas estructurado de **"Abajo hacia Arriba" (Bottom-Up)** combinado con una filosofÃ­a **Shift-Left Testing**. Esto implica que la calidad se inyecta desde la fase de desarrollo mediante metodologÃ­as como TDD (Test-Driven Development) y BDD (Behavior-Driven Development), minimizando el descubrimiento de defectos en las fases tardÃ­as de UI/E2E.

### 1.1. Ciclo de Vida Organizacional de las Pruebas
Todas las pruebas, independientemente de su nivel (Unitaria, IntegraciÃ³n, Sistema), seguirÃ¡n el siguiente flujo estÃ¡ndar estipulado por el equipo QA.

![Flujo de trabajo con Wiki](/tests-docs/01-plan-de-pruebas/01-plan-general/img/workflow-wiki.png) 

*(PropÃ³sito del diagrama: Establecer la regla inquebrantable de que ninguna prueba se codifica sin antes haber sido diseÃ±ada y aprobada en la Wiki de QA).*

## 2. OrganizaciÃ³n del Equipo y Responsabilidades
El equipo opera en un esquema progresivo. La fase de planeaciÃ³n inicial se ejecuta con el **Core QA Team (3 miembros)**, escalando a 6 miembros para las fases posteriores. Las responsabilidades se especifican en la siguiente tabla:

| Rol | Integrantes | JustificaciÃ³n |
| --- | ---: | --- |
| **Test Lead** | 1 | Responsable de coordinar al equipo, supervisar el cumplimiento de hitos, gestionar el tablero de trabajo, validar entregables y realizar el seguimiento general del avance del proyecto. |
| **Test Analyst** | 2 | Encargados de analizar el software, identificar funcionalidades y determinar los elementos que serÃ¡n considerados dentro del plan de pruebas. |
| **Test Design** | 2 | Responsables de diseÃ±ar los casos de prueba, definiendo entradas, pasos de ejecuciÃ³n, resultados esperados y criterios de aceptaciÃ³n correspondientes. |
| **Test Architect** | 1 | Define la estructura tÃ©cnica del proceso de pruebas, la organizaciÃ³n del repositorio y la estrategia de pruebas; ademÃ¡s, brinda soporte en tareas relacionadas con CI/CD y GitHub Actions cuando sea requerido. |

## 3. Control Documental y Criterios de RevisiÃ³n
Para garantizar la integridad, consistencia y auditabilidad del Plan de Pruebas, se adopta un enfoque de Docs-as-Code (DocumentaciÃ³n como CÃ³digo). Toda la estructura de /tests-docs reside en un repositorio Git, lo que permite control de versiones, revisiÃ³n por pares y trazabilidad histÃ³rica.

### 3.1. Flujo de RevisiÃ³n por Pares (Peer Review)
Dado que la documentaciÃ³n es compartida por todo el equipo, queda **estrictamente prohibida la ediciÃ³n directa (commit directo)** sobre la rama principal (en este caso `develop`) de la documentaciÃ³n.

El flujo de trabajo colaborativo debe seguir estos pasos:
1.  **CreaciÃ³n de Rama:** El integrante que deba documentar una nueva suite o modificar un plan crearÃ¡ una rama especÃ­fica (ej. `docs/suite-core-services`).
2.  **Desarrollo Documental:** Se redacta el contenido utilizando las plantillas obligatorias ubicadas en `.github/`.
3.  **Pull Request (PR):** Se abre un PR solicitando la integraciÃ³n de los cambios.
4.  **RevisiÃ³n Obligatoria:** El PR requiere la aprobaciÃ³n de al menos un revisor calificado.
    *   *Regla de AprobaciÃ³n:* El Test Lead es el aprobador principal de los planes maestros y estrategias.
    *   *AprobaciÃ³n Delegada:* Para cambios en especificaciones de diseÃ±o (Suites), los Test Analyst pueden realizar revisiones cruzadas.

### 3.2. Criterios de AceptaciÃ³n Documental (DoD de QA)
Un Pull Request documental solo serÃ¡ aprobado si cumple los siguientes criterios:
*   **Consistencia Estructural:** Utiliza la plantilla oficial sin alterar las secciones obligatorias.
*   **Trazabilidad Garantizada:** Todos los hipervÃ­nculos a requisitos (Ã‰picas/Issues) y a scripts de cÃ³digo (`.py`, `.js`) son funcionales y precisos.
*   **Cero AmbigÃ¼edad:** Los pasos de las pruebas o condiciones lÃ³gicas estÃ¡n redactados de forma determinista (un Ãºnico resultado esperado claro).
*   **Alineamiento ISO:** Las tÃ©cnicas de diseÃ±o (*Valores LÃ­mite*, *Particiones de Equivalencia*) estÃ¡n explÃ­citamente declaradas.

### 3.3. Versionado de la DocumentaciÃ³n (SemVer)
El versionado del Plan de Pruebas no sigue las versiones del software, sino su propio ciclo de madurez basÃ¡ndose en **Versionado SemÃ¡ntico (SemVer - X.Y.Z)**:

*   **Cambio Mayor (X.0.0):** Se incrementa cuando hay un cambio de paradigma o se inicia una nueva gran fase del estÃ¡ndar.
    *   *Ejemplo:* Pasar de la Fase de Pruebas Unitarias a la Fase de Pruebas de IntegraciÃ³n (versiÃ³n `1.x.x` a `2.0.0`).
*   **Cambio Menor (0.Y.0):** Se incrementa al agregar nuevas suites de pruebas o realizar adiciones funcionales significativas a un plan existente, sin alterar lo que ya estaba documentado.
    *   *Ejemplo:* Se documenta por primera vez la suite de validaciÃ³n de tareas (`1.0.0` a `1.1.0`).
*   **Parche (0.0.Z):** Se utiliza para correcciones ortogrÃ¡ficas, actualizaciÃ³n de enlaces rotos, formateo Markdown o clarificaciÃ³n de tÃ©rminos.
    *   *Ejemplo:* Corregir la URL de un hipervÃ­nculo en el Plan Maestro (`1.1.0` a `1.1.1`).

La trazabilidad histÃ³rica (quiÃ©n, cuÃ¡ndo y por quÃ© modificÃ³ un documento) queda registrada inmutablemente en el historial de *commits* de Git, sirviendo como registro de auditorÃ­a legal y de calidad.

## 4. Trazabilidad y MÃ©tricas Core

Para cumplir con la **Parte 4 (MediciÃ³n y TÃ©cnicas)** y **Parte 2 (Procesos de Control)** del estÃ¡ndar ISO/IEC/IEEE 29119, el equipo establece un modelo matemÃ¡tico y relacional para medir la calidad del producto y la eficiencia del propio proceso de testing.

### 4.1. El Ecosistema de Trazabilidad Bidireccional
La trazabilidad es el eje central del QA profesional. Asegura que ningÃºn requisito de Tasking Manager carezca de cobertura de pruebas, y que ninguna prueba exista sin justificaciÃ³n de negocio.

Se establece la siguiente cadena de trazabilidad bidireccional (registrada en `matriz-trazabilidad-unitaria.md`):
1.  **Requisito de Negocio / Ã‰pica** (Origen en GitHub Projects).
2.  **MÃ³dulo de CÃ³digo** (Archivo fuente en `hotosm/tasking-manager`).
3.  **EspecificaciÃ³n de DiseÃ±o de Prueba** (Caso documentado en la Wiki `/tests-docs`).
4.  **Test Script Automatizado** (Prueba automatizada en el repositorio).
5.  **Evidencia de EjecuciÃ³n** (Log o reporte de CI/CD).

### 4.2. MÃ©tricas de Cobertura Base (ISO/IEC/IEEE 29119-4)
El estÃ¡ndar internacional exige medir la efectividad de las tÃ©cnicas de diseÃ±o de pruebas empleadas. Para ello, define una fÃ³rmula universal que el equipo aplicarÃ¡ obligatoriamente.

**FÃ³rmula de Cobertura de DiseÃ±o:**

```math
$$ Cobertura\ de\ DiseÃ±o\ (\%) = \left( \frac{N}{T} \right) \times 100 $$
```

*   **T** (Total de Elementos de Cobertura Identificados): Representa el nÃºmero total de escenarios o condiciones que *deberÃ­an* probarse segÃºn el anÃ¡lisis de caja negra (por ejemplo, el total de valores lÃ­mite identificados en un mÃ³dulo).
*   **N** (Elementos Cubiertos / Ejecutados): Representa el nÃºmero de esos escenarios que efectivamente tienen un caso de prueba documentado y ejecutado.

*Ejemplo de aplicaciÃ³n:* Si al analizar el mÃ³dulo de "CreaciÃ³n de Tareas" se identifican 20 combinaciones posibles usando tablas de decisiÃ³n ($T=20$), pero solo se han automatizado y ejecutado 15 ($N=15$), la cobertura de diseÃ±o de esa tÃ©cnica es del **75%**.

### 4.3. MÃ©tricas de EjecuciÃ³n y Calidad del Software
Adicionalmente a la cobertura de diseÃ±o de la ISO, el equipo recolectarÃ¡ y analizarÃ¡ las siguientes mÃ©tricas de ejecuciÃ³n al finalizar cada ciclo de pruebas:

**Cobertura de Pruebas Unitarias (Code Coverage):**
*   *DefiniciÃ³n:* Porcentaje de lÃ­neas lÃ³gicas de cÃ³digo fuente ejecutadas por los scripts de prueba.
*   *FÃ³rmula:* $(LÃ­neas\ de\ cÃ³digo\ ejecutadas / LÃ­neas\ totales\ del\ mÃ³dulo) \times 100$.
*   *Herramienta:* Generado automÃ¡ticamente por herramientas de CI (en este caso se usarÃ¡ Coverage.py). Umbral mÃ­nimo aceptable: **80%**.

**Tasa de EjecuciÃ³n de Pruebas:**
*   *DefiniciÃ³n:* Refleja el estado operacional de la suite de pruebas.
*   *Desglose:*
    *   % Ã‰xito (Passed): $(Pruebas Exitosas / Total Ejecutadas) \times 100$.
    *   % Fallo (Failed): $(Pruebas Fallidas / Total Ejecutadas) \times 100$.
    *   % Bloqueadas (Blocked): Pruebas que no pudieron ejecutarse por dependencias caÃ­das o errores de entorno.

**Densidad de Defectos (Defect Density):**
*   *DefiniciÃ³n:* Indica la madurez y fragilidad de un mÃ³dulo de cÃ³digo especÃ­fico.
*   *FÃ³rmula:* $Total\ de\ Bugs\ Confirmados / TamaÃ±o\ del\ MÃ³dulo$.
*   *PropÃ³sito:* Identificar quÃ© componentes del Tasking Manager (por ejemplo, LÃ³gica espacial vs. AutenticaciÃ³n) concentran la mayor cantidad de errores (Hotspots) para reasignar esfuerzos de QA en futuras iteraciones.

## 5. Estrategia de EvoluciÃ³n del Plan
Este plan es un artefacto vivo. Se ha programado una sesiÃ³n de reevaluaciÃ³n (Test Strategy Review) al finalizar el ciclo de Pruebas de IntegraciÃ³n (Fase 2) para incorporar los procesos metodolÃ³gicos de los 3 nuevos integrantes y adaptar la estrategia hacia las pruebas de Sistema (Fase 3).



