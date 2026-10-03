import ast
import json

class SafeEvaluator(ast.NodeVisitor):
    allowed_nodes = (ast.Expression, ast.Compare, ast.Load, ast.Name, ast.Gt, ast.Lt, ast.Eq, ast.Constant, ast.BoolOp, ast.And, ast.Or)

    def visit(self, node):
        if not isinstance(node, self.allowed_nodes):
            raise ValueError("Unsafe expression detected in rules.")
        return super().visit(node)

class RuleEngineAST:
    def __init__(self, rule_file="rules/config.json"):
        with open(rule_file, "r") as f:
            self.rules = json.load(f)

    def evaluate(self, incident: dict, similar_cases: list):
        for rule in self.rules:
            condition = rule["if"]
            action = rule["then"]

            try:
                parsed = ast.parse(condition, mode="eval")
                SafeEvaluator().visit(parsed)

                if eval(condition, {}, {"incident": incident, "similar": similar_cases}):
                    return action
            except Exception as e:
                print(f"Error in rule evaluation: {e}")
                continue

        return "NO_ACTION"

