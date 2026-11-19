# Instalación y uso de los plugins NPV

Prueba desde la fuente **Business Bots** en ChatGPT de escritorio, en modo Trabajo. Usa conversaciones nuevas y datos ficticios.

| Configuración | Prueba | Se espera |
| --- | --- | --- |
| Solo NPV Datos | Selecciona `@NPV Datos` y pide comparar dos periodos de una tabla adjunta. | El menú ofrece el plugin NPV Datos, cuya skill se llama Inteligencia de Mercado. La respuesta cita cifras, periodos y fuente. |
| Solo NPV Marketing | Selecciona `@NPV Marketing` y pide revisar un brief ficticio. | El menú ofrece el plugin NPV Marketing, cuya skill se llama Estrategia de Marketing. La respuesta aplica su flujo de marketing. |
| Solo uno de los dos | Pide una tarea que corresponda al otro plugin. | El menú omite el plugin sin instalar y el asistente ofrece un traspaso que el usuario puede retomar. |
| Ambos | Selecciona cada plugin por separado, luego pasa el resumen de una alternativa elegida en Datos a Marketing. | Aparecen dos nombres en el menú y Marketing puede aprovechar el resumen como entrada a su propia etapa. |
| Actualización desde 0.7.0 | Reinstala `npv-marketing` usando la misma fuente. | El plugin anterior se actualiza a NPV Marketing. NPV Datos se instala por separado. |
