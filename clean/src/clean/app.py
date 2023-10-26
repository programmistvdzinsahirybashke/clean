# -*- coding: utf-8 -*-
"""
clean app
"""
import datetime
import psycopg2 as db
import toga
from psycopg2 import sql
from toga.style.pack import *


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
        self.employee_and_address_id_result = None
        self.employee_address_id = None
        self.employee_street_number_selected = None
        self.employee_street_name_selected = None
        self.employee_city_selected = None
        self.employee_street_id_result = None
        self.employee_street_number_selection = None
        self.employee_all_street_numbers = None
        self.employee_street_name_selection = None
        self.new_employee_all_streets = None
        self.employee_all_streets = None
        self.employee_city_id_result = None
        self.employee_city_selection = None
        self.employee_all_cities = None
        self.employee_selections_box = None
        self.street_number_selected = None
        self.street_name_selected = None
        self.city_selected = None
        self.new_all_streets = None
        self.selections_box = None
        self.all_street_numbers = None
        self.street_id_result = None
        self.all_streets = None
        self.city_id_result = None
        self.city_selection = None
        self.all_cities = None
        self.street_number_selection = None
        self.street_name_selection = None
        self.work_types = None
        self.address_selected = None
        self.employee_id_result = None
        self.address_id_result = None
        self.work_type_id_result = None
        self.comments_result = None
        self.journal_insert_time_result = None
        self.work_type_selected = None
        self.employee_work_address = None
        self.all_addresses = None
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

    # Функция, запускающая приложение и открывающая главное окно программы
    def startup(self):
        try:
            # Пытаемся подключиться к базе данных
            self.conn = db.connect(dbname='postgres', user='postgres', password='123', host='localhost')
            print('Established connection to database')
            # Создание объекта курсора для выполнения SQL-запросов
            self.cur = self.conn.cursor()
        except Exception as e:
            # В случае сбоя подключения будет выведено сообщение и текст ошибки в консоли
            print(e)
            print('Can`t establish connection to database')

        # Создание названий полей
        login_label = toga.Label(
            "Введите логин: ",
            style=Pack(padding=(0, 8, 0, 8), font_family="montserrat", font_size=12)
        )
        password_label = toga.Label(
            "Введите пароль: ",
            style=Pack(padding=(15, 0, 0, 8), font_family="montserrat", font_size=12)
        )

        # Создание кнопок главного меню
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

    # Функция, проверяющая логин и пароль после нажатия кнопки
    def user_login(self, widget):
        # Получение введенных логина и пароля из базы данных
        self.cur.execute('SELECT пароль FROM Сотрудники WHERE логин = %s;', (self.login_input.value,))
        check_pass = self.cur.fetchall()
        self.cur.execute(f'SELECT логин FROM Сотрудники WHERE пароль =%s;', (self.password_input.value,))
        check_login = self.cur.fetchall()

        # Проверка введенного логина и пароля на существование и соответствие в базе данных
        if check_pass and check_pass[0][0] == self.password_input.value and check_login and check_login[0][
            0] == self.login_input.value:
            select_employee_id_on_login_query = """SELECT сотрудник_id
            FROM Сотрудники
            WHERE логин = %s AND пароль = %s;"""
            self.cur.execute(select_employee_id_on_login_query, (self.login_input.value, self.password_input.value,))
            employee_id = self.cur.fetchone()
            self.employee_id = employee_id[0]
            self.open_journal_window(widget)
        else:
            # Вызов диалогового окна с ошибкой неправильного логина или пароля
            self.main_window.error_dialog("Неверный логин или пароль",
                                          "Вы ввели неверный логин или пароль. Попробуйте еще раз.")
            return

    # Функция, создающая окно отправки обратной связи
    def create_feedback_window(self):
        # Создание названий полей
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
            "Выберите адрес: ",
            style=Pack(padding=(0, 0, 5, 20), font_family="montserrat", font_size=14)
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
        self.appeal_text_input = toga.MultilineTextInput(
            style=Pack(flex=2, height=100, padding=(0, 20, 5, 20), font_family="montserrat", font_size=12))

        # Создание кнопок окна с обращениями
        send_feedback_button = toga.Button(
            "Отправить обращение",
            on_press=self.send_feedback,
            style=Pack(flex=1, padding=(0, 20, 5, 20), font_family="montserrat", font_size=16)
        )
        cancel_button = toga.Button(
            "Выход",
            on_press=self.close_feedback_window,
            style=Pack(flex=1, padding=(0, 18, 5, 20), font_family="montserrat", font_size=16)
        )

        # Обработка выбора адреса пользователем
        self.inhabitant_select_address()
        # Создание контейнеров
        main_box = toga.Box(style=Pack(direction=COLUMN))
        name_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        self.selections_box = toga.Box(style=Pack(direction=ROW))
        btn_box = toga.Box(style=Pack(direction=ROW, padding=5))
        # Добавление элементов в контейнеры
        name_box.add(
            inhabitant_surname_label, self.inhabitant_surname_input,
            inhabitant_name_label, self.inhabitant_name_input,
            inhabitant_phone_label, self.inhabitant_phone_input,
            inhabitant_appeal_label, self.appeal_text_input)
        self.selections_box.add(inhabitant_address_label, self.city_selection, self.street_name_selection,
                                self.street_number_selection)
        btn_box.add(send_feedback_button, cancel_button)
        # Добавление контейнеров в главный контейнер
        main_box.add(name_box)
        main_box.add(self.selections_box)
        main_box.add(btn_box)

        # Создание окна отправки обратной связи, определение его содержимого и его добавление в список окон программы
        self.feedback_window = toga.Window(title="Обратная связь", resizeable=True,
                                           on_close=self.close_feedback_window)
        self.feedback_window.content = main_box
        self.windows.add(self.feedback_window)

    # Функция, создающая список городов и осуществляющая последующие выборы пользователя из выпадающих списков (выбор улицы и номера улицы)
    def inhabitant_select_address(self, *widget):
        # Создание списка всех городов
        select_all_cities_query = """SELECT название FROM Города"""
        self.cur.execute(select_all_cities_query, (self.id,))
        all_cities_tuple = self.cur.fetchall()
        self.all_cities = []
        for city in all_cities_tuple:
            self.all_cities.append(city[0])

        self.city_selection = toga.Selection(items=self.all_cities, on_select=self.change_city_handler,
                                             style=Pack(flex=1, padding=(0, 21, 0, 20)))

        # Получение id выбранного города по его названию
        select_all_cities_query = """SELECT город_id FROM Города WHERE название = %s;"""
        self.cur.execute(select_all_cities_query, (self.city_selection.value,))
        self.city_id_result = self.cur.fetchone()

        # Создание списка всех названий улиц выбранного города и определенного сотрудника
        select_all_street_names_query = """SELECT Улицы.название
        FROM Улицы
        inner join Дворы on Дворы.улица = Улицы.улица_id
        WHERE Дворы.город = %s"""
        self.cur.execute(select_all_street_names_query, (self.city_id_result,))
        all_streets_tuple = self.cur.fetchall()
        self.all_streets = []
        for street in all_streets_tuple:
            self.all_streets.append(street[0])
        self.new_all_streets = []
        [self.new_all_streets.append(item) for item in self.all_streets if item not in self.new_all_streets]
        self.street_name_selection = toga.Selection(items=self.new_all_streets,
                                                    on_select=self.change_street_handler,
                                                    style=Pack(flex=1, padding=(0, 20, 0, 20)))

        # Получение списка номеров выбранной улицы из выбранного города
        select_street_numbers_query = """SELECT Улицы.номер
        FROM Дворы
        inner join Улицы on Дворы.улица  = Улицы.улица_id
        inner join Города on Дворы.город  = Города.город_id
        WHERE Города.город_id = %s and Улицы.название = %s;"""
        self.cur.execute(select_street_numbers_query, (self.city_id_result, self.street_name_selection.value,))
        all_street_numbers_tuple = self.cur.fetchall()
        self.all_street_numbers = []
        for street_number in all_street_numbers_tuple:
            self.all_street_numbers.append(str(street_number[0]))
        self.street_number_selection = toga.Selection(items=self.all_street_numbers,
                                                      style=Pack(flex=1, padding=(0, 41, 0, 0)))

    # Функция, обновляющая список названий улиц при изменении выбранного города
    def change_city_handler(self, *widget):
        # Получение id выбранного города
        select_city_id_query = """SELECT город_id
        FROM Города
        WHERE название = %s;"""
        self.cur.execute(select_city_id_query, (self.city_selection.value,))
        city_id = self.cur.fetchall()
        self.city_id_result = city_id[0]
        # Создание списка всех названий улиц выбранного города и определенного сотрудника
        select_all_street_names_query = """SELECT Улицы.название
        FROM Улицы
        inner join Дворы on Дворы.улица  = Улицы.улица_id 
        WHERE Дворы.город = %s"""
        self.cur.execute(select_all_street_names_query, (self.city_id_result,))
        all_streets_tuple = self.cur.fetchall()
        self.all_streets = []
        for street in all_streets_tuple:
            self.all_streets.append(street[0])
        self.new_all_streets = []
        [self.new_all_streets.append(item) for item in self.all_streets if item not in self.new_all_streets]

        # Обновление списков названий улиц и номеров улиц
        self.selections_box.remove(self.street_name_selection, self.street_number_selection)
        self.street_name_selection = toga.Selection(items=self.new_all_streets, on_select=self.change_street_handler,
                                                    style=Pack(flex=1, padding=(0, 20, 0, 20)))
        self.street_number_selection = toga.Selection(items=[], style=Pack(flex=1, padding=(0, 40, 0, 0)))
        self.selections_box.add(self.street_name_selection, self.street_number_selection)
        self.all_streets.clear()

    # Функция, обновляющая список номеров улиц при изменении выбранной улицы
    def change_street_handler(self, *widget):
        # Получение id выбранной улицы
        select_city_id_query = """SELECT Улицы.улица_id
        FROM Улицы
        inner join Дворы on Дворы.улица  = Улицы.улица_id
        inner join Города on Дворы.город  = Города.город_id
        WHERE Улицы.название = %s AND Города.город_id = %s"""
        self.cur.execute(select_city_id_query, (self.street_name_selection.value, self.city_id_result))
        street_id = self.cur.fetchall()
        self.street_id_result = street_id[0]
        # Получение списка номеров выбранной улицы из выбранного города
        select_street_numbers_query = """SELECT Улицы.номер
        FROM Дворы
        inner join Улицы on Дворы.улица  = Улицы.улица_id
        inner join Города on Дворы.город  = Города.город_id
        WHERE Города.город_id = %s and Улицы.название = %s;"""
        self.cur.execute(select_street_numbers_query,
                         (self.city_id_result, self.street_name_selection.value,))
        all_street_numbers_tuple = self.cur.fetchall()
        self.all_street_numbers = []
        for street_number in all_street_numbers_tuple:
            self.all_street_numbers.append(str(street_number[0]))
        # Обновление списка номеров улицы
        self.selections_box.remove(self.street_name_selection, self.street_number_selection)
        self.street_number_selection = toga.Selection(items=self.all_street_numbers,
                                                      style=Pack(flex=1, padding=(0, 40, 0, 0)))
        self.selections_box.add(self.street_name_selection, self.street_number_selection)
        self.all_street_numbers.clear()

    # Функция, добавляющая жителя и его обращение в базу данных после нажатия кнопки
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

        # Получение выбранного жителем адреса из списка
        self.city_selected = self.city_selection.value
        self.street_name_selected = self.street_name_selection.value
        self.street_number_selected = self.street_number_selection.value

        select_address_id_query = """SELECT двор_id
        FROM Дворы
        inner join Улицы on Дворы.улица  = Улицы.улица_id
        inner join Города on Дворы.город  = Города.город_id
        WHERE Города.название = %s and Улицы.название = %s and Улицы.номер = %s;"""
        self.cur.execute(select_address_id_query,
                         (self.city_selected, self.street_name_selected, self.street_number_selected,))
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
        # Вызов окна с информацией об отправленном обращении
        self.feedback_window.info_dialog(title="Ваше обращение отправлено",
                                         message="Содержимое вашего обращения:\n\n"
                                                 f"Фамилия: {self.inhabitant_surname_input.value}\n\n"
                                                 f"Имя: {self.inhabitant_name_input.value}\n\n"
                                                 f"Адрес: {self.city_selected}, {self.street_name_selected}, {self.street_number_selected}\n\n"
                                                 f"Контактная информация: {self.inhabitant_phone_input.value}\n\n"
                                                 f"Текст обращения: {self.appeal_text_input.value}\n\n"
                                         )
        # Очистка полей
        self.inhabitant_surname_input.clear()
        self.inhabitant_name_input.clear()
        self.city_selection.value = self.all_cities[0]
        self.inhabitant_phone_input.clear()
        self.appeal_text_input.clear()

    # Функция, открывающая окно журнала работ
    def open_journal_window(self, widget):
        self.main_window.hide()
        self.create_journal_window()
        self.journal_window.show()

    # Функция, закрывающая окно журнала работ
    def close_journal_window(self, widget):
        self.login_input.clear()
        self.password_input.clear()
        self.main_window.show()
        self.journal_window.hide()

    # Функция, открывающая окно обратной связи
    def open_feedback_window(self, widget):
        self.main_window.hide()
        self.create_feedback_window()
        self.feedback_window.show()

    # Функция, закрывающая окно отправки обратной связи
    def close_feedback_window(self, widget):
        self.feedback_window.hide()
        self.main_window.show()

    # Функция, создающая окна журнала работ
    def create_journal_window(self):
        # Создание названий полей
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

        self.employee_select_address()
        self.employee_selections_box = toga.Box(style=Pack(direction=ROW))

        self.employee_selections_box.add(address_label, self.employee_city_selection,
                                         self.employee_street_name_selection, self.employee_street_number_selection)

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
        self.work_types = []
        for work_type in work_types_tuple:
            self.work_types.append(work_type[0])

        # Создание выпадающего списка с типами работ
        self.work_type_selection = toga.Selection(items=self.work_types, style=Pack(padding=(0, 20, 5, 20)))
        self.comments_input = toga.TextInput(
            style=Pack(flex=2, padding=(0, 20, 5, 20), font_family="montserrat", font_size=12))

        # Создание кнопок окна с журналом работ
        add_journal_entry_button = toga.Button(
            "Добавить уборку в журнал",
            on_press=self.insert_into_journal,
            style=Pack(flex=1, padding=(0, 20, 5, 20), font_family="montserrat", font_size=16)
        )
        logout_button = toga.Button(
            "Выход",
            on_press=self.close_journal_window,
            style=Pack(padding=(0, 18, 5, 20), font_family="montserrat", font_size=16)
        )

        # Создание контейнеров
        main_box = toga.Box(style=Pack(direction=COLUMN))
        name_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        btn_box = toga.Box(style=Pack(direction=ROW, padding=5))

        # Добавление элементов в контейнеры
        name_box.add(employee_label, self.employee_journal_input,
                     address_label, self.employee_selections_box,
                     date_label, self.date,
                     type_label, self.work_type_selection,
                     comment_label, self.comments_input)
        btn_box.add(add_journal_entry_button, logout_button)

        # Добавление контейнеров и кнопок в главный контейнер
        main_box.add(name_box)
        main_box.add(btn_box)
        # Создание окна журнала работ, определение его содержимого и его добавление в список окон программы
        self.journal_window = toga.Window(title="Журнал работ", resizeable=False, on_close=self.close_journal_window)
        self.journal_window.content = main_box
        self.windows.add(self.journal_window)

    # Функция, создающая список городов и осуществляющая последующие выборы пользователя из выпадающих списков (выбор улицы и номера улицы)
    def employee_select_address(self, *widget):
        # Создание списка всех городов сотрудника
        select_all_cities_query = """SELECT название
        FROM Дворы
        inner join Города on Дворы.город  = Города.город_id
        inner join Сотрудники_и_дворы on Сотрудники_и_дворы.двор  = Дворы.двор_id
        inner join Сотрудники on Сотрудники_и_дворы.сотрудник  = Сотрудники.сотрудник_id 
        WHERE Сотрудники_и_дворы.сотрудник = %s;"""
        self.cur.execute(select_all_cities_query, (self.employee_id,))
        all_cities_tuple = self.cur.fetchone()
        self.employee_all_cities = []
        for city in all_cities_tuple:
            self.employee_all_cities.append(str(city))

        self.employee_city_selection = toga.Selection(items=self.employee_all_cities,
                                                      on_select=self.employee_change_city_handler,
                                                      style=Pack(flex=1, padding=(0, 21, 0, 20)))

        # Получение id выбранного города по его названию
        select_all_cities_query = """SELECT город_id
                FROM Города
                WHERE название = %s;"""
        self.cur.execute(select_all_cities_query, (self.employee_city_selection.value,))
        self.employee_city_id_result = self.cur.fetchone()

        # Создание списка всех названий улиц выбранного города и определенного сотрудника
        select_all_street_names_query = """SELECT Улицы.название
                                            FROM Улицы
                                            inner join Дворы on Дворы.улица  = Улицы.улица_id 
                                            inner join Сотрудники_и_дворы on Сотрудники_и_дворы.двор  = Дворы.двор_id
                                            inner join Сотрудники on Сотрудники_и_дворы.сотрудник  = Сотрудники.сотрудник_id 
                                            WHERE Сотрудники_и_дворы.сотрудник = %s AND Дворы.город = %s"""
        self.cur.execute(select_all_street_names_query, (self.employee_id, self.employee_city_id_result))
        all_streets_tuple = self.cur.fetchall()
        self.employee_all_streets = []
        for street in all_streets_tuple:
            self.employee_all_streets.append(street[0])
        self.new_employee_all_streets = []
        [self.new_employee_all_streets.append(item) for item in self.employee_all_streets if
         item not in self.new_employee_all_streets]
        self.employee_street_name_selection = toga.Selection(items=self.new_employee_all_streets,
                                                             on_select=self.employee_change_street_handler,
                                                             style=Pack(flex=1, padding=(0, 20, 0, 20)))

        # Получение списка номеров выбранной улицы из выбранного города
        select_street_numbers_query = """SELECT Улицы.номер
          FROM Дворы
          inner join Улицы on Дворы.улица  = Улицы.улица_id
          inner join Города on Дворы.город  = Города.город_id
          inner join Сотрудники_и_дворы on Сотрудники_и_дворы.двор  = Дворы.двор_id
          WHERE Города.город_id = %s and Улицы.название = %s and Сотрудники_и_дворы.сотрудник = %s;"""
        self.cur.execute(select_street_numbers_query,
                         (self.employee_city_id_result, self.employee_street_name_selection.value, self.employee_id,))
        all_street_numbers_tuple = self.cur.fetchall()
        self.employee_all_street_numbers = []
        for street_number in all_street_numbers_tuple:
            self.employee_all_street_numbers.append(str(street_number[0]))
        self.employee_street_number_selection = toga.Selection(items=self.employee_all_street_numbers,
                                                               style=Pack(flex=1, padding=(0, 20, 0, 20)))

    # Функция, обновляющая список названий улиц при изменении выбранного города
    def employee_change_city_handler(self, *widget):
        # Получение id выбранного города
        select_city_id_query = """SELECT город_id
                         FROM Города
                         WHERE название = %s;"""
        self.cur.execute(select_city_id_query, (self.employee_city_selection.value,))
        city_id = self.cur.fetchall()
        self.employee_city_id_result = city_id[0]
        # Создание списка всех названий улиц выбранного города и определенного сотрудника
        select_all_street_names_query = """SELECT Улицы.название
                                                   FROM Улицы
                                                   inner join Дворы on Дворы.улица  = Улицы.улица_id 
                                                   inner join Сотрудники_и_дворы on Сотрудники_и_дворы.двор  = Дворы.двор_id
                                                   inner join Сотрудники on Сотрудники_и_дворы.сотрудник  = Сотрудники.сотрудник_id 
                                                   WHERE Сотрудники_и_дворы.сотрудник = %s AND Дворы.город = %s"""
        self.cur.execute(select_all_street_names_query, (self.employee_id, self.employee_city_id_result))
        all_streets_tuple = self.cur.fetchall()
        self.employee_all_streets = []
        for street in all_streets_tuple:
            self.employee_all_streets.append(street[0])
        self.new_employee_all_streets = []
        [self.new_employee_all_streets.append(item) for item in self.employee_all_streets if
         item not in self.new_employee_all_streets]

        # Обновление списков названий улиц и номеров улиц
        self.employee_selections_box.remove(self.employee_street_name_selection, self.employee_street_number_selection)
        self.employee_street_name_selection = toga.Selection(items=self.new_employee_all_streets,
                                                             on_select=self.employee_change_street_handler,
                                                             style=Pack(flex=1, padding=(0, 20, 0, 20)))
        self.employee_street_number_selection = toga.Selection(items=[], style=Pack(flex=1, padding=(0, 20, 0, 20)))
        self.employee_selections_box.add(self.employee_street_name_selection, self.employee_street_number_selection)
        self.employee_all_streets.clear()

    # Функция, обновляющая список номеров улиц при изменении выбранной улицы
    def employee_change_street_handler(self, *widget):
        # Получение id выбранной улицы
        select_city_id_query = """SELECT Улицы.улица_id
                        FROM Улицы
                        inner join Дворы on Дворы.улица  = Улицы.улица_id
                        inner join Города on Дворы.город  = Города.город_id
                        WHERE Улицы.название = %s AND Города.город_id = %s"""
        self.cur.execute(select_city_id_query,
                         (self.employee_street_name_selection.value, self.employee_city_id_result))
        street_id = self.cur.fetchall()
        self.employee_street_id_result = street_id[0]
        # Получение списка номеров выбранной улицы из выбранного города
        select_street_numbers_query = """SELECT Улицы.номер
                FROM Дворы
                inner join Улицы on Дворы.улица  = Улицы.улица_id
                inner join Города on Дворы.город  = Города.город_id
                inner join Сотрудники_и_дворы on Сотрудники_и_дворы.двор  = Дворы.двор_id
                WHERE Города.город_id = %s and Улицы.название = %s and Сотрудники_и_дворы.сотрудник = %s;"""
        self.cur.execute(select_street_numbers_query,
                         (self.employee_city_id_result, self.employee_street_name_selection.value, self.employee_id,))
        all_street_numbers_tuple = self.cur.fetchall()
        self.employee_all_street_numbers = []
        for street_number in all_street_numbers_tuple:
            self.employee_all_street_numbers.append(str(street_number[0]))
        # Обновление списка номеров улицы
        self.employee_selections_box.remove(self.employee_street_name_selection, self.employee_street_number_selection)
        self.employee_street_number_selection = toga.Selection(items=self.employee_all_street_numbers,
                                                               style=Pack(flex=1, padding=(0, 20, 0, 20)))
        self.employee_selections_box.add(self.employee_street_name_selection, self.employee_street_number_selection)
        self.employee_all_street_numbers.clear()

    # Функция, добавляющая запись в журнал работ после нажатия кнопки
    def insert_into_journal(self, widget):
        # Получение id сотрудника по его ФИО
        select_employee_id_by_full_name_query = """SELECT сотрудник_id 
        FROM Сотрудники
        WHERE фамилия = %s AND имя = %s AND отчество = %s;"""
        self.cur.execute(select_employee_id_by_full_name_query,
                         (self.employee_full_name[0], self.employee_full_name[1], self.employee_full_name[2],))
        employee_id = self.cur.fetchone()
        self.employee_id_result = employee_id[0]

        # Получение id выбранного двора по его городу, названию улицы и номеру
        self.employee_city_selected = self.employee_city_selection.value
        self.employee_street_name_selected = self.employee_street_name_selection.value
        self.employee_street_number_selected = self.employee_street_number_selection.value

        select_address_id_query = """SELECT двор_сотрудника_id
        FROM Сотрудники_и_дворы
        inner join Дворы on Сотрудники_и_дворы.двор  = Дворы.двор_id 
        inner join Улицы on Дворы.улица  = Улицы.улица_id
        inner join Города on Дворы.город  = Города.город_id
        inner join Сотрудники on Сотрудники_и_дворы.сотрудник  = Сотрудники.сотрудник_id 
        WHERE Города.название = %s and Улицы.название = %s and Улицы.номер = %s and Сотрудники.сотрудник_id = %s"""
        self.cur.execute(select_address_id_query,
                         (self.employee_city_selected, self.employee_street_name_selected,
                          self.employee_street_number_selected, self.employee_id))
        employees_addresses = self.cur.fetchone()
        self.employee_address_id = employees_addresses[0]

        select_address_and_employee_id_query = """SELECT двор_сотрудника_id
        FROM Сотрудники_и_дворы
        inner join Дворы on Дворы.двор_id  = Сотрудники_и_дворы.двор 
        inner join Сотрудники on Сотрудники_и_дворы.сотрудник  = Сотрудники.сотрудник_id 
        WHERE Сотрудники.сотрудник_id = %s and Дворы.двор_id = %s"""
        self.cur.execute(select_address_and_employee_id_query,
                         (self.employee_id, self.employee_address_id,))
        employee_and_address = self.cur.fetchone()
        self.employee_and_address_id_result = employees_addresses[0]

        # Получение id типа выполненной работы по его названию
        self.work_type_selected = self.work_type_selection.value
        select_query = """SELECT тип_работы_id 
        FROM Типы_работ 
        WHERE название = %s;"""
        self.cur.execute(select_query, (self.work_type_selected,))
        work_type = self.cur.fetchone()
        self.work_type_id_result = work_type[0]

        # Получение комментария от сотрудника
        self.comments_result = self.comments_input.value
        # Получение времени отправки отчета о работе
        self.journal_insert_time_result = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        # SQL-запрос для вставки данных в таблицу Журнал работ
        insert_result_query = sql.SQL(
            "INSERT INTO Журнал_уборки (двор_и_сотрудник, тип_работ, дата_и_время_уборки, комментарий) VALUES ("
            "{}, {}, {}, {});").format(
            sql.Literal(self.employee_and_address_id_result),
            sql.Literal(self.work_type_id_result),
            sql.Literal(self.journal_insert_time_result),
            sql.Literal(self.comments_result)
        )
        # Выполнение SQL-запроса
        self.cur.execute(insert_result_query)
        # Подтверждение изменений
        self.conn.commit()
        # Вызов окна с информацией о добавленной записи
        self.journal_window.info_dialog(title="Запись добавлена в журнал",
                                        message="Содержимое записи:\n\n"
                                                f"Сотрудник: {self.employee_full_name[0]} {self.employee_full_name[1]} {self.employee_full_name[2]}\n\n"
                                                f"Проделал работу по адресу: {self.employee_city_selected}, {self.employee_street_name_selected}, {self.employee_street_number_selected}\n\n"
                                                f"Дата и время добавления записи: {self.journal_insert_time_result}\n\n"
                                                f"Тип выполненных работ: {self.work_type_selected}\n\n"
                                                f"Комментарий сотрудника: {self.comments_result}\n\n"
                                        )
        # Очистка полей
        self.work_type_selection.value = self.work_types[0]
        self.comments_input.clear()


def main():
    return Clean()
