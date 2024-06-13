from logic_utils.logic import Predicate, Variable, UnaryOperation, BinaryOperation, QuantifiedExpression


class ExpressionChecker:
    def __init__(self, expressions_list=None):
        if expressions_list is None:
            expressions_list = []
        self.expressions_list = expressions_list
        self.result_checker = None
        self.error_message = ""

    def check(self):
        self.result_checker = True
        i = 1
        for expr in self.expressions_list:
            checkResult = self.check_expression(expr)
            i += 1
            if not checkResult[0]:
                self.result_checker = False
                self.error_message += "line " + str(i) + ": " + checkResult[1] + "\n"
        print(self.error_message)
        return self.result_checker

    def check_expression(self, expression):
        match expression:
            case expression if isinstance(expression, QuantifiedExpression):
                return self.check_quantified_expression(expression)
            case expression if isinstance(expression, BinaryOperation):
                check_result_left = self.check_expression(expression.left_operand)
                check_result_right = self.check_expression(expression.right_operand)
                return check_result_left[0] and check_result_right[0], check_result_left[1] + check_result_right[1]
            case expression if isinstance(expression, UnaryOperation):
                return self.check_expression(expression.operand)
            case expression if isinstance(expression, Predicate):
                return self.check_predicate(expression)
            case _:
                return False, 'Unknown type expression ' + str(expression)

    def check_predicate(self, predicate):
        if predicate.arity != 1:
            return False, 'there can only be a single predicate'
        if isinstance(predicate.dependencies.value[0], Variable):
            return False, 'an unrelated variable under a predicate'
        return True, ""

    def check_quantified_expression(self, quantified_expression):
        if not isinstance(quantified_expression.predicate, Predicate):
            return False, 'there can only be a single predicate under the quantifier: wrong type'
        if quantified_expression.predicate.arity != 1:
            return False, 'there can only be a single predicate under the quantifier: wrong arity'
        if quantified_expression.predicate.dependencies.value != [quantified_expression.variable]:
            return False, 'wrong variable under quantifier'
        return True, ''

    def get_variables(self, expression):
        pass
