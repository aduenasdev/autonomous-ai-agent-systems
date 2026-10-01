# Notas — Building Autonomous AI Agents

Notas personales (en español) del curso 1.

## Introducción

La evolución de la inteligencia artificial va desde los modelos de lenguaje simples hasta los **agentes autónomos**, capaces de razonar, actuar y aprender en tiempo real.

## Agentes de IA vs. modelos de lenguaje

| | Modelo de lenguaje (LLM) | Agente de IA |
|---|---|---|
| **Qué hace** | Genera texto a partir de patrones en los datos | Usa un LLM como motor de razonamiento, y además planifica, actúa y decide |
| **Intención** | Ninguna: no tiene intención ni conciencia | Persigue objetivos específicos |
| **Entorno** | No interactúa con sistemas externos | Interactúa con herramientas y sistemas externos |
| **Memoria** | No tiene | Puede mantenerla |

## Limitaciones de los modelos de lenguaje tradicionales

- Dependen de **indicaciones (prompts) estáticas**, lo que dificulta el razonamiento complejo y la adaptación a lo largo del tiempo.
- No tienen **memoria persistente**.
- No pueden **verificar ni mejorar sus respuestas mediante acciones**, así que requieren intervención humana constante.

## El enfoque ReAct: la siguiente generación

**ReAct = Reason + Act (Razonar y Actuar).** Combina razonamiento y acción en un ciclo iterativo y continuo:

1. **Pensar** sobre el problema.
2. **Actuar**: ejecutar código, consultar datos, llamar a APIs, usar herramientas externas.
3. **Aprender** de los resultados de esas acciones y volver a razonar.

```
   ┌──────────► Razonar (Thought) ──────────┐
   │                                        ▼
Observar (Observation)              Actuar (Action)
   ▲                                        │
   └────────── Resultado de la herramienta ◄┘
```

Esto transforma un modelo estático en un **sistema autónomo y adaptativo**: de generador pasivo de texto a un sistema que interactúa con herramientas externas y se adapta dinámicamente para resolver problemas complejos.

## Ideas clave

- Un agente = LLM + planificación + herramientas + memoria + bucle de decisión.
- ReAct es el patrón base sobre el que se construyen los frameworks de agentes.
- La acción permite verificar y corregir: el agente no depende de que el humano revise cada paso.
