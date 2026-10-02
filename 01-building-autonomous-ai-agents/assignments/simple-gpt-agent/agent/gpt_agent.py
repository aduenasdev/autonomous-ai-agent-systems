import os
import unicodedata
try:
    import openai
except Exception:
    openai = None
from dotenv import load_dotenv
import re

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class GPTAgent:
    def __init__(self, memory):
        self.memory = memory
        self.tools = {}
        self.tool_aliases = {
            'summarize': ('summarize', 'summary', 'resumir', 'resume', 'resumen'),
            'joke': ('joke', 'chiste', 'broma', 'curiosidad'),
            'weather': ('weather', 'clima', 'tiempo meteorológico', 'tiempo'),
        }

        # Configure OpenAI if key present
        if OPENAI_API_KEY and openai is not None:
            openai.api_key = OPENAI_API_KEY

    def register_tool(self, name, tool):
        self.tools[name] = tool

    def _call_openai(self, prompt, model='gpt-3.5-turbo'):
        if openai is None:
            return self._simulate_response(prompt)
        try:
            resp = openai.ChatCompletion.create(
                model=model,
                messages=[{'role':'user','content':prompt}],
                max_tokens=200,
                temperature=0.7
            )
            return resp['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"[Simulated GPT fallback due to error: {str(e)}] {self._simulate_response(prompt)}"

    def _simulate_response(self, prompt):
        # Very basic rule-based fallback
        low = prompt.lower()
        if 'summarize' in low:
            words = prompt.split()
            return 'Summary: ' + ' '.join(words[:20]) + ('...' if len(words) > 20 else '')
        if 'joke' in low:
            return 'Why did the neural network cross the road? To get to the other layer!'
        if 'weather' in low:
            return 'Simulated weather: 20°C, Clear.'
        return "I'm a simulated agent. Provide a clearer prompt or set OPENAI_API_KEY to get real GPT responses."

    def _use_tool(self, user_input):
        for name, tool in self.tools.items():
            aliases = self.tool_aliases.get(name, (name,))
            pattern = '|'.join(re.escape(alias) for alias in aliases)
            if re.search(rf"\b(?:{pattern})\b", user_input, flags=re.IGNORECASE):
                try:
                    return tool.run(user_input)
                except Exception as e:
                    return f"Tool '{name}' error: {e}"
        return None

    def _memory_response(self, user_input):
        normalized = ''.join(
            character
            for character in unicodedata.normalize('NFD', user_input.lower())
            if unicodedata.category(character) != 'Mn'
        )
        asks_last = any(
            phrase in normalized
            for phrase in (
                'what did i just ask',
                'what was my last question',
                'que te acabo de preguntar',
                'cual fue mi ultima pregunta',
            )
        )
        asks_all = any(
            phrase in normalized
            for phrase in (
                'what have i asked',
                'remember our conversation',
                'recuerdame nuestra conversacion',
                'que te he preguntado',
                'que te pregunte',
            )
        )
        previous_requests = self.memory.user_messages()[:-1]
        if asks_last:
            if not previous_requests:
                return "Aún no hay una interacción anterior en esta sesión."
            return f"Tu última solicitud fue: {previous_requests[-1]}"
        if asks_all:
            if not previous_requests:
                return "Aún no hay solicitudes anteriores en esta sesión."
            items = '\n'.join(
                f"{index}. {request}"
                for index, request in enumerate(previous_requests, start=1)
            )
            return f"Solicitudes de esta sesión:\n{items}"
        return None

    def handle(self, user_input):
        self.memory.add({'user': user_input})
        memory_result = self._memory_response(user_input)
        if memory_result:
            self.memory.add({'agent': memory_result})
            return memory_result

        tool_result = self._use_tool(user_input)
        if tool_result:
            self.memory.add({'agent': tool_result})
            return tool_result

        if OPENAI_API_KEY and openai is not None:
            prompt = f"You are an assistant. User said: {user_input}"
            resp = self._call_openai(prompt)
        else:
            resp = self._simulate_response(user_input)
        self.memory.add({'agent': resp})
        return resp
