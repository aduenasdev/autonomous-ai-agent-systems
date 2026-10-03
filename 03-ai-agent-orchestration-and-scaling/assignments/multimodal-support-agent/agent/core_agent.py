from logger import log_event
from rag import retriever
from agent import recommender, rule_engine_ast


def analyze_incident(incident):
    log_event(f"Received Incident: {incident}")

    # Step 1: Retrieve similar incidents
    similar = retriever.get_similar(incident)
    log_event(f"Retrieved {len(similar)} similar incidents")

    # Step 2: Apply rule engine
    decision = rule_engine_ast.evaluate(incident, similar)
    log_event(f"Decision Engine Output: {decision}")

    # Step 3: Recommend action
    action = recommender.recommend(decision)
    log_event(f"Recommended Action: {action}")

    return action
