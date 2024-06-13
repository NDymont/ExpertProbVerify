from algorithms.check_algorythm1 import Algo1

import copy

import intvalpy as ip
import numpy as np

from logic_utils.expression_checker import ExpressionChecker
from logic_utils.formula_parser import FormulaParser


class NewFormulaEstimator:
    def __init__(self):
        pass

    def makeVerdict(self, A, b):
        uss = ip.linear.Uss.maximize(A, b)
        if uss[1] < 0:
            return False
        else:
            return True

    def findLeftBorder(self, A, b0, step, leftBorder, rightBorder):
        stepLeftBorder = leftBorder
        stepRigthBorder = stepLeftBorder + step
        b = copy.copy(b0)
        while stepRigthBorder <= rightBorder:
            estimation = ip.SingleInterval(stepLeftBorder, stepRigthBorder)
            b[0] = estimation
            compatibility = self.makeVerdict(A, b)
            if compatibility:
                return stepLeftBorder

            stepLeftBorder = stepRigthBorder
            stepRigthBorder += step
        raise Exception("something wrong in findLeftBorder")

    def findRightBorder(self, A, b0, step, leftBorder, rightBorder):
        stepRigthBorder = rightBorder
        stepLeftBorder = stepRigthBorder - step
        b = copy.copy(b0)
        while stepLeftBorder >= leftBorder:
            estimation = ip.SingleInterval(stepLeftBorder, stepRigthBorder)
            b[0] = estimation
            compatibility = self.makeVerdict(A, b)
            if compatibility:
                return stepRigthBorder
            stepRigthBorder = stepLeftBorder
            stepLeftBorder -= step

        raise Exception("что-то пошло не так в findRightBorder")

    def divisionNSegments(self, A, b, accuracy):
        N = 2
        step = 1. / N
        leftBorder = self.findLeftBorder(A, b, step, 0., 1.)
        rightBorder = self.findRightBorder(A, b, step, 0., 1.)
        count_steps = int(np.ceil(-np.log2(accuracy))) - 1

        for i in range(count_steps):
            step /= N
            newLeft = self.findLeftBorder(A, b, step, leftBorder, leftBorder + step * N)
            newRight = self.findRightBorder(A, b, step, rightBorder - step * N, rightBorder)
            leftBorder = newLeft
            rightBorder = newRight

        return leftBorder + step, rightBorder - step

    def estimate(self, listSystemExpr, systemProbabilities, newFormula, accuracy=0.1):
        formula_parser = FormulaParser()
        expression_checker = ExpressionChecker()
        result_check = expression_checker.check_expression(formula_parser.parse(newFormula))
        if not result_check[0]:
            raise Exception(result_check[1])

        listExpr = [newFormula] + listSystemExpr
        probabilities = [[0.0, 1.0]] + systemProbabilities

        check_algo = Algo1(listExpr, probabilities)
        A, b = check_algo.prepare_data()

        b[0] = ip.SingleInterval(0, 0 + 1e-12)
        if self.makeVerdict(A, b):
            b[0] = ip.SingleInterval(1 - 1e-12, 1)
            if self.makeVerdict(A, b):
                return 0, 1
        return self.divisionNSegments(A, b, accuracy)

