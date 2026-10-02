import ast
from typing import Any, Dict, List

class RuleEngineAST:
    SAFE_NODES = (
        ast.Expression, ast.IfExp, ast.BinOp, ast.UnaryOp, ast.BoolOp,
        ast.And, ast.Or,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
        ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
        ast.Name, ast.Load, ast.Constant, ast.Tuple, ast.List
    )

    def __init__(self, allowed_names: List[str] = None):
        self.allowed_names = set(allowed_names or [])

    def _check_node(self, node: ast.AST):
        if not isinstance(node, self.SAFE_NODES):
            raise ValueError(f'Unsafe AST node: {node.__class__.__name__}')
        for child in ast.iter_child_nodes(node):
            self._check_node(child)

    def evaluate(self, expr: str, context: Dict[str, Any]):
        tree = ast.parse(expr, mode='eval')
        self._check_node(tree)
        # validate names
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if node.id not in self.allowed_names and node.id not in ('True','False','None'):
                    raise ValueError(f'Name {node.id} not allowed in rule expressions')
        code = compile(tree, '<rule>', 'eval')
        safe_globals = {'__builtins__': {}}
        return eval(code, safe_globals, dict(context))
