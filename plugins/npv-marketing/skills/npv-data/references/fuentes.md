# Fuentes para NPV

Elegir fuentes por la pregunta y cobertura disponible; no descargar todo por rutina. Verificar identificadores, unidades y metodología antes de agregar un indicador al catálogo. No confundir datos observados con proyecciones de un informe.

| Fuente | Información pertinente | Acceso del prototipo |
| --- | --- | --- |
| Banco de México | FIX, tasa objetivo, CETES; ampliar después a otras series pertinentes | Adaptador SIE API con token del entorno. |
| INEGI | Inflación, actividad, construcción, población, empleo y contexto por geografía | Web, documentos o CSV preparado con herramientas disponibles; adaptador pendiente. |
| CANADEVI | Reportes y tableros de vivienda por segmento y estado | Leer y registrar documentos; verificar el organismo que originó la estadística. |
| CONAVI/SNIIV, SHF, RUV | Oferta, financiamiento y precios de vivienda, según cobertura | Consultar publicación o descarga oficial pertinente; adaptadores pendientes. |
| Bancos, BMV y emisoras | Hipotecario, perspectivas y resultados del sector | Conservar versiones de reportes; no sustituir tasa comercial por TIIE. |
| Webs y portales de desarrollos | Oferta anunciada y características de comparables | Observaciones fechadas; no inferir cierres ni absorción de una sola captura. |
| Fuentes internas NPV | Inventario, precios, ventas, costos y benchmarks | Archivos autorizados; CSV normalizado para series agregadas. Modelo operativo detallado pendiente. |
| Prensa y fuentes locales | Eventos que puedan afectar demanda o ejecución | Consultar por pertinencia y contrastar; identificar noticias, testimonios e indicadores por separado. |

## Catálogo Banxico inicial

El [catálogo ejecutable](../assets/banxico-series.json) restringe el adaptador a:

| Serie | Significado | Unidad |
| --- | --- | --- |
| SF43718 | Tipo de cambio FIX | MXN por USD |
| SF61745 | Tasa objetivo | Porcentaje anual |
| SF60633 | CETES a 28 días | Porcentaje anual |

El endpoint `datos/oportuno` entrega el último dato publicado: no implica una cotización intradía ni un valor publicado hoy. Reportar la fecha de observación, incluso en fines de semana. Para compras en dólares, distinguir FIX, cotización bancaria y supuestos del escenario.

No fijar una serie TIIE sin verificar referencia, plazo y régimen aplicable. El documento de alcance menciona «CNIC»: confirmar con el equipo a qué organismo se refiere antes de crear un adaptador o sustituirlo por otra cámara.

## Referencias oficiales

- [SIE API Banxico: autenticación, catálogo y consultas](https://www.banxico.org.mx/SieAPIRest/service/v1/).
- [API de indicadores INEGI](https://www.inegi.org.mx/servicios/api_indicadores.html).
- [Información del sector CANADEVI](https://canadevi.com.mx/informacion-del-sector/).

Catálogo inicial comprobado el 2026-10-10; verificar nuevamente al extenderlo.
