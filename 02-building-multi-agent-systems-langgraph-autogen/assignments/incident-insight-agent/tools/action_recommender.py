class ActionRecommender:
    def __init__(self):
        pass
    def recommend(self, severity_label, matches):
        if severity_label == 'CRITICAL':
            return 'Scale service, open priority incident, roll back recent deploys if correlated'
        if severity_label == 'MAJOR':
            return 'Notify on-call, increase replicas, throttle traffic to service'
        if severity_label == 'MINOR':
            return 'Create ticket, monitor metrics, consider investigation in non-peak hours'
        return 'Log for awareness; no immediate action'
