# Ejecución y credenciales del prototipo

Resolver las rutas contra la carpeta instalada de `npv-data`. Los ejemplos se ejecutan desde esa carpeta. Instalar dependencias en el entorno de trabajo antes de ejecutar:

```bash
python -m pip install -r scripts/requirements.txt
```

## Destino local

Elegir un archivo fuera del repositorio, por ejemplo `/tmp/npv-demo.duckdb`. Este destino sirve para pruebas y no garantiza almacenamiento durable al terminar el entorno temporal. Para persistencia compartida usar una base MotherDuck configurada.

```bash
python scripts/npv_data.py --database /tmp/npv-demo.duckdb init
python scripts/npv_data.py --database /tmp/npv-demo.duckdb fetch-banxico --series SF43718 --latest
python scripts/npv_data.py --database /tmp/npv-demo.duckdb show-series --indicator banxico:SF43718 --geography MX
```

Configurar `BANXICO_TOKEN` una vez mediante los secretos del entorno. No pegarlo en la conversación, incluirlo en argumentos ni imprimir variables. El adaptador lo envía solo en `Bmx-Token` al host oficial; rechaza redirecciones. Necesita acceso HTTPS a `www.banxico.org.mx`. Un secreto de red del entorno puede sustituir un marcador al llamar al dominio autorizado; comprobarlo con una consulta real sin imprimir el valor. No asumir que un secreto de Codex Cloud se suministra a cualquier chat.

Para un rango explícito, sustituir `--latest` por `--start 2026-09-01 --end 2026-09-30`. Catálogo permitido: SF43718, SF61745, SF60633. Tres intentos como máximo para HTTP 429/5xx seleccionados; timeout de 20 segundos y límite de respuesta de 8 MiB. No hay descarga programada.

## CSV y reportes

Registrar fuente y luego cargar el [CSV normalizado](modelo.md). No etiquetar datos ficticios ni una extracción manual como descarga API oficial.

```bash
python scripts/npv_data.py --database /tmp/npv-demo.duckdb register-source --id demo --name 'Ejemplo ficticio' --url https://example.com/ --category demo
python scripts/npv_data.py --database /tmp/npv-demo.duckdb import-csv --source-id demo --file /tmp/demo.csv --retrieved-at 2026-10-10T12:00:00Z
python scripts/npv_data.py --database /tmp/npv-demo.duckdb show-series --indicator demo:ventas --geography project:demo
python scripts/npv_data.py --database /tmp/npv-demo.duckdb show-series --indicator demo:ventas --geography project:demo --history
```

Antes de registrar un documento, guardar el original con las capacidades del repositorio autorizado y obtener su ubicación durable. Si no se pudo guardar, explicar el límite; registrar metadatos no resuelve ese faltante. No modificar adjuntos originales por rutina.

```bash
python scripts/npv_data.py --database /tmp/npv-demo.duckdb register-document --source-id demo --file /tmp/reporte.pdf --title 'Reporte ficticio' --original-locator https://example.com/reporte.pdf --published-on 2026-09-30
python scripts/npv_data.py --database /tmp/npv-demo.duckdb list-documents
```

El comando calcula SHA-256, registra metadatos y confirma `original_uploaded: false`. Repetir contenido de una fuente devuelve el mismo ID; una nueva versión recibe otro ID. Para enlazarla, indicar `--supersedes <id_anterior>` de la misma fuente. La extracción y lectura de contenido usa herramientas de documentos, no esta CLI.

## MotherDuck

Crear/elegir una base autorizada (por ejemplo `npv_pilot`) y configurar `motherduck_token` en el entorno; el cliente DuckDB lo obtiene de esa variable. Reemplazar el destino local por `--database md:npv_pilot` en los mismos comandos. No poner el token en el URI. La extensión MotherDuck necesita red y permisos de la cuenta. La variable debe estar disponible para el cliente; los secretos de red con proxy requieren una comprobación específica y no se presuponen compatibles con este cliente.

La ruta remota está implementada, pero requiere prueba real del cliente, versión, permisos y esquema con la cuenta elegida. Las consultas de la CLI usan SELECT; los permisos remotos efectivos los impone MotherDuck. Un archivo local comprobado entre procesos no demuestra conexión cloud ni disponibilidad desde otra cuenta.

El plugin MotherDuck puede consultar la misma base mediante su conexión independiente. La autenticación del plugin y la del script son rutas distintas: conectar el plugin no entrega su token a los scripts. Data de OpenAI es opcional para análisis; no almacena estas credenciales.

Para el equipo, la siguiente versión puede alojar los adaptadores en un servidor MCP con secretos del servidor. Esta v1 no despliega ese servicio ni instala conexiones automáticamente.

Referencias: [secretos de Codex Cloud](https://learn.chatgpt.com/docs/environments/cloud-environments), [cliente DuckDB Python](https://duckdb.org/docs/current/clients/python/dbapi), [conexión MotherDuck](https://motherduck.com/duckdb-book-summary-chapter7/).
