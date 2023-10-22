# -*- coding: utf-8 -*-
"""
clean app
"""
import toga
from toga.style import Pack
from toga.style.pack import *
import psycopg2 as db
import datetime
from psycopg2 import sql


class Clean(toga.App):
    def __init__(
            self,
            formal_name=None,
            app_id=None,
            app_name=None,
            id=None,
            icon=None,
            author=None,
            version=None,
            home_page=None,
            description=None,
            startup=None,
            windows=None,
            on_exit=None,
            factory=None,  # DEPRECATED !
    ):
        super().__init__(formal_name, app_id, app_name, id, icon, author, version, home_page, description, startup,
                         windows, on_exit, factory)
        self.journal_insert_datetime = None
        self.inhabitant_id_result = None
        self.address_result = None
        self.feedback_datetime_result = None
        self.inhabitant_phone_input = None
        self.appeal_text_input = None
        self.address_selection = None
        self.inhabitant_surname_input = None
        self.inhabitant_name_input = None
        self.feedback_window = None
        self.comments_input = None
        self.journal_window = None
        self.work_type_selection = None
        self.date = None
        self.employee_id = None
        self.address_input = None
        self.employee_journal_input = None
        self.employee_full_name = None
        self.password_input = None
        self.login_input = None
        self.cur = None
        self.conn = None

    def startup(self):
        try:
            # пытаемся подключиться к базе данных
            self.conn = db.connect(dbname='cleandb', user='postgres', password='123', host='localhost')
            print('Established connection to database')
            # Создание объекта курсора для выполнения SQL-запросов
            self.cur = self.conn.cursor()
        except Exception as e:
            # в случае сбоя подключения будет выведено сообщение в консоли
            print(e)
            print('Can`t establish connection to database')

        # Названия полей
        login_label = toga.Label(
            "Введите логин: ",
            style=Pack(padding=(0, 8, 0, 8), font_family="montserrat", font_size=12)
        )
        password_label = toga.Label(
            "Введите пароль: ",
            style=Pack(padding=(15, 0, 0, 8), font_family="montserrat", font_size=12)
        )

        # Кнопки главного меню
        login_button = toga.Button(
            "Войти",
            on_press=self.user_login,
            style=Pack(padding=(20, 18, 5, 8), font_family="montserrat", font_size=14)
        )
        feedback_button = toga.Button(
            "Оставить обращение (для жителей)",
            on_press=self.open_feedback_window,
            style=Pack(padding=(10, 18, 5, 8), font_family="montserrat", font_size=14)
        )

        # Создание полей ввода
        self.login_input = toga.TextInput(
            style=Pack(width=500, padding=(0, 35, 0, -1), font_family="montserrat", font_size=10))
        self.password_input = toga.PasswordInput(
            style=Pack(width=500, padding=(15, 35, 0, -3), font_family="montserrat", font_size=10))

        # Создание контейнеров
        auth_main_box = toga.Box(style=Pack(direction=COLUMN))
        login_box = toga.Box(style=Pack(direction=ROW))
        password_box = toga.Box(style=Pack(direction=ROW))

        # Добавление элементов в контейнеры
        login_box.add(login_label, self.login_input)
        password_box.add(password_label, self.password_input)

        # Добавление контейнеров и кнопок в главный контейнер
        auth_main_box.add(login_box)
        auth_main_box.add(password_box)
        auth_main_box.add(login_button, feedback_button)

        # Создание главного окна, определение его содержимого и его показ
        self.main_window = toga.MainWindow(title="Авторизация", resizeable=False)
        self.main_window.content = auth_main_box
        self.main_window.show()

    def user_login(self, widget):
        # Получение введенных логина и пароля из базы данных
        self.cur.execute('SELECT пароль FROM Сотрудники WHERE логин = %s;', (self.login_input.value,))
        check_pass = self.cur.fetchall()
        self.cur.execute(f'SELECT логин FROM Сотрудники WHERE пароль =%s;', (self.password_input.value,))
        check_login = self.cur.fetchall()

        # Проверка введенного логина и пароля на существование и соответствие в базе данных
        if check_pass and check_pass[0][0] == self.password_input.value and check_login and check_login[0][0] == self.login_input.value:
            select_employee_id_on_login_query = """SELECT сотрудник_id
            FROM Сотрудники
            WHERE логин = %s AND пароль = %s;"""
            self.cur.execute(select_employee_id_on_login_query, (self.login_input.value, self.password_input.value,))
            employee_id = self.cur.fetchone()
            self.employee_id = employee_id[0]
            self.open_journal_window(widget)
            print("====================================\n"
                  "Successfully login!\n"
                  f"Employee_id = {self.employee_id}\n"
                  f"Login = {self.login_input.value}\n"
                  f"Password = {self.password_input.value}\n"
                  "====================================")
        else:
            # Вызов диалогового окна с ошибкой неправильного логина или пароля
            self.main_window.error_dialog("Неверный логин или пароль",
                                          "Вы ввели неверный логин или пароль. Попробуйте еще раз.")
            print("====================================\n"
                  "Error while logging in!\n"
                  f"Login = {self.login_input.value}\n"
                  f"Password = {self.password_input.value}\n"
                  "====================================")
            return

    def create_feedback_window(self):
        # Названия полей
        inhabitant_surname_label = toga.Label(
            "Ваша фамилия: ",
            style=Pack(padding=(0, 20, 5, 20), font_family="montserrat", font_size=14)
        )
        inhabitant_name_label = toga.Label(
            "Ваше имя: ",
            style=Pack(padding=(0, 20, 5, 20), font_family="montserrat", font_size=14)
        )
        inhabitant_phone_label = toga.Label(
            "Введите ваш номер телефона: ",
            style=Pack(padding=(0, 20, 5, 20), font_family="montserrat", font_size=14)
        )
        inhabitant_address_label = toga.Label(
            "Введите адрес: ",
            style=Pack(padding=(0, 20, 5, 20), font_family="montserrat", font_size=14)
        )
        inhabitant_appeal_label = toga.Label(
            "Введите текст обращения (жалобы): ",
            style=Pack(padding=(0, 20, 5, 20), font_family="montserrat", font_size=14)
        )
        # Создание полей ввода
        self.inhabitant_surname_input = toga.TextInput(
            style=Pack(padding=(0, 20, 5, 20), font_family="montserrat", font_size=12))
        self.inhabitant_name_input = toga.TextInput(
            style=Pack(padding=(0, 20, 5, 20), font_family="montserrat", font_size=12))
        self.inhabitant_phone_input = toga.TextInput(
            style=Pack(padding=(0, 20, 5, 20), font_family="montserrat", font_size=12))
        self.appeal_text_input = toga.TextInput(
            style=Pack(flex=2, padding=(0, 20, 5, 20), font_family="montserrat", font_size=12))

        # Создание списка всех адресов
        select_all_addresses_query = """SELECT адрес FROM Дворы"""
        self.cur.execute(select_all_addresses_query)
        all_addresses_tuple = self.cur.fetchall()
        all_addresses = []
        for address in all_addresses_tuple:
            all_addresses.append(address[0])
        # Выпадающий список с адресами
        self.address_selection = toga.Selection(items=all_addresses, style=Pack(padding=(0, 20, 5, 20)))
        # Создание кнопок окна с обращениями
        send_feedback_button = toga.Button(
            "Отправить обращение",
            on_press=self.send_feedback,
            style=Pack(flex=1, padding=(0, 20, 5, 20), font_family="montserrat", font_size=16)
        )
        cancel_button = toga.Button(
            "Отмена",
            on_press=self.close_feedback_window,
            style=Pack(flex=1, padding=(0, 30, 5, 20), font_family="montserrat", font_size=16)
        )
        # Создание контейнеров
        main_box = toga.Box(style=Pack(direction=COLUMN))
        name_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        btn_box = toga.Box(style=Pack(direction=ROW, padding=5))
        # Добавление элементов в контейнеры
        name_box.add(
            inhabitant_surname_label, self.inhabitant_surname_input,
            inhabitant_name_label, self.inhabitant_name_input,
            inhabitant_phone_label, self.inhabitant_phone_input,
            inhabitant_address_label, self.address_selection,
            inhabitant_appeal_label, self.appeal_text_input)
        btn_box.add(send_feedback_button, cancel_button)

        main_box.add(name_box)
        main_box.add(btn_box)

        # Создание окна с обратной связью
        self.feedback_window = toga.Window(title="Обратная связь", resizeable=False,
                                           on_close=self.close_feedback_window)
        self.feedback_window.content = main_box
        self.windows.add(self.feedback_window)

    def send_feedback(self, widget):
        # SQL-запрос для вставки данных пользователя в таблицу Жители
        insert_inhabitant_full_name_query = sql.SQL(
            "INSERT INTO Жители (фамилия, имя, контактная_информация) VALUES ("
            "{}, {}, {}) ON CONFLICT (контактная_информация) DO NOTHING;").format(
            sql.Literal(self.inhabitant_surname_input.value),
            sql.Literal(self.inhabitant_name_input.value),
            sql.Literal(self.inhabitant_phone_input.value)
        )
        self.cur.execute(insert_inhabitant_full_name_query)

        # Получение выбранного жителем из списка адреса
        address_selected = self.address_selection.value
        select_address_id_query = """SELECT двор_id
        FROM Дворы
        WHERE адрес = %s;"""
        self.cur.execute(select_address_id_query, (address_selected,))
        address = self.cur.fetchone()
        self.address_result = address[0]

        # Получение времени отправки обращения
        self.feedback_datetime_result = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        # SQL-запрос для получения житель_id по данным жителя
        select_inhabitant_id_by_full_name_query = """SELECT житель_id 
        FROM Жители
        WHERE фамилия = %s AND имя = %s AND контактная_информация = %s;"""
        self.cur.execute(select_inhabitant_id_by_full_name_query, (
        self.inhabitant_surname_input.value, self.inhabitant_name_input.value, self.inhabitant_phone_input.value,))
        inhabitant_id = self.cur.fetchone()
        self.inhabitant_id_result = inhabitant_id[0]

        # SQL-запрос для вставки данных обращения в таблицу Обращения
        insert_feedback_query = sql.SQL(
            "INSERT INTO Жалобы_и_предложения (двор_id, текст, дата_и_время_подачи, житель_id) VALUES ("
            "{}, {}, {}, {});").format(
            sql.Literal(self.address_result),
            sql.Literal(self.appeal_text_input.value),
            sql.Literal(self.feedback_datetime_result),
            sql.Literal(self.inhabitant_id_result)
        )
        # Выполнение SQL-запросов
        self.cur.execute(insert_feedback_query)
        # Подтверждение изменений
        self.conn.commit()

    def open_journal_window(self, widget):
        self.main_window.hide()
        self.create_journal_window()
        self.journal_window.show()

    def close_journal_window(self, widget):
        self.login_input.clear()
        self.password_input.clear()
        self.main_window.show()
        self.journal_window.hide()

    def open_feedback_window(self, widget):
        self.main_window.hide()
        self.create_feedback_window()
        self.feedback_window.show()

    def close_feedback_window(self, widget):
        self.feedback_window.hide()
        self.main_window.show()

    def create_journal_window(self):
        # Названия полей
        employee_label = toga.Label(
            "Сотрудник: ",
            style=Pack(padding=(0, 20, 5, 20), font_family="montserrat", font_size=14)
        )
        address_label = toga.Label(
            "Адрес уборки: ",
            style=Pack(padding=(0, 20, 5, 20), font_family="montserrat", font_size=14)
        )
        date_label = toga.Label(
            "Дата и время уборки: ",
            style=Pack(padding=(0, 20, 5, 20), font_family="montserrat", font_size=14)
        )
        type_label = toga.Label(
            "Введите тип работ: ",
            style=Pack(padding=(0, 20, 5, 20), font_family="montserrat", font_size=14)
        )
        comment_label = toga.Label(
            "Введите комментарий: ",
            style=Pack(padding=(0, 20, 5, 20), font_family="montserrat", font_size=14)
        )

        # Получение полного имени сотрудника по его id
        select_employee_full_name_query = """SELECT фамилия, имя, отчество
        FROM Сотрудники
        WHERE сотрудник_id = %s;"""
        self.cur.execute(select_employee_full_name_query, (self.employee_id,))
        self.employee_full_name = self.cur.fetchone()
        self.employee_journal_input = toga.TextInput(
            value=self.employee_full_name[0] + " " + self.employee_full_name[1] + " " + self.employee_full_name[2],
            readonly=True, style=Pack(padding=(0, 20, 5, 20), font_family="montserrat", font_size=12))

        # Получение адреса двора в котором работает сотрудник по его id
        select_employee_work_address_query = """SELECT адрес
        FROM Сотрудники
        INNER JOIN Дворы ON Сотрудники.двор_id = Дворы.двор_id
        WHERE сотрудник_id = %s;"""
        self.cur.execute(select_employee_work_address_query, (self.employee_id,))
        employee_work_address = self.cur.fetchone()
        employee_work_address = employee_work_address[0]
        self.address_input = toga.TextInput(value=employee_work_address, readonly=True,
                                            style=Pack(padding=(0, 20, 5, 20), font_family="montserrat", font_size=12))

        # Получение времени отправки отчета о работе
        self.journal_insert_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        self.date = toga.TextInput(value=self.journal_insert_datetime, readonly=True,
                                   style=Pack(padding=(0, 20, 5, 20), font_family="montserrat", font_size=12))

        # Получение типов работ которые есть у должности сотрудника по его id и создание списка с типами работ
        select_employees_work_types_query = """SELECT название
        FROM Типы_работ
        inner join Должности_и_типы_работ on Типы_работ.тип_работы_id = Должности_и_типы_работ.тип_работы
        inner join Сотрудники on Сотрудники.должность = Должности_и_типы_работ.должность
        where Сотрудники.сотрудник_id = %s;"""
        self.cur.execute(select_employees_work_types_query, (self.employee_id,))
        work_types_tuple = self.cur.fetchall()
        work_types = []
        for work_type in work_types_tuple:
            work_types.append(work_type[0])

        # Выпадающий список с типами работ
        self.work_type_selection = toga.Selection(items=work_types, style=Pack(padding=(0, 30, 5, 20)))
        self.comments_input = toga.TextInput(
            style=Pack(flex=2, padding=(0, 20, 5, 20), font_family="montserrat", font_size=12))

        # Создание кнопок окна с журналом работ
        add_journal_entry_button = toga.Button(
            "Добавить уборку в журнал",
            on_press=self.insert_into_journal,
            style=Pack(flex=1, padding=(0, 20, 5, 20), font_family="montserrat", font_size=16)
        )
        logout_button = toga.Button(
            "Выйти",
            on_press=self.close_journal_window,
            style=Pack(padding=(0, 20, 5, 20), font_family="montserrat", font_size=16)
        )

        # Создание контейнеров
        main_box = toga.Box(style=Pack(direction=COLUMN))
        name_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        btn_box = toga.Box(style=Pack(direction=ROW, padding=5))

        # Добавление элементов в контейнеры
        name_box.add(employee_label, self.employee_journal_input,
                     address_label, self.address_input,
                     date_label, self.date,
                     type_label, self.work_type_selection,
                     comment_label, self.comments_input)
        btn_box.add(add_journal_entry_button, logout_button)

        # Добавление контейнеров и кнопок в главный контейнер
        main_box.add(name_box)
        main_box.add(btn_box)
        # Создание окна журнала работ, определение его содержимого и его добавление в список окон программы
        self.journal_window = toga.Window(title="Журнал уборки", resizeable=False, on_close=self.close_journal_window)
        self.journal_window.content = main_box
        self.windows.add(self.journal_window)

    def insert_into_journal(self, widget):
        # Получение id сотрудника по его данным
        select_employee_id_by_full_name_query = """SELECT сотрудник_id 
        FROM Сотрудники
        WHERE фамилия = %s AND имя = %s AND отчество = %s;"""
        self.cur.execute(select_employee_id_by_full_name_query,
                         (self.employee_full_name[0], self.employee_full_name[1], self.employee_full_name[2],))
        employee_id = self.cur.fetchone()
        employee_id_result = employee_id[0]

        # Получение id двора в котором работает сотрудник
        select_courtyard_id_by_employee_id_query = """SELECT Дворы.двор_id 
        FROM Дворы
        INNER JOIN Сотрудники ON Сотрудники.двор_id = Дворы.двор_id 
        WHERE сотрудник_id = %s;"""
        self.cur.execute(select_courtyard_id_by_employee_id_query, (self.employee_id,))
        employees_addresses = self.cur.fetchone()
        address_id_result = employees_addresses[0]

        # Получение id типа выполненной работы по его названию
        work_type_selected = self.work_type_selection.value
        select_query = """SELECT тип_работы_id 
        FROM Типы_работ 
        WHERE название = %s;"""
        self.cur.execute(select_query, (work_type_selected,))
        work_type = self.cur.fetchone()
        work_type_id_result = work_type[0]

        # Получение id типа выполненной работы по его названию
        comments_result = self.comments_input.value
        # Получение времени отправки отчета о работе
        journal_insert_time_result = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        print(f"=============================================\n"
              f"Employee №{employee_id_result} did work at address = {address_id_result}\n"
              f"Date and time = {journal_insert_time_result}\n"
              f"Work type = {work_type_id_result}\n"
              f"Comments = {comments_result}\n"
              "=============================================\n")

        # SQL-запрос для вставки данных в таблицу Журнал работ
        insert_result_query = sql.SQL(
            "INSERT INTO Журнал_уборки (дата_и_время_уборки, сотрудник_id, двор_id, тип_работ, комментарий) VALUES ("
            "{}, {}, {}, {}, {});").format(
            sql.Literal(journal_insert_time_result),
            sql.Literal(employee_id_result),
            sql.Literal(address_id_result),
            sql.Literal(work_type_id_result),
            sql.Literal(comments_result)
        )
        # Выполнение SQL-запроса
        self.cur.execute(insert_result_query)
        # Подтверждение изменений
        self.conn.commit()


def main():
    return Clean()
