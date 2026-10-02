# Incident Insight Agent (CLI) — End-to-End
This project is a fully local, command-line simulation of a single Agent that:
- Streams simulated incident logs in real time
- Retrieves similar past incidents (RAG-style) from a local incident DB
- Applies AST-safe heuristic rules to classify severity and recommend actions
- Maintains short-term memory of past incidents in the session
- Logs every decision to logs/audit.log

## Run
```bash
pip install -r requirements.txt
python main.py
```

## Project Structure
- `main.py` - entrypoint (CLI)
- `agent/` - core agent, memory manager, rule engine
- `tools/` - log streamer, retriever (RAG), action recommender
- `data/incidents.json` - mock incident knowledge base
- `utils/logger.py` - audit logger
- `logs/audit.log` - created on run

The system is deliberately self-contained and requires no external APIs.

## Validation

The demonstration runs locally with simulated incidents. The end-to-end test can be executed with:

```bash
python -m pytest -q
```

The AST rule engine accepts boolean `and` and `or` expressions while keeping the allowed syntax restricted.
