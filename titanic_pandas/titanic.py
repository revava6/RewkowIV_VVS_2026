"""Практическая работа: анализ данных Титаника с помощью Pandas и NumPy."""

import numpy as np
import pandas as pd

# Чтобы широкие таблицы целиком влезали в вывод, а не обрезались многоточием
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)


def section(title):
    """Печатает заголовок раздела, чтобы вывод было удобно читать."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


# ---------------------------------------------------------------------------
# Часть II. Загрузка и первичный анализ данных
# ---------------------------------------------------------------------------
section("Часть II. Загрузка и первичный анализ")

# 6. Загружаем CSV в DataFrame
df = pd.read_csv("titanic.csv")
print("6. Файл загружен.")

# 7. Первые n строк, n вводит пользователь
n = int(input("7. Сколько первых строк показать? n = "))
print(df.head(n))

# 8. Последние 5 строк
print("\n8. Последние 5 строк:")
print(df.tail(5))

# 9. Размер таблицы
rows, cols = df.shape
print(f"\n9. Строк: {rows}, столбцов: {cols}")

# 10. Названия столбцов
print("\n10. Столбцы:", list(df.columns))

# 11. Типы данных
print("\n11. Типы данных:")
print(df.dtypes)

# 12. Числовые и категориальные признаки (делим по смыслу, не по типу dtype)
# Pclass хранится числами, но это категория (класс 1/2/3), см. контрольный вопрос
numeric_cols = ["Age", "SibSp", "Parch", "Fare"]
categorical_cols = ["Survived", "Pclass", "Sex", "Embarked", "Cabin", "Ticket", "Name"]
print("\n12. Числовые по смыслу:", numeric_cols)
print("    Категориальные по смыслу:", categorical_cols)
print("    (PassengerId - просто номер строки, как признак не используем)")

# 13. Описательная статистика числовых признаков
print("\n13. Статистика числовых признаков:")
stats = df[numeric_cols].agg(["mean", "median", "min", "max", "std"]).T
stats.columns = ["среднее", "медиана", "минимум", "максимум", "ст.откл."]
print(stats.round(2))

# 14. Пассажиры по классам
print("\n14. Пассажиров в каждом классе:")
print(df["Pclass"].value_counts().sort_index())

# 15. Уникальные значения в Embarked
print("\n15. Уникальных значений в Embarked:", df["Embarked"].nunique())
print("    Это:", list(df["Embarked"].dropna().unique()))

# ---------------------------------------------------------------------------
# Часть III. Обработка пропущенных значений
# ---------------------------------------------------------------------------
section("Часть III. Обработка пропусков")

shape_before = df.shape  # запомним для пункта 26

# 16. Пропуски в каждом столбце
missing = df.isna().sum()
print("16. Пропусков по столбцам:")
print(missing)

# 17. Процент пропусков
missing_pct = (missing / len(df) * 100).round(2)
print("\n17. Процент пропусков (%):")
print(missing_pct)

# 18. Столбец с максимумом пропусков
print(f"\n18. Больше всего пропусков в столбце: {missing.idxmax()} ({missing.max()} шт.)")


def age_stats(series):
    """Шесть характеристик возраста для таблицы «до / после»."""
    return {
        "Среднее арифметическое": series.mean(),
        "Медиана": series.median(),
        "Минимальный возраст": series.min(),
        "Максимальный возраст": series.max(),
        "Стандартное отклонение": series.std(),
        "Количество известных значений": series.count(),
    }


# 19. Статистика Age ДО заполнения
age_before = age_stats(df["Age"])

# 20. Заполняем пропуски медианой, посчитанной по известным возрастам
age_median = df["Age"].median()  # median() сам игнорирует NaN
df["Age"] = df["Age"].fillna(age_median)
print(f"\n20. Пропуски в Age заполнены медианой = {age_median}")

# 21. Статистика Age ПОСЛЕ заполнения
age_after = age_stats(df["Age"])

# 22. Таблица «до / после»
compare = pd.DataFrame({"До обработки": age_before, "После обработки": age_after})
print("\n22. Сравнение Age до / после:")
print(compare.round(2))

# 23. Удаляем строки без Embarked
df = df.dropna(subset=["Embarked"])
print(f"\n23. После удаления строк без Embarked осталось строк: {len(df)}")

# 24. Доля пропусков в Cabin; если больше 50% - удаляем столбец
cabin_share = missing["Cabin"] / shape_before[0] * 100
print(f"\n24. Доля пропусков в Cabin: {cabin_share:.2f}%")
if cabin_share > 50:
    df = df.drop(columns="Cabin")
    print("    Больше 50% -> столбец Cabin удалён.")

# 25. Что осталось пропущенным
print("\n25. Оставшиеся пропуски:")
print(df.isna().sum())

# 26. Размер до и после
print(f"\n26. Размер до: {shape_before}, после: {df.shape}")

# ---------------------------------------------------------------------------
# Часть IV. Анализ данных с помощью NumPy
# ---------------------------------------------------------------------------
section("Часть IV. NumPy")

# Переводим нужные столбцы в массивы NumPy
survived = df["Survived"].to_numpy()
sex = df["Sex"].to_numpy()
age = df["Age"].to_numpy()
fare = df["Fare"].to_numpy()  # на случай NaN используем nanmin/nanmax/nanmean

male = sex == "male"      # булева маска: True там, где мужчина
female = sex == "female"
alive = survived == 1
dead = survived == 0

# 31. Общий процент выживших (среднее по 0/1 = доля единиц)
print(f"31. Выжило всего: {np.mean(survived) * 100:.2f}%")

# 32. Процент выживших среди мужчин и женщин
surv_m = np.mean(survived[male]) * 100
surv_f = np.mean(survived[female]) * 100
print(f"32. Мужчины: {surv_m:.2f}%, женщины: {surv_f:.2f}%")

# 33. Средний возраст мужчин и женщин
print(f"33. Средний возраст: мужчины {np.mean(age[male]):.2f}, женщины {np.mean(age[female]):.2f}")

# 34. Средний возраст выживших и погибших отдельно по полу
age_m_alive = np.mean(age[male & alive])
age_m_dead = np.mean(age[male & dead])
age_f_alive = np.mean(age[female & alive])
age_f_dead = np.mean(age[female & dead])
print("34. Средний возраст выживших / погибших:")
print(f"    мужчины: выжившие {age_m_alive:.2f}, погибшие {age_m_dead:.2f}")
print(f"    женщины: выжившие {age_f_alive:.2f}, погибшие {age_f_dead:.2f}")

# 35. Стоимость билета
print(f"35. Билет: min {np.nanmin(fare):.2f}, max {np.nanmax(fare):.2f}, средняя {np.nanmean(fare):.2f}")

# 36. Стандартное отклонение возраста (после заполнения медианой)
print(f"36. Стандартное отклонение возраста: {np.std(age, ddof=1):.2f}")

# Сводная таблица сравнения
numpy_table = pd.DataFrame(
    {
        "Мужчины": [surv_m, np.mean(age[male]), age_m_alive, age_m_dead],
        "Женщины": [surv_f, np.mean(age[female]), age_f_alive, age_f_dead],
    },
    index=["Выжило, %", "Средний возраст", "Ср. возраст выживших", "Ср. возраст погибших"],
)
print("\nТаблица сравнения мужчин и женщин:")
print(numpy_table.round(2))

# ---------------------------------------------------------------------------
# Часть V. Фильтрация данных
# ---------------------------------------------------------------------------
section("Часть V. Фильтрация")

# Задание 1: мужчины старше 30, первый класс
f1 = df[(df["Sex"] == "male") & (df["Age"] > 30) & (df["Pclass"] == 1)]
print(f"Задание 1. Найдено пассажиров: {len(f1)}")
print(f1.head(10))

# Задание 2: моложе 18 лет ИЛИ (женщины, которые выжили)
f2 = df[(df["Age"] < 18) | ((df["Sex"] == "female") & (df["Survived"] == 1))]
print(f"\nЗадание 2. Найдено пассажиров: {len(f2)}")

# Задание 3: 3 класс, билет дороже среднего по этому классу
mean_fare_3 = df.loc[df["Pclass"] == 3, "Fare"].mean()
f3 = df[(df["Pclass"] == 3) & (df["Fare"] > mean_fare_3)]
print(f"\nЗадание 3. Средняя цена билета в 3 классе: {mean_fare_3:.2f}")
print(f"          Пассажиров с билетом дороже: {len(f3)}")

# Задание 4: возраст от 20 до 40 включительно, порт S
f4 = df[df["Age"].between(20, 40) & (df["Embarked"] == "S")]
print(f"\nЗадание 4. Найдено пассажиров: {len(f4)}")

# ---------------------------------------------------------------------------
# Часть VI. Группировка и агрегирование
# ---------------------------------------------------------------------------
section("Часть VI. Группировка")

# 37. По классу и полу
by_class_sex = (
    df.groupby(["Pclass", "Sex"])
    .agg(
        Количество=("PassengerId", "count"),
        Средний_возраст=("Age", "mean"),
        Выжило_процент=("Survived", lambda s: s.mean() * 100),
        Средний_билет=("Fare", "mean"),
    )
    .round(2)
)
print("37. Группировка по Pclass и Sex:")
print(by_class_sex)

# 38. По порту посадки
by_port = (
    df.groupby("Embarked")
    .agg(Количество=("PassengerId", "count"), Выжило_процент=("Survived", lambda s: s.mean() * 100))
    .round(2)
)
print("\n38. Группировка по Embarked:")
print(by_port)

# 39. Класс с наибольшей долей выживших
surv_by_class = df.groupby("Pclass")["Survived"].mean() * 100
print("\n39. Выжило по классам (%):")
print(surv_by_class.round(2))
print(f"    Максимум: класс {surv_by_class.idxmax()} ({surv_by_class.max():.2f}%)")

# ---------------------------------------------------------------------------
# Часть VII. Сохранение результатов
# ---------------------------------------------------------------------------
section("Часть VII. Сохранение")

# 40. Обработанная таблица, 41. результаты группировки (индекс нужен - в нём Pclass и Sex)
df.to_csv("titanic_processed.csv", index=False)
by_class_sex.to_csv("titanic_statistics.csv")
print("40-41. Сохранено: titanic_processed.csv, titanic_statistics.csv")

# 42. Загружаем обратно и сверяем с тем, что было в памяти
check = pd.read_csv("titanic_processed.csv")
pd.testing.assert_frame_equal(check, df.reset_index(drop=True), check_dtype=False)
print(f"42. Проверка пройдена: загружено {check.shape[0]} строк, {check.shape[1]} столбцов, данные совпадают.")
check_stats = pd.read_csv("titanic_statistics.csv", index_col=["Pclass", "Sex"])
pd.testing.assert_frame_equal(check_stats, by_class_sex, check_dtype=False)
print("    Статистика тоже сохранилась корректно.")
