# -*- coding: utf-8 -*-

import random
from tkinter import * 
from tkinter import ttk
from tkinter import messagebox

def load_dict(fn):
    f = open(fn, "r", encoding="utf-8")
    words = f.readlines()
# Обрезаем пробелы и переносы строки
    words = [w.strip() for w in words]
    return words

def change_word():
    global word
    i = random.randrange(len(words))
    word = words[i]

def init_words():
    global words
# Загружаем словарь слов
words = load_dict("dict.txt")
change_word()

# Игровое поле
def create_field(frm, count):
    field = []
    for i in range(count):
        row = []
        for j in range(5):
            l = ttk.Label(frm, text=" ", style="Wordle.Cell.TLabel")
            row.append(l)
        field.append(row)
    return field

def init_field(frame):
    global field
    field = create_field(frame, count)
    for row in range(len(field)):
        for col in range(len(field[row])):
            field[row][col].grid(column=col, row=row, padx=1, pady=1, ipady=14, sticky="nswe")

def init_onscreen_keyboard(frame, letters):
    keyboard_dic = {}
    for row in range(len(letters)):
        for col in range(len(letters[row])):
            letter = letters[row][col]
            b = ttk.Button(frame, text=letter, style="Wordle.TButton")
            b.bind("<Button-1>", on_screen_keypress)
            keyboard_dic[letter] = b
            b.grid(column=col, row=row, sticky="nswe", padx=1, pady=1)
    # Кнопки для Enter и Backspace
    btn_backspace = ttk.Button(frame, text="<---", style="Wordle.TButton")
    btn_backspace.bind("<Button-1>", on_backspace)
    btn_backspace.grid(column=0, row=len(letters), sticky="nswe", padx=1, pady=1)
    btn_enter = ttk.Button(frame, text="<Ввод>", style="Wordle.TButton")
    btn_enter.bind("<Button-1>", on_enter)
    btn_enter.grid(column=1, row=len(letters), sticky="nswe", padx=1, pady=1) 
    return keyboard_dic

def clear_onscreen_keyboard():
    for b in keyboard_dic.values():
        b["style"] = "Wordle.TButton"

def init_menu(frame):
    ttk.Button(frame, text="Новая игра", command=new_game).grid(column=0, row=0, padx=1, sticky="nswe")
    ttk.Button(frame, text="Выйти", command=quit_game).grid(column=1, row=0, padx=1, sticky="nswe")

def reset():
    global cursor_row, cursor_col
    cursor_col = 0
    cursor_row = 0
    clear_field() 
    clear_onscreen_keyboard()
    change_word()

def new_game():
    reset()

def quit_game():
    window.destroy()

def clear_field():
    for row in range(len(field)):
        for col in range(len(field[row])):
            field[row][col]["text"] = " "
            field[row][col]["style"] = "Wordle.Cell.TLabel"

def you_won():
    messagebox.showinfo("Победа", "Слово угадано!")
    reset()

def game_over():
    messagebox.showinfo("Игра окончена!", "Слово не угадано: " + word)
    reset()

def handle_char_press(c):
    global cursor_row, cursor_col
    if(c.strip() == ""):
        return
    if(c in "".join(keyboard)):
        if cursor_col < len(field[0]):
            field[cursor_row][cursor_col]["text"] = c
            cursor_col += 1

def on_keypress(event):
    handle_char_press(event.char)

def on_screen_keypress(event):
    c = event.widget["text"]
    handle_char_press(c)

def on_enter(event):
    global cursor_row, cursor_col
    if cursor_col < len(field[cursor_row]):
        return
    typed_word = ""
    for i in range(len(field[cursor_row])):
        typed_word += field[cursor_row][i]["text"]
    if not (typed_word in words):
       return

# Подсвечиваем угаданные буквы
    for i in range(len(field[cursor_row])):
        cell = field[cursor_row][i]
        if cell["text"].upper() == word[i].upper():
            cell["style"] = "Wordle.Cell.Green.TLabel"
            keyboard_dic[cell["text"]]["style"] = "Wordle.Green.TButton"
        elif cell["text"] in word:
            cell["style"] = "Wordle.Cell.Yellow.TLabel"
            keyboard_dic[cell["text"]]["style"] = "Wordle.Yellow.TButton"
        else:
            cell["style"] = "Wordle.Cell.Gray.TLabel"
            keyboard_dic[cell["text"]]["style"] = "Wordle.Gray.TButton"

# Победа
    if typed_word == word:
        you_won()
        return

# Поражение
    if cursor_row == count - 1:
        game_over()
        return

    cursor_row += 1
    cursor_col = 0

def on_backspace(event):
    global cursor_row, cursor_col
    if cursor_col > 0:
        cursor_col -= 1
    field[cursor_row][cursor_col]["text"] = " "

# Число попыток
count = 6

# Размер слова
word_size = 5

# Курсор
cursor_row = 0
cursor_col = 0

window = Tk()
window.title("Wordle")
Grid.rowconfigure(window, 0, weight=1)
Grid.columnconfigure(window, 0, weight=1)

# Стили
ttk.Style().configure("Wordle.TButton", foreground="#000000", background="#e4e7eb", relief="flat")
ttk.Style().configure("Wordle.Green.TButton", foreground="#ffffff", background="#6aaa64")
ttk.Style().configure("Wordle.Yellow.TButton", foreground="#ffffff", background="#c9b458")
ttk.Style().configure("Wordle.Gray.TButton", foreground="#ffffff", background="#787c7e")
ttk.Style().configure("Wordle.TFrame")

font = ("Roboto Bold", 16)
ttk.Style().configure("Wordle.Cell.TLabel", background='white', foreground = "black", font = font, anchor="center", width=5) 
ttk.Style().configure("Wordle.Cell.Yellow.TLabel", background = "#c9b458", foreground = "#ffffff", anchor="center", font = font, width=5)
ttk.Style().configure("Wordle.Cell.Gray.TLabel", background = "#787c7e", foreground = "#ffffff", anchor="center", font = font, width=5)
ttk.Style().configure("Wordle.Cell.Green.TLabel", background = "#6aaa64", foreground = "#ffffff", anchor="center", font = font, width=5)

# Загружаем словарь
init_words()

# Инициализация поля
frm = ttk.Frame(window, padding=10, style="Wordle.TFrame")
frm.grid()
init_field(frm)

# Инициализация экранной клаиватуры
keyboard = ["ёйцук", "енгшщ", "зхъфы", "вапро", "лджэя", "чсмит", "ьбю"]
frm2 = ttk.Frame(window, padding=10, style="Wordle.TFrame")
frm2.grid()
keyboard_dic = init_onscreen_keyboard(frm2, keyboard)

# Обработчики нажатия на физическую клавиатуру
window.bind("<Key>", on_keypress)
window.bind("<Return>", on_enter)
window.bind("<BackSpace>", on_backspace)

frm3 = ttk.Frame(window, padding=10, style="Wordle.TFrame")
frm3.grid()
init_menu(frm3)

window.mainloop() 