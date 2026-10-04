# Fuentes, arquitectura y continuidad

## Tres niveles de información

El plugin contiene la metodología canónica; no contiene datos de un desarrollo. Cada ChatGPT Project debe contener un solo desarrollo y sus materiales. Usar estos niveles, de mayor a menor especificidad:

| Nivel | Contenido | Ubicación | Versión y vigencia |
| --- | --- | --- | --- |
| Capa NPV | Información común de empresa: marca, roles, agencias, brokers, activos, proceso comercial, reglas y aprobaciones. | Archivo compartido y cargado en cada proyecto. | Debe indicar versión, por ejemplo `v1.0`; cambia solo ante cambios de empresa. |
| Ficha del desarrollo | Estado, decisiones, evidencia, hipótesis, pendientes y avances del desarrollo actual. | Un único archivo vivo en su propio proyecto. | Indica su versión, fecha y versión de Capa NPV usada. |
| Documentos del desarrollo | Brochure, inventario, ventas, leads, campañas, reportes, testimonios y otras fuentes particulares. | Solo en el proyecto del desarrollo correspondiente. | Registrar fecha de corte, periodo y alcance cuando aplique. |

Consultar primero la Ficha existente; usar la Capa NPV y los documentos para completarla o contrastarla. Si la Ficha contradice a la Capa NPV, prevalece la Ficha para el desarrollo actual y se debe señalar la contradicción, el dato afectado y si requiere confirmación. Una contradicción no autoriza a alterar la Capa NPV.

Nunca usar información de otro desarrollo como dato del actual, aunque esté accesible o se mencione en conversación. Puede proponerse únicamente como hipótesis por validar aquí, identificando su origen y el dato propio que la confirmaría. Un aprendizaje solo pasa a la Capa NPV por decisión explícita del equipo; hasta entonces no es una regla común.

Si la Ficha registra una versión antigua de la Capa NPV, señalarlo antes de apoyarse en una regla común potencialmente modificada. Comparar lo afectado, conservar las decisiones específicas de la Ficha y registrar la versión nueva solo cuando se haya revisado el impacto.

## Drive y acceso

Drive es la ubicación inicial de NPV para documentos vivos. Los adjuntos pueden ser copias o cortes. Cuando una decisión dependa de información cambiante como precio, inventario o fecha de entrega, comprobar su vigencia cuando sea necesario.

Usar las capacidades de Drive, Docs o Sheets disponibles en la sesión. Si falta acceso a una fuente necesaria, indicar la limitación concreta y continuar con la información disponible.

## Lectura

En hojas extensas, localizar las pestañas, fechas o columnas útiles antes de ampliar la lectura.

Si un archivo de leads, testimonios o conversaciones contiene nombres, teléfonos, correos, domicilios, identificadores u otros datos personales, advertirlo antes de analizarlo. Trabajar con una versión anonimizada: sustituir o eliminar identificadores directos y conservar solo los atributos mínimos necesarios para el diagnóstico. No copiar esos datos a la Ficha, al repositorio, a casos de prueba ni a resúmenes; referirse a registros anonimizados, agregados o muestras sin identificadores. No inferir residencia por LADA ni capacidad económica o motivación por nacionalidad.

## Organización, Ficha y guardado

Cuando se necesite una estructura inicial, usar una carpeta del desarrollo y una Ficha del desarrollo basada en la plantilla enlazada desde SKILL.md. Antes de crearla, revisar si ya existe una Ficha o documento equivalente. Completar lo conocido sin inventar datos; una Ficha vacía es válida para un proyecto nuevo.

La Ficha es el registro vivo de continuidad. Al actualizarla, conservar todo contenido aprobado y su estructura; no regenerarla desde cero ni reemplazarla por una copia que pierda contexto. Incrementar su versión, actualizar la fecha y agregar al registro de cambios: qué se modificó, la evidencia o conversación que lo motivó y lo que sigue pendiente. Mantener visibles las decisiones aprobadas, pendientes e hipótesis. Cada hipótesis debe tener estado `Abierta`, `Confirmada` o `Descartada`; al resolverse, conservar su historial y cambiar el estado, no eliminarla.

Registrar la versión de la Capa NPV utilizada. Si no se conoce, escribir `Por confirmar`; no inventar una versión. Cuando se actualice una Ficha por primera vez en una conversación, leer su control, decisiones, pendientes e hipótesis antes de preguntar. Así se evita repetir preguntas ya resueltas.

Enlazar los originales donde están, sin moverlos ni copiarlos. Al actualizar documentos existentes, conservar su identidad y enlace en lugar de crear copias por cada conversación. Verificar lo escrito y devolver el enlace del documento. Si no está disponible la escritura en Drive, preparar el cambio incremental en la conversación e indicar que todavía no se ha guardado.

## Continuidad

Guardar solo el contexto que ayude a retomar el trabajo: desarrollo, problema que se quiere resolver, evidencia relevante con enlaces y fechas de documentos e investigación web, decisiones, pendientes, hipótesis y siguiente acción. La Ficha es la fuente de continuidad; la memoria de la conversación la complementa, no la sustituye.

Al retomar el diagnóstico, aprovechar ese contexto antes de repetir preguntas. Si no hay Ficha disponible, continuar con el contexto de la conversación y proponer crearla solo si el equipo quiere guardar el avance.
