# Multimodal Support Agent - Practice Project (Demo)

## Overview
Lightweight, local demo that simulates a multimodal (text + image) support agent.
The agent:
- Accepts text and "image path" inputs (image is simulated)
- Extracts an error code/message from image-path strings (mock vision)
- Retrieves similar past incidents from a local JSON dataset
- Runs mock diagnostic tools and generates recommendations
- Maintains short-term session memory and writes audit logs
- Exposes a simple Flask API and a CLI mode

## Run (CLI)
```
python app.py
```
Then use commands:
- `text:CPU usage critical on backend nodes.`
- `image:mock_err_ERR504.png`

## Run (server)
```
pip install -r requirements.txt
python app.py --serve
```

Endpoints:
- POST /start_session  -> returns session_id
- POST /submit_text   -> JSON {session_id, text}
- POST /submit_image  -> JSON {session_id, image_path}

## Extend
- Add new past cases in data/past_cases.json
- Add more tool behaviors in tools/tool_executor.py
