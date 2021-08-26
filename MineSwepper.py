import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror

colors = {
    1: '#2100a6',
    2: '#076b07',
    3: '#bab241',
    4: '#53508a',
    5: '#b52ab0',
    6: '#0fb5b8',
    7: '#c45c33',
    8: '#d40b0b'
}


class MyButton(tk.Button):

    def __init__(self, master, x, y, number=0, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False


class MineSweeper:
    window = tk.Tk()
    ROW = 10
    COLUMNS = 10
    MINES = 20
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True

    def __init__(self):
        self.buttons = []
        for i in range(MineSweeper.ROW + 2):
            temp = []
            for j in range(MineSweeper.COLUMNS + 2):
                btn = MyButton(MineSweeper.window, x=i, y=j)
                btn.config(command=lambda button=btn: self.click(button))
                btn.bind("<Button-3>", self.right_click)
                temp.append(btn)
            self.buttons.append(temp)

    def right_click(self, event):
        if MineSweeper.IS_GAME_OVER:
            return
        cur_btn = event.widget
        if cur_btn['state'] == 'normal':
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '★'
            cur_btn['disabledforeground'] = 'pink'
        elif cur_btn['text'] == '★':
            cur_btn['text'] = ''
            cur_btn['state'] = 'normal'



    def click(self, clicked_button: MyButton):

        if MineSweeper.IS_GAME_OVER:
            return

        if MineSweeper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()
            self.print_buttons()
            MineSweeper.IS_FIRST_CLICK = False

        if clicked_button.is_mine:
            clicked_button.config(text="♥", background='pink', disabledforeground='black')
            clicked_button.is_open = True
            MineSweeper.IS_GAME_OVER = True
            showinfo('Game over', 'The game is over, sorry :(')
            for i in range(1, MineSweeper.ROW + 1):
                for j in range(1, MineSweeper.COLUMNS + 1):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '♥'
        else:
            color = colors.get(clicked_button.count_bomb, 'black')
            if clicked_button.count_bomb:
                clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color)
                clicked_button.is_open = True
            else:
                self.breadth_first_search(clicked_button)
        clicked_button.config(state='disabled')
        clicked_button.config(relief=tk.SUNKEN)

    def breadth_first_search(self, btn: MyButton):
        queue = [btn]
        while queue:

            cur_btn = queue.pop()
            color = colors.get(cur_btn.count_bomb, 'black')
            if cur_btn.count_bomb:
                cur_btn.config(text=cur_btn.count_bomb, disabledforeground=color)
            else:
                cur_btn.config(text=' ', disabledforeground=color)
            cur_btn.is_open = True
            cur_btn.config(state='disabled')
            cur_btn.config(relief=tk.SUNKEN)

            if cur_btn.count_bomb == 0:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        # if not abs(dx-dy) == 1:
                        #   continue

                        next_btn = self.buttons[x + dx][y + dy]
                        if not next_btn.is_open and 1 <= next_btn.x <= MineSweeper.ROW and \
                                1 <= next_btn.y <= MineSweeper.COLUMNS and next_btn not in queue:
                            queue.append(next_btn)

    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        MineSweeper.IS_FIRST_CLICK = True
        MineSweeper.IS_GAME_OVER = False

    def create_setting_win(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Настройки')
        tk.Label(win_settings, text='По диагонали').grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, MineSweeper.ROW)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='По вертикали').grid(row=1, column=0)
        column_entry = tk.Entry(win_settings)
        column_entry.insert(0, MineSweeper.COLUMNS)
        column_entry.grid(row=1, column=1, padx=20, pady=20)
        tk.Label(win_settings, text='Мины').grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0, MineSweeper.MINES)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        save_btn = tk.Button(win_settings, text='ОК',
                  command=lambda: self.change_setting(row_entry, column_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_setting(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror('Ошибка', 'Вы ввели неверное значение')
            return
        MineSweeper.ROW = int(row.get())
        MineSweeper.COLUMNS = int(column.get())
        MineSweeper.MINES = int(mines.get())
        self.reload()

    def create_widgets(self):

        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Играть', command=self.reload)
        settings_menu.add_command(label='Изменить', command=self.create_setting_win)
        settings_menu.add_command(label='Выйти', command=self.window.destroy)
        menubar.add_cascade(label='Настройки', menu=settings_menu)

        count = 1
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                btn.number = count
                btn.grid(row=i, column=j, stick='NWES')
                count += 1

        for i in range(1, MineSweeper.ROW + 1):
            tk.Grid.rowconfigure(self.window, i, weight=1)

        for j in range(1, MineSweeper.COLUMNS + 1):  # i no j
            tk.Grid.columnconfigure(self.window, j, weight=1)  # i no j

    def open_all_buttons(self):
        for i in range(MineSweeper.ROW + 2):
            for j in range(MineSweeper.COLUMNS + 2):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text="*", background='red', disabledforeground='black')
                elif btn.count_bomb in colors:  # даем цифрам свои цвета
                    color = colors.get(btn.count_bomb, 'black')
                    btn.config(text=btn.count_bomb, fg=color)

    def start(self):  # запуск игры
        self.create_widgets()  # вызываем кнопки
        # self.open_all_buttons()
        MineSweeper.window.mainloop()  # открываем окно в винде

    def print_buttons(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    print('B', end='')
                else:
                    print(btn.count_bomb, end='')
            print()

    def insert_mines(self, number: int):  # вставляем бомбы в значения кнопок
        index_mines = self.get_mines_places(number)
        print(index_mines)
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                if btn.number in index_mines:
                    btn.is_mine = True  # то мы значение кнопки с лжи меняем на правду то есть кладем в нее бомбу

    def count_mines_in_buttons(self):
        for i in range(1, MineSweeper.ROW + 1):
            for j in range(1, MineSweeper.COLUMNS + 1):
                btn = self.buttons[i][j]
                count_bomb = 0  # счетчик комб вблизи
                if not btn.is_mine:  # если нажатая кнопка не бомба
                    for row_dx in [-1, 0, 1]:  # координаты по колонкам вокруг нажатой кнопки
                        for col_dx in [-1, 0, 1]:  # координаты по строкам вокруг нажатой кнопки
                            neighbour = self.buttons[i + row_dx][j + col_dx]  # рассматриваем соседей
                            if neighbour.is_mine:  # если среди соседей есть бомбы
                                count_bomb += 1  # увеличиваем счетчик бомб на одну
                btn.count_bomb = count_bomb  # показываем итоговое число бомб

    @staticmethod
    def get_mines_places(exclude_number: int):  # генерируем бомбы
        indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROW + 1))
        print(f'Исключаем кнопку номер{exclude_number}')
        indexes.remove(exclude_number)
        shuffle(indexes)  # перемешиваем все номера ячеек
        return indexes[:MineSweeper.MINES]  # делаем срез по колличеству мин заданых в начале


game = MineSweeper()  # помещаем класс в переменную
game.start()  # вызываем старт игры
