from enum import Enum


class Quantifier(Enum):
    EXISTS = "∃"
    FOR_ALL = "∀"

    def __str__(self):
        return self.value


class UnaryOperator(Enum):
    NEGATION = "¬"

    def __str__(self):
        return self.value


class BinaryOperator(Enum):
    CONJUNCTION = "∧"
    DISJUNCTION = "∨"

    def __str__(self):
        return self.value


class Predicate:
    def __init__(self, name, dependencies):
        self.name = name
        self.arity = dependencies.arity
        self.dependencies = dependencies
        self.truth_value = None

    def __repr__(self):
        return f"{self.name}_{self.arity}({str(self.dependencies)})"

    def __str__(self):
        return f"{self.name}[{str(self.dependencies)}]"

    def __eq__(self, other):
        if isinstance(other, Predicate):
            return self.name == other.name and self.dependencies == other.dependencies
        return False

    def __hash__(self):
        return hash((self.name, tuple(self.dependencies.value)))


class Argument:
    def __init__(self, value):
        self.value = value
        self.arity = len(value)

    def __str__(self):
        res = str(self.value[0])
        if self.arity > 1:
            for i in range(1, self.arity):
                res += f", {self.value[i]}"
        return res

    def __repr__(self):
        res = 'ARGS:\t'
        for x in self.value:
            res += str(x) + ', '
        return res

    def __eq__(self, other):
        if isinstance(other, Argument):
            return self.value == other.value
        return False


class Variable:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "VAR " + self.name

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)


class Constant:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return "CONST " + str(self.value)

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, Constant):
            return self.value == other.value
        return False


class UnaryOperation:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __str__(self):
        return f"{self.operator}⟨ {self.operand} ⟩"


class BinaryOperation:
    def __init__(self, operator, left_operand, right_operand):
        self.operator = operator
        self.left_operand = left_operand
        self.right_operand = right_operand

    def __repr__(self):
        return f"BIN OP: (\n{repr(self.left_operand)}\n{self.operator}\n {repr(self.right_operand)})"

    def __str__(self):
        # if self.operator.value:
        #     return f"({self.left_operand} {self.operator.value} {self.right_operand})"
        return f"({self.left_operand} {self.operator} {self.right_operand})"


class QuantifiedExpression:
    def __init__(self, quantifier, variable, predicate):
        self.quantifier = quantifier
        self.variable = variable
        self.predicate = predicate

    def __str__(self):
        return f"[{self.quantifier} {self.variable}. {{{self.predicate}}}]"


def predicate_creation_examples():
    a = Predicate("P", Argument([Constant("X")]))
    b = Predicate("G", Argument([Constant("X"), Constant("Y")]))
    return a, b
