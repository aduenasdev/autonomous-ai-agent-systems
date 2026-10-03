import uuid, time, os, json
from modules.vision_extractor import VisionExtractor
from memory.ltm_retriever import LTM_Retriever
from tools.tool_executor import ToolExecutor

LOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'logs', 'audit.log')
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def log(entry):
    ts = time.strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_PATH, 'a') as f:
        f.write(f'[{ts}] {entry}\n')

class Orchestrator:
    def __init__(self):
        self.sessions = {}
        self.vision = VisionExtractor()
        self.retriever = LTM_Retriever()
        self.executor = ToolExecutor()

    def create_session(self):
        sid = str(uuid.uuid4())[:8]
        self.sessions[sid] = {'memory': []}
        log(f'CREATE_SESSION {sid}')
        return sid

    def handle_text(self, session_id, text):
        s = self.sessions.get(session_id)
        if s is None:
            return {'error':'unknown session'}
        log(f'{session_id} RECEIVED_TEXT: {text}')
        # simple triage: check keywords
        issue_type = 'general'
        if 'cpu' in text.lower():
            issue_type = 'cpu'
        if 'database' in text.lower() or 'db' in text.lower():
            issue_type = 'database'
        # retrieval
        past = self.retriever.find_similar(text)
        log(f'{session_id} RETRIEVAL: found {len(past)} past cases')
        # plan: pick action
        action = self.executor.decide_action(issue_type, text, past)
        log(f'{session_id} DECISION: {action}')
        # update memory
        s['memory'].append({'input':text, 'action':action})
        return {'session':session_id, 'input':text, 'retrieved':past, 'action':action}

    def handle_image(self, session_id, image_path):
        s = self.sessions.get(session_id)
        if s is None:
            return {'error':'unknown session'}
        log(f'{session_id} RECEIVED_IMAGE: {image_path}')
        extracted = self.vision.extract_from_path(image_path)
        log(f'{session_id} VISION_EXTRACT: {extracted}')
        past = self.retriever.find_similar(extracted)
        log(f'{session_id} RETRIEVAL: found {len(past)} past cases')
        issue_type = 'general'
        if 'ERR504' in extracted or 'timeout' in extracted.lower():
            issue_type = 'network'
        action = self.executor.decide_action(issue_type, extracted, past)
        log(f'{session_id} DECISION: {action}')
        s['memory'].append({'input':extracted, 'action':action})
        return {'session':session_id, 'extracted':extracted, 'retrieved':past, 'action':action}
