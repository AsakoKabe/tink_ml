import ast
from _ast import AST


def remove_docstring(tree: AST) -> None:
    for node in ast.walk(tree):
        # let's work only on functions & classes definitions
        if not isinstance(
                node,
                (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)
        ):
            continue

        if not len(node.body):
            continue

        if not isinstance(node.body[0], ast.Expr):
            continue

        if not hasattr(node.body[0], 'value') or not isinstance(
                node.body[0].value, ast.Str):
            continue

        node.body = node.body[1:]


class MyVisitor(ast.NodeVisitor):
    def visit_ClassDef(self, node):
        node.body = sorted(
            node.body,
            key=lambda x: x.name if hasattr(x, 'name') else ''
        )
        return node


def sort_methods(tree: AST) -> None:
    MyVisitor().visit(tree)


def normalizing_code(code: str) -> str:
    tree = ast.parse(code)
    remove_docstring(tree)
    sort_methods(tree)
    normalized_code = ast.dump(tree)

    return normalized_code
