from pyparsing import Word, alphas, nums, Forward, Group, Suppress, Optional, opAssoc, infix_notation, oneOf
from logic_utils.logic import Predicate, Variable, Constant, Argument, UnaryOperation, BinaryOperation, \
    QuantifiedExpression, \
    BinaryOperator, UnaryOperator, Quantifier


class FormulaParser:
    def __init__(self):
        self.predicate_name = Word(alphas.upper(), alphas + nums + "_")
        self.variable = Word('xyzwvu', alphas + nums + "_").setParseAction(lambda t: Variable(t[0]))
        self.constant = Word(alphas.lower() + "_", alphas + nums + "_").setParseAction(lambda t: Constant(t[0]))

        self.argument = self.variable | self.constant
        self.argument_list = Group(self.argument + Optional(Suppress(',') + self.argument))
        self.dependency = self.argument_list.setParseAction(lambda t: [Argument(arg) for arg in t.asList()])

        self.unary_operator = oneOf("¬ ! not ~").setParseAction(lambda t: UnaryOperator.NEGATION)

        self.conjunction_symbol = oneOf("∧ ^ & and *").setParseAction(lambda t: BinaryOperator.CONJUNCTION)
        self.disjunction_symbol = oneOf("∨ v V | or +").setParseAction(lambda t: BinaryOperator.DISJUNCTION)
        self.expression = Forward()
        self.predicate_expr = Forward()
        self.predicate_expr << (self.predicate_name + Suppress('(') + self.dependency + Suppress(')'))

        self.quantifier_exists = oneOf("∀ A for_all any").setParseAction(lambda t: Quantifier.FOR_ALL)
        self.quantifier_for_all = oneOf("∃ E exists").setParseAction(lambda t: Quantifier.EXISTS)
        self.quantifier = self.quantifier_exists | self.quantifier_for_all
        self.quantifier_expr = Forward()
        self.quantifier_expr << self.quantifier + self.variable + (
                self.predicate_expr | self.expression | self.quantifier_expr)
        self.quantifier_expr.setParseAction(self.create_quantifier_expr)

        self.expression << infix_notation(
            self.quantifier_expr | self.predicate_expr,
            [
                (self.unary_operator, 1, opAssoc.RIGHT, self.create_unary_operation),
                (self.conjunction_symbol, 2, opAssoc.LEFT, self.create_binary_operation),
                (self.disjunction_symbol, 2, opAssoc.LEFT, self.create_binary_operation)
            ]
        )

        self.predicate_expr.setParseAction(self.parse_predicate)

        self.any_expression = self.expression | self.quantifier_expr

    def create_quantifier_expr(self, tokens):
        return QuantifiedExpression(quantifier=tokens[0], variable=tokens[1], predicate=tokens[2])

    def parse_predicate(self, tokens):
        name = tokens[0]
        dependencies = tokens[1]
        return Predicate(name, dependencies)

    def create_binary_operation(self, tokens):
        left_operand, operator, right_operand = tokens[0][0], tokens[0][1], tokens[0][2]
        return BinaryOperation(operator, left_operand, right_operand)

    def create_unary_operation(self, tokens):
        return UnaryOperation(tokens[0][0], tokens[0][1])

    def parse(self, predicate_str):
        return self.any_expression.parseString(predicate_str, parseAll=True)[0]

