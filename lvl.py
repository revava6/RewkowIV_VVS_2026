test_texts = {
    1: 'nPuBem MUP',
    2: 'Ботать это круто Очень кртуо',
    3: '1,2,3,4',
    5: '----pY+Hon;is;AWESome;----',
}

while True:
    print('\n--- Меню ---')
    print('1 - Уровень 1 (upper, lower, capitalize)')
    print('2 - Уровень 2 (find, replace, count)')
    print('3 - Уровень 3 (split, join)')
    print('4 - Уровень 4 (isdigit, isalpha, strip, format)')
    print('5 - Уровень 5 (Практика: очистка строки "----pY+Hon;is;AWESome;----")')
    print('0 - Выход')

    level = int(input('Выберите уровень (1, 2, 3, 4, 5 или 0 для выхода): '))

    if level == 0:
        print('Пока!')
        break

    if level not in (1, 2, 3, 4, 5):
        print('Нет такого уровня!')
        continue

    test = int(input('Тестовый режим? (1 - да, 0 - нет): '))
    if test == 1:
        if level == 4:
            which = int(input('Какую тестовую строку взять? (1 - "1234*&%$", 2 - "___abc1234___"): '))
            if which == 1:
                s = '1234*&%$'
            else:
                s = '___abc1234___'
        else:
            s = test_texts[level]
        print('Тестовая строка:', s)
    else:
        s = input('Введите текст: ')

    if level == 1:
        print('\nВаш текст:', s)
        print('Метод str.upper() вернет строку в верхнем регистре.')
        print('Метод str.lower() вернет строку в нижнем регистре.')
        print('Метод str.capitalize() сделает первую букву заглавной, остальные строчными.')

        method = int(input('Выберите метод (1 - upper, 2 - lower, 3 - capitalize): '))
        if method == 1:
            print(s.upper())
        elif method == 2:
            print(s.lower())
        elif method == 3:
            print(s.capitalize())
        else:
            print('Нет такого метода!')

    elif level == 2:
        print('\nВаш текст:', s)
        print('Метод str.find() возвращает индекс первого совпадения подстроки.')
        print('Метод str.replace() заменяет подстроку old на new.')
        print('Метод str.count() считает количество вхождений подстроки.')

        method = int(input('Выберите метод (1 - find, 2 - replace, 3 - count): '))
        if method == 1:
            sub = input('Что искать: ')
            print('Индекс:', s.find(sub))
        elif method == 2:
            old = input('Что заменить: ')
            new = input('На что заменить: ')
            print('Результат:', s.replace(old, new))
        elif method == 3:
            sub = input('Что посчитать: ')
            print('Количество:', s.count(sub))
        else:
            print('Нет такого метода!')

    elif level == 3:
        print('\nВаш текст:', s)
        print('1 - только split (разбивает строку на список)')
        print('2 - только join (склеивает список в строку)')
        print('3 - и split, и join')

        method = int(input('Выберите метод (1 - split, 2 - join, 3 - оба): '))

        if method in (1, 3):
            sep = input('Введите разделитель для split (Enter - пробел): ')
            if sep == '':
                parts = s.split()
            else:
                parts = s.split(sep)
            print('Результат split:', parts)

        if method in (2, 3):
            str1 = input('Введите первую строку для join: ')
            str2 = input('Введите вторую строку для join: ')
            sep2 = input('Введите разделитель (Enter - без разделителя): ')
            print('Результат join:', sep2.join([str1, str2]))

        if method not in (1, 2, 3):
            print('Нет такого метода!')

    elif level == 4:
        print('\nВаш текст:', s)
        print('1 - isdigit() (проверка: только ли цифры в строке)')
        print('2 - isalpha() (проверка: только ли буквы в строке)')
        print('3 - strip() (удаление символов или пробелов с краёв)')
        print('4 - format() и f-строка (форматирование)')

        method = int(input('Выберите метод (1 - isdigit, 2 - isalpha, 3 - strip, 4 - format): '))

        if method == 1:
            print('Только цифры?:', s.isdigit())
        elif method == 2:
            print('Только буквы?:', s.isalpha())
        elif method == 3:
            char = input('Какой символ удалить с краёв (Enter - пробелы): ')
            if char == '':
                print('Результат strip():', repr(s.strip()))
            else:
                print(f'Результат strip("{char}"):', repr(s.strip(char)))
        elif method == 4:
            name = input('Введите ваше имя для вставки: ')
            res_format = "Привет, {}! Твой текст: '{}'".format(name, s)
            res_fstring = f"Привет, {name}! Твой текст: '{s}'"
            print('\nЧерез .format():', res_format)
            print('Через f-строку: ', res_fstring)
        else:
            print('Нет такого метода!')

    elif level == 5:
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

            words = []
            for word in step2.split(';'):
                if word:
                    words.append(word)
            print('3) Разбиваем на слова через split(";"):', words)
            if not words:
                print('После очистки строка пустая.')
                continue

            fixed_words = [words[0].capitalize()]
            for word in words[1:]:
                fixed_words.append(word.lower())
            step4 = " ".join(fixed_words)
            print('4) Собираем красивую строку через join(" "):', step4)

            result = f"{step4}!"
            print('5) Итоговый результат:', result)

        elif choice == 2:
            sym_strip = input('Что удалить по краям strip (например, -): ')
            if sym_strip:
                cleaned = s.strip(sym_strip)
            else:
                cleaned = s.strip()

            old_ch = input('Что заменить (replace old): ')
            new_ch = input('На что заменить (replace new): ')
            cleaned = cleaned.replace(old_ch, new_ch)

            sep = input('Разделитель для split (Enter - пробел): ')
            if sep == '':
                parts = cleaned.split()
            else:
                parts = []
                for part in cleaned.split(sep):
                    if part:
                        parts.append(part)

            join_sym = input('Чем склеить обратно (например, пробел): ')
            final_res = join_sym.join(parts)
            print('Итог ручной очистки:', final_res)
        else:
            print('Нет такого варианта!')
