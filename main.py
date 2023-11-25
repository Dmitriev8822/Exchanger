from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QComboBox
from PyQt5.QtGui import QFont

import datetime
from forex_python.converter import CurrencyRates
from db import DataBase

unicode_dict = {
    "USD": "\u0024",  # Доллар США
    "EUR": "\u20AC",  # Евро
    "JPY": "\u00A5",  # Японская иена
    "GBP": "\u00A3",  # Британский фунт
    "CNY": "\u00A5",  # Китайский юань/ренминби
    "RUB": "\u20BD",  # Российский рубль
    "CAD": "\u0024",  # Канадский доллар
    "AUD": "\u0024",  # Австралийский доллар
    "CHF": "\u20A3",  # Швейцарский франк
    "INR": "\u20B9"   # Индийская рупия
}

currency_dict = {
    'Доллар США (USD)': 'USD',
    'Евро (EUR)': 'EUR',
    'Японская иена (JPY)': 'JPY',
    'Британский фунт (GBP)': 'GBP',
    'Китайский юань/ренминби (CNY)': 'CNY',
    'Российский рубль (RUB)': 'RUB',
    'Канадский доллар (CAD)': 'CAD',
    'Австралийский доллар (AUD)': 'AUD',
    'Швейцарский франк (CHF)': 'CHF',
    'Индийская рупия (INR)': 'INR'
}


class CurrencyConverterWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.init_ui()
        self.active_user_id = user_id
        self.convert_button.clicked.connect(self.convert)

    def init_ui(self):
        self.setWindowTitle('Конвертер валют')
        self.resize(600, 300)

        self.converter = CurrencyRates()
        self.data_limit = datetime.datetime(2015, 1, 1)

        self.amount_label = QLabel('Сумма:')
        self.from_currency_label = QLabel('Из валюты:')
        self.to_currency_label = QLabel('В валюту:')
        self.result_label = QLabel('')

        self.amount_label.setStyleSheet("font-size: 16pt;")
        self.from_currency_label.setStyleSheet("font-size: 16pt;")
        self.to_currency_label.setStyleSheet("font-size: 16pt;")
        self.result_label.setStyleSheet("font-size: 16pt;")

        self.amount_edit = QLineEdit()
        self.from_currency_combo = QComboBox()
        self.to_currency_combo = QComboBox()
        self.result_label = QLabel('')

        self.amount_edit.setStyleSheet("font-size: 16pt;")
        self.from_currency_combo.setStyleSheet("font-size: 16pt;")
        self.to_currency_combo.setStyleSheet("font-size: 16pt;")
        self.result_label.setStyleSheet("font-size: 16pt;")

        from_currency_options = ['Доллар США (USD)',
                                 'Евро (EUR)',
                                 'Японская иена (JPY)',
                                 'Британский фунт (GBP)',
                                 'Китайский юань/ренминби (CNY)',
                                 'Российский рубль (RUB)',
                                 'Канадский доллар (CAD)',
                                 'Австралийский доллар (AUD)',
                                 'Швейцарский франк (CHF)',
                                 'Индийская рупия (INR)']
        to_currency_options = ['Доллар США (USD)',
                                 'Евро (EUR)',
                                 'Японская иена (JPY)',
                                 'Британский фунт (GBP)',
                                 'Китайский юань/ренминби (CNY)',
                                 'Российский рубль (RUB)',
                                 'Канадский доллар (CAD)',
                                 'Австралийский доллар (AUD)',
                                 'Швейцарский франк (CHF)',
                                 'Индийская рупия (INR)']

        self.from_currency_combo.addItems(from_currency_options)
        self.to_currency_combo.addItems(to_currency_options)

        self.convert_button = QPushButton('Конвертировать')
        self.convert_button.setStyleSheet("font-size: 16pt;")

        layout = QVBoxLayout()
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_edit)
        layout.addWidget(self.from_currency_label)
        layout.addWidget(self.from_currency_combo)
        layout.addWidget(self.to_currency_label)
        layout.addWidget(self.to_currency_combo)
        layout.addWidget(self.result_label)
        layout.addWidget(self.convert_button)

        self.setLayout(layout)

    def convert(self):
        amount = self.amount_edit.text()
        from_currency = currency_dict[self.from_currency_combo.currentText()]
        to_currency = currency_dict[self.to_currency_combo.currentText()]
        rate = 0

        if amount and any(char.isdigit() for char in amount) and from_currency and to_currency:
            amount = float(''.join([el if el in '0123456789' else '' for el in list(amount)]))
            date = datetime.datetime.now()
            while date > self.data_limit:
                try:
                    rate = round(self.converter.get_rate(from_currency, to_currency, date), 5)
                except Exception:
                    date = date - datetime.timedelta(days=365)
                    continue
                break

            profit = 1
            res = str(round(amount * (rate + rate * (profit / 100))))
            formatted_number = "{0:,}".format(int(res)).replace(',', '.')
            self.result_label.setText(
                f'{formatted_number}{unicode_dict[to_currency]}; Курс актуален на {str(date).split()[0]}.')

            db.new_log(self.active_user_id, from_currency, to_currency, amount, str(date).split()[0], str(date).split()[1].split('.')[0])



class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Регистрация")
        self.resize(400, 300)

        self.layout = QVBoxLayout()

        self.error_flag = True

        self.first_name_label = QLabel("Имя:")
        self.first_name_input = QLineEdit()

        self.last_name_label = QLabel("Фамилия:")
        self.last_name_input = QLineEdit()

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton("Зарегистрироваться")

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.register_button)
        self.button_layout.addStretch()

        self.layout.addWidget(self.first_name_label)
        self.layout.addWidget(self.first_name_input)
        self.layout.addWidget(self.last_name_label)
        self.layout.addWidget(self.last_name_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addLayout(self.button_layout)

        self.first_name_input.setFixedHeight(50)
        self.last_name_input.setFixedHeight(50)
        self.password_input.setFixedHeight(50)

        font = QFont()
        font.setPointSize(16)
        self.first_name_input.setFont(font)
        self.last_name_input.setFont(font)
        self.password_input.setFont(font)
        self.register_button.setFont(font)

        label_font = QFont()
        label_font.setPointSize(16)

        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                widget.setFont(label_font)

        self.register_button.setMinimumSize(400, 80)

        # Применяем стили
        self.setStyleSheet(
            "QWidget {background-color: #f0f0f0;}"
            "QLabel {color: #000000;}"
            "QLineEdit {background-color: #ffffff; color: #000000; border: 1px solid #000000; padding: 5px;}"
            "QPushButton {background-color: #ff6347; color: #ffffff; padding: 10px;}"
            "QPushButton:hover {background-color: #ff7f50;}"
        )

        self.setLayout(self.layout)

        self.register_button.clicked.connect(self.create_user)

    def print_error(self, text):
        if self.error_flag:
            self.error = QLabel()
            self.error_font = QFont()
            self.error_font.setPointSize(10)
            self.error.setFont(self.error_font)
            self.layout.insertWidget(0, self.error)
            self.error_flag = False

        self.error.setText(text)

    def create_user(self):
        name = self.first_name_input.text()
        surname = self.last_name_input.text()
        password = self.password_input.text()

        if name and surname and password:
            res = db.new_user(name, surname, password)
            if res > 0:
                message_box = QMessageBox()
                message_box.setWindowTitle("Информация")
                message_box.setText(f"Ваш уникальный идентификатор: {res}.")
                message_box.addButton(QMessageBox.Ok)
                message_box.exec()

                self.atrn = AuthorizationWindow()
                self.close()
                self.atrn.show()
            else:
                self.print_error('Возникли технические шоколадки')
        else:
            self.print_error('Все поля должны быть заполнены')


class AuthorizationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Авторизация")
        self.resize(400, 300)

        self.layout = QVBoxLayout()

        self.error_flag = True

        self.user_id_label = QLabel("Ваш ID:")
        self.user_id_input = QLineEdit()

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.authorization_button = QPushButton("Войти")
        self.register_button = QPushButton("Регистрация")

        self.button_authorization_layout = QHBoxLayout()
        self.button_authorization_layout.addStretch()
        self.button_authorization_layout.addWidget(self.authorization_button)
        self.button_authorization_layout.addStretch()

        self.button_register_layout = QHBoxLayout()
        self.button_register_layout.addStretch()
        self.button_register_layout.addWidget(self.register_button)
        self.button_register_layout.addStretch()

        self.layout.addWidget(self.user_id_label)
        self.layout.addWidget(self.user_id_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addLayout(self.button_authorization_layout)
        self.layout.addLayout(self.button_register_layout)

        self.user_id_input.setFixedHeight(50)
        self.password_input.setFixedHeight(50)

        font = QFont()
        font.setPointSize(16)
        self.user_id_input.setFont(font)
        self.password_input.setFont(font)
        self.register_button.setFont(font)
        self.authorization_button.setFont(font)

        label_font = QFont()
        label_font.setPointSize(16)

        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                widget.setFont(label_font)

        self.register_button.setMinimumSize(300, 60)
        self.authorization_button.setMinimumSize(300, 60)

        # Применяем стили
        self.setStyleSheet(
            "QWidget {background-color: #f0f0f0;}"
            "QLabel {color: #000000;}"
            "QLineEdit {background-color: #ffffff; color: #000000; border: 1px solid #000000; padding: 5px;}"
            "QPushButton {background-color: #ff6347; color: #ffffff; padding: 10px;}"
            "QPushButton:hover {background-color: #ff7f50;}"
        )

        self.setLayout(self.layout)

        self.authorization_button.clicked.connect(self.authorization)
        self.register_button.clicked.connect(self.register)

    def print_error(self, text):
        if self.error_flag:
            self.error = QLabel()
            self.error_font = QFont()
            self.error_font.setPointSize(10)
            self.error.setFont(self.error_font)
            self.layout.insertWidget(0, self.error)
            self.error_flag = False

        self.error.setText(text)

    def authorization(self):
        user_id = self.user_id_input.text()
        password = self.password_input.text()
        if user_id and password:
            res = db.check_user_password(user_id, password)

            if res == 0:
                self.win_cur = CurrencyConverterWindow(user_id)
                self.close()
                self.win_cur.show()
            elif res == 1:
                self.print_error('Некорректный пароль')
            elif res == -1:
                self.print_error('Пользователь не найден')
            elif res == -2:
                self.print_error('Возникла непредвиденная ошибка')
        else:
            self.print_error('Все поля должны быть заполнены')

    def register(self):
        self.regw = RegistrationWindow()
        self.close()
        self.regw.show()


if __name__ == '__main__':
    db = DataBase()
    app = QApplication([])
    win = AuthorizationWindow()
    win.show()
    app.exec_()
    db.close_connection()
