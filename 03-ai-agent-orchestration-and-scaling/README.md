# Course 3 — AI Agent Orchestration and Scaling

- **Course page:** <https://www.coursera.org/learn/ai-agent-orchestration-and-scaling>
- **Specialization:** [Autonomous AI Agent Systems and Orchestration](https://www.coursera.org/specializations/autonomous-ai-agent-systems-and-orchestration)
- **Provider:** Edureka
- **Level:** Advanced
- **Duration:** 8 hours (4 modules)
- **Branch:** `course-03-ai-agent-orchestration-and-scaling`
- **Status:** Completed

## Overview

Takes a multi-agent system from a working prototype to a production service: multimodal input, stateful orchestration with LangGraph, long-term memory, dynamic replanning, governance, and deployment and scaling. It closes with a capstone that integrates everything into one autonomous support agent.

## Learning outcomes

- Design orchestration frameworks that coordinate autonomous agents.
- Implement scaling strategies for high-performance multi-agent systems.
- Monitor and evaluate agent workflows for consistency and reliability.
- Build agents that learn, adapt and optimize over time.

## Modules

| # | Module | Main topics |
|---|---|---|
| 1 | Multimodal Inputs and Stateful Orchestration | LangGraph fundamentals, vision LLMs, multimodal reasoning, external API tools, diagnostic triage agents |
| 2 | Long-Term Memory and Dynamic Re-Planning | Episodic vs. semantic memory, knowledge graphs, retrieval and integration (LlamaIndex), self-correction, feedback loops, nested subgraphs |
| 3 | Orchestration, Governance and Scaling | Guardrails, audit trails, human-in-the-loop, Flask API, Docker and Kubernetes, edge vs. cloud scaling, monitoring |
| 4 | Course Wrap-Up and Assessment | Capstone: autonomous multimodal support agent |

## Key topics

- Stateful orchestration with LangGraph: shared state, conditional routing, pausing and resuming.
- Vision LLMs that extract structured data (error codes) from screenshots.
- Multi-tool orchestration with fallbacks and handoff to a human.
- Long-term memory: episodic and semantic memory, knowledge graphs, semantic retrieval and ranking.
- Dynamic replanning and feedback loops that write back into memory.
- Governance: irreversible-action guardrails, human-in-the-loop and audit logs.
- Deployment with Flask, Docker and Kubernetes; autoscaling and self-healing.

## Skills and tools

Generative AI agents, agentic systems, memory management, AI integrations, prompt engineering, model deployment. Tools: LangGraph, LlamaIndex, Flask, Docker, Kubernetes.

## Assignments

Solutions live in [`assignments/`](assignments).

| Assignment | Status |
|---|---|
| [Practical project — Multimodal autonomous support agent](assignments/multimodal-support-agent) | Completed |

### Practical project: Multimodal autonomous support agent

A lightweight local demo of a support agent that handles text and screenshots. It runs as a CLI (`python app.py`) or as a Flask API (`python app.py --serve`).

It includes:

- A mock vision extractor that reads error codes (e.g. `ERR504`) from image names.
- Retrieval of similar past incidents from a local JSON dataset.
- Rule-based triage and recommendations with a confidence score.
- Short-term session memory per conversation.
- An audit log of every input, retrieval and decision.
- A Dockerfile to run the API in a container.

The provided project is a simplified version: it does not use LangGraph nodes, replanning or a human handoff. Those parts are covered in the course notes.

## Notes

See [`NOTES.md`](NOTES.md) for my personal notes (in Spanish).
