import math
import sys

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
        QComboBox, QSpinBox, QListWidget, QMessageBox,
        QVBoxLayout, QHBoxLayout, QFormLayout,
    )
    from PyQt6.QtCore import Qt
except ImportError:
    raise SystemExit(
        "Для запуска нужен PyQt6. Установите его вручную в виртуальном окружении: "
        "python -m pip install -r requirements.txt"
    )

UNITS = {
    "Длина": {"мм": 0.001, "см": 0.01, "м": 1, "км": 1000, "дюйм": 0.0254, "фут": 0.3048},
    "Масса": {"г": 0.001, "кг": 1, "т": 1000, "фунт": 0.453592},
    "Температура": {"°C": None, "°F": None, "K": None},
}


def convert(value, category, src, dst):
    if category != "Температура":
        factors = UNITS[category]
        return value * factors[src] / factors[dst]

    c = value
    if src == "°F":
        c = (value - 32) * 5 / 9
    elif src == "K":
        c = value - 273.15
    elif src != "°C":
        raise KeyError(src)

    if dst == "°F":
        return c * 9 / 5 + 32
    if dst == "K":
        return c + 273.15
    if dst == "°C":
        return c
    raise KeyError(dst)


class Converter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конвертер величин")
        self.resize(420, 500)

        title = QLabel("Конвертер величин")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Например, 12.5")

        self.category = QComboBox()
        self.category.addItems(list(UNITS))
        self.src = QComboBox()
        self.dst = QComboBox()
        self.precision = QSpinBox()
        self.precision.setRange(0, 6)
        self.precision.setValue(2)

        self.convert_btn = QPushButton("Перевести")
        self.swap_btn = QPushButton("⇄ Поменять местами")
        self.clear_btn = QPushButton("Очистить историю")

        self.result_label = QLabel("Результат: —")
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.history = QListWidget()

        form = QFormLayout()
        form.addRow("Величина:", self.category)
        form.addRow("Значение:", self.value_input)
        form.addRow("Из:", self.src)
        form.addRow("В:", self.dst)
        form.addRow("Знаков после запятой:", self.precision)

        buttons = QHBoxLayout()
        buttons.addWidget(self.convert_btn)
        buttons.addWidget(self.swap_btn)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addLayout(buttons)
        layout.addWidget(self.result_label)
        layout.addWidget(QLabel("История:"))
        layout.addWidget(self.history)
        layout.addWidget(self.clear_btn)
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        self.category.currentTextChanged.connect(self.update_units)
        self.convert_btn.clicked.connect(self.do_convert)
        self.value_input.returnPressed.connect(self.do_convert)
        self.swap_btn.clicked.connect(self.swap)
        self.clear_btn.clicked.connect(self.clear_history)
        self.update_units(self.category.currentText())

    def update_units(self, category):
        units = list(UNITS[category])
        for box in (self.src, self.dst):
            box.clear()
            box.addItems(units)
        self.dst.setCurrentIndex(1)

    def swap(self):
        old_src = self.src.currentIndex()
        self.src.setCurrentIndex(self.dst.currentIndex())
        self.dst.setCurrentIndex(old_src)

    def do_convert(self):
        category = self.category.currentText()
        src = self.src.currentText()
        dst = self.dst.currentText()
        text = self.value_input.text().strip().replace(",", ".")

        try:
            value = float(text)
        except ValueError:
            QMessageBox.warning(self, "Ошибка ввода", "Введите число.")
            return
        if not math.isfinite(value):
            QMessageBox.warning(self, "Ошибка ввода", "Введите конечное число.")
            return
        if category == "Температура" and convert(value, category, src, "K") < 0:
            QMessageBox.warning(self, "Ошибка ввода", "Температура ниже абсолютного нуля.")
            return
        if category != "Температура" and value < 0:
            QMessageBox.warning(self, "Ошибка ввода", "Значение не может быть отрицательным.")
            return

        result = convert(value, category, src, dst)
        if not math.isfinite(result):
            QMessageBox.warning(self, "Ошибка ввода", "Результат слишком велик. Введите меньшее число.")
            return
        digits = self.precision.value()
        answer = f"{result:.{digits}f} {dst}"
        self.result_label.setText(f"Результат: {answer}")
        self.history.insertItem(0, f"{value:g} {src} = {answer}")

    def clear_history(self):
        if self.history.count() == 0:
            QMessageBox.information(self, "История", "История и так пуста.")
            return
        answer = QMessageBox.question(
            self, "Подтверждение", "Удалить всю историю?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.history.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Converter()
    window.show()
    sys.exit(app.exec())
