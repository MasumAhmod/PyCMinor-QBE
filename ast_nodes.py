
from dataclasses import dataclass, field
from typing import List, Optional


# ==========================================
# 1. BASE AST NODE
# ==========================================

@dataclass
class ASTNode:
    """Base class for all AST nodes."""
    pass


# ==========================================
# 2. PROGRAM AND FUNCTION NODES
# ==========================================

@dataclass
class Program(ASTNode):
    """Represents the complete CMinor program."""
    declarations: List[ASTNode] = field(default_factory=list)


@dataclass
class Function(ASTNode):
    """Represents a function declaration."""
    return_type: str
    name: str
    parameters: List[ASTNode] = field(default_factory=list)
    body: Optional[ASTNode] = None


@dataclass
class Parameter(ASTNode):
    """Represents a function parameter."""
    param_type: str
    name: str


# ==========================================
# 3. VARIABLE DECLARATION
# ==========================================

@dataclass
class VariableDeclaration(ASTNode):
    """Represents a variable declaration."""
    var_type: str
    name: str
    initializer: Optional[ASTNode] = None


# ==========================================
# 4. STATEMENT NODES
# ==========================================

@dataclass
class Block(ASTNode):
    """Represents a block of statements."""
    statements: List[ASTNode] = field(default_factory=list)


@dataclass
class ExpressionStatement(ASTNode):
    """Represents an expression followed by a semicolon."""
    expression: Optional[ASTNode] = None


@dataclass
class ReturnStatement(ASTNode):
    """Represents a return statement."""
    expression: Optional[ASTNode] = None


@dataclass
class IfStatement(ASTNode):
    """Represents an if-else statement."""
    condition: ASTNode
    then_branch: ASTNode
    else_branch: Optional[ASTNode] = None


@dataclass
class WhileStatement(ASTNode):
    """Represents a while loop."""
    condition: ASTNode
    body: ASTNode


# ==========================================
# 5. EXPRESSION NODES
# ==========================================

@dataclass
class BinaryExpression(ASTNode):
    """Represents binary operations like a + b."""
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class UnaryExpression(ASTNode):
    """Represents unary operations like -a or !a."""
    operator: str
    operand: ASTNode


@dataclass
class AssignmentExpression(ASTNode):
    """Represents assignments like x = 10."""
    target: ASTNode
    value: ASTNode


@dataclass
class VariableExpression(ASTNode):
    """Represents a variable reference."""
    name: str


@dataclass
class IntegerLiteral(ASTNode):
    """Represents an integer constant."""
    value: int


@dataclass
class CallExpression(ASTNode):
    """Represents function calls like add(a, b)."""
    function_name: str
    arguments: List[ASTNode] = field(default_factory=list)


# ==========================================
# 6. ARRAY NODES
# ==========================================

@dataclass
class ArrayDeclaration(ASTNode):
    """Represents an array declaration."""
    element_type: str
    name: str
    size: Optional[int] = None


@dataclass
class ArrayAccess(ASTNode):
    """Represents array access like arr[0]."""
    array_name: str
    index: ASTNode


# ==========================================
# 7. BOOLEAN LITERAL
# ==========================================

@dataclass
class BooleanLiteral(ASTNode):
    """Represents true or false."""
    value: bool


# ==========================================
# 8. AST DISPLAY FUNCTION
# ==========================================

def print_ast(node: Optional[ASTNode], indent: int = 0):
    """Prints the AST in a readable tree format."""

    # Handle None safely
    if node is None:
        return

    prefix = " " * indent

    # Program
    if isinstance(node, Program):
        print(prefix + "Program")

        for declaration in node.declarations:
            print_ast(declaration, indent + 2)

    # Function
    elif isinstance(node, Function):
        print(prefix + f"Function: {node.name} -> {node.return_type}")

        for param in node.parameters:
            print_ast(param, indent + 2)

        if node.body is not None:
            print_ast(node.body, indent + 2)

    # Parameter
    elif isinstance(node, Parameter):
        print(prefix + f"Parameter: {node.param_type} {node.name}")

    # Variable Declaration
    elif isinstance(node, VariableDeclaration):
        print(prefix + f"Variable: {node.var_type} {node.name}")

        if node.initializer is not None:
            print_ast(node.initializer, indent + 2)

    # Block
    elif isinstance(node, Block):
        print(prefix + "Block")

        for statement in node.statements:
            print_ast(statement, indent + 2)

    # Return Statement
    elif isinstance(node, ReturnStatement):
        print(prefix + "Return")

        if node.expression is not None:
            print_ast(node.expression, indent + 2)

    # If Statement
    elif isinstance(node, IfStatement):
        print(prefix + "If")
        print_ast(node.condition, indent + 2)

        print(prefix + "Then")
        print_ast(node.then_branch, indent + 2)

        if node.else_branch is not None:
            print(prefix + "Else")
            print_ast(node.else_branch, indent + 2)

    # While Statement
    elif isinstance(node, WhileStatement):
        print(prefix + "While")
        print_ast(node.condition, indent + 2)
        print_ast(node.body, indent + 2)

    # Expression Statement
    elif isinstance(node, ExpressionStatement):
        print(prefix + "ExpressionStatement")
        print_ast(node.expression, indent + 2)

    # Binary Expression
    elif isinstance(node, BinaryExpression):
        print(prefix + f"BinaryExpression: {node.operator}")
        print_ast(node.left, indent + 2)
        print_ast(node.right, indent + 2)

    # Unary Expression
    elif isinstance(node, UnaryExpression):
        print(prefix + f"UnaryExpression: {node.operator}")
        print_ast(node.operand, indent + 2)

    # Assignment Expression
    elif isinstance(node, AssignmentExpression):
        print(prefix + "Assignment")
        print_ast(node.target, indent + 2)
        print_ast(node.value, indent + 2)

    # Variable Expression
    elif isinstance(node, VariableExpression):
        print(prefix + f"VariableReference: {node.name}")

    # Integer Literal
    elif isinstance(node, IntegerLiteral):
        print(prefix + f"IntegerLiteral: {node.value}")

    # Boolean Literal
    elif isinstance(node, BooleanLiteral):
        print(prefix + f"BooleanLiteral: {node.value}")

    # Function Call
    elif isinstance(node, CallExpression):
        print(prefix + f"FunctionCall: {node.function_name}")

        for argument in node.arguments:
            print_ast(argument, indent + 2)

    # Array Declaration
    elif isinstance(node, ArrayDeclaration):
        print(prefix + f"Array: {node.element_type} {node.name}[{node.size}]")

    # Array Access
    elif isinstance(node, ArrayAccess):
        print(prefix + f"ArrayAccess: {node.array_name}")
        print_ast(node.index, indent + 2)

    # Unknown Node
    else:
        print(prefix + f"Unknown Node: {type(node).__name__}")
