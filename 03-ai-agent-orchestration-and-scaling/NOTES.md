# Notas — AI Agent Orchestration and Scaling

Notas personales (en español) del curso 3. Organizadas por tema, no por orden de lección.

## 1. Memoria a largo plazo (LTM) y replanificación

### Memoria episódica y semántica

La LTM guarda experiencias, datos aprendidos y resultados de tareas, y **persiste entre sesiones** (la memoria a corto plazo solo dura una sesión).

| Tipo | Qué guarda | Permite |
|---|---|---|
| **Episódica** | Experiencias: diálogos, historiales de tareas, estados del entorno | Recordar «lo que ocurrió» |
| **Semántica** | Conocimiento general: conceptos, relaciones, reglas de dominio | Razonar más allá de eventos aislados |

### Grafos de conocimiento (KG)

- Columna vertebral de la memoria semántica: **entidades** (usuarios, herramientas, errores) y **relaciones** (causas, dependencias, similitudes).
- Recorrer el grafo permite encontrar experiencias relacionadas y la **causa raíz** de problemas recurrentes (p. ej. una configuración que falla siempre → avisar de forma preventiva).
- Cada evento se guarda con embeddings contextuales (tarea, timestamp, éxito/fallo) y se enlaza en el KG. Consultar = **búsqueda semántica**.

### Recuperación e integración

1. **Codificar** el contexto actual (vector o representación simbólica).
2. **Coincidencia semántica:** búsqueda por similitud o recorrido del grafo.
3. **Ranking** por recencia, tasa de éxito y solapamiento contextual.

Lo recuperado se **integra**, no se pega: el planificador decide si reutiliza una estrategia pasada o genera una nueva. La **consolidación** fusiona datos redundantes (módulos de memoria de LlamaIndex). Ventajas: continuidad, adaptabilidad y eficiencia.

### Autocorrección y flujo dinámico

- **Replanificación:** el nodo de replanificación detecta desvíos y actualiza el plan **sin reiniciar el workflow**.
- **Feedback:** señales explícitas (valoraciones, correcciones) e implícitas (éxito de la interacción) se escriben en la LTM: refuerzan lo que funciona y restan prioridad a lo que falla.
- **Subgrafos:** los objetivos complejos se dividen en subgrafos anidados, para replanificar una subtarea sin tocar la misión global.

**Idea clave:** LTM + replanificación = paso de la autonomía reactiva a la proactiva.

## 2. Agente multimodal con estado

### Visión y herramientas

- Un **LLM de visión** lee capturas (incluso borrosas o parciales) y, además de extraer el texto, lo **interpreta** (código de error → gravedad → acción).
- El nodo de visión devuelve salida estructurada `{error_code, error_message, additional_context}` y, si la imagen no sirve, lo dice y sigue solo con texto.
- Las herramientas externas (`check_system_status`, `query_inventory`, `validate_credentials`…) necesitan **contratos claros** (entradas, salidas, errores) y manejo de fallos: si una API da timeout, el agente continúa con un diagnóstico local.

### Orquestación de varias herramientas

- El orden de las herramientas es **dinámico**: tras cada llamada el agente razona «con lo que sé, ¿qué necesito después?». Si el RAG ya da una solución definitiva, se omite el check de estado.
- Si fallan todas las vías, reconoce la laguna y **deriva a un humano**.

### Flujo de un ticket

| Nodo | Aporta al estado |
|---|---|
| Visión | Código de error de la captura |
| Clasificación | Categoría y gravedad (texto + imagen), con **puntuación de confianza** |
| Enrutamiento | Alta gravedad → ruta urgente; baja → estándar |
| Diagnóstico | Herramienta según categoría (auth, pagos, base de datos) |
| Resolución | Respuesta que sintetiza todo el estado |

- Confianza alta: texto e imagen coinciden. Baja: se contradicen o faltan datos → revisión humana.
- Si falta información (p. ej. una captura), el agente la pide.

### Por qué el estado importa

| Sin estado | Con estado |
|---|---|
| Olvida el contexto y repite diagnósticos | Comprensión progresiva y referencias al contexto previo |
| Pide al cliente repetir información | Conversaciones coherentes de varios turnos |
| Guion rígido | Puede pausar, reanudar, volver atrás y escalar a un humano **conservando el contexto** |

Además, una **interfaz de chat simulada** (con historial y estado visible: qué extrajo, qué herramientas usó, qué decidió) sirve para probar sin montar una interfaz de producción.

**Multimodal = más precisión e igualdad:** una captura es un hecho objetivo («botón desactivado») y ayuda tanto a quien sabe describir el problema como a quien no.

## 3. Gobernanza, despliegue y escalado

### Gobernanza

- **Irreversible Action Guardrails:** puntos de control que interceptan los workflows de alto riesgo antes de una acción irreversible.
- **Human-in-the-loop (HITL):** el workflow se detiene hasta que un humano valida.
- **Auditoría y linaje:** registro automático de cada decisión, resultado y transición de estado → cumplimiento y razonamiento explicable.

### Despliegue

- **Flask** expone el workflow de LangGraph como API: cada solicitud lanza una ejecución nueva o reanuda un estado persistente (sin estado de cara al cliente, con estado en el backend). Va detrás de un balanceador.
- **Docker** empaqueta cada instancia con sus dependencias; **Kubernetes** automatiza despliegue, **autoescalado** y **autorreparación**.

| Escalado | Ventajas | Encaja en |
|---|---|---|
| **Edge** (cerca de los datos) | Menor latencia, más privacidad | Decisiones locales, cumplimiento estricto |
| **Nube** | Escalado elástico, monitorización unificada | Cómputo centralizado, alcance global |

Lo habitual es un **sistema híbrido**. Diseñar desde el principio pensando en resiliencia, observabilidad y escalabilidad.

### Integración final

Un agente completo tiene seis capas: **entrada** (multimodal) → **razonamiento** (LangGraph) → **herramientas** → **memoria** (LTM, vectores) → **gobernanza** → **interfaz de despliegue**. El estado compartido del grafo las conecta.

- **Validación:** inspección de estado, sesiones de usuario simuladas y pruebas de estrés; los logs de gobernanza ayudan a depurar.
- **Próximos pasos:** reentrenamiento dinámico con feedback real, **meta-orquestación** (agentes que coordinan agentes) y escalado predictivo.

La autonomía no sale de un único modelo potente, sino de la **interacción de componentes estructurados**.

## 4. Proyecto práctico

[`assignments/multimodal-support-agent`](assignments/multimodal-support-agent): demo de un agente de soporte con texto e imágenes simuladas, recuperación de casos pasados (JSON), herramientas simuladas, memoria de sesión, audit log y API Flask. El código del curso es una versión simplificada: el orquestador usa reglas por palabras clave, no un grafo de LangGraph completo.
