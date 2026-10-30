# Базовые тестовые строки
t = 'nPuBem MUP'
t1 = 'Ботать это круто Очень кртуо'
t2 = '1,2,3,4'

# Тестовые строки с доски для 4 и 5 уровней
text_4a = "1234*&%$"
text_4b = "___abc1234___"
text_5 = "----pY+Hon;is;AWESome;----"

while True:
    print('\n--- Меню ---')
    print('1 - Уровень 1 (upper, lower, capitalize)')
    print('2 - Уровень 2 (find, replace, count)')
    print('3 - Уровень 3 (split, join)')
    print('4 - Уровень 4 (isdigit, isalpha, strip, format)')
    print('5 - Уровень 5 (Практика: очистка строки "----pY+Hon;is;AWESome;----")')
    print('0 - Выход')

    a = int(input('Выберите уровень (1, 2, 3, 4, 5 или 0 для выхода): '))

    if a == 0:
        print('Пока!')
        break

    if a not in (1, 2, 3, 4, 5):
        print('Нет такого уровня!')
        continue

    # Выбор тестового режима
    test = int(input('Тестовый режим? (1 - да, 0 - нет): '))
    if test == 1:
        if a == 1:
            s = t
        elif a == 2:
            s = t1
        elif a == 3:
            s = t2
        elif a == 4:
            # На 4 уровне на доске две разные тестовые строки
            which = int(input('Какую тестовую строку взять? (1 - "1234*&%$", 2 - "___abc1234___"): '))
            s = text_4a if which == 1 else text_4b
        else:
            s = text_5
        print('Тестовая строка:', s)
    else:
        s = input('Введите текст: ')

    # ---------- УРОВЕНЬ 1 ----------
    if a == 1:
        print('\nВаш текст:', s)
        print('Метод str.upper() вернет строку в верхнем регистре.')
        print('Метод str.lower() вернет строку в нижнем регистре.')
        print('Метод str.capitalize() сделает первую букву заглавной, остальные строчными.')

        b = int(input('Выберите метод (1 - upper, 2 - lower, 3 - capitalize): '))
        if b == 1:
            print(s.upper())
        elif b == 2:
            print(s.lower())
        elif b == 3:
            print(s.capitalize())
        else:
            print('Нет такого метода!')

    # ---------- УРОВЕНЬ 2 ----------
    elif a == 2:
        print('\nВаш текст:', s)
        print('Метод str.find() возвращает индекс первого совпадения подстроки.')
        print('Метод str.replace() заменяет подстроку old на new.')
        print('Метод str.count() считает количество вхождений подстроки.')

        b = int(input('Выберите метод (1 - find, 2 - replace, 3 - count): '))
        if b == 1:
            sub = input('Что искать: ')
            print('Индекс:', s.find(sub))
        elif b == 2:
            old = input('Что заменить: ')
            new = input('На что заменить: ')
            print('Результат:', s.replace(old, new))
        elif b == 3:
            sub = input('Что посчитать: ')
            print('Количество:', s.count(sub))
        else:
            print('Нет такого метода!')

    # ---------- УРОВЕНЬ 3 ----------
    elif a == 3:
        print('\nВаш текст:', s)
        print('1 - только split (разбивает строку на список)')
        print('2 - только join (склеивает список в строку)')
        print('3 - и split, и join')

        b = int(input('Выберите метод (1 - split, 2 - join, 3 - оба): '))

        if b == 1 or b == 3:
            sep = input('Введите разделитель для split (Enter - пробел): ')
            if sep == '':
                parts = s.split()
            else:
                parts = s.split(sep)
            print('Результат split:', parts)

        if b == 2 or b == 3:
            str1 = input('Введите первую строку для join: ')
            str2 = input('Введите вторую строку для join: ')
            sep2 = input('Введите разделитель (Enter - без разделителя): ')
            print('Результат join:', sep2.join([str1, str2]))

        if b not in (1, 2, 3):
            print('Нет такого метода!')

    # ---------- УРОВЕНЬ 4 ----------
    elif a == 4:
        print('\nВаш текст:', s)
        print('1 - isdigit() (проверка: только ли цифры в строке)')
        print('2 - isalpha() (проверка: только ли буквы в строке)')
        print('3 - strip() (удаление символов или пробелов с краёв)')
        print('4 - format() и f-строка (форматирование)')

        b = int(input('Выберите метод (1 - isdigit, 2 - isalpha, 3 - strip, 4 - format): '))

        if b == 1:
            print('Только цифры?:', s.isdigit())
        elif b == 2:
            print('Только буквы?:', s.isalpha())
        elif b == 3:
            char = input('Какой символ удалить с краёв (Enter - пробелы): ')
            if char == '':
                print('Результат strip():', repr(s.strip()))
            else:
                print(f'Результат strip("{char}"):', repr(s.strip(char)))
        elif b == 4:
            name = input('Введите ваше имя для вставки: ')
            # Показываем и .format(), и f-строку (как было на доске)
            res_format = "Привет, {}! Твой текст: '{}'".format(name, s)
            res_fstring = f"Привет, {name}! Твой текст: '{s}'"
            print('\nЧерез .format():', res_format)
            print('Через f-строку: ', res_fstring)
        else:
            print('Нет такого метода!')

    # ---------- УРОВЕНЬ 5 ----------
    elif a == 5:
        print('\nВаш исходный текст:', s)
        print('Задача уровня 5 — очистить строку и привести её к идеальному виду.')
        print('1 - Автоматическая пошаговая очистка (решение задачи с доски)')
        print('2 - Очистить вручную своими параметрами')

        choice = int(input('Выберите вариант (1 или 2): '))

        if choice == 1:
            step1 = s.strip('-')
            print('1) Убираем дефисы по краям strip("-"):', step1)

            step2 = step1.replace('+', 't')
            print('2) Исправляем опечатку replace("+", "t"):', step2)

            step3 = step2.split(';')
            # Фильтруем пустые элементы от точек с запятой на конце
            words = [w for w in step3 if w != '']
            print('3) Разбиваем на слова через split(";"):', words)

            # Приводим к красивому регистру каждое слово
            fixed_words = [words[0].capitalize(), words[1].lower(), words[2].lower()]
            step4 = " ".join(fixed_words)
            print('4) Собираем красивую строку через join(" "):', step4)

            # Финальная f-строка
            result = f"{step4}!"
            print('5) Итоговый результат:', result)

        elif choice == 2:
            sym_strip = input('Что удалить по краям strip (например, -): ')
            cleaned = s.strip(sym_strip) if sym_strip else s.strip()

            old_ch = input('Что заменить (replace old): ')
            new_ch = input('На что заменить (replace new): ')
            cleaned = cleaned.replace(old_ch, new_ch)

            sep = input('Разделитель для split (например, ;): ')
            parts = [p for p in cleaned.split(sep) if p]

            join_sym = input('Чем склеить обратно (например, пробел): ')
            final_res = join_sym.join(parts)
            print('Итог ручной очистки:', final_res)
        else:
            print('Нет такого варианта!')
