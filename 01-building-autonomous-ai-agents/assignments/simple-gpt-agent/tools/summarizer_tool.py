class SummarizerTool:
    def run(self, user_input: str) -> str:
        # expect format: "Summarize: <text>"
        parts = user_input.split(':', 1)
        text = parts[1].strip() if len(parts) > 1 else user_input
        # very simple summarization (first sentence/first 20 words)
        words = text.split()
        summary = ' '.join(words[:20]) + ('...' if len(words) > 20 else '')
        return f"Summary: {summary}"
