from logic_utils.logic import Predicate, Variable, Constant, Argument, UnaryOperation, BinaryOperation, \
    QuantifiedExpression, BinaryOperator, Quantifier


class QuantifierTransformer:

    def __init__(self, expressions_list):
        self.expressions_list = expressions_list
        self.constants_set = {Constant('a1'), Constant('a2')}  # !!!
        self.result_expressions_list = []

    def transform(self):
        self.__get_all_constant_from_expressions()
        for expression in self.expressions_list:
            self.result_expressions_list.append(self.__transform_expression(expression))
        return self.result_expressions_list

    def __transform_expression(self, expression):
        if isinstance(expression, QuantifiedExpression):
            return self.__transform_quantified_expression(expression)
        if isinstance(expression, BinaryOperation):
            return BinaryOperation(expression.operator,
                                   self.__transform_expression(expression.left_operand),
                                   self.__transform_expression(expression.right_operand))
        if isinstance(expression, UnaryOperation):
            return UnaryOperation(expression.operator, self.__transform_expression(expression.operand))
        if isinstance(expression, Predicate):
            return expression
        raise Exception('in QuantifierTransformer transform_expression:\twrong type of expression')

    def __transform_quantified_expression(self, expression):
        # проверки для выражения под квантором: только одноместный предикат, от переменной, которая совпадает с переменной квантора
        # эти условия должны отсекаться на этапе парсинга и создания выражение, но вдруг
        if (not isinstance(expression, QuantifiedExpression) or not isinstance(expression.predicate, Predicate)
                or expression.predicate.arity != 1 or Argument(
                    [expression.variable]) != expression.predicate.dependencies):
            raise Exception('in QuantifierTransformer transform_quantified_expression:\t', expression)

        if expression.quantifier == Quantifier.FOR_ALL:
            operation = BinaryOperator.CONJUNCTION
        elif expression.quantifier == Quantifier.EXISTS:
            operation = BinaryOperator.DISJUNCTION
        else:
            raise Exception('unknown quantifier:\t', expression)
        return self.__create_predicate_combinations(expression.predicate.name, operation)

    def __create_predicate_combinations(self, predicate_name, operator):  # работает только для одноместных предикатов
        constant_list = sorted(list(self.constants_set), key=lambda c: c.value)
        expression = Predicate(predicate_name, Argument([constant_list[0]]))
        for constant in constant_list[1:]:
            predicate = Predicate(predicate_name, Argument([constant]))
            expression = BinaryOperation(operator, expression, predicate)
        return expression

    def __get_all_constant_from_expressions(self):
        for expression in self.expressions_list:
            expr_const_set = self.__get_constant_from_expression(expression)
            self.constants_set = self.constants_set.union(expr_const_set)

    def __get_constant_from_expression(self, expression):
        if isinstance(expression, QuantifiedExpression):
            return self.__get_constant_from_expression(expression.predicate)
        if isinstance(expression, BinaryOperation):
            return self.__get_constant_from_expression(expression.right_operand).union(
                self.__get_constant_from_expression(expression.left_operand))
        if isinstance(expression, UnaryOperation):
            return self.__get_constant_from_expression(expression.operand)
        if isinstance(expression, Predicate):
            return self.__get_constant_from_expression(
                expression.dependencies)  # Вернуть множество из одного предиката expression
        if isinstance(expression, Argument):
            constants = set()
            for arg in expression.value:
                if isinstance(arg, Constant):
                    constants.add(arg)
            return constants
        raise Exception('in QuantifierTransformer get_constant_from_expression:\twrong type of expression')
