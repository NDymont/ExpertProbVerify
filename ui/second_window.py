from tkinter import ttk
import tkinter as tk

from algorithms.estimator_algorythm2 import NewFormulaEstimator


class SecondWindow(tk.Toplevel):
    def __init__(self, data):
        super().__init__()
        self.title("Оценка новой формулы")

        self.originalSystem = data

        number_f = len(self.originalSystem['listExpr'])

        self.original_system_label = ttk.Label(self, text='Исходная система:')
        self.original_system_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.labels = []

        for i in range(0, number_f):
            label1 = ttk.Entry(self, width=30)
            label2 = ttk.Entry(self, width=10)
            label3 = ttk.Entry(self, width=10)
            label1.insert(0, self.originalSystem['listExpr'][i])
            label2.insert(0, self.originalSystem['probabilities'][i][0])
            label3.insert(0, self.originalSystem['probabilities'][i][1])
            label1.config(state="readonly")
            label2.config(state="readonly")
            label3.config(state="readonly")
            label1.grid(row=i + 1, column=0, padx=10, pady=3)
            label2.grid(row=i + 1, column=1, padx=10, pady=3)
            label3.grid(row=i + 1, column=2, padx=10, pady=3)
            self.labels.append((label1, label2, label3))

        self.entryLabel = ttk.Label(self, text="Новая формула:")
        self.entryLabel.grid(row=number_f + 1, column=0, padx=10, pady=10, sticky="w")

        self.inputField = ttk.Entry(self, width=30)
        self.inputField.grid(row=number_f + 2, column=0, padx=10, pady=3)
        self.inputField.insert(0, "P(_a)")

        self.from_result = ttk.Entry(self, width=10)
        self.from_result.grid(row=number_f + 2, column=1, padx=10, pady=3)
        self.to_result = ttk.Entry(self, width=10)
        self.to_result.grid(row=number_f + 2, column=2, padx=10, pady=3)

        self.entryAccuracyLabel = ttk.Label(self, text="Точность оценки:")
        self.entryAccuracyLabel.grid(row=number_f + 3, column=0, padx=10, pady=10, sticky="w")

        self.inputAccuracyField = ttk.Entry(self, width=10)
        self.inputAccuracyField.grid(row=number_f + 4, column=0, padx=10, pady=3, sticky="w")
        self.inputAccuracyField.insert(0, "0.1")

        self.processButton = ttk.Button(self, text="Расчитать оценку",
                                        command=self.processEntry)
        self.processButton.grid(row=number_f + 5, column=0, padx=10, pady=10)

        self.info = ttk.Label(self, text="")
        self.info.grid(row=number_f + 5, column=1, padx=10, pady=10)

        self.errorMessage = ttk.Label(self, text="", foreground="red")
        self.errorMessage.grid(row=number_f + 7, column=0, padx=10, pady=10)

        self.bind('<Return>', self.processEntry)

    def processEntry(self, event=None):
        newFormula = self.inputField.get()
        accuracy = float(self.inputAccuracyField.get())
        self.info.config(text="считаем...")
        self.errorMessage.config(text="")
        self.errorMessage.update()
        self.info.update()

        self.from_result.config(state="normal")
        self.to_result.config(state="normal")
        self.from_result.delete(0, 'end')
        self.to_result.delete(0, 'end')
        self.from_result.update()
        self.to_result.update()

        newFormulaEst = NewFormulaEstimator()
        try:
            formulaEstimation = newFormulaEst.estimate(self.originalSystem['listExpr'],
                                                       self.originalSystem['probabilities'],
                                                       newFormula,
                                                       accuracy=accuracy)
            self.errorMessage.config(text="")
            self.info.config(text="")

            if formulaEstimation is None:
                self.errorMessage.config(text="something went wrong")
            else:
                self.from_result.insert(0, formulaEstimation[0])
                self.to_result.insert(0, formulaEstimation[1])
                self.from_result.config(state="readonly")
                self.to_result.config(state="readonly")

        except Exception as e:
            print("\n\tERROR: 320", str(e))
            self.errorMessage.config(text=f"Ошибка: {str(e)}")
            self.info.config(text="")
