# -*- coding: windows-1251 -*-
import psycopg2 as db
import datetime
from psycopg2 import sql

try:
    # пытаемся подключиться к базе данных
    conn = db.connect(dbname='cleandb', user='postgres', password='123', host='localhost')
    print('Established connection to database')
    # Создание объекта курсора для выполнения SQL-запросов
    cur = conn.cursor()
except Exception as e:
    # в случае сбоя подключения будет выведено сообщение в консоли
    print(e)
    print('Can`t establish connection to database')


def print_all():
    # Выполнение SQL-запроса
    # SQL-запрос для выборки данных по идентификатору
    journal_id = 1

    select_query = """SELECT Журнал_уборки.дата_и_время_уборки,
           Двор.адрес,
           Сотрудник.фамилия,
           Сотрудник.имя,
           Сотрудник.отчество,
           Тип_уборки.название,
           Журнал_уборки.комментарий
    FROM Журнал_уборки
    INNER JOIN Двор ON Журнал_уборки.двор_id = Двор.двор_id
    INNER JOIN Сотрудник ON Журнал_уборки.сотрудник_id = Сотрудник.сотрудник_id
    INNER JOIN Тип_уборки ON Журнал_уборки.тип_уборки = Тип_уборки.тип_уборки_id
    WHERE Журнал_уборки.журнал_id = %s;"""

    # Выполнение SQL-запроса с использованием параметра
    cur.execute(select_query, (journal_id,))

    # Получение результатов
    result = cur.fetchone()

    # Вывод данных
    if result:
        date, address, surname, name, patronymic, clean_type, comments = result
        print("Дата и время уборки:", date)
        print("Сотрудник:", surname, name, patronymic)
        print("Двор:", address)
        print("Тип уборки:", clean_type)
        print("Комментарий:", comments)
    else:
        print("Запись с указанным идентификатором не найдена.")

    # Подтверждение изменений и закрытие соединения
    conn.commit()
    conn.close()


def list():
    employee_id = 1
    select_query = """SELECT адрес FROM Сотрудник 
    INNER JOIN Двор ON Сотрудник.двор_id = Двор.двор_id 
    WHERE сотрудник_id = %s;"""
    cur.execute(select_query, (employee_id,))
    employees_adresses_tuple = cur.fetchall()
    employees_adresses = []
    for address in employees_adresses_tuple:
        address = str(address)
        employees_adresses.append(address)

    # selection = toga.Selection(items=employees_adresses)


def select():
    employee_id = 24
    select_query = """SELECT Двор.двор_id FROM Двор 
        INNER JOIN Сотрудник ON Сотрудник.двор_id = Двор.двор_id 
        WHERE сотрудник_id = %s;"""
    cur.execute(select_query, (employee_id,))
    employees_adresses = cur.fetchone()
    address_result = employees_adresses[0]
    print(address_result)

    #
    # select_query = """SELECT фамилия, имя, отчество FROM Сотрудник
    #             INNER JOIN Двор ON Сотрудник.двор_id = Двор.двор_id
    #             WHERE сотрудник_id = %s;"""
    # cur.execute(select_query, (employee_id,))
    # employees_name = cur.fetchone()
    # print(employees_name)
    # # if employees_name:
    # #     surname, name, patronymic = employees_name
    # #
    # #     emploeee = employees_name[0] + " " + employees_name[1] + " " + employees_name[2]
    #
    # select_query = """SELECT сотрудник_id FROM Сотрудник WHERE фамилия = %s AND имя = %s AND отчество = %s;"""
    # cur.execute(select_query, (employees_name[0], employees_name[1], employees_name[2], ))
    # employee_id = cur.fetchone()
    # employee_id = employee_id[0]
    #
    # print(employee_id)

select()