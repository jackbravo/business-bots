# Persistencia y vigencia

| Información | Conservar | Actualizar para una consulta |
| --- | --- | --- |
| Indicadores oficiales | Historial, definición, geografía y revisiones | Si pide actualidad, consultar último dato publicado; si pide historia, reutilizar cobertura pertinente. |
| Tipo de cambio y tasas | Históricos más controles de consulta | Verificar último publicado para preguntas actuales, indicando fecha y referencia; no equiparar FIX a cotización comercial. |
| Datos internos | Originales y cortes de inventario, precios, ventas y costos | Incorporar nuevas versiones recibidas; no llamar vigente a un archivo antiguo sin comprobar. |
| Competencia | Evidencia con fecha, ubicación y características comparables | Revisar oferta en decisiones que dependan de su estado actual. |
| Reportes y proyecciones publicadas | Original por versión, publicación, periodo y ubicación | Buscar edición pertinente; distinguir proyección de resultado observado. |
| Noticias/contexto local | Evidencia utilizada, fuente y fecha | Consultar según pregunta; no construir un archivo de noticias indiscriminado. |
| Análisis | Fuentes, corte y cálculos reproducibles cuando sean reutilizables | Recalcular si cambian insumos o definiciones. No guardar inferencias como cifras oficiales. |

## Reglas

Conservar originales en el repositorio autorizado (Drive u otro); SQL conserva datos estructurados y referencias, no reemplaza ese repositorio. La base pertenece a NPV; las credenciales viven en secretos del entorno o del servidor. GitHub conserva metodología, scripts, esquema y ejemplos ficticios.

Distinguir periodo observado, publicación del reporte, recuperación de la fuente y carga. Registrar fecha de publicación cuando la fuente la proporcione; nunca sustituirla por fecha de descarga. La v1 registra publicación en documentos; para series API puede ser desconocida y no debe inventarse.

Conservar correcciones como nuevas revisiones. Una segunda consulta idéntica actualiza el último control sin duplicar observaciones; cada carga deja registro. Una carga manual anterior al último control de un periodo se rechaza para evitar regresiones. Reversiones auténticas generan otra revisión aunque el valor haya existido antes.

Las proyecciones publicadas permanecen en documentos en v1: no ingresarlas como series observadas. El modelo de pronósticos con fecha de emisión y horizonte queda pendiente. No convertir silenciosamente MXN/USD a USD/MXN, porcentajes a fracciones ni periodos trimestrales a mensuales.

Si una actualización falla, conservar la versión anterior y explicar su corte. No responder «actual» usando un dato anterior sin indicar el límite. Una actualización solicitada no es un permiso para programar tareas recurrentes.

## Entrega al marketing skill

Entregar: indicador o documento, valor/resultado, unidad, geografía/desarrollo, periodo, fuente, fecha del último control y límites de comparabilidad. Mantener las decisiones de campaña en la Ficha del desarrollo. No transferir datos privados de otros desarrollos como contexto por defecto.
