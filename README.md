# Business Bots

Repositorio de plugins y skills para asistentes de trabajo.

## Catálogo

| Plugin | Versión | Contenido |
| --- | --- | --- |
| [NPV Marketing y Datos](plugins/npv-marketing/) | 0.4.0 | Marketing por etapas y prototipo de datos trazables. |

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

Usar un proyecto de ChatGPT por desarrollo y una conversación por etapa. El skill [npv-marketing](plugins/npv-marketing/skills/npv-marketing/SKILL.md) tiene un núcleo común, cuatro referencias de etapa y una [Ficha inicial propuesta](plugins/npv-marketing/skills/npv-marketing/assets/ficha-del-desarrollo.md). La plantilla oficial del proyecto, si existe, tiene prioridad.

Mantener en el proyecto:
- **Capa NPV:** marca, equipo, agencias, brokers, activos, proceso comercial y reglas comunes.
- **Ficha del desarrollo:** decisiones, estrategia, plan, resultados e hipótesis.
- **Documentos del desarrollo:** oferta, inventario, ventas, leads y reportes.

Se puede empezar sin Ficha ni carpeta, en cualquier etapa. Ejemplos: “Revisa este brief”, “Planeemos canales y presupuesto” o “Las consultas no se convierten en visitas; ¿qué comprobamos?”.

El bot pregunta solo por vacíos relevantes, investiga fuentes públicas pertinentes y pide visto bueno al entregar cada subetapa. Al cerrar una etapa genera la Ficha completa con fecha y versión; el director reemplaza el archivo del proyecto. La memoria ayuda, pero la Ficha es el contexto principal.

Los archivos pueden estar en el proyecto, adjuntos o repositorios compartidos como Drive o Dropbox. Su acceso depende de las herramientas disponibles; el plugin no instala conectores ni credenciales. Tampoco ejecuta campañas ni administra cuentas.

## Datos NPV (prototipo 0.4.0)

El segundo skill, [npv-data](plugins/npv-marketing/skills/npv-data/SKILL.md), obtiene y usa evidencia con fuentes, periodos y revisiones. Incluye una CLI para DuckDB local o un destino MotherDuck configurado: descarga FIX, tasa objetivo y CETES de Banxico, importa CSV normalizados, registra metadatos de reportes y consulta series.

Consultar [ejecución y credenciales](plugins/npv-marketing/skills/npv-data/references/ejecucion.md) antes de usarlo. Los tokens se configuran en el entorno; nunca en el chat, el repositorio ni la base. El registro documental no sube ni indexa originales: conservarlos en el repositorio autorizado y leerlos con las herramientas de archivos.

La ruta MotherDuck requiere conexión, permisos y prueba real. Los adaptadores INEGI/CANADEVI y el servidor MCP propio quedan pendientes. Data de OpenAI y el plugin MotherDuck pueden complementar el skill cuando estén disponibles; no son dependencias instaladas automáticamente.

Ejemplos: “¿Qué fuentes necesitamos para comparar nuestro proyecto con la competencia?”, “Incorpora este reporte y conserva su fuente y fecha” o “Consulta el último FIX publicado y compáralo con el mes anterior”. Con información parcial, el skill pregunta solo por vacíos relevantes y distingue información cargada de nuevas consultas externas.

## Desarrollo

```bash
python3 scripts/validate.py
python3 -m pip install -r plugins/npv-marketing/skills/npv-data/scripts/requirements.txt
python3 -m unittest discover -s tests -p 'test_*.py'
```

Probar los casos de [marketing](tests/behavior/npv-marketing.md) y [datos](tests/behavior/npv-data.md) en hilos nuevos. La validación estructural comprueba configuración y enlaces; no sustituye pruebas del comportamiento.

El repositorio conserva instalación y validación. La versión 0.3.0 reemplaza el skill de diagnóstico anterior: actualizar referencias explícitas de `npv-diagnostico-comercial` a `npv-marketing`. Reutilizar los documentos existentes como contexto; no reiniciar el trabajo comercial.

Mantener aquí metodología y plantillas reutilizables. Los datos comerciales, Capa NPV y Fichas reales pertenecen a los proyectos, no a este repositorio.

La versión 0.3.1 integra el repertorio de preguntas NPV en las cuatro referencias: brief, revisión de agencia, selección de canales y cálculo inverso de objetivos. No requiere cargar un archivo adicional de “Marcos y preguntas” en cada proyecto.

La versión 0.3.2 refuerza validación e investigación antes de recomendaciones estratégicas: ubicación, competencia, entorno y tendencias. Mantiene el trabajo provisional con datos parciales y evita elegir mensajes o posicionamiento antes de aclarar supuestos determinantes.
