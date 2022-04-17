# -*- coding: utf-8 -*-

import random

# для подсветки текста
from colorama import Fore, Back, Style

# загружаем словарь слов
f = open("dict.txt", "r", encoding="utf-8")
words = f.readlines()
words = [w.strip() for w in words] # обрезаем пробелы и переносы строки

# выбираем случайное слово
i = random.randrange(len(words))
word = words[i]

# число попыток
count = 5

# игровое поле
field = ["*****"] * count

def print_field(field):
    for line in field:
        print(line)

print_field(field)
i = 0 # счётчик попыток
while True:
    s = input("-> ").strip()
    if len(s) != 5:
        continue
    if not (s in words):
        continue
    # проверяем угадано ли слово
    if s == word:
        field[i] = Fore.GREEN + s + Style.RESET_ALL
        print_field(field)
        print("Слово угадано!")
        break
    # если слово целиком не угадано, то подсвечиваем буквы
    field[i] = ""
    for j in range(len(s)):
        if s[j] == word[j]:
            field[i] += Fore.GREEN  + s[j] + Style.RESET_ALL
        elif s[j] in word:
            field[i] += Fore.YELLOW + s[j] + Style.RESET_ALL
        else:
            field[i] += s[j]
    print_field(field)
    i += 1
    if i >= count:
        print("Игра закончена! Слово: " + Fore.RED + word + Style.RESET_ALL)
        break