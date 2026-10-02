from tools.retriever import Retriever
from agent.memory_manager import MemoryManager
from agent.rule_engine_ast import RuleEngineAST
from tools.action_recommender import ActionRecommender
from utils.logger import AuditLogger

class CoreAgent:
    def __init__(self):
        self.rertr = Retriever()
        self.memory = MemoryManager()
        # define safe names used in rules
        self.rule_engine = RuleEngineAST(allowed_names=['cpu_usage','latency_ms','error_count','similarity','recent_count'])
        self.recommender = ActionRecommender()
        self.logger = AuditLogger('CoreAgent')
        # Example rules (evaluated in order). Return action string when rule expr yields True.
        # Expressions must evaluate to a boolean or be an if-expression that returns an action string.
        self.rules = [
            """('CRITICAL' if (cpu_usage > 90 and latency_ms > 500) or error_count > 100 else None)""" ,
            """('MAJOR' if similarity > 0.5 and error_count > 20 else None)""" ,
            """('MINOR' if latency_ms > 300 and cpu_usage > 70 else None)""" ,
            """('INFO')"""
        ]

    def handle_event(self, event):
        # Step 1: retrieve similar incidents
        query = event.get('description','')[:400]
        docs = self.rertr.query(query, top_k=3)
        similarity = docs[0]['score'] if docs else 0.0
        self.logger.log('retrieved', {'incident': event['id'], 'matches': len(docs)})
        # Step 2: update memory
        recent_count = self.memory.count_similar(event['title'])
        self.memory.add(event['id'], event)
        # Step 3: prepare rule context
        ctx = {
            'cpu_usage': event.get('metrics',{}).get('cpu',0),
            'latency_ms': event.get('metrics',{}).get('latency_ms',0),
            'error_count': event.get('metrics',{}).get('errors',0),
            'similarity': similarity,
            'recent_count': recent_count
        }
        action = None
        matched_rule = None
        for r in self.rules:
            try:
                res = self.rule_engine.evaluate(r, ctx)
                self.logger.log('rule_eval', {'rule': r, 'result': res, 'ctx': ctx})
                if isinstance(res, str) and res in ('CRITICAL','MAJOR','MINOR','INFO'):
                    matched_rule = r
                    action = res
                    break
            except Exception as e:
                self.logger.log('rule_error', {'rule': r, 'error': str(e)})
        # Step 4: map to human action
        human_action = self.recommender.recommend(action, docs)
        self.logger.log('decision', {'incident': event['id'], 'action': human_action, 'rule': matched_rule})
        return {'action': human_action, 'matched_rule': matched_rule, 'matches': docs}
