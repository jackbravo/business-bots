# Business Bots

Repositorio de plugins y skills para asistentes de trabajo. Cada plugin agrupa una o más skills y se mantiene en su propia carpeta.

## Catálogo

| Plugin | Versión | Contenido |
| --- | --- | --- |
| [NPV Marketing](plugins/npv-marketing/) | 0.2.1 | Arranque y diagnóstico comercial inmobiliario, con evidencia y preguntas mínimas. |

El catálogo instalable está en `.agents/plugins/marketplace.json`; sus rutas se resuelven desde la raíz del repositorio. Cada plugin declara sus componentes en `.codex-plugin/plugin.json` y contiene sus skills en `skills/<nombre>/`.

## Instalar

Clona el repositorio y registra el marketplace local:

```bash
git clone https://github.com/jackbravo/business-bots.git
cd business-bots
bash scripts/install.sh npv-marketing
```

Abre un hilo nuevo de Codex después de instalar. Para traer cambios posteriores y reinstalar:

```bash
git pull --ff-only
bash scripts/install.sh --update npv-marketing
```

Consulta [CONTRIBUTING.md](CONTRIBUTING.md) para el ciclo de ramas, validación, cachebusters locales y pruebas.

## NPV Marketing

El piloto incluye una skill, una plantilla de inicio del desarrollo y dos referencias: criterios de diagnóstico y manejo de fuentes/continuidad. La metodología es reutilizable entre desarrollos; los índices, inventarios, precios, leads y documentos comerciales se mantienen en Google Drive y se proporcionan desde el proyecto de trabajo.

La conexión de Google Drive se configura por separado. Este repositorio no incluye credenciales ni instala automáticamente conectores. Tampoco conecta campañas o CRM automáticamente.

Para empezar, compartir el índice si existe, archivos sueltos, enlaces o una explicación del problema y pedir: “Inicia con lo que tenemos y ayúdame a organizarlo”. La skill puede proponer un documento de inicio y completarlo con lo conocido; organizar o llenar todos sus campos no es requisito para diagnosticar.

## Añadir más capacidades

- Para ampliar un plugin, añadir una carpeta en `plugins/<plugin>/skills/` con su `SKILL.md` y solo los recursos que necesite.
- Para una solución independiente, añadir otro plugin en `plugins/<nombre>/` y registrarlo en el catálogo con una ruta relativa.
- Mantener los nombres de carpetas y manifiestos consistentes. Usar versiones semánticas y actualizar este catálogo al cambiar una versión.
- Validar el manifiesto, el frontmatter de cada skill y los enlaces relativos antes de publicar cambios.
- Probar cambios de comportamiento con casos representativos y sin datos personales de clientes.

## Alcance de esta publicación

La versión 0.2.0 añade arranque sin índice y organización documental gradual. Publicar aquí no equivale a instalar el plugin en un workspace; la instalación y su prueba se realizan por separado en el entorno de destino.
