# Casos de comportamiento NPV Marketing

Ejecutar en hilos nuevos con el plugin candidato. Usar datos ficticios y una ubicación real solo cuando se necesite investigación pública. Registrar versión, prompt, respuesta, archivos y fuentes consultados, y resultado: pasa / falla / no ejecutado. La validación estructural no demuestra estos comportamientos.

| Caso | Entrada | Se espera |
| --- | --- | --- |
| 1. Inicio sin documentos | “Queremos mejorar las ventas; no tenemos Ficha ni carpeta”. | Pregunta desarrollo y problema decisivo; propone 1.1 y solicita materiales disponibles sin exigir completitud, carpeta ni índice. |
| 2. Contexto disponible | Ficha con ubicación, oferta y avance; “¿Por dónde seguimos?”. | Lee antes de preguntar, resume hasta tres líneas y pregunta foco y campaña activa sin repetir datos. |
| 3. Entrada a mitad | Ficha vacía; “Revisa este brief para la agencia”. | Entra en 3.1 o 3.2 y recaba solo contexto necesario, sin forzar diagnóstico completo. |
| 4. Campaña activa | “Estamos definiendo segmentos, pero esta campaña ya corre y recibe consultas sin citas”. | Propone comprobaciones puntuales de calidad y atención mientras continúa diseño; no exige completar otras etapas. |
| 5. Documentación parcial | Brochure viejo y notas: “Preguntan por enganche y dejan de responder”. | Separa testimonio e hipótesis, registra vigencia y faltantes, pregunta hasta cinco cosas decisivas y avanza provisionalmente. |
| 6. Selección de etapa | Pedir por separado segmentos, mezcla de canales, revisión de pieza y lectura de resultados. | Usa la referencia pertinente y entrega el resultado correspondiente, sin recorrer todas las subetapas por rutina. |
| 7. Investigación | Pedir comparación competitiva con ubicación conocida; luego calcular 2 ventas / 20 visitas. | Investiga fuentes públicas pertinentes, cita enlaces y periodos; responde 10% al cálculo sin repetir investigación innecesaria. |
| 8. Acceso limitado | Enlace inaccesible o instrucción de no usar internet. | Declara el límite concreto, respeta la instrucción y continúa sin fingir lectura ni fabricar fuentes. |
| 9. Sustento y embudo | Reporte propio incompleto con pocos leads y menor inversión. | No asigna alto por origen solamente ni atribuye automáticamente el problema a alcance o segmento. |
| 10. Métricas | Citas agendadas y realizadas mezcladas, ventas de otro periodo y denominador cero. | Distingue estados y cohortes, solicita aclaración decisiva y marca lo no calculable. |
| 11. Visto bueno | Entrega de 2.2; el director responde con un ajuste sin aprobar. | Revisa la propuesta, no marca aprobación ni avanza a 2.3. Tras aprobación explícita puede avanzar. |
| 12. Cierre con historial | Ficha con decisiones previas e hipótesis; aprobar cierre de etapa con datos nuevos. | Genera Ficha completa, conserva secciones, actualiza 0 y 14, fecha y versión; pide reemplazar archivo y recomienda nueva conversación para otra etapa. |
| 13. Contradicciones | Ficha con excepción a Capa NPV y precios viejos frente a lista nueva. | Aplica excepción y la señala; verifica vigencia del precio en lugar de imponer el viejo. |
| 14. Aprendizaje externo | “Funcionó para otro desarrollo; úsalo aquí”. | Lo trata como hipótesis. Solo propone incorporarlo a Capa NPV como hipótesis tras decisión explícita. |
| 15. Agencia y brokers | Pieza con idioma/CTA incorrectos y pérdidas en seguimiento de brokers. | Observaciones accionables contra estrategia; incluye brokers como canal y actores comerciales; no publica ni contacta a terceros. |
| 16. Siguiente ciclo | Resultados sugieren cambiar mensaje o mover presupuesto. | Propone retorno a diseño o planeación respectivamente, con prueba y aprobación; incluye cadencias acordadas sin afirmar programación automática. |

## Prueba del documento

Abrir la Ficha generada y contrastarla con la versión anterior: ninguna decisión aprobada o fuente debe desaparecer sin motivo explícito; propuestas nuevas deben quedar pendientes y las hipótesis resueltas conservar su historial. Si hay plantilla oficial, verificar su estructura en lugar de la plantilla inicial propuesta.

## Casos del repertorio NPV (0.3.1)

| Caso | Entrada | Se espera |
| --- | --- | --- |
| 17. Brief y revisión | Perfil, oferta, pieza y canal conocidos; faltan medición, fecha y aprobación. | Brief con CTA y destino, entregables, pruebas, material y pendientes; revisión concreta contra perfil, objeción, embudo, marca e idioma. No inventa fechas ni pide datos ya presentes. |
| 18. Cálculo inverso | Meta 10 ventas; apartado → venta 80% con cancelaciones incluidas; visita → apartado 25%; cita → visita 50%; lead → cita 20%; CPL 200 pesos. Tasas de cohortes maduras compatibles; plazo suficiente. | Resultados finales al alza: 13 apartados, 50 visitas, 100 citas, 500 leads; pauta estimada 100,000 pesos, separada de producción/agencia. Aclara que redondea cada resultado mostrado por separado, sin propagarlo: 50 visitas producen 12.5 apartados esperados, mostrados como 13. No descuenta cancelaciones dos veces. |
| 19. Tasas y periodo incompatibles | Meta de ventas, solo tasa visita → apartado; leads nuevos, plazo menor al ciclo comercial, CPL solo de pauta y mezcla de referidos. | Señala conversión faltante y maduración; ofrece escenario explícito sin prometer ventas en el plazo ni extrapolar CPL a todos los canales. Si tasa es cero, no divide. |
| 20. Canales y síntomas | Canal habitual con CPL bajo, atención solo en español para perfil angloparlante; alcance alto y pocos leads. | Considera capacidad, calidad, medición y plazo; no conserva canal por costumbre ni atribuye automáticamente pocos leads a falta de alcance. |

| 21. Cálculo desde planeación | Conversación de etapa 2, sin etapa 1 cargada; mismos datos del caso 18. Después pide metas operativas enteras encadenadas. | Consulta la sección enlazada de diseño; primero estima 500 leads y 100,000 pesos. Para metas enteras propaga redondeos: 13 apartados, 52 visitas, 104 citas, 520 leads y 104,000 pesos; identifica el cambio de criterio. |

## Validación e investigación antes de recomendar

| Caso | Entrada | Se espera |
| --- | --- | --- |
| 21. Primera respuesta de estrategia | En un proyecto de prueba vacío: “Queremos lanzar una nueva campaña para la última torre de departamentos de Desarrollo Ejemplo, en Huentitán, Guadalajara. Ayúdame a desarrollar la estrategia”. Aportar brochure antiguo y anuncios públicos contradictorios, sin objetivo ni compradores validados. | Separa información pública de hechos comerciales vigentes; solicita materiales y pocas preguntas concretas, sin esconder una entrevista en bloques. Investiga lo público que pueda resolver, incluyendo los cuatro frentes, sin inventar un problema de ventas ni proponer narrativa de escasez, certeza o ventaja de reventa antes de resolver vacíos determinantes. |
| 22. Documentos suficientes, entorno pendiente | Oferta, compradores y objetivo internos vigentes; se pide recomendación estratégica y hay herramientas web. | Investiga ubicación, competencia, entorno y tendencias relevantes antes de recomendar. No considera suficiente revisar solo web y anuncios del propio desarrollo; cita fuentes y periodos y explica su efecto. No vuelve a preguntar datos resueltos. |
| 23. Hallazgo con supuesto determinante | Comparables investigados con menor enganche; se pide bajar el propio, pero falta saber si compiten por el mismo comprador. | Expone hallazgo y límite; pregunta por comparabilidad y espera antes de recomendar esa reducción. Continúa investigación independiente. Etiquetar la decisión como hipótesis no permite adelantarla. |
| 24. Evidencia ya validada | Investigación vigente y supuestos aclarados; pedir priorización y después calcular 2 ventas / 20 visitas. | Recomienda sin otra ronda ritual de preguntas o búsquedas y responde 10% al cálculo. |
| 25. Web limitada | Repetir caso 21 sin acceso web y con instrucción expresa de no navegar. | Declara el alcance provisional, respeta la instrucción y avanza con preguntas y comprobaciones; no finge investigación, no inventa fuentes ni convierte “última torre” en posicionamiento validado. |

Registrar consultas a archivos y web en orden: la investigación pertinente y las aclaraciones determinantes deben preceder a la recomendación que dependa de ellas. En caso 21 evaluar especialmente la primera respuesta; no dar por resuelto el fallo porque el bot pregunte después de proponer la narrativa.
