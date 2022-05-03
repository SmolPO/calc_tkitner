import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkFont
from math import *


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Memory:
    """
    класс для работы с ячейками памяти
    """
    memory = list()

    def __init__(self):
        self.memory = list([0 for _ in range(10)])  # создать 10 ячеек

    def read(self, n_box):
        """ MR """
        return str(self.memory[n_box])

    def save(self, n_box: int, val: str):
        """ MS """
        if is_float(val):
            self.memory[n_box] = float(val)
        return

    def clear(self, n_box):  
        """ MC """
        self.memory[n_box] = 0
        return self.read(n_box)

    def plus(self, n_box, val): 
        """ M+ """
        if is_float(val):
            val = float(val)
            try:
                res = eval(f"{val} + {float(self.memory[n_box])}")
            except SyntaxError:
                res = f"{val} + {float(self.memory[n_box])}"
            return str(res)

    def sub(self, n_box, val):
        """ M- """
        if is_float(val):
            val = float(val)
            try:
                res = eval(f"{val}-{float(self.memory[n_box])}")
            except SyntaxError:
                res = f"{val}-{float(self.memory[n_box])}"
            return str(res)


BG_COLOR = "#212121"    # цвет фона
AC_COLOR = "orange"     # цвет нажатой кнопки
WHITE = "#ffffff"       # цвет текста
T_SIZE = 14             # размер шрифта
FONT = "TIMES"          # шрифт
ERROR = ("func: bad value",
         "division by zero",
         "error: value not in [-1, 1]"
         )
# ошибки, которые выводятся в поле


class Calc(tk.Tk):
    memory = Memory()   
    stack = list()      # журнал всех операций
    b_numbers = list()  # кнопки цифр
    b_oper = list()     # кнопки операторов
    base_btns = list()  # кнопки простого калькулятора
    prog_btns = list()  # кнопки инженерного калькулятора
    b_memory = dict()   # кнопки для работы с памятью 

    OPS = "*/-+^"       # возможные операторы
    last_op = "+"       # последний оператор

    is_prog = False     # какой режим калькулятора
    is_exp = False          # какая форма записи экспонедциальная или нет
    is_add_point = False    # была ли добавлена точка или нет
    count_rows_in_display = 10  # кол-во строк на дисплее

    b_sing: tk.Button = None    # изменить знак
    point_b: tk.Button = None   # .
    b_ce: tk.Button = None      # CE
    b_calc: tk.Button = None    # =
    b_sqrt: tk.Button = None    # sqrt
    b_braked: tk.Button = None  # )

    def __init__(self):
        super(Calc, self).__init__()
        self["bg"] = BG_COLOR   # цвет фона
        fontStyle = tkFont.Font(family=FONT, size=T_SIZE, weight="bold")
        self.style = {"relief": tk.FLAT, "activebackground": AC_COLOR, "bg": BG_COLOR, "fg": WHITE,     # стиль кнопок
                      "font": fontStyle, "width": 1, "height": 1}

        buttons = (('MR', 'MS', "MC", "M+", "M-"),
                   ('7', '8', '9', '+', '-'),
                   ('4', '5', '6', '*', '/'),
                   ('1', '2', '3', '^', 'sqrt'),
                   ('0', ')', '.', '+/-', '='))

        self.text = tk.Label(self.master,                   # поле вывода
                             text='0', height=2, width=35,
                             font=("TIMES", 20),
                             anchor="e", justify=tk.RIGHT,
                             bg=WHITE, fg=BG_COLOR)

        self.text.grid(row=0, column=0, columnspan=5, sticky="nsew")

        # элементы из инженерного калькулятора
        self.display = scrolledtext.ScrolledText(self.master, height=10, width=30, font=FONT)
        self.display.configure(state='normal')
        self.display.see("end")
        
        # ID
        self.label = tk.Label(self.master, text="ID", fg='#fff', font=self.style["font"], bg="#212121")
        self.t_id = tk.Entry(self.master)
        self.b_show = tk.Button(self.master, text="Обновить", command=self.refresh, **self.style)

        # функции инженерного
        self.b_x2 = tk.Button(self.master, text="x^2",  **self.style)
        self.b_fe = tk.Button(self.master, text="F/E",   **self.style)
        self.b_log_xy = tk.Button(self.master, text="log_xy",   **self.style)
        self.b_one_1x = tk.Button(self.master, text="1/x",   **self.style)
        self.b_factorial = tk.Button(self.master, text="!n",   **self.style)
        self.b_comma = tk.Button(self.master, text=",",   **self.style)
        self.b_cos = tk.Button(self.master, text="cos",   **self.style)
        self.b_acos = tk.Button(self.master, text="acos",   **self.style)
        self.b_tan = tk.Button(self.master, text="tan",   **self.style)
        self.b_atan = tk.Button(self.master, text="atan",   **self.style)
        self.b_ce = tk.Button(self.master, text='CE', **self.style)
        self.b_prog = tk.Button(self.master, text='П', **self.style)
        self.b_one_back = tk.Button(self.master, text='C', **self.style)

        self.prog_btns.append(self.b_x2)
        self.prog_btns.append(self.b_log_xy)
        self.prog_btns.append(self.b_fe)
        self.prog_btns.append(self.b_one_1x)
        self.prog_btns.append(self.b_factorial)
        self.prog_btns.append(self.b_comma)
        self.prog_btns.append(self.b_cos)
        self.prog_btns.append(self.b_acos)
        self.prog_btns.append(self.b_tan)
        self.prog_btns.append(self.b_atan)
        self.prog_btns.append(self.b_comma)

        self.b_ce.grid(row=1, column=4, sticky="nsew")
        self.b_prog.grid(row=1, column=0, sticky="nsew")
        self.b_one_back.grid(row=1, column=3, sticky="nsew")

        # содаем кнопки памяти
        style = self.style.copy()
        style["width"] = 4
        types = ("MS", "MC", "MR", "M+", "M-")
        for t in types:
            self.b_memory[t] = list()
        
        # добавляем кнопки в массив для кнопок работы с памятью
        for row in range(10):
            for col in range(5, 10):
                button = tk.Button(self.master, text=types[col - 5], **style)
                button.bind('<Button-1>', self.memory_op)
                self.b_memory[button["text"]].append(button)

        # создаем кнопки простого калькулятора
        for row in range(5):
            for col in range(5):
                button = tk.Button(self.master, text=buttons[row][col],  **self.style)
                if button["text"] in "0123456789":
                    self.b_numbers.append(button)
                elif button["text"] in ".":
                    self.b_point = button
                elif button["text"] in self.OPS:
                    self.b_oper.append(button)
                elif button["text"] == "+/-":
                    self.b_sing = button
                elif button["text"] == ")":
                    self.b_braked = button
                elif button["text"] == "sqrt":
                    self.b_sqrt = button
                elif button["text"] == "=":
                    self.b_calc = button
                elif button["text"] in "M+M-MSMRMC":
                    button = self.b_memory[button["text"]][0]
                button.grid(row=row + 2, column=col, sticky="nsew")
                self.base_btns.append(button)

        # подключаем обработчики
        for btn in self.b_numbers:
            btn.bind('<Button-1>', self.add_number)
        for btn in self.b_oper:
            btn.bind('<Button-1>', self.add_oper)
        for btn in self.b_memory.keys():
            self.b_memory[btn][0].bind('<Button-1>', self.memory_op)

        # подключаем обработчики
        # с передачей sender в функцию
        self.b_x2["command"] = self.to_x2
        self.b_fe["command"] = self.fe_oper
        self.b_log_xy["command"] = self.log_xy
        self.b_one_1x["command"] = self.one_div_x
        self.b_factorial["command"] = self.factorial
        self.b_comma["command"] = self.add_comma

        self.b_cos.bind('<Button-1>', self.function)
        self.b_acos.bind('<Button-1>', self.function)
        self.b_tan.bind('<Button-1>', self.function)
        self.b_atan.bind('<Button-1>', self.function)
        self.b_sqrt.bind('<Button-1>', self.function)

        # без передачи sender в функцию
        self.b_show["command"] = self.refresh
        self.b_point["command"] = self.add_point
        self.b_sing["command"] = self.change_sing
        self.b_calc["command"] = self.calc
        self.b_ce["command"] = self.ce
        self.b_braked["command"] = self.add_bracket
        self.b_prog["command"] = self.simple_to_prog
        self.b_one_back["command"] = self.del_one_s

    # добавление и удавление из поля
    def add_number(self, event):
        num = event.widget.cget('text')
        last_s_is_bracket = len(num) > 0 and num[-1] in ")"
        if last_s_is_bracket:
            return

        text = self.text.cget("text")
        if text in ERROR:
            return

        if len(text) > 1 and text[-1] == ")":
            return

        if text == "0":
            self.text["text"] = num
            return

        last_s_is_oper = len(text) > 0 and text[-1] in "+*/-^"
        if last_s_is_oper:
            self.last_op = text[-1]
            self.text["text"] += num
            return

        self.text["text"] += num

    def add_point(self):
        text = self.text["text"]
        if text in ERROR:
            return
        last_s_is_oper = len(text) > 0 and text[-1] in "/*-+^"
        if last_s_is_oper:
            text += "0."
        elif text[-1] == ")":
            return
        elif not text:
            text = "0."
        elif text[-1].isdigit() and not self.is_add_point:
            text += "."
        elif not self.is_add_point:
            text += "0."
        else:
            return
        self.is_add_point = True
        self.text["text"] = text

    def add_oper(self, event):
        op = event.widget.cget('text')
        text = self.text["text"]
        if text in ERROR:
            return
        self.is_add_point = False

        if len(text) > 3 and text[-1] == "-" and text[-2] == "(":
            if op == "+":
                self.text["text"] = text[:-1]
                return
            else:
                return

        if text[-1] == "(" and op == "-":
            self.text["text"] += op
            return

        last_s_is_bracket = len(text) > 0 and text[-1] in "("
        if not text or last_s_is_bracket:
            return

        last_s_is_operator = len(text) > 0 and text[-1] in "+-*/^"
        if last_s_is_operator:
            self.text["text"] = text[:-1] + op
            return
        else:
            last_op = self.last_op
            if op == "+-*/^" and last_op == "^" or \
                    op in "*/" and last_op in "*/^" or \
                    op in "+-" and last_op in "+-*/^":
                self.text["text"] += op
                return
            else:
                self.text["text"] += op
                return

    def add_bracket(self):
        text = self.text["text"]
        if text in ERROR:
            return
        if text[-1] in "0123456789)":
            count_on = 0
            count_off = 0
            for s in text:
                if s == ")":
                    count_off += 1
                if s == "(":
                    count_on += 1
            if count_on == 0:
                return
            if count_on > count_off:
                text += ")"
                text: str
                i = max([text.rfind(x) for x in ("cos", "acos", "sqrt", "log", "tan", "atan")])
                if i > 0 and text[i-1] == "a":
                    i -= 1
                if i == -1:
                    self.text["text"] += ")"
                    return
                try:
                    eval(text[i:])
                    self.text["text"] += ")"
                except:
                    self.text["text"] = "func: bad value"

    def del_one_s(self):
        text = self.text.cget("text")
        if text in ERROR:
            self.text["text"] = "0"
            return

        if text == "0":
            return

        elif text[-1] == ".":
            text = text[:-1]
            self.is_add_point = False
            self.text["text"] = text

        elif text[-1] in self.OPS:
            self.last_op = "+"  # по умолчанию последний оператор+
            for s in text[-1::-1]:  # идем с конца и ищем оператор
                if s in self.OPS:   # если нашли
                    self.last_op = s    # меняем и запоминаем
                    break
            self.text["text"] = text[:-1]

        elif len(text) == 1:
            self.text["text"] = "0"
        else:
            self.text["text"] = text[:-1]

    def add_comma(self):
        text = self.text["text"]
        if text in ERROR:
            self.text["text"] = "0"
            return
        i = text.rfind("log(")
        if i == -1:
            return
        try:
            n = text[i+4:].rfind(",")
            if n != -1:
                return
            val = eval(text[i+4:])
            if val < 0:
                return
            self.text["text"] += ","
        except:
            return

    # funcs
    def factorial(self):
        text = self.text["text"]
        if text in ERROR:
            self.text["text"] = "0"
            return
        if text in ("0", "0.", "0.0") or \
            text[-1] in self.OPS or \
            text[-1] == "(":
            self.text["text"] = "!("
            return

    def log_xy(self):
        # функция вида log(x, y)
        text = self.text["text"]
        if text in ERROR:
            self.text["text"] = "0"
            return
        if text in ERROR:
            return

        if text in ("0.0", "0", ""):
            self.text["text"] = "log("
            return

        last_s_is_oper = len(text) > 0 and text[-1] in self.OPS + "("
        if last_s_is_oper:
            self.text["text"] += "log("

    def one_div_x(self):
        text = self.text["text"]
        if text in ERROR:
            self.text["text"] = "0"
            return
        self.text["text"] = f"1/({text})"

    def to_x2(self):
        text = self.text["text"]
        if text in ERROR:
            self.text["text"] = "0"
            return
        self.text["text"] = f"({text})^2"

    def fe_oper(self):
        text = self.text["text"]
        if text in ERROR:
            self.text["text"] = "0"
            return
        if not self.is_exp:
            if is_float(text):
                self.text["text"] = "%e" % float(text)
                self.is_exp = True
        else:
            self.text["text"] = str(eval(text))
            self.is_exp = False

    def change_sing(self):
        text = self.text["text"]
        if text in ERROR:
            self.text["text"] = "0"
            return
        if text[0] == "-":
            self.text["text"] = text[1:]
        else:
            self.text["text"] = "-" + text

    def function(self, event=None):
        func = event.widget.cget('text')
        text = self.text["text"]
        if text in ERROR:
            self.text["text"] = "0"
            return

        if text in ("", "0", "0.0"):
            self.text["text"] = func + "("
            return

        if is_float(text):
            try:
                self.text["text"] = str(eval(f"{func}({text})"))
            except Exception as e:
                if str(e) == "math domain error":
                    self.text["text"] = "error: value not in [-1, 1]"
            return

        last_s_is_oper = len(text) > 0 and text[-1] in self.OPS + "("
        if last_s_is_oper:
            self.text["text"] += f"{func}("

    # others
    def memory_op(self, event):
        func = event.widget.cget('text')
        self.calc()
        self.b_memory[func]: list
        box_id = self.b_memory[func].index(event.widget)
        text = self.text["text"]
        if func == "MC":
            self.memory.clear(box_id)

        elif func == "MS":
            self.memory.save(box_id, text)

        elif func == "MR":
            if text in ERROR:
                self.text["text"] = "0"
                return
            if text[-1] in "+-*/^(":
                self.text["text"] += self.memory.read(box_id)

        elif func == "M+":
            if text in ERROR:
                self.text["text"] = "0"
                return
            if text[-1] in "0123456789":
                self.text["text"] = self.memory.plus(box_id, text)

        elif func == "M-":
            if text in ERROR:
                self.text["text"] = "0"
                return
            if text[-1] in "0123456789":
                self.text["text"] = self.memory.sub(box_id, text)

    def ce(self):
        self.text["text"] = "0"
        self.stack.append("c")
        self.show_on_display()

    # расчет
    def calc(self):
        try:
            example = self.text["text"]
            example = example.replace("^", "**")
            example = example.replace("!", "factorial")
            res: float = eval(example)
            self.text["text"] = str(res)
            if "." in str(res):
                self.is_add_point = True
            if self.is_prog:    # если инженерный, то вывести на дисплей
                self.stack.append(example)
                self.stack.append("=")
                self.stack.append(str(res))
                self.show_on_display()
        except (SyntaxError, ZeroDivisionError, NameError) as e:
            if e == ZeroDivisionError:
                self.text["text"] = str(e)
            elif e == SyntaxError:
                return

    # refresh
    def prog_to_simple(self):
        self.is_prog = False
        self.b_prog["command"] = self.simple_to_prog
        self.b_x2.grid_remove()
        self.b_fe.grid_remove()
        self.b_log_xy.grid_remove()
        self.b_one_1x.grid_remove()
        self.b_comma.grid_remove()

        col = 0
        for btn in self.base_btns:
            grid_info = btn.grid_info()
            if grid_info["column"] > 4:
                btn.grid(row=2, column=col)
                col += 1
                continue
            row, col = grid_info["row"], grid_info["column"]
            btn.grid(row=row-1, column=col)

        for key in self.b_memory:
            for item in self.b_memory[key][1:]:
                item.grid_remove()

        self.display.grid_remove()
        self.t_id.grid_remove()
        self.label.grid_remove()
        self.b_show.grid_remove()

    def simple_to_prog(self):
        self.is_prog = True
        self.b_prog["command"] = self.prog_to_simple

        for btn in self.base_btns[:5]:
            btn.grid_remove()

        for btn in self.base_btns[5:]:
            grid_info = btn.grid_info()
            row, col = grid_info["row"], grid_info["column"]
            btn.grid(row=row + 1, column=col)

        self.b_x2.grid(row=2, column=0, sticky="nsew")
        self.b_fe.grid(row=2, column=1, sticky="nsew")
        self.b_log_xy.grid(row=2, column=2, sticky="nsew")
        self.b_one_1x.grid(row=2, column=3, sticky="nsew")
        self.b_comma.grid(row=2, column=4, sticky="nsew")

        self.b_factorial.grid(row=3, column=0, sticky="nsew")
        self.b_cos.grid(row=3, column=1, sticky="nsew")
        self.b_acos.grid(row=3, column=2, sticky="nsew")
        self.b_tan.grid(row=3, column=3, sticky="nsew")
        self.b_atan.grid(row=3, column=4, sticky="nsew")

        self.b_show.grid(row=10, column=1, columnspan=3, sticky="nsew")
        self.t_id.grid(row=9, column=1, columnspan=3, sticky="nsew")
        self.label.grid(row=9, column=0, sticky="nsew")

        self.refresh()

    # пересчет по ID
    def calc_count_boxes(self):
        text = self.t_id.get()
        if len(str(text)) < 3:
            return
        text = text[-3:]
        while len(text) > 1 and text != '10':
            text = str(sum([int(x) for x in text]))
        if text == '1':
            text = '2'
        return int(text)

    def calc_count_rows_in_display(self):
        text = self.t_id.get()
        if len(text) == 0:
            return

        while len(text) == 1 or text == '10':
            text = str(sum([int(x) for x in text]))
        self.count_rows_in_display = int(text)

    # отображение
    def show_memory(self, count=10):
        types = ("MS", "MC", "MR", "M+", "M-")
        for row in range(count):
            for key in self.b_memory.keys():
                self.b_memory[key][row].grid(row=row, column=types.index(key)+5, sticky="nsew")

        for row in range(count, 10):
            for key in self.b_memory.keys():
                self.b_memory[key][row].grid_remove()

    def refresh(self):
        # расчет числа ячеек памяти
        count_boxes = self.calc_count_boxes()
        self.show_memory(count_boxes if count_boxes else 10)

        # расчет кол-ва строк дисплея
        self.calc_count_rows_in_display()
        count_rows = self.count_rows_in_display
        self.display.grid(row=0, column=10, rowspan=5, columnspan=3, sticky="nsew")

    def show_on_display(self):
        self.display.delete('1.0', tk.END)
        count = 13  # число строчек на дисплее всего (взял просто запустив приложение и посчитав)
        print(self.display["height"])
        for line in self.stack:
            self.display.insert("end", line + "\n")
        for _ in range(count-self.count_rows_in_display):
            self.display.insert("end", "\n")
        self.display.see("end")


if __name__ == '__main__':
    wnd = Calc()
    wnd.mainloop()