class ToolExecutor:
    """Executes simple rule-based support actions based on issue type and past cases."""

    def decide_action(self, issue_type, text, past_cases):
        # simple rule-based decision
        if issue_type == 'cpu':
            return {'recommendation': 'Scale up workers', 'confidence': 0.8}

        if issue_type == 'database':
            return {'recommendation': 'Check DB pool and slow queries', 'confidence': 0.85}

        if issue_type == 'network':
            return {'recommendation': 'Restart gateway / check upstream', 'confidence': 0.9}

        # fallback: if past case suggests resolution, use it
        if past_cases:
            return {'recommendation': past_cases[0]['resolution'], 'confidence': 0.7}

        return {
            'recommendation': 'Open support ticket / escalate to DevOps',
            'confidence': 0.5
        }


def decide_action(issue_type, text, past_cases):
    """Backward-compatible function wrapper for existing direct imports."""
    return ToolExecutor().decide_action(issue_type, text, past_cases)
