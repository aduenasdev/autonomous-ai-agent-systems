# Simple Flask + CLI entrypoint for the Multimodal Support Agent demo
from flask import Flask, request, jsonify
from graph.orchestrator import Orchestrator
import threading, argparse

app = Flask(__name__)
orchestrator = Orchestrator()

@app.route('/start_session', methods=['POST'])
def start_session():
    session = orchestrator.create_session()
    return jsonify({'session_id': session}), 201

@app.route('/submit_text', methods=['POST'])
def submit_text():
    data = request.json
    session_id = data.get('session_id')
    text = data.get('text','')
    result = orchestrator.handle_text(session_id, text)
    return jsonify(result), 200

@app.route('/submit_image', methods=['POST'])
def submit_image():
    data = request.json
    session_id = data.get('session_id')
    image_path = data.get('image_path','')
    result = orchestrator.handle_image(session_id, image_path)
    return jsonify(result), 200

def run_server(port=5000):
    app.run(port=port, debug=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--serve', action='store_true', help='Run Flask server')
    args = parser.parse_args()
    if args.serve:
        run_server()
    else:
        # CLI demo
        sid = orchestrator.create_session()
        print(f'Created session: {sid}')
        print('Type "text:<your message>" or "image:<mock path>" or "exit"')
        while True:
            line = input('> ').strip()
            if line == 'exit':
                break
            if line.startswith('text:'):
                text = line.split(':',1)[1].strip()
                out = orchestrator.handle_text(sid, text)
                print(out)
            elif line.startswith('image:'):
                img = line.split(':',1)[1].strip()
                out = orchestrator.handle_image(sid, img)
                print(out)
            else:
                print('Unknown command. Use text:<msg> or image:<path>')
