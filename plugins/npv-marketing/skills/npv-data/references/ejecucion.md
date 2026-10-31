# Ejecución y credenciales del prototipo

Resolver las rutas contra la carpeta instalada de `npv-data`. Los ejemplos se ejecutan desde esa carpeta. La CLI requiere Python 3.10 o posterior con `sqlite3`; no necesita paquetes externos. Las herramientas conectadas pueden trabajar con las tablas del cliente sin ejecutar la CLI.

## Destino local

Elegir un archivo fuera del repositorio, por ejemplo `/tmp/npv-demo.sqlite`. Este destino sirve para pruebas y no garantiza almacenamiento durable al terminar el entorno temporal. Para conservar los datos, guardar el archivo o una exportación en un destino durable autorizado. No tratar la ruta temporal como memoria compartida entre conversaciones.

```bash
python scripts/npv_data.py --database /tmp/npv-demo.sqlite init
python scripts/npv_data.py --database /tmp/npv-demo.sqlite fetch-banxico --series SF43718 --latest
python scripts/npv_data.py --database /tmp/npv-demo.sqlite show-series --indicator banxico:SF43718 --geography MX
```

Configurar `BANXICO_TOKEN` una vez mediante los secretos del entorno. No pegarlo en la conversación, incluirlo en argumentos ni imprimir variables. El adaptador lo envía solo en `Bmx-Token` al host oficial; rechaza redirecciones. Necesita acceso HTTPS a `www.banxico.org.mx`. Un secreto de red del entorno puede sustituir un marcador al llamar al dominio autorizado; comprobarlo con una consulta real sin imprimir el valor. No asumir que un secreto de Codex Cloud se suministra a cualquier chat.

Para un rango explícito, sustituir `--latest` por `--start 2026-09-01 --end 2026-09-30`. Catálogo permitido: SF43718, SF61745, SF60633. Tres intentos como máximo para HTTP 429/5xx seleccionados; timeout de 20 segundos y límite de respuesta de 8 MiB. No hay descarga programada.

## CSV y reportes

Registrar fuente y luego cargar el [CSV normalizado](modelo.md). No etiquetar datos ficticios ni una extracción manual como descarga API oficial.

```bash
python scripts/npv_data.py --database /tmp/npv-demo.sqlite register-source --id demo --name 'Ejemplo ficticio' --url https://example.com/ --category demo
python scripts/npv_data.py --database /tmp/npv-demo.sqlite import-csv --source-id demo --file /tmp/demo.csv --retrieved-at 2026-10-10T12:00:00Z
python scripts/npv_data.py --database /tmp/npv-demo.sqlite show-series --indicator demo:ventas --geography project:demo
python scripts/npv_data.py --database /tmp/npv-demo.sqlite show-series --indicator demo:ventas --geography project:demo --history
```

Antes de registrar un documento, guardar el original con las capacidades del repositorio autorizado y obtener su ubicación durable. Si no se pudo guardar, explicar el límite; registrar metadatos no resuelve ese faltante. No modificar adjuntos originales por rutina.

```bash
python scripts/npv_data.py --database /tmp/npv-demo.sqlite register-document --source-id demo --file /tmp/reporte.pdf --title 'Reporte ficticio' --original-locator https://example.com/reporte.pdf --published-on 2026-09-30
python scripts/npv_data.py --database /tmp/npv-demo.sqlite list-documents
```

El comando calcula SHA-256, registra metadatos y confirma `original_uploaded: false`. Repetir contenido de una fuente devuelve el mismo ID; una nueva versión recibe otro ID. Para enlazarla, indicar `--supersedes <id_anterior>` de la misma fuente. La extracción y lectura de contenido usa herramientas de documentos, no esta CLI.

## Tablas del cliente en Drive o Dropbox

1. Abrir el archivo o tabla indicada con el conector disponible y comprobar acceso. Leer las hojas y columnas relevantes antes de planear la escritura.
2. Mantener nombres, unidades, fórmulas y formato del cliente. Definir la clave de cada fila y el tratamiento de correcciones según esa tabla; no imponer el CSV normalizado de la CLI.
3. Guardar únicamente los cambios solicitados mediante las capacidades de escritura disponibles. En hojas nativas, usar rangos concretos; en archivos, conservar el original y generar una nueva versión según el destino autorizado.
4. Volver a leer las filas o el archivo actualizado para confirmar. Si solo hay enlace de lectura o no hay conector de escritura, entregar una copia actualizada o datos para incorporar y declarar que el original sigue sin modificar.

La CLI opera sobre archivos SQLite locales y CSV normalizados; no descarga enlaces de Drive/Dropbox ni sincroniza archivos. No abrir una hoja de cálculo o un CSV como si fuera SQLite. Preparar una copia de trabajo para el análisis cuando corresponda. No convertir ni migrar bases existentes automáticamente.

## Token de Banxico

Para usar la API, obtener el token desde https://www.banxico.org.mx/SieAPIRest/service/v1/ y abrir «Token de consulta», completar la imagen de seguridad y pulsar «Generar token». Si el enlace directo https://www.banxico.org.mx/SieAPIRest/service/v1/token muestra un error de formulario, volver a la página principal.

Configurar el valor como `BANXICO_TOKEN` en los secretos del entorno que ejecuta la descarga. Si ya existe, comprobar disponibilidad sin mostrar su valor; no pedir repetir la configuración. El skill no proporciona un servidor ni una interfaz de secretos propia. Si el entorno no admite configuración segura, consultar publicaciones oficiales con las herramientas disponibles o explicar que la API queda pendiente. Verificar una consulta real antes de afirmar conexión; conservar fuente, fecha y unidad.
