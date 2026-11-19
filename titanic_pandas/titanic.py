import numpy as np
import pandas as pd

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)


def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def age_stats(series):
    return {
        "Среднее арифметическое": series.mean(),
        "Медиана": series.median(),
        "Минимальный возраст": series.min(),
        "Максимальный возраст": series.max(),
        "Стандартное отклонение": series.std(),
        "Количество известных значений": series.count(),
    }


section("Часть II. Загрузка и первичный анализ")

df = pd.read_csv("titanic.csv")
print("6. Файл загружен.")

n = int(input("7. Сколько первых строк показать? n = "))
print(df.head(n))

print("\n8. Последние 5 строк:")
print(df.tail(5))

shape_before = df.shape
rows, cols = shape_before
print(f"\n9. Строк: {rows}, столбцов: {cols}")

print("\n10. Столбцы:", list(df.columns))

print("\n11. Типы данных:")
print(df.dtypes)

numeric_cols = ["Age", "SibSp", "Parch", "Fare"]
categorical_cols = ["Survived", "Pclass", "Sex", "Embarked", "Cabin", "Ticket", "Name"]
print("\n12. Числовые по смыслу:", numeric_cols)
print("    Категориальные по смыслу:", categorical_cols)
print("    (PassengerId - просто номер строки, как признак не используем)")

print("\n13. Статистика числовых признаков:")
stats = df[numeric_cols].agg(["mean", "median", "min", "max", "std"]).T
stats.columns = ["среднее", "медиана", "минимум", "максимум", "ст.откл."]
print(stats.round(2))

print("\n14. Пассажиров в каждом классе:")
print(df["Pclass"].value_counts().sort_index())

print("\n15. Уникальных значений в Embarked:", df["Embarked"].nunique())
print("    Это:", list(df["Embarked"].dropna().unique()))

section("Часть III. Обработка пропусков")

missing = df.isna().sum()
print("16. Пропусков по столбцам:")
print(missing)

missing_pct = (missing / len(df) * 100).round(2)
print("\n17. Процент пропусков (%):")
print(missing_pct)

print(f"\n18. Больше всего пропусков в столбце: {missing.idxmax()} ({missing.max()} шт.)")

age_before = age_stats(df["Age"])

age_median = age_before["Медиана"]
df["Age"] = df["Age"].fillna(age_median)
print(f"\n20. Пропуски в Age заполнены медианой = {age_median}")

age_after = age_stats(df["Age"])

compare = pd.DataFrame({"До обработки": age_before, "После обработки": age_after})
print("\n22. Сравнение Age до / после:")
print(compare.round(2))

df = df.dropna(subset=["Embarked"])
print(f"\n23. После удаления строк без Embarked осталось строк: {len(df)}")

cabin_share = missing["Cabin"] / rows * 100
print(f"\n24. Доля пропусков в Cabin: {cabin_share:.2f}%")
if cabin_share > 50:
    df = df.drop(columns="Cabin")
    print("    Больше 50% -> столбец Cabin удалён.")

print("\n25. Оставшиеся пропуски:")
print(df.isna().sum())

print(f"\n26. Размер до: {shape_before}, после: {df.shape}")

section("Часть IV. NumPy")

survived = df["Survived"].to_numpy()
sex = df["Sex"].to_numpy()
age = df["Age"].to_numpy()
fare = df["Fare"].to_numpy()

male = sex == "male"
female = sex == "female"
alive = survived == 1
dead = survived == 0

print(f"31. Выжило всего: {np.mean(survived) * 100:.2f}%")

surv_m = np.mean(survived[male]) * 100
surv_f = np.mean(survived[female]) * 100
print(f"32. Мужчины: {surv_m:.2f}%, женщины: {surv_f:.2f}%")

age_m = np.mean(age[male])
age_f = np.mean(age[female])
print(f"33. Средний возраст: мужчины {age_m:.2f}, женщины {age_f:.2f}")

age_m_alive = np.mean(age[male & alive])
age_m_dead = np.mean(age[male & dead])
age_f_alive = np.mean(age[female & alive])
age_f_dead = np.mean(age[female & dead])
print("34. Средний возраст выживших / погибших:")
print(f"    мужчины: выжившие {age_m_alive:.2f}, погибшие {age_m_dead:.2f}")
print(f"    женщины: выжившие {age_f_alive:.2f}, погибшие {age_f_dead:.2f}")

print(f"35. Билет: min {np.nanmin(fare):.2f}, max {np.nanmax(fare):.2f}, средняя {np.nanmean(fare):.2f}")

print(f"36. Стандартное отклонение возраста: {np.std(age, ddof=1):.2f}")

numpy_table = pd.DataFrame(
    {
        "Мужчины": [surv_m, age_m, age_m_alive, age_m_dead],
        "Женщины": [surv_f, age_f, age_f_alive, age_f_dead],
    },
    index=["Выжило, %", "Средний возраст", "Ср. возраст выживших", "Ср. возраст погибших"],
)
print("\nТаблица сравнения мужчин и женщин:")
print(numpy_table.round(2))

section("Часть V. Фильтрация")

f1 = df[(df["Sex"] == "male") & (df["Age"] > 30) & (df["Pclass"] == 1)]
print(f"Задание 1. Найдено пассажиров: {len(f1)}")
print(f1.head(10))

f2 = df[(df["Age"] < 18) | ((df["Sex"] == "female") & (df["Survived"] == 1))]
print(f"\nЗадание 2. Найдено пассажиров: {len(f2)}")

class_3 = df["Pclass"] == 3
mean_fare_3 = df.loc[class_3, "Fare"].mean()
f3 = df[class_3 & (df["Fare"] > mean_fare_3)]
print(f"\nЗадание 3. Средняя цена билета в 3 классе: {mean_fare_3:.2f}")
print(f"          Пассажиров с билетом дороже: {len(f3)}")

f4 = df[df["Age"].between(20, 40) & (df["Embarked"] == "S")]
print(f"\nЗадание 4. Найдено пассажиров: {len(f4)}")

section("Часть VI. Группировка")

by_class_sex = df.groupby(["Pclass", "Sex"]).agg(
    Количество=("PassengerId", "count"),
    Средний_возраст=("Age", "mean"),
    Выжило_процент=("Survived", "mean"),
    Средний_билет=("Fare", "mean"),
)
by_class_sex["Выжило_процент"] = by_class_sex["Выжило_процент"] * 100
by_class_sex = by_class_sex.round(2)
print("37. Группировка по Pclass и Sex:")
print(by_class_sex)

by_port = df.groupby("Embarked").agg(
    Количество=("PassengerId", "count"),
    Выжило_процент=("Survived", "mean"),
)
by_port["Выжило_процент"] = by_port["Выжило_процент"] * 100
by_port = by_port.round(2)
print("\n38. Группировка по Embarked:")
print(by_port)

surv_by_class = df.groupby("Pclass")["Survived"].mean() * 100
print("\n39. Выжило по классам (%):")
print(surv_by_class.round(2))
print(f"    Максимум: класс {surv_by_class.idxmax()} ({surv_by_class.max():.2f}%)")

section("Часть VII. Сохранение")

df.to_csv("titanic_processed.csv", index=False)
by_class_sex.to_csv("titanic_statistics.csv")
print("40-41. Сохранено: titanic_processed.csv, titanic_statistics.csv")

check = pd.read_csv("titanic_processed.csv")
pd.testing.assert_frame_equal(check, df.reset_index(drop=True), check_dtype=False)
print(f"42. Проверка пройдена: загружено {check.shape[0]} строк, {check.shape[1]} столбцов, данные совпадают.")
check_stats = pd.read_csv("titanic_statistics.csv", index_col=["Pclass", "Sex"])
pd.testing.assert_frame_equal(check_stats, by_class_sex, check_dtype=False)
print("    Статистика тоже сохранилась корректно.")
