from agent.gpt_agent import GPTAgent
from memory.memory_manager import MemoryManager
from tools.summarizer_tool import SummarizerTool
from tools.joke_tool import JokeTool
from tools.weather_tool import WeatherTool

def main():
    memory = MemoryManager()
    agent = GPTAgent(memory=memory)
    # register tools
    agent.register_tool("summarize", SummarizerTool())
    agent.register_tool("joke", JokeTool())
    agent.register_tool("weather", WeatherTool())

    print("Simple GPT Agent Demo (type 'exit' to quit)\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAgent: Goodbye!")
            break
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Agent: Goodbye!")
            break
        response = agent.handle(user_input)
        print(f"Agent: {response}\n")

if __name__ == '__main__':
    main()
