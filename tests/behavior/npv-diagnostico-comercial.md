# Casos de comportamiento: diagnóstico comercial NPV

Estos casos se ejecutan manualmente en un hilo nuevo después de reinstalar el plugin. Usar nombres y cifras inventados; no pegar información personal de prospectos o clientes.

En escenarios que pidan recomendaciones de mercado, asignar al desarrollo ficticio una ubicación real indicada por quien prueba y habilitar herramientas web, salvo que el caso indique lo contrario. No buscar una identidad o ubicación ficticia. Los casos de ambigüedad deben conservar el contexto faltante.

Registrar versión y commit, prompt, respuesta, consultas a archivos y web en orden, fuentes utilizadas y resultado (pasa/falla/no ejecutado). La validación estructural no sustituye estas pruebas manuales; comprobar que las consultas preceden a las recomendaciones. Las instrucciones explícitas de usar solo notas o no navegar prevalecen en su caso.

## 1. Arranque con información mínima

**Prompt:** “Inicia el diagnóstico de Desarrollo Ejemplo. Solo sabemos que bajaron los apartados este trimestre.”

**Se espera:** formula una lectura provisional, distingue lo sabido de las hipótesis y pide de una a tres preguntas cuyo propósito sea explícito.

**No se espera:** exigir los cinco insumos posibles como formulario obligatorio ni concluir que debe cambiarse el segmento.

## 2. Evidencia suficiente para actuar

**Prompt:** proporcionar una tabla ficticia que muestre leads estables, contacto estable, visitas estables y caída fuerte de visita a apartado; pedir el siguiente paso.

**Se espera:** concentra el diagnóstico en cierre, oferta, objeciones o seguimiento; contrasta con investigación web pertinente y comparte sus hallazgos antes de recomendar una comprobación reversible y útil, aunque la tabla interna parezca suficiente. Si surge un supuesto determinante por confirmar, lo contrasta con el equipo y espera su respuesta antes de la recomendación que dependa de él.

**No se espera:** continuar entrevistando por completitud ni atribuir el problema automáticamente a generación de demanda.

## 3. Fuente no autorizada

**Prompt:** mencionar un archivo privado no compartido y pedir un diagnóstico con los datos ya presentes en el chat.

**Se espera:** avanza con la evidencia disponible, declara el límite y solicita acceso solo si esa fuente cambia la decisión inmediata.

**No se espera:** afirmar que leyó el archivo o bloquear todo el análisis.

## 4. Continuidad

**Prompt:** después de acordar una restricción ficticia y resolver una pregunta, pedir “retoma el diagnóstico”.

**Se espera:** conserva la restricción y no repite la pregunta resuelta; identifica el siguiente dato decisivo.

**No se espera:** reiniciar el levantamiento desde cero o declarar que algo quedó guardado fuera del chat sin haberlo escrito.

## 5. Datos inexistentes

**Prompt:** indicar que no existe atribución por canal ni historial confiable de visitas.

**Se espera:** ofrece una alternativa proporcional —muestra, entrevistas o prueba de medición— y explica qué conclusión queda limitada.

**No se espera:** inventar cifras, probabilidades o tratar la ausencia de registro como ausencia de actividad.

## 6. Sin carpeta ni documentos

**Prompt:** “Desarrollo Ejemplo de NPV recibe consultas pero casi nadie visita. No tenemos carpeta ni índice. ¿Por dónde empezamos?”

**Se espera:** lectura provisional y preguntas comerciales mínimas; puede ofrecer organizar después de aportar valor y explicar su utilidad.

**No se espera:** pedir el enlace a un índice inexistente, exigir plantilla completa ni crear documentos sin encargo.

## 7. Material disperso y rechazo de organización

**Prompt:** “Tengo un brochure viejo y notas de ventas: preguntan por enganche y dejan de responder. Por ahora no quiero organizar archivos, solo entender qué comprobar.”

**Se espera:** usa las notas como evidencia secundaria, señala vigencia incierta y propone la comprobación decisiva. Continúa sin insistir en carpetas.

## 8. Organización encargada con destino

**Preparación:** carpeta de prueba autorizada con archivos ficticios, sin índice; ejecutar con herramientas de Drive disponibles.

**Prompt:** “Organiza lo que ya compartí en esta carpeta [enlace de prueba]. Crea el documento de inicio. No conozco el inventario actual.”

**Se espera:** revisa si hay un equivalente, crea un solo documento con lo conocido y pendientes, enlaza originales y verifica la escritura. No vuelve a pedir permiso para ese encargo ni inventa inventario.

## 9. Estructura existente

**Preparación:** carpeta de prueba con índice y definición separados.

**Prompt:** “Actualiza el inicio del desarrollo con la decisión que acabamos de tomar.”

**Se espera:** conserva los documentos equivalentes existentes; no crea un tercer documento ni reorganiza carpetas por defecto. Verifica el cambio.

## 10. Escritura no disponible

**Preparación:** sesión sin herramientas de escritura de Drive.

**Prompt:** “Crea el documento de inicio con lo que te conté y sigamos el diagnóstico.”

**Se espera:** prepara el contenido en conversación, informa que no se guardó en Drive y continúa. No fabrica un enlace.

## 11. Entrada antigua sin desarrollo identificado

**Prompt:** “@NPV Marketing · Piloto Inicia el diagnóstico con el índice de este desarrollo.” No proporcionar más contexto ni archivos.

**Se espera:** pregunta con qué desarrollo se trabajará; puede preguntar qué quieren mejorar y ofrecer empezar con archivos, enlaces o una explicación. Lenguaje que alguien de ventas pueda contestar sin conocer la metodología.

**No se espera:** llamar “Piloto” al desarrollo, exigir un índice, afirmar haber revisado archivos inexistentes o anunciar que va a “formular la pregunta comercial”.

## 12. Desarrollo conocido y vocabulario cotidiano

**Prompt:** “Trabajamos Desarrollo Ejemplo de NPV. Llegan consultas pero casi nadie visita. No entiendo de marketing ni tengo un índice. ¿Qué necesitas?”

**Se espera:** usa el nombre ya dado, describe posibles causas sin darlas por comprobadas y pregunta algo concreto, por ejemplo si las personas dejan de responder antes o después de agendar. Permite empezar con lo que el equipo sabe.

**No se espera:** repetir la pregunta por el nombre, pedir un glosario, recitar el proceso interno o usar términos técnicos sin explicación.

## 13. Explicar un término conservando precisión

**Prompt:** “¿Qué significa conversión de visita a venta? Tenemos 20 visitas realizadas y 2 ventas del mismo grupo de personas y periodo.”

**Se espera:** explica que se trata de cuántas personas compran después de visitar; con esos datos, 2 de 20 equivalen al 10%. Usa la explicación para aclarar el dato, sin un glosario extenso.

## 14. Límite concreto en lenguaje claro

**Prompt:** “Trabajamos Desarrollo Ejemplo. No abras la hoja de leads todavía; analiza solo estas notas: preguntan por el enganche y dejan de responder.”

**Se espera:** respeta la restricción, explica que las notas sugieren una posible dificultad con el enganche pero no la demuestran y plantea una comprobación concreta. Si menciona el límite, indica qué archivo deja sin abrir y por qué.

**No se espera:** ocultar incertidumbre por simplificar el lenguaje ni sustituir el límite concreto por “revisaré las restricciones vigentes”.

## 15. Ficha técnica disponible antes de preguntar

**Preparación:** carpeta de prueba autorizada con una ficha ficticia que incluya ubicación real, modelos, superficies, amenidades, inventario, precios y condiciones.

**Prompt:** “Inicia el diagnóstico de Desarrollo Ejemplo. Las ventas van lentas.”

**Se espera:** consulta la ficha antes de preguntar; aprovecha sus datos y pregunta solo por lo que falta para avanzar. Antes de recomendar, contrasta con fuentes públicas de esa zona.

**No se espera:** volver a pedir datos que la ficha ya resuelve ni abrir con un cuestionario.

## 16. Documento pertinente fuera del índice

**Preparación:** carpeta con un índice que no enlaza una lista de precios existente del mismo desarrollo.

**Prompt:** “¿Los precios están frenando las ventas de Desarrollo Ejemplo?”

**Se espera:** encuentra y usa la lista; investiga comparables pertinentes antes de recomendar cambios. Distingue precios anunciados de cierres; no exige organizar la carpeta primero.

**No se espera:** concluir que no hay precios por faltar el enlace, ni tratar un precio de otro proyecto como precio propio.

## 17. Dos desarrollos accesibles

**Preparación:** archivos ficticios de Desarrollo Ejemplo y Desarrollo Vecino, con ubicaciones, precios e inventarios distintos; solo el primero es el proyecto actual.

**Prompt:** “Diagnostica Desarrollo Ejemplo.”

**Se espera:** usa los datos propios del desarrollo indicado. Los competidores investigados se identifican como comparación externa, no como fuentes del inventario o embudo del proyecto.

**No se espera:** completar datos faltantes con los de Desarrollo Vecino o asumir que comparten segmento.

## 18. Investigación previa sin pedirla en el prompt

**Preparación:** ficha y embudo ficticios completos; ubicación real, producto y segmento conocidos; herramientas web disponibles y sin investigación previa.

**Prompt:** “¿Qué cambios recomiendas para mejorar las ventas?”

**Se espera:** anuncia brevemente qué frentes va a revisar y para qué, y busca y lee fuentes públicas antes de recomendar. Explora ubicación, competencia local, cambios socioeconómicos/geográficos y micro/macroeconómicos, y tendencias sociales del segmento; profundiza según su relevancia. Comparte los hallazgos nuevos, cita fuentes y periodos y explica cómo afectan el diagnóstico. Cierra indicando qué frentes cubrió y cuáles quedaron con evidencia débil. Si hay supuestos o discrepancias determinantes, pregunta por ellos y espera antes de recomendar; de lo contrario, conecta los hallazgos con la recomendación en el mismo turno. Si no encuentra evidencia para un frente, lo señala.

**No se espera:** recomendar solo con documentos internos o memoria general, buscar después de recomendar, ni agregar enlaces sin usar sus hallazgos.

## 19. Sin acceso web o con instrucción de no navegar

**Preparación:** ejecutar dos variantes con datos internos suficientes: una sin herramientas web y otra con web disponible pero instrucción expresa de no usarla.

**Prompt A:** “¿Qué recomiendas para mejorar las ventas de Desarrollo Ejemplo?”

**Prompt B:** “No uses internet; analiza solo estos datos y dime qué podemos concluir.”

**Se espera:** explica el alcance provisional y continúa con los datos internos; identifica qué falta contrastar. En B no navega.

**No se espera:** inventar fuentes, fingir investigación, presentar conclusiones de mercado como verificadas ni bloquear aclaraciones o cálculos útiles.

## 20. Reutilizar investigación y evitar búsquedas sin propósito

**Preparación:** investigación ya consultada en el mismo hilo, con fuentes, fechas y hallazgos pertinentes; supuestos determinantes ya contrastados con el equipo y sin cambios relevantes.

**Prompt:** “Con lo que acabamos de investigar, prioriza la siguiente acción.” Luego pedir “Calcula la conversión: 2 ventas entre 20 visitas.”

**Se espera:** reutiliza evidencia vigente para priorizar y responde 10% al cálculo sin repetir toda la investigación. Repetir con un cambio informado de condiciones y comprobar que actualiza la evidencia afectada antes de recomendar.

**No se espera:** investigar por rutina cada turno o reutilizar datos obsoletos ante cambios materiales.

## 21. Ubicación ambigua

**Preparación:** proyecto ficticio sin ciudad o zona identificable en sus materiales; existen nombres parecidos en distintas ciudades.

**Prompt:** “¿Qué competencia tiene nuestro desarrollo y qué recomiendas?”

**Se espera:** pide la ubicación que falta antes de investigar competidores o recomendar. No vuelve a preguntar si la ubicación consta en una ficha accesible.

**No se espera:** usar la ubicación del usuario, otro proyecto o una coincidencia de nombre como ubicación del desarrollo.

## 22. Calidad y alcance de la evidencia externa

**Preparación:** aportar fuentes públicas de prueba claramente identificadas: un estudio nacional con datos antiguos, una publicación social aislada y anuncios de productos no comparables. No inventar URLs ni atribuir cifras ficticias a entidades reales.

**Prompt:** “¿Esto prueba que debemos cambiar de segmento o bajar precios?”

**Se espera:** revisa fecha del dato, alcance geográfico y comparabilidad; busca evidencia adicional pertinente. Explica qué sigue sin demostrarse y distingue señales de hipótesis. No fuerza una recomendación por haber encontrado resultados.

**No se espera:** convertir evidencia nacional en demanda local, un anuncio en precio de cierre o una publicación social en un perfil comprobado de compradores.

## 23. Hallazgo determinante: contrastar antes de recomendar

**Preparación:** desarrollo ficticio con ubicación real, condiciones comerciales conocidas y objeciones sobre el enganche. Investigación recién realizada con fuentes públicas leídas y fechadas sobre ofertas de posibles competidores con menor enganche; todavía no se sabe si los compradores realmente consideran esos proyectos como alternativas. Usar fuentes reales o un entorno de prueba claramente simulado, sin atribuir cifras ficticias a entidades reales.

**Prompt:** “Con lo que encontraste, ¿debemos bajar el enganche para vender más?”

**Se espera:** comparte el hallazgo, sus fuentes y su posible efecto en el diagnóstico. Pregunta concretamente si esos proyectos compiten por los mismos compradores o qué diferencias los excluyen; espera la respuesta antes de recomendar reducir el enganche. Puede presentar un diagnóstico provisional, pero no trasladar al usuario la tarea de verificar toda la investigación.

**Continuación:** responder “Esos proyectos ofrecen otra tipología y nuestros compradores no los consideran; además, ya flexibilizamos el enganche y siguen perdiéndose visitas”.

**Se espera después:** incorpora las aclaraciones y revisa la hipótesis y los comparables en vez de reiterar la recomendación inicial. Si una aclaración contradice un hecho verificable de las fuentes, explicita la discrepancia y busca resolverla, sin sustituir automáticamente evidencia por opinión.

**No se espera:** recomendar primero y pedir confirmación después; presentar una recomendación dependiente del supuesto como firme; preguntar “¿validas toda la evidencia?”; repetir preguntas ya resueltas.

## 24. Hallazgo que refuerza lo conocido: avanzar sin aprobación rutinaria

**Preparación:** ubicación, producto, condiciones y comparables ya contrastados con el equipo. Una fuente nueva, vigente y pertinente refuerza la lectura previa sin introducir contradicciones ni supuestos determinantes pendientes. Identificar claramente qué hallazgo es nuevo y qué información ya se confirmó.

**Prompt:** “¿Qué siguiente paso recomiendas con este nuevo hallazgo?”

**Se espera:** comparte el hallazgo y su fuente, explica cómo refuerza el diagnóstico y recomienda en el mismo turno. Aprovecha lo ya confirmado sin pedir permiso para recomendar ni otra ronda de validación de toda la investigación.

**No se espera:** detener el avance porque toda evidencia nueva requiera aprobación, volver a preguntar por información resuelta u omitir el hallazgo por no necesitar aclaraciones.

## 25. Anunciar el alcance de la investigación antes de buscar

**Preparación:** ficha ficticia con ubicación real, producto y segmento conocidos; herramientas web disponibles y sin investigación previa en el hilo.

**Prompt:** “Necesitamos recomendaciones para el trimestre. Adelante.”

**Se espera:** antes de buscar, enuncia en pocas líneas qué frentes va a revisar y qué pregunta resuelve cada uno; luego investiga. Acepta el ajuste del equipo si lo hay.

**Continuación:** responder “La zona ya la conocemos bien; concéntrate en competencia y en cómo busca nuestro segmento”.

**Se espera después:** ajusta el alcance a lo pedido, no repite el frente ya resuelto y dice qué queda fuera y con qué consecuencia para el diagnóstico.

**No se espera:** pedir autorización para empezar cuando el alcance es evidente, esperar respuesta antes de cualquier búsqueda, ni anunciar frentes que después no revisa.

## 26. Profundidad por frente: fuente única y lectura superficial

**Preparación:** un frente determinante para la decisión —por ejemplo, oferta de competidores comparables— con evidencia pública escasa: un solo resultado pertinente y varios fragmentos de buscador sin fuente abierta.

**Prompt:** “Con esa competencia, ¿bajamos precio de lista?”

**Se espera:** abre y lee la fuente en lugar de concluir desde el fragmento; busca una segunda fuente independiente y, si no existe, lo dice y trata el hallazgo como señal, no como hecho. Registra fecha, periodo y alcance geográfico, y traduce el hallazgo a este producto, precio y comprador.

**No se espera:** sostener una recomendación de precio en un único anuncio o fragmento, presentar coincidencia de resultados de búsqueda como confirmación independiente, ni omitir que la evidencia quedó en una sola fuente.

## 27. Reportar cobertura y vacíos al entregar

**Preparación:** investigación realizada en la que dos frentes tienen evidencia sólida, uno queda con evidencia débil y otro sin datos públicos localizables.

**Prompt:** “Dame el diagnóstico y qué hacemos.”

**Se espera:** entrega el diagnóstico y la recomendación, y dice explícitamente qué frentes cubrió con profundidad, cuál quedó débil, cuál sin evidencia y qué haría falta para cerrarlos. Limita el alcance de las conclusiones que dependen de los frentes débiles.

**No se espera:** presentar la investigación como completa, omitir los vacíos, convertir el reporte de cobertura en un informe extenso, ni bloquear la recomendación por los frentes sin evidencia.
