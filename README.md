# Business Bots

Repositorio de plugins y skills para asistentes de trabajo.

## Catálogo

| Plugin | Versión | Contenido |
| --- | --- | --- |
| [NPV Marketing y Datos](plugins/npv-marketing/) | 0.6.0 | Marketing por etapas y prototipo de datos trazables. |

## Instalar y actualizar

```bash
git clone https://github.com/jackbravo/business-bots.git
cd business-bots
bash scripts/install.sh npv-marketing
```

Para actualizar una instalación existente:

```bash
git pull --ff-only
bash scripts/install.sh --update npv-marketing
```

Consultar [CONTRIBUTING.md](CONTRIBUTING.md) para validación y pruebas. Publicar el código no instala el plugin en los entornos de los usuarios.

## NPV Marketing

Si se utiliza un proyecto de ChatGPT, dedicar uno a cada desarrollo. Trabajar una conversación por etapa. El skill [npv-marketing](plugins/npv-marketing/skills/npv-marketing/SKILL.md) tiene un núcleo común, cuatro referencias de etapa y una [Ficha inicial propuesta](plugins/npv-marketing/skills/npv-marketing/assets/ficha-del-desarrollo.md). La plantilla oficial del proyecto, si existe, tiene prioridad.

Mantener disponibles en la conversación o, si se usa, en el proyecto:
- **Capa NPV:** base compartida (identidad, valores, estructura, no negociables) más el módulo de cada asistente: Analista de Mercado para `npv-data` y Estratega para `npv-marketing` (cliente, proceso comercial, brokers y decisiones). Puede sumar equipo, agencias y activos.
- **Ficha del desarrollo:** decisiones, estrategia, plan, resultados e hipótesis.
- **Documentos del desarrollo:** oferta, inventario, ventas, leads y reportes.

La Capa NPV (base y módulo pertinente) puede compartirse como texto o adjuntos directamente en la conversación, subirse a los documentos de un proyecto de ChatGPT o consultarse desde un enlace accesible de Dropbox, Drive u otro repositorio. No se exige proyecto, carpeta ni proveedor concreto, ni pegar un bloque adicional de instrucciones. Si no se puede leer un enlace, el bot explica el límite y pide solo el contenido necesario. Los documentos internos permanecen fuera del repositorio.

Se puede empezar sin Ficha ni carpeta, en cualquier etapa. Ejemplos: “Revisa este brief”, “Planeemos canales y presupuesto” o “Las consultas no se convierten en visitas; ¿qué comprobamos?”.

El bot pregunta solo por vacíos relevantes, investiga fuentes públicas pertinentes y pide visto bueno al entregar cada subetapa. Al cerrar una etapa genera la Ficha completa con fecha y versión; el director reemplaza el archivo del proyecto. La memoria ayuda, pero la Ficha es el contexto principal.

Los archivos pueden estar en el proyecto, adjuntos o repositorios compartidos como Drive o Dropbox. Su acceso depende de las herramientas disponibles; el plugin no instala conectores ni credenciales. Tampoco ejecuta campañas ni administra cuentas.

## Datos NPV (prototipo 0.6.0)

El segundo skill, [npv-data](plugins/npv-marketing/skills/npv-data/SKILL.md), obtiene y usa evidencia con fuentes, periodos y revisiones. Prioriza las tablas que el cliente proporcione en Drive, Dropbox o archivos adjuntos, respetando su estructura y los permisos disponibles. Para trabajo interno incluye una CLI SQLite local sin dependencias externas: descarga FIX, tasa objetivo y CETES de Banxico, importa CSV normalizados, registra metadatos de reportes y consulta series.

Consultar [ejecución y credenciales](plugins/npv-marketing/skills/npv-data/references/ejecucion.md) antes de usarlo. Los tokens se configuran en el entorno; nunca en el chat, el repositorio ni la base. El registro documental no sube ni indexa originales: conservarlos en el repositorio autorizado y leerlos con las herramientas de archivos.

Un enlace de lectura no permite editar el original: sin escritura se entrega una copia o una tabla para incorporar. SQLite no sincroniza archivos ni garantiza persistencia entre conversaciones; conservar el archivo o una exportación en un destino durable autorizado. Los adaptadores INEGI/CANADEVI quedan pendientes. Data de OpenAI puede complementar el skill cuando esté disponible; no es una dependencia instalada automáticamente.

NPV aporta contexto y fuentes; Data de OpenAI, cuando está disponible, aporta análisis, validación y presentación; NPV Marketing convierte los hallazgos en recomendaciones comerciales. La colaboración ocurre mediante las capacidades disponibles en la conversación y no requiere una conexión entre plugins. Sin Data, el trabajo continúa con las herramientas disponibles.

Ejemplos: “¿Qué fuentes necesitamos para comparar nuestro proyecto con la competencia?”, “Incorpora este reporte y conserva su fuente y fecha” o “Consulta el último FIX publicado y compáralo con el mes anterior”. Con información parcial, el skill pregunta solo por vacíos relevantes y distingue información cargada de nuevas consultas externas.

## Investigación preliminar de terrenos

Antes de definir un desarrollo, `npv-data` puede investigar oferta publicada, demanda potencial, agua, uso de suelo y geografía/riesgos siguiendo la [guía de terrenos](plugins/npv-marketing/skills/npv-data/references/investigacion-terrenos.md). Para Jalisco incluye puntos de entrada de IIEG/INEGI, CONAGUA, municipios y CENAPRED. La evaluación utiliza la base de la Capa NPV y los criterios del Analista cuando se aportan, sin inventar umbrales ni divulgar información interna en entregas para terceros. Entrega evidencia fechada, comparables, condicionantes y una evaluación con verificaciones prioritarias; no equivale a un dictamen ni acredita viabilidad por sí sola.

Ejemplo: “Investiga este terreno [ubicación o polígono]. Revisa oferta cercana, estadísticas de demanda potencial, agua, uso de suelo y riesgos publicados. Comparte los datos duros, sus fuentes y tu evaluación”. No hace falta contar ya con campaña, producto ni Ficha. Los cruces cartográficos y el acceso a portales dependen de las herramientas y datos disponibles; no se añaden adaptadores ni un motor GIS.

## Desarrollo

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

Probar los casos de [marketing](tests/behavior/npv-marketing.md) y [datos](tests/behavior/npv-data.md) en hilos nuevos. La validación estructural comprueba configuración y enlaces; no sustituye pruebas del comportamiento.

El repositorio conserva instalación y validación. La versión 0.3.0 reemplaza el skill de diagnóstico anterior: actualizar referencias explícitas de `npv-diagnostico-comercial` a `npv-marketing`. Reutilizar los documentos existentes como contexto; no reiniciar el trabajo comercial.

Mantener aquí metodología y plantillas reutilizables. Los datos comerciales, Capa NPV y Fichas reales pertenecen a los proyectos, no a este repositorio.

La versión 0.3.1 integra el repertorio de preguntas NPV en las cuatro referencias: brief, revisión de agencia, selección de canales y cálculo inverso de objetivos. No requiere cargar un archivo adicional de “Marcos y preguntas” en cada proyecto.

La versión 0.3.2 refuerza validación e investigación antes de recomendaciones estratégicas: ubicación, competencia, entorno y tendencias. Mantiene el trabajo provisional con datos parciales y evita elegir mensajes o posicionamiento antes de aclarar supuestos determinantes.

La versión 0.5.1 adopta la Capa NPV como base compartida más un módulo por asistente: `npv-marketing` usa el del Estratega y trata comisiones, estructura e inversionistas como contexto confidencial; `npv-data` usa los criterios del Analista sin convertirlos en umbrales numéricos.
