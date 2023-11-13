from .token import Token

class Node:
    pass

class Number(Node):
    def __init__(self, token: Token):
        self.token = token

    def __str__(self):
        return f"Number ({self.token})"

class BinOp(Node):
    def __init__(self, left: Node, op: Token, right: Node):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"BinOp{self.op.value} ({self.left}, {self.right})"

class UnOp(Node):
    def __init__(self, op: Token, right: Node):
        self.op = op
        self.right = right

    def __str__(self):
        return f"UnOp{self.op.value} ({self.right})"

class Semi(Node):
    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right

    def __str__(self):
        return f"Semi ({self.left}, {self.right})"

class Var(Node):
    def __init__(self, token: Token):
        self.token = token

    def __str__(self):
        return f"Variable ({self.token})"

class Assigment(Node):
    def __init__(self, variable: Var, right: Node):
        self.variable = variable
        self.right = right

    def __str__(self):
        return f"Assigment {self.variable} ({self.right})"

class Empty(Node):
    def __init__(self, token: Token):
        self.token = token

    def __str__(self):
        return f"Empty ({self.token})"
