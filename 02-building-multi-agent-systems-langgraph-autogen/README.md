# Course 2 — Building Multi-Agent Systems using LangGraph and Autogen

- **Course page:** <https://www.coursera.org/learn/building-multi-agent-systems-langgraph-autogen>
- **Specialization:** [Autonomous AI Agent Systems and Orchestration](https://www.coursera.org/specializations/autonomous-ai-agent-systems-and-orchestration)
- **Provider:** Edureka
- **Duration:** 8 hours (4 modules)
- **Branch:** `course-02-building-multi-agent-systems-langgraph-autogen`

## Overview

Designing systems where several agents reason and collaborate on shared objectives, using LangGraph and AutoGen for communication and coordination.

## Key topics

- Communication strategies between agents
- Coordination mechanisms
- Performance evaluation
- Optimization for scalability

## Assignments

Solutions live in [`assignments/`](assignments).

| Assignment | Status |
|---|---|
| [Practical project — Real-time multi-agent coordinator](assignments/incident-insight-agent) | Completed |

### Practical project: Real-time multi-agent coordinator

This local CLI exercise demonstrates an incident analysis workflow with a single coordinating agent. It combines RAG-style retrieval from a local incident dataset, explainable AST-based heuristic rules, short-term memory and structured audit logging.

The project was executed locally with simulated incidents and includes:

- Historical incident retrieval with TF-IDF.
- Safe rule evaluation through Python AST validation.
- Recommendations based on incident severity.
- Session memory for recent incidents.
- Audit entries for retrieval, rule evaluation and decisions.

## Notes

See [`NOTES.md`](NOTES.md) for my personal notes (in Spanish).
