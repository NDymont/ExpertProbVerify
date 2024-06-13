from logic_utils.atomic_extractor import AtomicExtractor
from logic_utils.expression_checker import ExpressionChecker
from logic_utils.formula_parser import FormulaParser
from logic_utils.quantifier_transformer import QuantifierTransformer
from logic_utils.truth_table_calculator import TruthTableCalculator

import intvalpy as ip
import numpy as np

from utils import utils1
from utils import number2interval as n2i


class Algo1:

    def __init__(self, listStringExpr, probabilities):
        self.listStringExpr = listStringExpr
        self.probabilities = probabilities
        self.listExpr = []
        self.countDiz = None
        self.A = None
        self.b = None

    def prepare_data(self):
        self.build_left_part()
        self.build_right_part()
        return self.A, self.b

    def build_left_part(self):
        # парсинг
        formula_parser = FormulaParser()
        self.listExpr = [formula_parser.parse(expr) for expr in self.listStringExpr]
        # проверка выражений
        expression_checker = ExpressionChecker(self.listExpr)
        if not expression_checker.check():
            raise Exception(expression_checker.error_message)

        # замена кванторов
        trans = QuantifierTransformer(self.listExpr)
        transformed = trans.transform()

        # получение таблицы истинности
        extr = AtomicExtractor()
        set_expr = extr.extract(transformed)

        table_calculator = TruthTableCalculator(transformed, set_expr)
        truth_table = table_calculator.calculate_truth_table()

        # добавление ограничений, перевод в интервальные
        self.countDiz = len(truth_table[0])
        tables = np.array(truth_table)
        matrixE = utils1.unitMatrix(self.countDiz)
        line1 = utils1.lineOne(self.countDiz)
        tableIval = n2i.numer2interval(tables)
        limitations = n2i.concatInval(n2i.numer2interval(line1), n2i.numer2interval(matrixE))
        self.A = n2i.concatInval(tableIval, limitations)
        # print(self.A)

    def build_right_part(self):
        estimations = ip.Interval(self.probabilities)
        partB = n2i.concatInval(utils1.makeOneOne(), utils1.makeZeroOneList(self.countDiz))
        self.b = n2i.concatInval(estimations, partB)

    def checkCompatibility(self):
        self.prepare_data()
        uss = ip.linear.Uss.maximize(self.A, self.b)
        if uss[1] < 0:
            return False
        else:
            return True
