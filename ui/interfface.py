from tkinter import ttk
import tkinter as tk

import os
import sys

from ui.scrollable_frame import ScrollableFrame
from ui.second_window import SecondWindow

sys.path.append(os.getcwd())
from algorithms.check_algorythm1 import Algo1

import pkg_resources


def checkProbabilityEntry(entry):
    try:
        value = float(entry.get())
        if not 0 <= value <= 1:
            entry.config(foreground="red")
            return False
        else:
            entry.config(foreground="black")
    except ValueError:
        entry.config(foreground="red")
        return False
    entry.config(foreground="black")
    return True


class FirstWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.resultFrame, self.entriesFrame, self.result_label, self.errorMessage = None, None, None, None
        self.add_button, self.process_button, self.clear_button, self.open_second_window_button = None, None, None, None

        self.entry_list = []
        self.delete_button_list = []
        self.inputData = {'listExpr': [], 'probabilities': []}

        self.setup_style()
        self.setup_ui()

        # self.add_record()
        self.addExample()

        self.bind('<Return>', self.process_records)

    def addExample(self):

        examples = [("(P(_a) & Q(_b) | (!R(_c)))", "0.7", "0.8"),
                    ("R(_c) & !Q(_b)", "0.2", "0.3"),
                    ("!P(_a) | Q(_b)", "0.8", "0.9")
                    ]

        for i in range(len(examples)):
            self.add_record()
            example_values = examples[i]
            entry_fields = self.entry_list[i]

            for j in range(len(example_values)):
                entry_fields[j].insert(0, example_values[j])

    def setup_style(self):
        try:
            style = ttk.Style(self)

            # Определение базового пути в зависимости от контекста запуска
            if getattr(sys, 'frozen', False):
                # Путь для временного каталога при использовании PyInstaller
                base_path = os.environ.get('_MEIPASS2', os.path.abspath('.'))
            else:
                # Путь при нормальном запуске скрипта
                base_path = os.path.dirname(os.path.abspath(__file__))

            # Построение полного пути к файлу tcl
            tcl_file_path = os.path.join(base_path, 'forest-light.tcl')

            # Используем файл tcl для настройки темы
            self.tk.call("source", tcl_file_path)
            style.theme_use("forest-light")
        except Exception as e:
            print(f"Error: {e}")

    def setup_ui(self):
        self.title("Проверка системы")
        self.setup_entries_frame()
        self.setup_result_frame()
        self.setup_buttons()

    def setup_entries_frame(self):
        self.entriesFrame = ScrollableFrame(self)
        self.entriesFrame.grid(row=2, column=0, columnspan=4, padx=10, pady=5)

    def setup_result_frame(self):
        self.resultFrame = ttk.Frame()
        self.resultFrame.grid(row=1, column=0, columnspan=4, padx=10, pady=0)

        self.result_label = ttk.Label(self.resultFrame, text="", font=('Arial', 12))
        self.result_label.grid(row=0, column=0)

        self.errorMessage = ttk.Label(self.resultFrame, text="")
        self.errorMessage.grid(row=0, column=1)

    def setup_buttons(self):
        self.add_button = ttk.Button(self, text="Добавить запись", command=self.add_record)
        self.add_button.grid(row=3, column=0, padx=10, pady=10)

        self.process_button = ttk.Button(self, text="Проверить совместность", command=self.validate_entries)
        self.process_button.grid(row=0, column=0, padx=10, pady=10)

        self.clear_button = ttk.Button(self, text="Очистить записи", command=self.clear_records)
        self.clear_button.grid(row=3, column=2, padx=10, pady=10, sticky='e')

        self.open_second_window_button = ttk.Button(self, text="Оценить новую формулу", state=tk.DISABLED,
                                                    command=self.open_second_window)
        self.open_second_window_button.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

    def add_record(self):
        long_entry = ttk.Entry(self.entriesFrame.scrollable_frame, width=30)
        short1_entry = ttk.Entry(self.entriesFrame.scrollable_frame, width=10)
        short2_entry = ttk.Entry(self.entriesFrame.scrollable_frame, width=10)

        row_num = len(self.entry_list) + 4

        long_entry.grid(row=row_num, column=0, padx=(10, 5), pady=5)
        short1_entry.grid(row=row_num, column=1, padx=5, pady=5)
        short2_entry.grid(row=row_num, column=2, padx=5, pady=5)

        self.entry_list.append((long_entry, short1_entry, short2_entry))

        delete_button = ttk.Button(self.entriesFrame.scrollable_frame, text="Удалить запись",
                                   command=lambda e=(long_entry, short1_entry, short2_entry): self.delete_record(e))
        delete_button.grid(row=row_num, column=3, padx=5, pady=5)
        self.delete_button_list.append(delete_button)

        canvasHeight = len(self.entry_list) * 40
        if canvasHeight > 250:
            canvasHeight = 250
        self.entriesFrame.canvas.config(height=canvasHeight)

    def delete_record(self, record_to_delete):
        for entry in record_to_delete:
            entry.destroy()

        delete_button = self.delete_button_list[self.entry_list.index(record_to_delete)]
        delete_button.destroy()

        self.entry_list.remove(record_to_delete)
        self.delete_button_list.remove(delete_button)

        canvasHeight = len(self.entry_list) * 40
        if canvasHeight > 250:
            canvasHeight = 250
        self.entriesFrame.canvas.config(height=canvasHeight)

    def getDataFromForm(self):
        listExpr = []
        probabilities = []
        for record in self.entry_list:
            formula = record[0].get()
            left_border = record[1].get()
            right_border = record[2].get()
            listExpr.append(formula)
            probabilities.append([left_border, right_border])
        self.inputData = {'listExpr': listExpr, 'probabilities': probabilities}
        return {'listExpr': listExpr, 'probabilities': probabilities}

    def process_records(self, event=None):
        self.result_label.config(text="считаем...")
        self.result_label.update()
        self.getDataFromForm()

        cc = Algo1(self.inputData['listExpr'], self.inputData['probabilities'])
        try:
            result = cc.checkCompatibility()
            # result = checkCompatibility(self.inputData['listExpr'], self.inputData['probabilities'])
            if result:
                self.result_label.config(text="Система совместна", foreground="#006400")
                self.open_second_window_button["state"] = tk.NORMAL
            else:
                self.result_label.config(text="Система не совместна", foreground="red")
                self.open_second_window_button["state"] = tk.DISABLED

        except Exception as e:
            self.errorMessage.config(text=f"Ошибка: {str(e)}", foreground="red")
            self.result_label.config(text="", foreground="black")
            self.open_second_window_button["state"] = tk.DISABLED

    def validate_entries(self):
        self.errorMessage.config(text="")
        dataCorrect = True
        for entry in self.entry_list:
            for widget in entry:
                if not widget.get():
                    dataCorrect = False

        for entry in self.entry_list:
            long_entry, short1_entry, short2_entry = entry
            var1 = checkProbabilityEntry(short1_entry)
            var2 = checkProbabilityEntry(short2_entry)
            if var1 and var2:
                short1 = float(short1_entry.get())
                short2 = float(short2_entry.get())
                if short2 < short1:
                    short1_entry.config(foreground="red")
                    short2_entry.config(foreground="red")
                    dataCorrect = False
                else:
                    short1_entry.config(foreground="black")
                    short2_entry.config(foreground="black")
            else:
                dataCorrect = False

        if dataCorrect:
            self.process_records()

    def clear_records(self):
        for record, delete_button in zip(self.entry_list, self.delete_button_list):
            for entry in record:
                entry.delete(0, tk.END)
                entry.destroy()
            delete_button.destroy()

        self.entry_list.clear()
        self.delete_button_list.clear()
        self.entriesFrame.canvas.config(height=0)

    def open_second_window(self):
        SecondWindow(self.inputData)
