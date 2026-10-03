class Recommender:
    def __init__(self):
        self.action_map = {
            "RESTART_SERVICE": "Restart the affected service immediately.",
            "SCALE_RESOURCES": "Scale up infrastructure capacity.",
            "ESCALATE": "Escalate to the DevOps/SRE team.",
            "CHECK_LOGS": "Review logs for deeper diagnostics.",
            "NO_ACTION": "No significant action required at this time."
        }

    def recommend(self, decision: str):
        return self.action_map.get(decision, "No valid recommendation available.")
