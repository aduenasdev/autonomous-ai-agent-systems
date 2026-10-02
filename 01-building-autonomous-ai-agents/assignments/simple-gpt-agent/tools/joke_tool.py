class JokeTool:
    def run(self, user_input: str) -> str:
        jokes = [
            "Why did the AI go to therapy? Too many unresolved layers.",
            "I told my computer I needed a break, and it said: 'No problem, I'll go to sleep.'",
            "Why did the neural network cross the road? To get to the other layer!"
        ]
        import random
        return random.choice(jokes)
