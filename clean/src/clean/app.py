# -*- coding: utf-8 -*-
"""
clean app
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN
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

        login_label = toga.Label(
            "Введите логин: ",
            style=Pack(padding=(0, 0, 2, 0))
        )
        password_label = toga.Label(
            "Введите пароль: ",
            style=Pack(padding=(10, 0, 2, 0))
        )

        login_button = toga.Button(
            "Войти",
            on_press=self.user_login,
            style=Pack(padding=5)
        )

        self.login_input = toga.TextInput(style=Pack(flex=2, padding=(0, 0, 5, 0)))
        self.password_input = toga.TextInput(style=Pack(flex=2, padding=(0, 0, 5, 0)))

        auth_main_box = toga.Box(style=Pack(direction=COLUMN))

        auth_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        auth_box.add(login_label, self.login_input, password_label, self.password_input)

        auth_main_box.add(auth_box)
        auth_main_box.add(login_button)

        self.main_window = toga.MainWindow(title="Авторизация")
        self.main_window.content = auth_main_box
        self.main_window.show()

    def user_login(self, widget):
        self.cur.execute('SELECT пароль FROM Сотрудник WHERE логин = %s;', (self.login_input.value,))
        check_pass = self.cur.fetchall()

        self.cur.execute(f'SELECT логин FROM Сотрудник WHERE пароль =%s;', (self.password_input.value,))
        check_login = self.cur.fetchall()

        if len(self.login_input.value) == 0:
            print('login is empty')
            return

        if len(self.password_input.value) == 0:
            print('password is empty')
            return

        if check_pass[0][0] == self.password_input.value and check_login[0][0] == self.login_input.value:
            select_employee_id_on_login_query = """SELECT сотрудник_id 
            FROM Сотрудник 
            WHERE логин = %s AND пароль = %s;"""
            self.cur.execute(select_employee_id_on_login_query, (self.login_input.value, self.password_input.value,))
            employee_id = self.cur.fetchone()
            self.employee_id = employee_id[0]
            self.main_window.hide()
            self.create_journal_window()
            self.journal_window.show()
            print(f"""====================================
Successfully login! 
Employee_id = {self.employee_id}
Login = {self.login_input.value}
Password = {self.password_input.value}
====================================
        """)
        else:
            print(f"""====================================
Error while logging in! 
Login = {self.login_input.value}
Password = {self.password_input.value}
====================================
            """)
            return

    def user_logout(self, widget):
        self.login_input.clear()
        self.password_input.clear()
        self.main_window.show()
        self.journal_window.hide()

    def create_journal_window(self):
        self.main_window.hide()
        main_box = toga.Box(style=Pack(direction=COLUMN))

        employee_label = toga.Label(
            "Сотрудник: ",
            style=Pack(padding=(0, 0, 2, 0))
        )
        address_label = toga.Label(
            "Адрес уборки: ",
            style=Pack(padding=(10, 0, 2, 0))
        )
        date_label = toga.Label(
            "Дата и время уборки: ",
            style=Pack(padding=(10, 0, 2, 0))
        )
        type_label = toga.Label(
            "Введите тип уборки: ",
            style=Pack(padding=(10, 0, 2, 0))
        )
        comment_label = toga.Label(
            "Введите комментарий: ",
            style=Pack(padding=(10, 0, 2, 0))
        )

        select_employee_full_name_query = """SELECT фамилия, имя, отчество
                FROM Сотрудник
                INNER JOIN Двор ON Сотрудник.двор_id = Двор.двор_id
                WHERE сотрудник_id = %s;"""
        self.cur.execute(select_employee_full_name_query, (self.employee_id,))
        self.employee_full_name = self.cur.fetchone()
        self.employee_journal_input = toga.TextInput(value=self.employee_full_name[0] + " " + self.employee_full_name[1] + " " + self.employee_full_name[2], readonly=True)

        select_employee_work_address_query = """SELECT адрес
                FROM Сотрудник
                INNER JOIN Двор ON Сотрудник.двор_id = Двор.двор_id
                WHERE сотрудник_id = %s;"""
        self.cur.execute(select_employee_work_address_query, (self.employee_id,))
        employee_work_address = self.cur.fetchone()
        employee_work_address = employee_work_address[0]
        self.address_input = toga.TextInput(value=employee_work_address, readonly=True)

        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        self.date = toga.TextInput(value=current_datetime, readonly=True)

        select_all_work_types_query = """SELECT название
                FROM Тип_уборки"""
        self.cur.execute(select_all_work_types_query)
        work_types_tuple = self.cur.fetchall()
        work_types = []
        for work_type in work_types_tuple:
            work_types.append(work_type[0])

        self.work_type_selection = toga.Selection(items=work_types)
        self.comments_input = toga.TextInput(style=Pack(flex=2, padding=(0, 0, 5, 0)))

        name_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        name_box.add(employee_label, self.employee_journal_input, address_label, self.address_input, date_label,
                     self.date, type_label, self.work_type_selection, comment_label, self.comments_input)

        add_journal_entry_button = toga.Button(
            "Добавить уборку в журнал",
            on_press=self.insert_into_journal,
            style=Pack(padding=5)
        )

        logout_button = toga.Button(
            "Выйти",
            on_press=self.user_logout,
            style=Pack(padding=5)
        )

        main_box.add(name_box)
        main_box.add(add_journal_entry_button)
        main_box.add(logout_button)

        self.journal_window = toga.MainWindow(title="Журнал уборки")
        self.windows.add(self.journal_window)
        self.journal_window.content = main_box

    def insert_into_journal(self, widget):
        select_employee_id_by_full_name_query = """SELECT сотрудник_id 
        FROM Сотрудник 
        WHERE фамилия = %s AND имя = %s AND отчество = %s;"""
        self.cur.execute(select_employee_id_by_full_name_query,
                         (self.employee_full_name[0], self.employee_full_name[1], self.employee_full_name[2],))
        employee_id = self.cur.fetchone()
        employee_id_result = employee_id[0]

        select_courtyard_id_by_employee_id_query = """SELECT Двор.двор_id 
        FROM Двор 
        INNER JOIN Сотрудник ON Сотрудник.двор_id = Двор.двор_id 
        WHERE сотрудник_id = %s;"""
        self.cur.execute(select_courtyard_id_by_employee_id_query, (self.employee_id,))
        employees_addresses = self.cur.fetchone()
        address_result = employees_addresses[0]

        work_type_selected = self.work_type_selection.value
        select_query = """SELECT тип_уборки_id 
        FROM Тип_уборки 
        WHERE название = %s;"""
        self.cur.execute(select_query, (work_type_selected,))
        work_type = self.cur.fetchone()
        work_type_result = work_type[0]

        comment_result = self.comments_input.value
        current_datetime_result = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        result = f"""=============================================
Sotrudnik {employee_id_result} prodelal raboty po adresu = {address_result}
Date = {current_datetime_result}
Tip yborki = {work_type_result}
Kommentarii = {comment_result}
=============================================
        """
        print(result)

        # SQL-запрос для вставки данных
        insert_result_query = sql.SQL(
            "INSERT INTO Журнал_уборки (дата_и_время_уборки, сотрудник_id, двор_id, тип_уборки, комментарий) VALUES ("
            "{}, {}, {}, {}, {});").format(
            sql.Literal(current_datetime_result),
            sql.Literal(employee_id_result),
            sql.Literal(address_result),
            sql.Literal(work_type_result),
            sql.Literal(comment_result)
        )
        # Выполнение SQL-запроса
        self.cur.execute(insert_result_query)
        # Подтверждение изменений и закрытие соединения
        self.conn.commit()


def main():
    return Clean()
