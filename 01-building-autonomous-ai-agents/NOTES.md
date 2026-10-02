# Notas — Building Autonomous AI Agents

Notas personales (en español) del curso 1.

## Resumen: The Agentic Foundation (ReAct & Tool Use)

### Introducción

Los fundamentos de la IA agéntica (ReAct y uso de herramientas) establecen las bases conceptuales y técnicas para comprender los sistemas modernos de IA agéntica. El módulo presenta la evolución de los agentes autónomos, explica en qué se diferencian de los modelos de lenguaje a gran escala (LLM) tradicionales y describe los principios que permiten a los agentes razonar, actuar y adaptarse en entornos del mundo real.

Se explora **ReAct**, el marco unificado de razonamiento y acción, y se adquiere experiencia práctica en el desarrollo de herramientas y la integración de la memoria a corto plazo para flujos de trabajo coherentes de varios pasos.

### Fundamentos de la IA agéntica

La IA agéntica marca un cambio desde la generación estática de texto hacia una inteligencia dinámica y orientada a objetivos. Los LLM tradicionales funcionan solo a partir de respuestas a indicaciones (prompts); los sistemas agénticos están diseñados para **planificar, actuar, observar y adaptarse**, lo que les permite realizar tareas estructuradas de varios pasos de forma autónoma.

En el centro está el marco **ReAct**, que integra el razonamiento («pensamiento») con la acción (uso de herramientas). Los sistemas agénticos usan arquitecturas modulares que combinan modelos de lenguaje, APIs, herramientas y lógica de decisión.

Ejemplo práctico: en los flujos de trabajo de un representante de desarrollo de ventas (SDR), los agentes pueden investigar prospectos de forma autónoma, interpretar datos del CRM y redactar mensajes de contacto, manteniendo **transparencia y trazabilidad** en sus pasos de razonamiento.

### Desarrollo de herramientas y acción

El uso de herramientas es una característica definitoria de la inteligencia agéntica. Un LLM por sí solo puede analizar o explicar conceptos; las herramientas permiten al agente interactuar con el mundo exterior: bases de datos, APIs, motores de cálculo.

Una herramienta puede ser desde una función simple hasta un envoltorio de servicio complejo. Las herramientas eficaces comparten:

- Un **propósito y alcance claros**.
- **Esquemas de entrada y salida** bien definidos.
- **Documentación exhaustiva** que describe su uso.

Se suelen usar **modelos Pydantic** para validar las entradas de forma estructurada, con seguridad de tipos y comportamiento predecible. Esto evita fallos en tiempo de ejecución y ayuda al agente a invocar las herramientas de forma fiable durante su razonamiento.

En el curso se construyen herramientas como utilidades de búsqueda web o conectores CRM. Integradas en ReAct, permiten al modelo pasar de generar texto de forma pasiva a **operar de forma activa**: recuperar información, tomar decisiones y ejecutar acciones con relevancia contextual.

### Implementación de ReAct y memoria

El bucle ReAct conecta el razonamiento interno con la acción externa. El razonamiento se guía con prompts estructurados que describen cuándo y cómo realizar cada paso. Cada iteración sigue la secuencia:

**Pensamiento → Acción → Observación**

| Fase | Qué hace el agente |
|---|---|
| **Pensamiento** | Evalúa los datos disponibles y decide el siguiente paso lógico |
| **Acción** | Invoca una herramienta o ejecuta un comando |
| **Observación** | Incorpora los resultados de la herramienta a su contexto de razonamiento |

La **memoria** es fundamental para mantener flujos de varios pasos coherentes. La **memoria a corto plazo (de trabajo)** conserva las acciones, observaciones y decisiones recientes dentro de una sesión. Al retener este contexto, el agente evita acciones redundantes, garantiza coherencia y facilita un razonamiento más profundo.

En la práctica, la memoria se implementa con **objetos de estado** o **búferes contextuales** a corto plazo que evolucionan con la toma de decisiones del agente. Combinada con herramientas bien diseñadas y la lógica ReAct, da lugar a agentes adaptativos y sensibles al contexto.

### RAG, herramientas y generación fundamentada

La construcción de sistemas de inteligencia artificial autónomos, confiables y precisos requiere combinar la arquitectura **RAG (Retrieval-Augmented Generation)** con herramientas adecuadas y una estrategia de redacción fundamentada.

#### Arquitectura RAG y procesamiento de datos

Los documentos sin procesar no son directamente útiles para una IA. Antes deben pasar por un flujo de ingestión que incluye:

1. **Carga** de los documentos.
2. **División en fragmentos** manejables.
3. **Creación de embeddings** para representar semánticamente el contenido.
4. **Indexación** para permitir búsquedas relevantes.

Estos pasos permiten recuperar información contextual y reducen el riesgo de respuestas irrelevantes o inventadas. RAG proporciona al modelo acceso a información específica de la organización que no estaba presente en sus datos de entrenamiento.

#### Integración de herramientas y actuadores

Las herramientas permiten que el modelo no solo consulte información, sino que también actúe sobre sistemas externos. Es importante distinguir entre:

- **Herramientas de solo lectura**, que consultan información sin modificar el estado de los sistemas.
- **Actuadores**, que ejecutan acciones o modifican datos en sistemas externos.

Los actuadores requieren validación de entradas, restricciones claras y, cuando sea necesario, revisión humana. Estas medidas protegen la integridad de los datos y reducen el impacto de errores del modelo.

#### Redacción basada en estrategia

Para evitar que la IA genere contenido ficticio, la generación de respuestas puede organizarse en tres fases:

1. Traducir la solicitud del usuario en búsquedas precisas.
2. Recuperar y verificar la información relevante.
3. Redactar la respuesta con citas obligatorias de las fuentes utilizadas.

Este proceso mantiene las salidas ancladas en el conocimiento real de la organización y aumenta su confianza, trazabilidad y consistencia.

#### Importancia del enfoque RAG

La combinación de una buena ingestión de datos, herramientas correctamente diseñadas y redacción fundamentada es clave para evitar respuestas erróneas. El resultado son agentes más confiables, alineados con la estrategia empresarial y capaces de trabajar con el contexto específico del negocio.

## Orquestación, validación y despliegue con LangGraph

### Construcción de una máquina de estados

Los flujos de trabajo necesitan estructura cuando cada acción depende de lo ocurrido anteriormente. En un proceso de ventas, por ejemplo, no se debe llamar repetidamente a un prospecto, saltarse la calificación ni avanzar directamente hasta un trato ganado.

Una **máquina de estados** define dónde se encuentra el agente y qué transiciones son válidas:

- Los **nodos** representan posiciones del flujo, como «Prospecto identificado», «Comprometido», «Objeción», «Demostración programada» o «Cliente descartado».
- Los **bordes** representan las conexiones permitidas entre nodos.
- Cada borde puede tener condiciones y una acción asociada, como enviar una invitación de calendario al programar una demostración.

El estado debe contener solo la información relevante para la decisión actual. Por ejemplo, al gestionar una objeción son importantes la objeción, la característica relacionada y el contraargumento; los datos irrelevantes deben excluirse. También puede imponer restricciones temporales, como esperar 24 horas antes de realizar un seguimiento.

Un flujo SDR puede recorrer estados como:

**Prospecto identificado → Calificado → Intento de llamada → Respondido/Correo de voz/Número incorrecto/No llamar → Comprometido → Objeción o Interesado → Demostración o Materiales**.

El mapa completo de resultados evita que el agente se desvíe o se salte pasos.

### Control avanzado y autocorrección

Seguir una ruta válida no garantiza que las decisiones sean correctas. Por eso se incorporan barreras de validación:

- **Nodos de validación:** el agente debe justificar una decisión con criterios y evidencias; un evaluador comprueba que la evidencia no sea inventada.
- **Bucles de reflexión:** si una respuesta no resuelve la objeción, la validación devuelve comentarios y el agente la revisa. Normalmente son necesarios dos o tres intentos.
- **Aristas condicionales:** la ruta se decide mediante comprobaciones de contexto, como distinguir una objeción real de una demora o impedir nuevas llamadas después de varios intentos.
- **Puntos de control humanos:** las decisiones de alto riesgo requieren aprobación o redirección humana, por ejemplo ofertas superiores a 500 000 $, comunicaciones confidenciales o eliminación de contactos.

Así, el agente investiga, propone y aprende de la retroalimentación, mientras las personas mantienen el control sobre las decisiones importantes.

### Produccionalización del agente

Un agente que funciona en un portátil puede fallar en producción si no se diseña para errores, concurrencia y escala.

#### Escrituras atómicas

Al actualizar un CRM, se debe construir y validar primero el registro completo y realizar después una escritura atómica dentro de una transacción. Si falla una parte, toda la operación se revierte: el registro queda completo o no existe, pero nunca parcialmente guardado.

#### API y errores operativos

Una API RESTful, por ejemplo con FastAPI, permite separar el agente de los consumidores del sistema. Un endpoint como `POST /prospect/qualify` recibe los datos, ejecuta la calificación y devuelve una respuesta versionada. Los errores deben ser explícitos y accionables, como campos ausentes, cola llena o modo de mantenimiento.

#### Fallo controlado

Los sistemas de producción deben contemplar:

- Tiempos de espera para no bloquearse indefinidamente.
- Reintentos con retroceso exponencial, por ejemplo 1, 2 y 4 segundos.
- Disyuntores que detengan llamadas a dependencias que están fallando.
- Colas asíncronas para aceptar trabajo rápidamente y procesarlo en segundo plano.

#### Monitorización y escalado

Es necesario medir latencia, errores, rutas de decisión y registros de ejecución, y configurar alertas para umbrales como una tasa de error superior al 5 % o una cola de más de 1 000 tareas. Para escalar se pueden usar balanceadores, varias instancias en contenedores, Redis para estado compartido y agrupación de conexiones de base de datos. También deben controlarse las condiciones de carrera cuando varios agentes actualizan el mismo prospecto.

#### Orquestación de múltiples agentes

Varios agentes especializados pueden coordinarse mediante las transiciones de la máquina de estados. El agente de calificación escribe el estado en un punto de entrada; el agente de objeciones lo lee desde allí. No necesitan comunicación directa, lo que mantiene una separación clara entre responsabilidades.

### Resumen del módulo

El módulo 1 une la comprensión conceptual con la implementación práctica: arquitectura agéntica, herramientas, ReAct, memoria, RAG, máquinas de estados, validación, supervisión humana y despliegue confiable. La disciplina de producción —escrituras atómicas, APIs, fallo controlado, monitorización, escalado y orquestación— es la que transforma un prototipo en un sistema fiable.
