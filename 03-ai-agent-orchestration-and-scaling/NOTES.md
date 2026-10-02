# Notas — AI Agent Orchestration and Scaling

Resumen inicial del curso 3, centrado en orquestación con estado, razonamiento multimodal, memoria a largo plazo, gobernanza y escalado.

## Resumen del curso

El curso está orientado a pasar de flujos básicos de agentes a sistemas capaces de interpretar entradas visuales, conservar contexto a largo plazo, replanificar dinámicamente y operar de forma segura, auditable y escalable en producción.

## Módulo 1: Entradas multimodales y orquestación con estado

Este módulo introduce las máquinas de estados de LangGraph, el enrutamiento condicional y el razonamiento multimodal:

- Diferenciar flujos digitales clásicos de agentes autónomos basados en estados.
- Comprender el estado del grafo, los nodos, las aristas y la lógica de enrutamiento.
- Construir y ejecutar un flujo de LangGraph de varios pasos.
- Implementar clasificación de nivel 1 con rutas condicionales.
- Usar modelos de visión para extraer códigos de error de capturas de pantalla.
- Integrar APIs externas con datos de dispositivos, metadatos y señales de diagnóstico.
- Crear un agente de triaje que combine texto, imágenes y señales del sistema.

**Resultado:** diseñar flujos de LangGraph con estado y agentes de triaje que se adapten a entradas visuales y señales en tiempo real.

## Módulo 2: Memoria a largo plazo y replanificación dinámica

Este módulo aborda la memoria episódica y semántica, los grafos de conocimiento y la capacidad de ajustar planes:

- Comprender el papel de la memoria a largo plazo (LTM).
- Modelar relaciones entre usuario, dispositivo y errores mediante grafos de conocimiento.
- Guardar nuevas experiencias y recuperar contexto histórico relevante.
- Usar módulos de memoria de LlamaIndex para consolidación y filtrado.
- Añadir nodos que decidan cuándo recuperar o guardar memoria.
- Incorporar un agente planificador que adapte el flujo según el historial.
- Crear motores de replanificación con bucles de retroalimentación.
- Implementar subgrafos anidados para tareas complejas y jerárquicas.
- Demostrar replanificación basada en LTM en flujos de varios pasos.

**Resultado:** crear agentes sensibles al contexto capaces de conservar experiencia y corregir dinámicamente sus planes.

## Módulo 3: Orquestación, gobernanza y escalabilidad

Este módulo prepara los agentes para producción empresarial:

- Aplicar controles de seguridad a decisiones de alto riesgo.
- Prevenir acciones autónomas irreversibles.
- Integrar nodos de intervención humana en flujos sensibles.
- Automatizar registros de auditoría y decisiones.
- Exponer agentes mediante APIs Flask.
- Desplegar flujos completos de LangGraph en entornos escalables.
- Comparar agentes en el borde con orquestación centralizada en la nube.
- Comprender contenedores y fundamentos de Kubernetes.
- Conectar clasificación, memoria, planificación y herramientas en un agente de soporte.
- Usar LangSmith para observabilidad, depuración y métricas de rendimiento.
- Explorar optimización autónoma y flujos que se mejoran a sí mismos.

**Resultado:** implementar sistemas regulados, observables, auditables y escalables para producción.

## Resumen y proyecto final

El curso unifica razonamiento multimodal, memoria a largo plazo, gobernanza, orquestación y escalado en un agente autónomo de soporte.

El proyecto final integra todos los módulos en un flujo de trabajo de principio a fin y se valida mediante pruebas y evaluaciones de autonomía, seguridad y fiabilidad. Al completarlo, el agente debe demostrar:

- Continuidad contextual.
- Replanificación dinámica.
- Razonamiento visual.
- Intervención humana y gobernanza.
- Auditabilidad.
- Despliegue fiable y escalable.

## Fundamentos de LangGraph y State

### De la colaboración a la autonomía

Los primeros agentes dependían de una persona para indicar cada siguiente paso. Eso es colaboración, no autonomía. Un agente autónomo gestiona su propio flujo de trabajo y decide qué hacer a continuación según el estado y las condiciones del proceso.

LangGraph permite modelar estos flujos como grafos. Los agentes navegan entre estados y toman rutas según decisiones y condiciones, coordinando procesos complejos de varios pasos sin instrucciones manuales en cada etapa.

### Estado del grafo

El estado representa todo lo que el agente conoce en un momento del flujo y funciona como su memoria de trabajo. En un ticket de soporte puede contener:

- Identificador del cliente.
- Descripción del problema.
- Código de error extraído.
- Resultados del diagnóstico.
- Estado de resolución.
- Historial de la conversación.

El estado se conserva al pasar de clasificación a diagnóstico y resolución. Debe definirse mediante un esquema estructurado y tipado, por ejemplo:

```python
{
    "customer_id": str,
    "error_code": str,
    "severity": int,
    "resolved": bool,
}
```

Cada nodo puede añadir información: la clasificación incorpora el código de error, el diagnóstico la causa raíz y la resolución la solución aplicada. Al final, el estado contiene el historial completo del proceso.

### Nodos

Los nodos son operaciones discretas del flujo, como extraer un código de error de una captura, buscar una solución o generar una respuesta para el cliente. Reciben el estado, ejecutan una acción y devuelven el estado actualizado.

Los nodos no se comunican directamente: intercambian información a través del estado. Esta separación permite añadir, eliminar o modificar nodos sin romper el resto del grafo.

Cada nodo debe tener un único propósito. Separar triaje, diagnóstico y resolución hace que cada operación sea más clara, fácil de probar y mantenible.

### Enrutamiento condicional

El enrutamiento estático siempre sigue la misma ruta; el condicional elige el siguiente nodo según lo que haya detectado el anterior:

- Gravedad alta: ruta urgente.
- Gravedad baja: ruta estándar.
- `AUTH_FAIL`: especialista en autenticación.
- `DB_TIMEOUT`: especialista en bases de datos.

Las condiciones leen el estado y determinan el siguiente paso. También pueden crear bucles: si el diagnóstico no encuentra una solución, el flujo vuelve al triaje con una nota que solicita un análisis más profundo. De este modo, el grafo se adapta a lo que funciona y a lo que necesita repetirse.

## Orquestación, gobernanza y ampliación

### Fundamentos de la gobernanza

Cuando los agentes toman decisiones con efectos reales, la gobernanza mantiene la confianza, la fiabilidad y el cumplimiento normativo. En LangGraph, cada nodo puede enviar alertas, modificar datos o activar flujos de trabajo, por lo que las acciones deben estar sujetas a controles explícitos.

La gobernanza incluye:

- Reglas que definen qué acciones están permitidas.
- Puntos de control que validan el estado antes de ejecutar.
- Registro de entradas, salidas y decisiones.
- Supervisión humana para acciones sensibles.
- Métricas de acciones, errores y cambios realizados.

Los nodos de control pueden bloquear, pausar o redirigir el grafo cuando detectan una infracción o un estado inseguro.

### Guardrail para acciones irreversibles

Una **barrera contra acciones irreversibles** intercepta acciones críticas, como eliminar registros, transferir fondos o ejecutar comandos, antes de que se realicen sin autorización.

El guardrail combina:

1. Validaciones automáticas.
2. Comprobación de políticas.
3. Pausa del flujo.
4. Aprobación explícita mediante un nodo supervisor o un operador humano.
5. Reanudación, rechazo o redirección según la decisión.

La barrera debe aplicarse a cualquier nodo que intente modificar datos de producción o ejecutar una operación de alto riesgo.

### Gobernanza de datos y auditabilidad

Cada transición de estado y ejecución de nodo debe generar un registro de auditoría. Estos registros permiten:

- Reconstruir cómo llegó el agente a una decisión.
- Verificar qué entradas y salidas participaron.
- Demostrar cumplimiento de políticas y normativas.
- Diagnosticar incidentes y corregir lógica defectuosa.

Los paneles de control pueden mostrar en tiempo real la frecuencia de acciones, las tasas de error y las modificaciones realizadas por usuarios o agentes.

### Human-in-the-loop (HITL)

Los nodos de traspaso manual son puntos de pausa estructurados. El operador puede revisar las variables de estado, validar el razonamiento y aportar correcciones antes de reanudar el flujo.

Los ejercicios de gobernanza implementan un guardrail de acciones irreversibles y un nodo HITL para demostrar que la automatización puede continuar siendo eficiente sin perder control humano ni responsabilidad.

### De prototipo a producción

La combinación de comprobaciones automáticas, aprobación humana y registros transparentes transforma un prototipo experimental en un sistema listo para producción. Este marco de autonomía responsable permite escalar agentes regulados y auditables hacia despliegues empresariales.
