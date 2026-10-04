# NPV Marketing · Documentación del plugin

| Campo | Detalle |
| --- | --- |
| Plugin | `npv-marketing` |
| Versión documentada | 0.2.4 |
| Skill | `npv-diagnostico-comercial` |
| Plataforma | Codex · plugins y skills |
| Repositorio | `business-bots` (fuente canónica) |
| Alcance | Arranque y diagnóstico comercial de un desarrollo inmobiliario |
| Fecha del documento | 2 de octubre de 2026 |

---

## 1. Propósito

`npv-marketing` es un piloto que ayuda al equipo de NPV a **entender por qué no se está vendiendo un desarrollo y qué conviene comprobar a continuación**, trabajando con los documentos que ya existen, investigación del mercado en internet y el mínimo de preguntas posible.

No produce campañas, no publica, no se conecta a CRM ni a plataformas de anuncios y no sustituye la decisión del equipo. Entrega un diagnóstico con su nivel de evidencia y un siguiente paso.

Este documento describe **lo que el plugin hace hoy**, no lo que podría hacer. Para la propuesta de un bot que cubra además planeación, implementación y validación, ver `CB2_Especificacion_construccion_NPV.pdf` y su revisión en `CB2_revision_feedback.md`.

---

## 2. Decisiones de diseño

Estas decisiones explican por qué el plugin está escrito como está. Cada una se sostiene con casos de prueba en `tests/behavior/`.

| Decisión | Implicación |
| --- | --- |
| **Empezar con lo que haya, no con un formulario** | El plugin no exige índice, brochure, inventario ni CRM para arrancar. Arranca con archivos sueltos, enlaces o una explicación hablada. |
| **La metodología es reutilizable entre desarrollos** | No se incrustan nombres, precios, inventarios, leads ni segmentos de ningún desarrollo. Todo lo específico vive en los documentos del proyecto de trabajo. |
| **Los datos viven en Drive, no en el repo** | El repositorio contiene instrucciones. Credenciales, archivos comerciales y datos de clientes pertenecen a los sistemas de trabajo. |
| **Investigar antes de recomendar** | Ninguna recomendación comercial sale solo de material interno. Se contrasta con fuentes públicas abiertas, leídas y fechadas. |
| **Evidencia separada de interpretación** | Siempre se distingue lo que muestran los datos de lo que el bot infiere. No se inventan cifras ni probabilidades. |
| **Hablar como parte del equipo comercial** | Lenguaje cotidiano. Quien contesta es alguien de ventas, no un especialista en marketing. |
| **Avanzar con lo incompleto** | Si falta un dato, se da una lectura provisional y se dice qué la confirmaría. La falta de organización documental no bloquea el diagnóstico. |
| **Carga progresiva de instrucciones** | `SKILL.md` es corto y enlaza referencias que solo se cargan cuando hacen falta. Evita el problema de instrucciones que no caben o se diluyen. |
| **Alcance acotado a propósito** | El piloto cubre arranque y diagnóstico. No afirma capacidades que no tiene. |

---

## 3. Arquitectura

### 3.1 Estructura del repositorio

```
business-bots/
├── .agents/plugins/marketplace.json     Catálogo instalable (marketplace local)
├── plugins/
│   └── npv-marketing/
│       ├── .codex-plugin/plugin.json    Manifiesto: nombre, versión, interfaz
│       └── skills/
│           └── npv-diagnostico-comercial/
│               ├── SKILL.md             Contrato de comportamiento
│               ├── references/          Se cargan bajo demanda
│               │   ├── criterios-diagnostico.md
│               │   └── fuentes-y-continuidad.md
│               ├── assets/
│               │   └── inicio-del-desarrollo.md
│               └── agents/openai.yaml   Interfaz de la skill
├── scripts/
│   ├── install.sh                       Instalar / reinstalar
│   ├── validate.py                      Validación estructural
│   └── cachebust.py                     Recarga local sin subir versión
├── tests/behavior/                      27 casos de prueba manual
└── .github/workflows/validate.yml       CI
```

### 3.2 Niveles de instrucción

El plugin usa tres niveles, cada uno con un criterio distinto de cuándo se carga:

| Nivel | Archivo | Contiene | Cuándo se carga |
| --- | --- | --- | --- |
| Contrato | `SKILL.md` | Cómo se comporta el bot de principio a fin | Siempre que la skill se activa |
| Referencia | `references/*.md` | Criterios detallados de diagnóstico y de manejo de fuentes | Cuando la situación lo requiere |
| Plantilla | `assets/*.md` | Estructura del documento "Inicio del desarrollo" | Cuando el equipo encarga organizar |

Esta separación es deliberada: mantiene el contrato corto y legible, y evita que criterios de detalle compitan por atención en cada conversación.

### 3.3 Dónde viven los datos

El plugin **no almacena nada**. Los índices, inventarios, precios, leads y documentos comerciales viven en Google Drive y se proporcionan desde el proyecto de trabajo. La conexión de Drive se configura por separado; el repositorio no incluye credenciales ni instala conectores.

---

## 4. Comportamiento de la skill

Lo que sigue es el contrato de `SKILL.md`, sección por sección.

### 4.1 Cuándo se activa

Se activa para iniciar o retomar el diagnóstico comercial de un desarrollo: pocos leads, baja calificación, pocas visitas, ventas lentas, reconsideración de segmento, o simplemente para organizar la información inicial —con o sin índice previo.

### 4.2 Lenguaje

- Español, salvo preferencia distinta del usuario.
- Expresiones cotidianas: *"qué quieren mejorar en las ventas"*, *"archivos y datos del desarrollo"*, *"posibles causas"*. No se recita la metodología interna.
- Los términos especializados se explican solo cuando ayudan a decidir.
- Los límites se nombran en concreto: *"dejaré la hoja de leads sin abrir, como pediste"*, nunca *"revisaré las restricciones vigentes"*.
- No se asume el nombre del desarrollo a partir del nombre del plugin o de etiquetas como "Piloto". Si no está claro, se pregunta.

### 4.3 Contexto antes de preguntas

1. Revisar primero la información disponible del desarrollo que pueda responder la pregunta.
2. Si existe un índice, usarlo como mapa —no como requisito ni como límite de búsqueda. Un documento pertinente fuera del índice se usa igual.
3. Leer con propósito: localizar ampliamente, profundizar solo en lo necesario.
4. Respetar cualquier restricción explícita sobre archivos que no deban consultarse.
5. **Después** de revisar el contexto, preguntar solo lo que falte y pueda cambiar la siguiente decisión. Normalmente de una a tres preguntas por turno.
6. Lo que el usuario ya autorizó o encargó no se vuelve a preguntar.

Objetivo/plazo, inventario/precios, embudo, inversión/leads y compradores recientes **no son un checklist obligatorio**.

Si un dato no existe, se ofrece una alternativa proporcional —una muestra, unas entrevistas, una medición simple— y se dice qué conclusión queda limitada. *La falta de registro no prueba falta de actividad.*

### 4.4 Organización documental

- Si ya existe una estructura, se aprovecha y no se duplica.
- Si el equipo quiere organizar, se ofrece una carpeta de trabajo y un documento "Inicio del desarrollo" basado en la plantilla.
- Antes de crearlo, se revisa si ya existe un equivalente.
- Los originales se enlazan donde están; no se mueven ni se copian.
- **Organizar nunca es requisito para empezar a diagnosticar.**

### 4.5 Investigación de mercado

El núcleo del trabajo de las versiones 0.2.3 y 0.2.4. Antes de cualquier recomendación comercial o de marketing, el material interno no basta.

**Antes de buscar:** decir en pocas líneas qué frentes se van a revisar y qué pregunta resuelve cada uno. Ajustar ese alcance con lo que el equipo aporte o ya tenga resuelto. No esperar aprobación cuando el alcance es evidente.

**Los cuatro frentes:**

| Frente | Qué buscar |
| --- | --- |
| Ubicación actual | Movilidad, infraestructura, servicios, usos del suelo, cambios geográficos y riesgos territoriales de la zona. |
| Competencia en la zona | Desarrollos comparables por ubicación, producto, precio, condiciones, entrega y segmento; oferta disponible y diferencias relevantes. |
| Entorno socioeconómico, micro y macro | Empleo, ingresos, actividad local, oferta y demanda, crédito, tasas e inflación, y su posible efecto sobre este producto y comprador. |
| Tendencias sociales del segmento | Cambios en hogares, formas de trabajo, preferencias de vivienda y hábitos de búsqueda o compra, sustentados en estudios o señales contrastadas. |

**Profundidad exigida en un frente que puede cambiar la decisión:**

- Abrir y leer la fuente; no concluir desde el fragmento del buscador.
- Buscar al menos dos fuentes independientes que coincidan. Si solo hay una, decirlo y tratar el hallazgo como señal, no como hecho.
- Registrar fecha de publicación, periodo del dato y alcance geográfico. *Un dato nacional no demuestra una tendencia local.*
- Traducir el hallazgo a este caso: qué implicaría para este producto, precio, condiciones y comprador.
- Nombrar lo que no se encontró en lugar de sustituirlo por un dato cercano.

Un frente que no pueda cambiar la decisión se revisa de forma somera y se dice que quedó así.

**Al entregar:** reportar qué frentes se cubrieron, cuáles quedaron con evidencia débil o sin evidencia, y qué haría falta para cerrarlos.

**Preferencias de fuente:** estadísticas oficiales para el entorno, fuentes directas para la oferta, estudios para tendencias. Se distinguen precios anunciados de precios de cierre, y comparables de datos propios. Internet complementa el contexto público: no sustituye el inventario vigente, el embudo ni las ventas internas.

**Excepciones:** las aclaraciones, cálculos y tareas de organización no disparan investigación de mercado por sí solos. La investigación ya hecha y vigente se reutiliza en lugar de repetirse.

**Si no hay acceso web** o el usuario pide no usarlo: informar el límite y continuar con un análisis provisional. No presentar recomendaciones como contrastadas con el mercado ni inventar fuentes.

**Ubicación:** se obtiene del contexto del proyecto. Si no está clara, se pregunta antes de buscar —nunca se usa la ubicación del usuario, de otro proyecto ni una coincidencia de nombre.

### 4.6 Diagnóstico

Se relaciona la evidencia con las causas posibles —producto, precio y condiciones, segmento, canal, mensaje, confianza y proceso comercial— evaluando solo las relevantes al caso. **Una caída de ventas no implica automáticamente cambiar de segmento.**

El mercado y los competidores se usan como comparación, sin atribuir sus datos, supuestos o segmentos al proyecto.

**Tabla de señal → qué distinguir** (`criterios-diagnostico.md`):

| Señal | Alternativas que conviene distinguir | Alternativa de bajo esfuerzo |
| --- | --- | --- |
| Pocos leads | Menos inversión, menor alcance, respuesta al anuncio, medición o cambio de oferta | Muestra de reportes y fechas de cambios de campaña |
| Muchos descartes | Presupuesto, enganche, crédito, ubicación, producto o calificación | Muestra anonimizada de conversaciones o entrevista con ventas |
| No contestan | Datos erróneos, demora, horario, canal o intención inicial | Revisar unos casos recientes con el asesor |
| Pocas visitas | Falta de calificación, objeciones, agenda o citas incumplidas | Revisar citas recientes y motivos de no asistencia |
| Visitas sin cierre | Precio, producto disponible, financiamiento, confianza, seguimiento o ciclo largo | Comparar compradores y no compradores recientes |
| Caída de velocidad | Cambio de mezcla/inventario, estacionalidad, captación o conversión | Reconstruir una cronología de cambios comerciales |

*Las filas son opciones, no una entrevista completa. Una misma señal puede tener varias causas y la falta de un dato no demuestra ninguna de ellas.*

**Salvaguardas al interpretar métricas:**

- Confirmar definiciones de lead, contacto, cita, visita, apartado y venta; validar códigos internos con el equipo.
- Distinguir citas agendadas de realizadas, y apartados de ventas; considerar cancelaciones.
- Usar denominadores, ventanas y poblaciones compatibles. No sumar estados que se superponen. Con denominador cero, indicar no calculable.
- Separar conversiones de una cohorte de leads de ventas registradas en un mes.
- Considerar la maduración del ciclo inmobiliario antes de juzgar campañas recientes.
- **No asignar una venta a un canal sin evidencia de atribución.**
- Una caída de leads con menor inversión no demuestra un problema de segmento. Un CPL menor no demuestra mejor desempeño comercial.

**Salvaguardas al evaluar segmentos:**

- No inferir residencia por LADA, ni capacidad o motivación por nacionalidad.
- Una persona compradora se apoya en evidencia y criterios de decisión; nada de biografías inventadas.
- No extrapolar atracción turística, población o demanda regional al tamaño del mercado alcanzable.
- Si se pide dimensionamiento: explicitar fuente, método, rangos y supuestos.

### 4.7 Entregar y continuar

Una respuesta útil deja claro cinco cosas:

1. qué se quiere mejorar;
2. qué sugieren los datos disponibles;
3. cuáles son las posibles causas relevantes;
4. qué falta comprobar;
5. cuál es el siguiente paso útil.

**Validación con el equipo.** Antes de recomendar se comparten los hallazgos nuevos relevantes, sus fuentes y cómo afectan la lectura del problema. Si un supuesto o discrepancia es **determinante** para la decisión, se contrasta con el usuario y **se espera su respuesta** antes de recomendar. Si no hay nada relevante por confirmar, se avanza sin repetir preguntas resueltas.

Esta distinción es intencional: evita tanto recomendar sobre un supuesto frágil como pedir aprobación de rutina en cada turno.

**Continuidad.** Se guarda solo el contexto que ayude a retomar: desarrollo, problema, evidencia con enlaces y fechas, decisiones, pendientes y siguiente acción. Al retomar, se aprovecha ese contexto antes de repetir preguntas.

**Guardado.** Solo cuando el usuario lo pida. Se verifica lo escrito y se devuelve el enlace. Si la escritura en Drive no está disponible, se prepara el contenido en la conversación y se dice que todavía no se guardó. **Nunca se afirma que algo quedó guardado si solo se mencionó en el chat, ni se fabrica un enlace.**

---

## 5. Referencias y plantilla

| Archivo | Contiene | Se consulta cuando |
| --- | --- | --- |
| `references/criterios-diagnostico.md` | Los cuatro frentes de investigación y su profundidad; tabla señal → alternativas; interpretación de métricas; evaluación de segmentos y producto | Hay que investigar el mercado o distinguir problemas de volumen, adecuación, contacto, visitas o cierre |
| `references/fuentes-y-continuidad.md` | Trabajo con Drive, lectura de hojas extensas, organización y guardado, continuidad entre conversaciones | Se trabaja con Drive o se retoma una conversación anterior |
| `assets/inicio-del-desarrollo.md` | Plantilla del documento de inicio: qué resolver, lo que se sabe, información disponible con vigencia y responsable, restricciones, decisiones, pendientes | El equipo encarga organizar o guardar avances |

La plantilla registra solo materiales disponibles: no exige brochure, inventario ni CRM para crearse, y distingue la fecha de actualización del documento de la fecha de corte de sus fuentes.

---

## 6. Dependencias del entorno

| Capacidad | Requisito | Si falta |
| --- | --- | --- |
| Investigación de mercado | Herramientas web disponibles en la sesión | Se informa el límite y el análisis se presenta como provisional |
| Lectura de documentos | Conexión de Google Drive autorizada | Se indica la limitación concreta y se continúa con lo disponible |
| Guardado y organización | Escritura de Drive, Docs o Sheets | Se prepara el contenido en la conversación, sin fabricar enlaces |
| Campañas y CRM | — | No soportado. El plugin no se conecta a anuncios ni a CRM |

---

## 7. Ciclo de desarrollo

### 7.1 Instalación

```bash
git clone https://github.com/jackbravo/business-bots.git
cd business-bots
bash scripts/install.sh npv-marketing
```

Abrir un **hilo nuevo** de Codex después de instalar. Para traer cambios posteriores:

```bash
git pull --ff-only
bash scripts/install.sh --update npv-marketing
```

`install.sh` valida antes de instalar, comprueba que el plugin esté registrado en el marketplace, registra el repositorio como marketplace local (solo en la instalación inicial) y ejecuta `codex plugin add`.

### 7.2 Flujo de un cambio

1. Actualizar `main` y crear una rama corta: `feature/...`, `fix/...` o `chore/...`.
2. Modificar únicamente la carpeta del plugin afectado y sus pruebas.
3. Ejecutar `python3 scripts/validate.py`.
4. Para probar localmente sin tocar la versión estable, generar un cachebuster:

   ```bash
   python3 scripts/cachebust.py plugins/npv-marketing
   bash scripts/install.sh --update npv-marketing
   ```

5. Probar en un hilo nuevo. Ejecutar `git restore plugins/npv-marketing/.codex-plugin/plugin.json` antes del commit si el único cambio del manifiesto es el cachebuster.
6. Revisar los casos de `tests/behavior/` y registrar cualquier cambio deliberado en las expectativas.
7. Abrir un pull request. Antes de fusionar un cambio publicable, actualizar la versión semántica en `plugin.json` y el catálogo del `README.md`.

**El cachebuster.** `cachebust.py` reemplaza la versión por `<base>+codex.local-<timestamp>` para que Codex no reutilice la copia anterior. Conserva la base de la versión y reemplaza cualquier sufijo previo. `validate.py` y CI **rechazan** versiones `+codex.*`; solo `install.sh --update` las permite. Esto impide que un cachebuster local llegue a `main` por accidente.

### 7.3 Validación estructural

`scripts/validate.py` corre sin dependencias externas y comprueba:

- marketplace: `name` válido, `interface.displayName` presente, lista de plugins no vacía, sin duplicados;
- cada entrada: `source` apunta a `./plugins/<nombre>`, `policy.installation` y `policy.authentication` con valores permitidos, `category` presente;
- manifiesto: existe, el `name` coincide con la carpeta, tiene `version` y `description`, `skills` es `./skills/`, no admite `hooks`, sin `[TODO:` pendientes, sin cachebuster (salvo `--allow-cachebuster`);
- cada skill: frontmatter bien formado, `name` coincide con la carpeta, `description` presente, sin `[TODO:`, y **todos los enlaces relativos resuelven a archivos existentes**;
- ningún plugin presente en `plugins/` queda fuera del marketplace.

CI ejecuta esta validación y `py_compile` sobre `scripts/*.py` en cada pull request y push a `main`.

### 7.4 Un PR está listo cuando

- `python3 scripts/validate.py` termina correctamente;
- el plugin puede reinstalarse desde `business-bots`;
- el comportamiento se probó en un hilo nuevo;
- los casos afectados tienen expectativas actualizadas;
- el PR explica el cambio observable y sus límites;
- no contiene datos sensibles ni un cachebuster local accidental.

---

## 8. Pruebas de comportamiento

27 casos en `tests/behavior/npv-diagnostico-comercial.md`, de ejecución **manual** en un hilo nuevo tras reinstalar. La validación estructural no los sustituye.

**Reglas de ejecución:** nombres y cifras inventados, nunca datos personales de prospectos o clientes. En escenarios de recomendación se asigna al desarrollo ficticio una **ubicación real** y se habilitan herramientas web. Se registra versión y commit, prompt, respuesta, consultas a archivos y web en orden, fuentes y resultado. Hay que comprobar que **las consultas preceden a las recomendaciones**.

| Grupo | Casos | Qué verifican |
| --- | --- | --- |
| Arranque y lenguaje | 1, 6, 11, 12, 13 | Lectura provisional sin formulario, preguntar el desarrollo cuando no consta, vocabulario que ventas pueda contestar, explicar un término sin glosario |
| Evidencia y límites | 2, 3, 5, 14 | Concentrar el diagnóstico donde apunta el embudo, declarar límites concretos, ofrecer alternativas cuando el dato no existe, no inventar cifras |
| Documentos y organización | 7, 8, 9, 10, 15, 16 | Usar la ficha antes de preguntar, encontrar documentos fuera del índice, no duplicar estructura existente, no fabricar enlaces |
| Aislamiento del desarrollo | 17, 21 | No completar datos con los de otro desarrollo; pedir la ubicación cuando es ambigua |
| Investigación de mercado | 18, 19, 20, 22, 25, 26, 27 | Investigar antes de recomendar, anunciar el alcance, reutilizar sin repetir, juzgar fecha y alcance de la evidencia, abrir la fuente, reportar cobertura y vacíos |
| Validación con el equipo | 23, 24 | Esperar respuesta cuando el supuesto es determinante; recomendar en el mismo turno cuando solo refuerza lo conocido |
| Continuidad | 4 | Conservar restricciones y no repetir preguntas resueltas |

---

## 9. Límites explícitos

El plugin **no**:

- ejecuta campañas, publica piezas ni administra cuentas;
- se conecta automáticamente a plataformas de anuncios o CRM;
- incluye credenciales ni instala conectores;
- almacena datos comerciales en el repositorio;
- sustituye la decisión del equipo;
- afirma que existen campañas publicadas, integraciones u otras skills que no estén disponibles;
- cubre planeación, implementación con agencias ni validación de resultados — ese es el alcance de la propuesta CB2.

---

## 10. Historial de versiones

| Versión | Commit | Fecha | Cambio |
| --- | --- | --- | --- |
| 0.1.0 | `113ff4e` | 2026-09-13 | Piloto inicial y catálogo de plugins extensible |
| 0.2.0 | `e8d7323` | 2026-09-14 | Diagnóstico sin índice previo |
| 0.2.1 | `1c5ff24` | 2026-09-16 | Conversation starter más claro para usuarios nuevos |
| 0.2.2 | `1861ebb` | 2026-09-16 | Lenguaje claro e identificación explícita del desarrollo |
| 0.2.3 | `e770098` | 2026-09-27 | Investigación de mercado obligatoria antes de recomendar; cuatro frentes; validación de hallazgos determinantes con el equipo |
| 0.2.4 | `80e72cd` | 2026-09-27 | Anuncio del alcance antes de buscar; profundidad exigida por frente (fuente abierta, fechada, preferentemente independiente); reporte de cobertura y vacíos al entregar |

---

## 11. Pendientes conocidos

Material que el plugin no cubre hoy y que vale la pena considerar:

- **Trabajo con agencias.** No hay plantilla de brief ni checklist de revisión de entregables. NPV trabaja con agencias y la propuesta CB2 sí los incluye.
- **Criterios para elegir canal.** Hoy no están explicitados.
- **Cálculo inverso de objetivos** (unidades → visitas → citas → leads → presupuesto).
- **Arquitectura de información entre desarrollos.** La separación entre lo que es de NPV como empresa y lo que es de cada desarrollo está menos resuelta que en la propuesta CB2.
- **Manejo de datos personales en conversación.** El repositorio lo prohíbe en pruebas, pero la skill no da guía sobre qué hacer cuando el equipo comparte un registro de leads con datos reales.
