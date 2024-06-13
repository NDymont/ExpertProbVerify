from logic_utils.logic import Predicate, UnaryOperation, BinaryOperation, QuantifiedExpression


class AtomicExtractor:
    def __init__(self):
        pass

    def extract(self, expression):  # get sorted list of atoms
        set_atoms = set()
        if isinstance(expression, list):
            for element in expression:
                set_atoms = set_atoms.union(self.__extract_from_expression(element))
            return sorted(set_atoms, key=str)
        return sorted(self.__extract_from_expression(expression), key=str)

    def __extract_from_expression(self, expression):
        if isinstance(expression, BinaryOperation):
            return self.__extract_from_expression(expression.right_operand).union(
                self.__extract_from_expression(expression.left_operand))
        if isinstance(expression, UnaryOperation):
            return self.__extract_from_expression(expression.operand)
        if isinstance(expression, Predicate):
            return {expression}  # Вернуть множество из одного предиката expression
        if isinstance(expression, QuantifiedExpression):
            return set()
        raise Exception('wrong type of expression' + str(expression))
