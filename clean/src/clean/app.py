# -*- coding: utf-8 -*-
"""
clean app
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import psycopg2 as db
import datetime
from psycopg2 import sql

class clean(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(style=Pack(direction=COLUMN))

        employee_label = toga.Label(
            "Введите номер сотрудника: ",
            style=Pack(padding=(0, 5))
        )
        address_label = toga.Label(
            "Введите адрес: ",
            style=Pack(padding=(0, 5))
        )
        type_label = toga.Label(
            "Введите тип уборки: ",
            style=Pack(padding=(0, 5))
        )
        comment_label = toga.Label(
            "Введите комментарий: ",
            style=Pack(padding=(0, 5))
        )

        self.employee_input = toga.NumberInput(style=Pack(flex=2))
        self.address_input = toga.TextInput(style=Pack(flex=1))
        self.type_input = toga.TextInput(style=Pack(flex=1))
        self.comments_input = toga.TextInput(style=Pack(flex=2))

        name_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        name_box.add(employee_label, self.employee_input, address_label, self.address_input, type_label, self.type_input, comment_label,  self.comments_input, )

        button = toga.Button(
            "Добавить в базу",
            on_press=self.insert_journal,
            style=Pack(padding=5)
        )

        main_box.add(name_box)
        main_box.add(button)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def insert_journal(self, widget):
        try:
            # пытаемся подключиться к базе данных
            conn = db.connect(dbname='cleandb', user='postgres', password='123', host='localhost')
            print('Established connection to database')
        except Exception as e:
            # в случае сбоя подключения будет выведено сообщение в консоли
            print(e)
            print('Can`t establish connection to database')

        employee = self.employee_input.value
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        address = self.address_input.value
        comment = self.comments_input.value
        clean_type = self.type_input.value

        result = f"""Sotrudnik {employee} ubralsya po adresu = {address}
        Date = {current_datetime}
        Tip yborki = {clean_type}
        Kommentarii = {comment}"""
        print(result)

        # SQL-запрос для вставки данных
        insert_query = sql.SQL(
            "INSERT INTO Журнал_уборки (дата_и_время_уборки, сотрудник_id, двор_id, тип_уборки, комментарий) VALUES ({}, {}, {}, {}, {});").format(
            sql.Literal(current_datetime),
            sql.Literal(employee),
            sql.Literal(address),
            sql.Literal(clean_type),
            sql.Literal(comment)
        )
        # Создание объекта курсора для выполнения SQL-запросов
        cur = conn.cursor()
        # Выполнение SQL-запроса
        cur.execute(insert_query)
        # Подтверждение изменений и закрытие соединения
        conn.commit()
        conn.close()
        
def main():
    return clean()
