# Modelo v1

Usar el [esquema SQL](../assets/schema-v1.sql) bajo el namespace `npv` en una base autorizada. `init` crea la v1 sin borrar tablas; rechaza versiones distintas. Cambios futuros requieren migraciones explícitas y respaldo, no recrear la base.

| Tabla/vista | Grano y uso |
| --- | --- |
| `sources` | Una fuente identificada; nombre, URL y categoría. Metadatos inmutables en v1. |
| `indicators` | Una definición por fuente/serie; unidad y frecuencia fijas. ID compuesto `fuente:serie`. |
| `observations` | Un valor o ausencia por indicador/geografía/periodo/revisión. Conservar revisiones. |
| `current_observations` | Última revisión de cada periodo; incluye controles de recuperación. |
| `ingestion_runs` | Una carga exitosa; hash del contenido, recuperación, carga, filas y revisiones nuevas. |
| `documents` | Un contenido por fuente y hash; publicación opcional, ubicación y versión anterior. |
| `schema_versions` | Versiones aplicadas; v1 inicial. |

Las cargas de observaciones son atómicas: fallo de validación revierte la carga completa. Los errores se informan al solicitante; la v1 no tiene registro persistente de intentos fallidos. Los hashes identifican contenido; no sirven para recuperar un archivo ni prueban que se haya archivado.

Campos `first_retrieved_at` y `last_checked_at` describen cuándo se vio/controló una revisión. `ingestion_runs.retrieved_at` conserva la fecha de la carga que creó esa revisión; para vigencia mostrar `last_checked_at`. `loaded_at` representa la ejecución, no el periodo observado.

Las series internas se limitan a agregados en v1. Separar fuentes por dataset y geografía por cobertura; usar un código explícito `project:<id>` para agregados de un desarrollo. No mezclar compradores identificables ni inventarios por unidad en una sola serie genérica. Tablas operativas, relación de proyectos y capturas de competidores se diseñarán con muestras reales anonimizadas.

## CSV normalizado

Usar exactamente estas columnas (el orden es libre):

```csv
series_id,series_name,unit,frequency,geography,period,value
ventas,Ventas netas,unidades,monthly,project:demo,2026-08,2
ventas,Ventas netas,unidades,monthly,project:demo,2026-09,3
```

Ejemplo ficticio; no representa un desarrollo NPV. Frecuencias: `daily` (YYYY-MM-DD), `monthly` (YYYY-MM), `quarterly` (YYYY-Q1 a YYYY-Q4), `annual` (YYYY). Usar punto decimal sin separador de miles; vacío, N/E, N/D, ND y N/A representan ausencia, nunca cero. Decimales: hasta 18 dígitos enteros y 10 decimales. La fecha de recuperación se suministra en la carga; no inferir actualidad del nombre del archivo.

No combinar definiciones distintas bajo el mismo ID. Para otra unidad o metodología, registrar otra serie y explicar la relación. Revisar cobertura, faltantes, duplicados y totales antes del análisis; una carga exitosa valida forma y consistencia, no exactitud comercial.

## Consulta SQL de lectura

```sql
SELECT o.period, o.value, i.unit, o.last_checked_at, s.url
FROM npv.current_observations o
JOIN npv.indicators i USING (indicator_id)
JOIN npv.sources s USING (source_id)
WHERE o.indicator_id = 'banxico:SF43718' AND o.geography = 'MX'
ORDER BY o.period DESC;
```

Con MotherDuck, seleccionar la base NPV o calificar `base.npv.tabla`. Consultar primero las tablas reales y sus permisos. La CLI no presupone que el plugin MotherDuck esté conectado y no proporciona herramientas MCP propias.
