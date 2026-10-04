# Revisión de CB2 · Especificación para construcción

**Documento revisado:** `CB2_Especificacion_construccion_NPV.pdf` (Especificación CB2 v1.0, 17 pp.)
**Contrastado contra:** plugin `npv-marketing` 0.2.4 — `SKILL.md`, `references/criterios-diagnostico.md`, `references/fuentes-y-continuidad.md`, `assets/inicio-del-desarrollo.md` y los 27 casos de `tests/behavior/npv-diagnostico-comercial.md`.
**Autor de la revisión:** Luis Aguirre
**Fecha:** 2 de octubre de 2026

---

## Resumen

El documento está bien hecho y es construible: la arquitectura de tres niveles (Capa NPV / Ficha / Documentos) resuelve limpio el problema de aislar desarrollos, y los anexos C, D, E, F y G son material operativo real, no relleno.

El problema no es la calidad del documento sino que **avanza por un carril distinto al plugin y no lo menciona ni una vez**, y que en el punto donde más trabajamos últimamente —disciplina de investigación y evidencia— es claramente más laxo que lo que ya tenemos probado.

**Orden sugerido para la conversación:** abrir con el punto 1 (arquitectura), porque condiciona todo lo demás; y poner el punto 4 (investigación de mercado) como la observación de contenido más importante, porque es donde el documento se queda corto frente a trabajo ya hecho y probado, y es barato de cerrar: el texto ya existe en el repo y solo hay que trasplantarlo.

---

## A. Lo que hay que decidir antes de construir

### 1. ¿CB2 reemplaza al plugin, convive con él, o es la especificación que el plugin debe implementar?

El doc asume ChatGPT Projects con instrucciones pegadas y archivos cargados a mano. El repo es un plugin de Codex con skills, referencias, versionado semántico, `install.sh`, `validate.py` y CI. Son dos modelos de distribución distintos.

Si los dos quedan vivos sin decir cuál manda, la misma metodología se bifurca en dos fuentes de verdad y en tres meses divergen. Esta es la pregunta que debería ir primero en la revisión.

Un síntoma concreto: §4.3 dice *"el Anexo A tiene cerca de 5,800 caracteres, hay que confirmar que la plataforma lo acepte completo; si lo recorta, mover VALIDACIÓN y FICHA DEL DESARROLLO al archivo de Marcos"*. Ese es exactamente el problema que el formato de skills ya resuelve por diseño (SKILL.md corto + referencias que se cargan cuando hacen falta). El doc está reinventando la carga progresiva a mano.

### 2. El versionado de la Capa NPV no tiene mecanismo

§3.1 y §4.3 dicen que el archivo se versiona "para detectar proyectos desactualizados". Pero cuando la Capa pase a v1.1, alguien tiene que entrar a los N proyectos y reemplazar el archivo.

La Ficha tiene el campo *"Versión de Capa NPV usada"* (bien), solo que el bot no puede compararlo contra nada: dentro de su proyecto no ve cuál es la versión vigente. En la práctica el campo detecta el desfase solo si un humano lo revisa.

**Falta:** nombrar responsable y procedimiento de actualización, o aceptar explícitamente que ese costo operativo existe.

### 3. Alcance de la v1.0

El plugin cubre arranque y diagnóstico, y lo cerramos así a propósito. CB2 cubre las cuatro etapas, incluida implementación con agencias. Es mucha superficie para una v1.0.

**Sugerencia:** construir por etapas. Etapa 1 y etapa 4 primero —son las que ya tienen disciplina de evidencia probada—, y dejar 2 y 3 —que son sobre todo plantillas— para una segunda entrega.

---

## B. Brechas sustantivas frente a lo que ya probamos

### 4. La investigación de mercado está muy por debajo de 0.2.4

**Esta es la observación más importante.**

El doc resuelve investigación con una línea: *"Investiga en internet lo que se puede saber de fuentes públicas y cita cada fuente con enlace"* (§3.3).

El plugin, después de tres commits de trabajo, exige:

- anunciar el alcance **antes** de buscar y qué pregunta resuelve cada frente (caso 25);
- cuatro frentes nombrados: ubicación, competencia, entorno socioeconómico, tendencias sociales del segmento;
- **abrir y leer la fuente**, no concluir desde el fragmento del buscador;
- dos fuentes independientes; si solo hay una, decirlo y tratarlo como señal, no como hecho (caso 26);
- registrar fecha de publicación, periodo del dato y alcance geográfico — un dato nacional no prueba una tendencia local;
- al entregar, **reportar qué frentes quedaron cubiertos, cuáles con evidencia débil y cuáles sin evidencia** (caso 27).

Nada de eso está en CB2. Los cuatro frentes aparecen dispersos en 1.3 y 1.4 del Anexo D, pero como sugerencias, nunca como requisito verificable.

Y la prueba de aceptación correspondiente —*"Afirmaciones de mercado → Indica nivel de sustento y cita fuente con enlace"* (§4.4)— la pasa un bot que pegó el snippet de Google sin abrir nada. Es justo el comportamiento que el caso 26 está diseñado para reprobar.

**Sugerencia concreta:** meter la tabla de cuatro frentes y el bloque *"Profundidad de un frente que puede cambiar la decisión"* de `criterios-diagnostico.md` como sección H del Anexo D, y agregar una prueba de aceptación de reporte de cobertura.

### 5. Falta el caso "sin acceso web"

El plugin es explícito: si no hay herramientas web o el usuario pide no usarlas, informar el límite, seguir con análisis provisional, y **no presentar recomendaciones como contrastadas ni inventar fuentes** (casos 19 A y B).

§4.3 solo dice "confirmar que la búsqueda esté disponible". Si no lo está, el doc no dice qué hace el bot.

### 6. Validar hallazgos determinantes ≠ pedir visto bueno

El doc pide confirmación al cerrar cada subetapa (§3.3, paso 4). Eso es aprobación de entregables.

Lo que trabajamos en el commit `363dca5` es otra cosa:

- cuando un supuesto **determinante** está sin confirmar, se contrasta y se **espera** antes de recomendar (caso 23);
- cuando el hallazgo solo refuerza lo ya sabido, se recomienda en el mismo turno sin ronda de aprobación (caso 24).

El "pide confirmación antes de avanzar" generalizado de CB2 produce el error opuesto —teatro de aprobación en cada subetapa— y con directores como únicos usuarios eso se desactiva solo, por fastidio.

### 7. Interpretación de métricas: riesgo de conclusiones falsas

La sección F (cálculo inverso) y la sección 13 de la Ficha trabajan con tasas y resultados por canal sin ninguna de las salvaguardas de `criterios-diagnostico.md`:

- distinguir citas agendadas de realizadas, y apartados de ventas;
- separar conversiones de una cohorte de leads de ventas registradas en un mes;
- considerar la maduración del ciclo inmobiliario antes de juzgar campañas recientes;
- **no atribuir una venta a un canal sin evidencia de atribución**.

El doc sí dice "si no hay tasas reales, usa supuestos explícitos y márcalos como hipótesis" —bien—, pero eso cubre la ausencia del dato, no el dato mal construido.

**Sugerencia:** importar completa la sección "Interpretar métricas".

### 8. Las tandas de preguntas van al revés

Tres menciones inconsistentes entre sí:

| Ubicación | Dice |
| --- | --- |
| §3.3 | "en tandas de 3 a 5 preguntas" |
| Anexo A | "Máximo 3 a 5 preguntas por turno" |
| §4.4 (prueba) | "Nunca más de 5 por turno" |

El plugin dice "normalmente de una a tres preguntas por turno".

Dos problemas: el piso de 3 contradice el propio *"pregunta solo lo que no sepas ya"*, y 5 preguntas seguidas a un director es demasiado.

**Sugerencia:** *hasta 3, solo las que desbloqueen la siguiente decisión*, y alinear las tres menciones.

### 9. El Anexo B es una barrera de entrada

Son ~35 preguntas que NPV debe contestar antes de que cualquier proyecto funcione. Todo el diseño del plugin apunta a lo contrario: arrancar con lo que haya y organizar después (casos 1, 6, 7, 11).

**Sugerencia:** marcar un subconjunto mínimo (8-10 preguntas: marca, quién aprueba, agencias, cuentas, proceso comercial, reglas de gasto) como necesario para la v1.0, y el resto como "se completa sobre la marcha".

### 10. Datos personales: no está tratado

El doc instruye cargar registro de leads, conversaciones y testimonios a un proyecto de ChatGPT compartido. El repo es explícito en lo contrario: `CONTRIBUTING.md` lo prohíbe y los casos de prueba exigen datos ficticios.

Para un documento clasificado como confidencial que va a ingeniería, falta un párrafo sobre anonimización y qué no se sube. Corto, pero debería estar.

### 11. Compradores extranjeros sin guardarraíl

El manejo del tema está bien y es pertinente para Ajijic/Chapala. Pero `criterios-diagnostico.md` prohíbe explícitamente inferir residencia por LADA y capacidad o motivación por nacionalidad, y el Anexo D segmenta bastante por "compradores extranjeros" sin esa línea.

Es una línea de texto. Vale la pena.

---

## C. Ajustes menores

- **§2, "la separación la garantiza la plataforma"** — "garantiza" es fuerte. Aísla archivos y memoria; no impide que el usuario pegue datos de otro desarrollo en el chat. El doc ya maneja ese caso; solo ajustaría la redacción.

- **Regenerar la Ficha completa en cada cierre de etapa** (§2 y Anexo C) — un LLM regenerando 15 secciones pierde contenido ya aprobado sin que se note, y no hay diff ni historial (la bitácora 12 registra cambios comerciales, no cambios de la Ficha). Pediría que cada versión encabece con "qué cambió respecto de la anterior". Compárese con `fuentes-y-continuidad.md`, que es más estricto: conservar identidad y enlace del documento en lugar de generar copias.

- **Tabla E (diagnóstico del embudo)** — le falta la columna que sí tiene el plugin, *"alternativa de bajo esfuerzo"*: qué hacer cuando el dato no existe. Y una línea que hoy falta: una misma señal puede tener varias causas, y que falte un dato no demuestra ninguna. Como está, la tabla se lee como síntoma → diagnóstico.

- **Aclaraciones y cálculos no disparan investigación** (caso 20) — la secuencia rígida de 4 pasos de §3.3 implica investigar en cada subetapa; falta la excepción.

- **Portada** — convendría que diga a qué versión de la metodología corresponde (0.2.4), si se espera que ambos documentos se mantengan alineados.

- **Nivel de sustento** (§3.5) — meter "testimonio del equipo" y "fuente pública confiable" juntos en Medio es una simplificación aceptable, pero pierde la distinción entre lo que dice el equipo y lo que está publicado y fechado. Mencionable, no bloqueante.

---

## D. Lo que me llevaría del CB2 de vuelta al plugin

Esto no es crítica al documento, es lo contrario: hay material ahí que al plugin le falta.

- **La arquitectura de tres niveles** (§3.1) — mejor que lo que tenemos hoy en `fuentes-y-continuidad.md`.
- **Anexo D, sección C (plantilla de brief para agencia)** y **sección D (checklist de revisión de entregables)** — el plugin no tiene nada para trabajo con agencia, y NPV sí trabaja así.
- **Anexo D, sección G (criterios para elegir canales)** — en particular *"ningún canal se elige solo porque ya se usa"*.
- **Anexo D, sección F (cálculo inverso de objetivos)**.
- **Proceso comercial con el mismo peso que la campaña** (§3.6 de etapas, VALIDACIÓN del Anexo A) — el plugin lo tiene en los criterios, pero no tan explícito.

---

## Referencias cruzadas rápidas

| Tema | CB2 | Plugin 0.2.4 |
| --- | --- | --- |
| Investigación de mercado | §3.3 paso 3 | `SKILL.md` "Investigar antes de recomendar"; `criterios-diagnostico.md` tabla de frentes; casos 18, 25, 26, 27 |
| Sin acceso web | — | `SKILL.md` cierre de la misma sección; caso 19 |
| Validación de hallazgos | §3.3 paso 4 | `SKILL.md` "Entregar y continuar"; casos 23 y 24 |
| Interpretación de métricas | Anexo D sección F | `criterios-diagnostico.md` "Interpretar métricas" |
| Preguntas por turno | §3.3, Anexo A, §4.4 | `SKILL.md` "Empezar con contexto, no con un formulario" |
| Arranque sin documentación | §4.4, Anexo D sección A | casos 1, 6, 7, 11 |
| Datos personales | — | `CONTRIBUTING.md`; encabezado de `tests/behavior/` |
| Segmentación por nacionalidad | Anexo D 1.2, 1.4 | `criterios-diagnostico.md` "Evaluar segmentos y producto" |
