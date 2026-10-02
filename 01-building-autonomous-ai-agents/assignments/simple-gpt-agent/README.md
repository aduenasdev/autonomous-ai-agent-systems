# Simple GPT Agent Demo (Simulated Weather)

## Overview
This demo is a small, modular GPT-powered agent. It will call the OpenAI API if you provide an API key in a `.env` file; otherwise it will fall back to simulated responses. Weather is simulated (no external weather API required).

## Features
- GPT reasoning via OpenAI (if API key present)
- Tools: summarizer, joke generator, simulated weather
- In-memory conversation history
- CLI interface
- Spanish and English tool prompts
- Session-memory queries such as "¿Qué te acabo de preguntar?"

## Setup
1. (Optional) Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS / Linux
   venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```
2. (Optional) If you want real GPT responses, copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.example .env
   # then edit .env and set OPENAI_API_KEY=your_key
   ```
3. Run the demo:
   ```bash
   python main.py
   ```

## Example Prompts
- `Summarize: <text>` → uses summarizer tool
- `Tell me a joke` → uses joke tool
- `What's the weather in London?` → uses simulated weather tool
- `¿Qué tiempo hace en Delhi?` → uses simulated weather tool
- `¿Qué te he preguntado hasta ahora?` → reads the current session memory
- Any other question is sent to GPT (or simulated fallback)
