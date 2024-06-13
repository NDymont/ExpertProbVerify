from itertools import product, repeat

from logic_utils.logic import Predicate, Variable, Constant, Argument, UnaryOperation, BinaryOperation, BinaryOperator, \
    UnaryOperator
from logic_utils import atomic_extractor


class TruthTableCalculator:
    def __init__(self, list_expressions, set_atoms):
        self.list_expressions = list_expressions
        self.set_atoms = set_atoms
        self.truth_table = [[] for _ in list_expressions]
        # my_dict = {key: 0 for key in my_set}
        self.atom_values_dict = {key: 0 for key in set_atoms}

    def __str__(self):
        return (f"TTC:\n atoms: {str(self.set_atoms)}\n expressions: {str(self.list_expressions)}\n "
                f"truth_table: {str(self.truth_table)}\n atom_values_dict: {str(self.atom_values_dict)}")

    def calculate_truth_table(self):
        for args in product(*repeat((0, 1), len(self.atom_values_dict))):
            i = 0
            for x in self.atom_values_dict:
                self.atom_values_dict[x] = args[i]
                i = i + 1

            for j, expr in enumerate(self.list_expressions):
                res = self.evaluate(expr)
                self.truth_table[j].append(res)
        return self.truth_table

    def evaluate(self, expression):
        if isinstance(expression, BinaryOperation):
            if expression.operator == BinaryOperator.CONJUNCTION:
                return self.evaluate(expression.right_operand) and self.evaluate(expression.left_operand)
            if expression.operator == BinaryOperator.DISJUNCTION:
                return self.evaluate(expression.right_operand) or self.evaluate(expression.left_operand)
            raise Exception('in TruthTableCalculator:\tunknown binary operator')
        if isinstance(expression, UnaryOperation):
            if expression.operator == UnaryOperator.NEGATION:
                return not self.evaluate(expression.operand)
            raise Exception('in TruthTableCalculator:\tunknown unary operator')
        if isinstance(expression, Predicate):
            return self.atom_values_dict[expression]

        raise Exception('in TruthTableCalculator:\twrong type of expression')
