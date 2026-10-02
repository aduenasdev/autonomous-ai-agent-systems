# Notas — Building Multi-Agent Systems using LangGraph and Autogen

Notas personales (en español) sobre seguridad y barandillas de grado de producción.

## Seguridad y barandillas de grado de producción

### El problema de la acción irrevocable

Las operaciones financieras son definitivas. Una vez ejecutadas no se pueden deshacer; solo es posible realizar una operación de compensación. Por eso, un agente que interpreta mal los datos, acepta una instrucción no autorizada o actúa durante una caída del mercado puede producir pérdidas económicas y responsabilidad legal.

Los sistemas de producción necesitan **defensa en profundidad**: varias capas de comprobaciones que detecten los problemas antes de que se conviertan en acciones irrevocables.

### Comprobaciones previas a la ejecución

Antes de ejecutar cualquier operación deben superarse controles obligatorios:

- **Tamaño de la posición:** comprobar que la operación no supere el límite máximo por activo o cartera. Si una posición actual del 5 % pasaría al 8,1 % cuando el máximo es 7 %, la orden debe bloquearse.
- **Disponibilidad de capital:** calcular el efectivo disponible descontando las órdenes pendientes y rechazar la operación si los fondos son insuficientes.
- **Condiciones del mercado:** verificar el horario de negociación, el estado de la bolsa y posibles suspensiones del valor.
- **Razonabilidad del precio:** establecer umbrales de desviación respecto a la oferta y la demanda. Una orden de compra muy por encima del precio actual debe marcarse como sospechosa.
- **Racionalidad del volumen:** comparar el tamaño de la orden con el volumen medio diario y limitarla a una fracción razonable, por ejemplo el 10 %.

Estas barreras deben ejecutarse automáticamente y de forma transparente para el agente. Si una falla, la respuesta debe ser estructurada y explicar el motivo, los valores actuales, el límite permitido y el resultado propuesto.

### Prevención de fugas del LLM

Las fugas o *jailbreaks* son intentos de conseguir que el agente ignore sus instrucciones o eluda los controles. La defensa debe incluir:

- Mensajes de sistema que describan explícitamente las solicitudes adversarias y ordenen rechazarlas.
- Separación de capas de instrucciones, con un filtro previo al agente que detecte patrones como «ignora las instrucciones», «modo de emergencia», «saltar comprobaciones» o «acceso de administrador».
- Entradas estructuradas, preferiblemente JSON, en lugar de texto libre. Por ejemplo: `{ "accion": "comprar", "simbolo": "AAPL", "cantidad": 100 }`.
- Supervisión de patrones inusuales, como cambios bruscos en el perfil de riesgo, tamaños de posición atípicos u operaciones con activos nunca utilizados anteriormente.

El filtro previo no sustituye las validaciones de negocio: ambas capas deben funcionar de forma independiente.

### Registro exhaustivo para cumplir la normativa

En sistemas financieros es necesario poder reconstruir qué ocurrió, cuándo y por qué. Por ello deben registrarse:

- **Cada entrada:** precios, noticias, documentos y demás datos recibidos por el agente.
- **Cada decisión:** análisis y justificación que llevaron a la propuesta.
- **Cada llamada a herramientas:** herramienta utilizada, parámetros enviados y respuesta recibida.
- **Cada validación:** controles superados, controles fallidos y motivo concreto del bloqueo.
- **Cada intento de ejecución:** resultado, precio, marca de tiempo, identificador de la orden del bróker y error, si lo hubiera.

Los registros deben tener un formato coherente y ser fáciles de consultar mediante símbolos, marcas de tiempo e identificadores de agente. Para evitar manipulaciones deben almacenarse en un sistema **inmutable y de solo adición** (*append-only*).

## Diseño de conjuntos de herramientas

### Por qué una sola herramienta no es suficiente

La toma de decisiones financieras necesita varias fuentes y tipos de acciones: análisis fundamental, datos de mercado, contexto de noticias y capacidad de ejecución. Ninguna herramienta cubre por sí sola todas esas responsabilidades, por lo que el agente debe coordinar un conjunto de herramientas especializadas según el objetivo.

### Herramientas de análisis fundamental

Una herramienta de análisis fundamental consulta ingresos, beneficios, deuda y márgenes en bases de datos estructuradas que suelen actualizarse con los informes trimestrales.

Debe definir esquemas claros y estables. Una consulta de beneficios puede devolver:

- Ingresos.
- Beneficio por acción.
- Periodo de referencia.
- Variación porcentual respecto al trimestre anterior.

También necesita errores estructurados para que el agente pueda interpretarlos, por ejemplo «Código de empresa no válido» o «Los beneficios del cuarto trimestre de 2024 aún no se han presentado».

### Herramientas de ejecución con restricciones de seguridad

Una herramienta que ejecuta operaciones reales necesita un esquema estricto:

- Símbolo bursátil válido.
- Cantidad entera y positiva.
- Tipo de orden, como mercado o límite.
- Precio obligatorio para órdenes limitadas.
- Acción restringida a compra o venta.

Cualquier dato fuera del esquema debe rechazarse antes de llegar a la API del bróker. Además, deben validarse los fondos disponibles, el horario del mercado, los límites de posición y las normas de riesgo.

La herramienta debe separar propuesta y ejecución. El agente propone la orden, la herramienta la valida y muestra un resumen como: «Se propone comprar 100 acciones de AAPL a precio de mercado. Coste estimado: 17 500 $. ¿Confirmar?». La operación no se activa hasta recibir una aprobación humana explícita.

Cada intento de ejecución, tanto exitoso como fallido, debe registrarse para auditoría, cumplimiento normativo y depuración.

### ReAct avanzado: coordinación de múltiples herramientas

**ReAct (Reasoning and Acting)** combina razonamiento, acción, observación y un nuevo ciclo de razonamiento. En su versión avanzada, el agente encadena varias herramientas:

1. Consulta el análisis fundamental para obtener datos de beneficios.
2. Consulta los datos de mercado para conocer precio y volumen actuales.
3. Consulta las noticias para comprobar el contexto reciente.
4. Razona si los factores justifican proponer una operación.
5. Invoca la herramienta de ejecución para preparar una orden.
6. Espera la confirmación humana.
7. Registra el resultado.

Cada respuesta de una herramienta alimenta el siguiente paso. El agente no decide toda la secuencia por adelantado: adapta sus acciones a los resultados y conserva el contexto de las cifras y noticias consultadas.

La coordinación necesita manejo de errores en cada etapa. Si falla el análisis fundamental, el agente puede continuar solo si el flujo lo permite y debe declarar la información ausente. Si el servicio de noticias no funciona, debe reconocer esa limitación y explicar que la decisión carece de ese contexto, en lugar de inventar datos.

> El fragmento original de esta sección termina en «explicar que la d»; la continuación no estaba incluida en el material recibido.

## Control avanzado de LangGraph

### Parada de emergencia

Los mercados pueden sufrir caídas repentinas, volatilidad extrema o activaciones de los cortacircuitos. En esas situaciones la lógica habitual de negociación deja de ser válida y el sistema necesita un mecanismo que detenga de inmediato las operaciones.

La **parada de emergencia** es un nodo especial que supervisa continuamente la volatilidad, los movimientos de precios y los picos de volumen. Puede activarse cuando se superan umbrales definidos, por ejemplo:

- Volatilidad general del mercado superior a 40.
- Variación del 15 % en una acción en un intervalo de dos minutos.

Cuando se activa, anula el flujo normal y redirige el grafo a un estado seguro:

1. Cierra las órdenes pendientes.
2. Detiene nuevas propuestas de negociación.
3. Cambia el sistema a modo de solo supervisión.
4. Notifica a los operadores el motivo y el estado.
5. Espera una reanudación o anulación manual.

El orquestador debe comprobar el estado de la parada antes de cada transición. Aunque un agente haya encontrado una oportunidad o haya preparado una compra, la transición debe dirigirse al estado seguro mientras la parada esté activa.

### Decisiones con plazos límite

Algunas decisiones tienen una fecha límite estricta: el cierre del mercado, una conferencia de resultados o el vencimiento de una opción. Cada flujo de trabajo debe llevar una marca de tiempo de plazo.

Antes de activar un agente, el orquestador comprueba si queda tiempo suficiente para que termine. Si un análisis suele tardar tres minutos y solo quedan dos, debe omitirse el análisis profundo y tomarse una decisión con la información disponible o descartar la oportunidad.

Se pueden establecer etapas progresivas:

- Tras dos minutos sin terminar la investigación, continuar con datos parciales.
- Tras otros dos minutos sin terminar el análisis, decidir con información incompleta.
- Registrar explícitamente la presión temporal y el aumento del riesgo.

La presión no justifica una decisión descuidada. A veces la decisión correcta es no actuar porque no existe tiempo suficiente para evaluar la oportunidad de forma adecuada.

### Cola de revisión final

Antes de ejecutar una operación, esta pasa por una cola de revisión humana. La cola debe mostrar un resumen estructurado con:

- Operación propuesta.
- Motivo de la recomendación.
- Análisis que la respalda.
- Parámetros de riesgo aplicados.
- Resultado esperado.

El revisor puede:

- **Aprobar:** la operación se ejecuta.
- **Rechazar:** la operación se cancela y se devuelve un comentario al agente.
- **Solicitar información adicional:** el flujo retrocede para realizar un análisis más detallado.

Las operaciones rutinarias y pequeñas pueden aprobarse por lotes, mientras que las operaciones de gran volumen, las nuevas posiciones o las marcadas como de alto riesgo requieren revisión individual.

La cola debe incluir caducidad. Si una operación permanece demasiado tiempo sin aprobación, debe expirar porque las condiciones del mercado y los precios pueden haber cambiado. Una operación caducada no debe ejecutarse automáticamente.

## RAG para datos financieros

### Por qué los documentos financieros necesitan RAG

Los documentos presentados ante la SEC, las transcripciones de conferencias de resultados y los informes anuales contienen información fundamental, pero pueden tener cientos de páginas. Un agente no debería procesar el documento completo cada vez que necesita un dato concreto.

**RAG (Retrieval-Augmented Generation)** permite indexar los documentos una vez y recuperar después solo las secciones relevantes. En lugar de leer un informe 10-K completo, el agente puede recuperar los párrafos relacionados con las obligaciones de deuda.

### Indexación de documentos e informes

Los documentos 10-K y 10-Q tienen una estructura definida, con secciones como descripción del negocio, factores de riesgo, estados financieros y análisis de la dirección. La indexación debe conservar esa estructura:

- Dividir por secciones y subsecciones, no solo por número de palabras.
- Conservar rutas como «Factores de riesgo > Riesgos normativos > Párrafo 3».
- Asociar metadatos como código bursátil, tipo de documento, fecha de presentación y ejercicio fiscal.

Los metadatos ayudan a interpretar el contexto y la actualidad de cada fragmento. Cuando se presenta un nuevo 10-K, el documento anterior debe marcarse como sustituido para priorizar la información vigente, salvo que se soliciten datos históricos.

### Conversión de tablas en texto buscable

Los balances, cuentas de resultados y estados de flujos de efectivo no siempre se representan bien mediante embeddings en su formato tabular original. Por eso conviene transformar las tablas en frases descriptivas, por ejemplo:

> En el cuarto trimestre de 2024, los ingresos fueron de 50,2 millones de dólares, un 15 % más que en el cuarto trimestre de 2023. Los gastos operativos ascendieron a 30,1 millones de dólares, el 60 % de los ingresos.

La representación textual permite que la búsqueda vectorial encuentre información numérica relevante por similitud semántica. A la vez, debe conservarse la tabla original como metadato para consultar las cifras exactas cuando sea necesario.

En tablas multidimensionales pueden generarse varios fragmentos independientes, como «El producto A generó 20 millones de dólares en Norteamérica» o «El producto B generó 15 millones de dólares en Europa».

### Agente de investigación: datos en tiempo real y RAG

Un agente de investigación combina:

1. Cotización y volumen actuales mediante una herramienta en tiempo real.
2. Resultados financieros históricos mediante RAG sobre registros de la SEC.
3. Noticias recientes mediante una fuente en tiempo real.
4. Síntesis razonada de toda la información.

Los datos en tiempo real indican lo que sucede ahora y RAG aporta contexto histórico y explicaciones detalladas. El agente debe considerar la actualidad: si un resultado de hace seis meses contradice una previsión publicada hoy, debe dar prioridad a la información reciente y explicitar la diferencia.

Las respuestas deben citar sus fuentes. Las afirmaciones sobre deuda deben indicar la sección del documento de la SEC de la que proceden, y las referencias a precios deben incluir fecha y hora. Esta transparencia permite verificar el análisis y aumenta la confianza.

## Datos en tiempo real y herramientas avanzadas

### Integración: cómo se conecta todo

Los agentes en tiempo real observan continuamente los flujos de datos. Cuando se activa una condición —por ejemplo, una caída por debajo de un umbral, una sorpresa en resultados o una noticia de última hora—, el agente inicia el flujo de investigación.

El proceso combina varias fuentes:

1. La herramienta de análisis fundamental aporta los datos financieros de la empresa.
2. RAG recupera las secciones relevantes de los documentos presentados ante la SEC.
3. La herramienta de noticias obtiene los titulares recientes.
4. El agente sintetiza los datos en tiempo real con el contexto histórico.
5. Si procede, la herramienta de ejecución prepara una propuesta con validación y confirmación completas.

Durante todo el proceso se registran las fuentes consultadas, las herramientas utilizadas, los pasos del razonamiento y los intentos de ejecución. Esto proporciona tanto un registro de auditoría como información útil para depurar el sistema.

### Gestión de la complejidad y el riesgo

Los agentes financieros en tiempo real operan en entornos de alto riesgo, por lo que necesitan varias capas de protección:

- Validar y limpiar los datos antes de iniciar el razonamiento.
- Aplicar medidas de seguridad en cada herramienta para impedir acciones inválidas.
- Usar aprobación humana en los casos extremos que la automatización no pueda evaluar con seguridad.
- Reconocer explícitamente los datos incompletos o contradictorios, en lugar de responder con una confianza injustificada.
- Aplicar límites de tasa y controles de costes para evitar un uso descontrolado de las APIs.
- Medir el número de llamadas y sus costes asociados.
- Continuar con la información disponible si falla una fuente, señalando claramente la laguna de datos.

### Flujo financiero completo en tiempo real

Un ciclo completo puede seguir estos pasos:

1. Se abren los mercados y el agente observador comienza a supervisar las posiciones.
2. Se detecta un movimiento relevante en los precios.
3. Se consulta el análisis fundamental para obtener el contexto de resultados.
4. RAG recupera las secciones pertinentes de los documentos de la SEC.
5. Se comprueban las noticias recientes.
6. El agente sintetiza la información y evalúa si el movimiento está justificado o presenta una oportunidad.
7. Si procede, propone una operación mediante la herramienta de ejecución.
8. Un operador humano revisa y aprueba la propuesta.
9. Se ejecuta la operación y se registra el resultado.
10. El agente actualiza los umbrales de supervisión.

Este ciclo se repite mientras los mercados estén activos y combina capacidad de respuesta en tiempo real, investigación contextual y gestión cuidadosa del riesgo.

## Extensiones de producción: contenedores y escalado

Esta sección consolida únicamente aspectos adicionales de infraestructura y escalado que no estaban desarrollados en las secciones anteriores.

### Contenedorización y API

Los contenedores Docker empaquetan código, dependencias y configuración en unidades portátiles. Separar los componentes en contenedores independientes permite escalarlos de forma individual según su carga.

La configuración de producción debe utilizar variables de entorno y nunca incluir credenciales estáticas en el código. Las operaciones pueden exponerse mediante endpoints de FastAPI con:

- Autenticación en cada solicitud.
- Limitación de tasa.
- Balanceadores de carga para distribuir solicitudes entre instancias.
- Comprobaciones de salud que retiren de la rotación las instancias no disponibles.

### Escalado de sistemas en tiempo real

Cuando los datos de mercado llegan continuamente, las colas de mensajes absorben el volumen y desacoplan la recepción del procesamiento. Varios trabajadores pueden extraer mensajes y procesarlos en paralelo.

La partición por código bursátil permite que distintos trabajadores gestionen valores diferentes y reduce las condiciones de carrera. Para optimizar el sistema también pueden utilizarse:

- Caché para cálculos repetidos.
- Réplicas de lectura para separar consultas de escrituras.
- Métricas de carga y latencia para ajustar el número de trabajadores.

### Gestión de carteras a gran escala

Cuando varios agentes toman decisiones sobre cientos de valores, se necesita coordinación global:

- Un gestor de riesgos centralizado comprueba todas las propuestas frente a las restricciones de la cartera completa.
- El bloqueo optimista verifica que la cartera no haya cambiado entre la propuesta y la ejecución.
- Las actualizaciones de estado por lotes reducen la contención en la base de datos.
- Las métricas globales permiten limitar nuevas propuestas cuando se aproximan los límites de riesgo.

### Integración en producción

Una arquitectura completa conecta los datos en tiempo real con colas de mensajes, agentes contenedorizados y orquestadores que distribuyen el trabajo con balanceo de carga. Cada propuesta atraviesa validación antes de ejecutarse y las operaciones aprobadas se registran de forma inmutable.

Las paradas de emergencia se supervisan continuamente y todos los eventos se registran con marcas de tiempo y contexto. La fiabilidad no depende solo de que el código funcione: el sistema debe mantener seguridad, trazabilidad y cumplimiento bajo presión.

## La arquitectura multiagente

### Por qué un solo agente no es suficiente

Un agente único que investiga empresas, supervisa precios, analiza riesgos y decide operaciones acaba concentrando demasiadas responsabilidades y conocimientos distintos. La arquitectura multiagente divide el trabajo en componentes especializados que colaboran e intercambian información.

### Definición de las funciones de los agentes

La separación de responsabilidades debe ser explícita:

- **Agente investigador:** recopila hechos mediante APIs, noticias y RAG sobre documentos de la SEC. Devuelve precio actual, resultados, titulares y valoraciones, pero no emite recomendaciones.
- **Agente analista:** interpreta los informes, identifica patrones y anomalías, conecta fuentes y produce conclusiones razonadas. Por ejemplo, puede explicar que unos resultados superiores a las expectativas conviven con previsiones débiles y márgenes en compresión.
- **Agente gestor de cartera:** combina los análisis, las posiciones actuales y las restricciones de riesgo para decidir comprar, vender o mantener. Puede proponer operaciones, pero debe seguir las barreras y aprobaciones establecidas.

Esta separación reduce los sesgos de cada etapa: el investigador no selecciona datos para apoyar una conclusión, el analista no oculta información inconveniente y el gestor recibe un análisis estructurado en lugar de datos brutos.

### El coordinador

El **agente coordinador** distribuye tareas, gestiona traspasos y mantiene el flujo de trabajo. No realiza la investigación ni sustituye al analista:

1. Asigna la solicitud al investigador.
2. Envía los datos recopilados al analista.
3. Remite el análisis al gestor de cartera.
4. Decide cómo actuar ante datos ausentes, desacuerdos o necesidad de investigación adicional.

El coordinador funciona como una lógica de flujo de trabajo que razona sobre el siguiente paso basándose en el resultado anterior y en las excepciones del proceso.

### Protocolos de comunicación

Los agentes necesitan mensajes estructurados y contratos claros. Un resultado de investigación puede tener esta forma:

```json
{
  "type": "research_complete",
  "ticker": "AAPL",
  "data": {},
  "timestamp": "2024-10-23T10:30:00Z"
}
```

El resultado del análisis puede seguir otro esquema:

```json
{
  "type": "analysis_complete",
  "ticker": "AAPL",
  "recommendation": "cautious",
  "confidence": 0.7,
  "reasoning": "..."
}
```

Los formatos estandarizados evitan traspasos ambiguos, pérdida de información y errores de interpretación. Las colas de mensajes permiten comunicación asíncrona: el investigador publica su resultado y continúa, mientras el analista lo consume cuando está disponible. Este desacoplamiento evita que los agentes dependan de una sincronización directa.

## Flujo de trabajo de análisis colaborativo

### El problema de síntesis del analista

El analista recibe señales simultáneas de noticias, fundamentos, mercado e indicadores técnicos. Su trabajo no consiste en enumerar datos, sino en construir una narrativa coherente:

- Relacionar acontecimientos, como una dimisión directiva y una caída de ingresos.
- Evaluar si una variación de precio es una reacción exagerada o está justificada.
- Resolver conflictos entre resultados positivos, previsiones negativas, noticias favorables y evolución técnica débil.
- Explicar por qué una señal tiene más peso que otra.

Una síntesis responsable también expresa la incertidumbre. Debe distinguir lo conocido de lo desconocido y describir cómo cambiarían las perspectivas si una cuestión pendiente se resolviera positiva o negativamente.

### Traspasos entre agentes en LangGraph

LangGraph representa el flujo como un grafo donde los nodos son agentes y las aristas son traspasos de control. Cuando un agente termina, comunica su resultado y el coordinador activa el siguiente nodo.

Los traspasos pueden ser condicionales:

- Si la confianza es superior a 0,8, el flujo pasa al nodo de decisión.
- Si la confianza es baja, vuelve al investigador para obtener datos adicionales.

La ruta se adapta a los resultados: una investigación insuficiente provoca otra iteración y un análisis claro puede avanzar directamente a la decisión.

El estado también se transfiere. El analista recibe los datos del investigador y el motivo del análisis; el gestor de cartera recibe el análisis junto con las posiciones actuales y las restricciones relevantes. Cada traspaso debe incluir todo lo que el siguiente agente necesita, sin depender de contexto implícito.

### Mecanismos de consenso

Cuando varios analistas discrepan, el sistema necesita una política explícita:

- **Voto mayoritario:** prevalece la recomendación con más votos.
- **Confianza ponderada:** se consideran la recomendación y el nivel de confianza, de modo que una opinión con 90 % de confianza puede pesar más que otra con 60 %.
- **Escalación:** ante discrepancias significativas, el gestor de cartera revisa directamente todos los análisis en lugar de recibir un consenso resumido.

El consenso evita que un único agente domine y hace visible la falta de claridad del equipo. El desacuerdo no es solo un problema: también es una señal de riesgo que puede justificar investigación adicional o revisión humana.

## Generación de señales y riesgo

### Del análisis a la acción

El análisis produce conocimiento; una señal lo transforma en una decisión concreta. Por ejemplo, detectar una reducción de márgenes es un hallazgo, mientras que «comprar 100 acciones a precio de mercado» es una señal accionable.

El gestor de cartera clasifica la situación en **comprar**, **vender** o **mantener**, siempre con razonamiento y límites de riesgo:

- **Comprar:** análisis positivo, capital disponible, posición dentro de los límites, tolerancia al riesgo adecuada y mercado favorable.
- **Vender:** análisis negativo, posición existente, necesidad de reducir exposición y condiciones adecuadas para una salida ordenada.
- **Mantener:** análisis mixto, posición ya óptima, restricciones que impiden cambios o condiciones desfavorables.

La clasificación no depende solo del análisis; combina el estado de la cartera, el riesgo y las condiciones de ejecución.

### Integración del riesgo en la señal

Antes de confirmar una señal se aplican:

- Límites máximos de tamaño de posición.
- Límites de correlación para evitar concentración.
- Restricciones cuando la cartera acumula pérdidas relevantes.
- Ajustes de tamaño o stops para activos muy volátiles.

Una señal positiva puede reducirse a «mantener» o rechazarse si contradice las restricciones de riesgo. La pregunta correcta es qué acción resulta prudente considerando análisis, cartera y contexto, no solo qué recomienda el análisis.

### Flujo completo de decisión

1. Una noticia activa una investigación.
2. El investigador recopila precios, informes, estimaciones, prensa y flujo de opciones.
3. Varios analistas estudian fundamentos, aspectos técnicos y sentimiento.
4. El coordinador sintetiza el consenso.
5. El gestor revisa posiciones y restricciones de riesgo.
6. Genera una señal concreta, por ejemplo comprar 100 acciones con un stop loss del 5 %.
7. La señal se registra y pasa a la cola de ejecución para aprobación humana.

Los mensajes estructurados y el contexto necesario acompañan cada traspaso.

## Colaboración y toma de decisiones entre múltiples agentes

### Ventajas de la arquitectura

La modularidad permite mejorar un investigador, un analista o el gestor de riesgos sin alterar los demás componentes. También facilita la depuración: cada decisión puede rastrearse desde los datos recopilados hasta el análisis, el consenso y las restricciones aplicadas.

Los sistemas multiagente se paralelizan de forma natural. Varios investigadores pueden recopilar datos simultáneamente y varios analistas pueden estudiar distintos aspectos del mismo activo, mientras el orquestador coordina el trabajo.

### Patrones de colaboración

El orquestador debe adaptar el flujo al contexto:

- Investigación rápida cuando no se necesita análisis profundo.
- Análisis individual cuando solo un especialista es relevante.
- Consenso multiagente cuando la decisión requiere perspectivas distintas.
- Especialización por ámbito, como datos bursátiles, opciones o sentimiento de noticias.

Los bucles de retroalimentación permiten mejorar el sistema. Las diferencias recurrentes entre las decisiones del gestor y las recomendaciones de los analistas pueden revelar ajustes necesarios en los modelos. Las omisiones repetidas del investigador pueden indicar que el orquestador debe solicitar nuevas fuentes.

### Gestión de la complejidad

Más agentes implican más puntos de fallo. Para mantener el control se necesitan:

- Protocolos de mensajería sólidos.
- Responsabilidades claramente delimitadas.
- Orquestación que evite bloqueos y esperas indefinidas.
- Métricas de latencia en los traspasos.
- Seguimiento de cuellos de botella y resultados de baja calidad.
- Gestión de estado que conserve solo el contexto relevante.

Cada agente debe recibir exactamente la información necesaria, ni un historial irrelevante enorme ni un contexto insuficiente.

### De la coordinación a la inteligencia colectiva

La colaboración no es solo dividir tareas. El investigador aporta datos de fuentes financieras, el analista interpreta documentos y señales, y el gestor evalúa riesgo y cartera. Mediante protocolos y traspasos estructurados, la combinación puede producir decisiones mejores que las de cualquiera de los componentes aislados.
