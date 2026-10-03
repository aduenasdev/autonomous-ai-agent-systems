# Course 3 — AI Agent Orchestration and Scaling

- **Course page:** <https://www.coursera.org/learn/ai-agent-orchestration-and-scaling>
- **Specialization:** [Autonomous AI Agent Systems and Orchestration](https://www.coursera.org/specializations/autonomous-ai-agent-systems-and-orchestration)
- **Provider:** Edureka
- **Duration:** 8 hours
- **Branch:** `course-03-ai-agent-orchestration-and-scaling`
- **Status:** Completed

## Overview

Orchestration frameworks, long-term memory, multimodal input, governance, and deployment and scaling of production agent systems.

## Key topics

- Long-term memory (episodic and semantic) and knowledge graphs
- Retrieval, integration and dynamic replanning
- Multimodal input (vision LLMs) and stateful orchestration with LangGraph
- Governance, guardrails and human-in-the-loop
- Deployment with Flask, Docker and Kubernetes; edge vs. cloud scaling

## Assignments

Solutions live in [`assignments/`](assignments).

| Assignment | Status |
|---|---|
| [Practical project — Multimodal autonomous support agent](assignments/multimodal-support-agent) | Completed |

### Practical project: Multimodal autonomous support agent

A lightweight local demo of a support agent that handles text and screenshots. It can run as a CLI or as a Flask API (`python app.py --serve`).

It includes:

- A mock vision extractor that reads error codes (e.g. `ERR504`) from image names.
- Retrieval of similar past incidents from a local JSON dataset.
- Rule-based triage and recommendations with a confidence score.
- Short-term session memory.
- An audit log of every input, retrieval and decision.

The provided project is a simplified version: it does not use LangGraph nodes, replanning or a human handoff, which are covered in the course notes.

## Notes

See [`NOTES.md`](NOTES.md) for my personal notes (in Spanish).
