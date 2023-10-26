# -*- coding: windows-1251 -*-
import psycopg2 as db
import datetime
from psycopg2 import sql

try:
    # пытаемся подключиться к базе данных
    conn = db.connect(dbname='postgres', user='postgres', password='123', host='localhost')
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

#
# def list():
#     employee_id = 1
#     select_query = """SELECT адрес FROM Сотрудник
#     INNER JOIN Двор ON Сотрудник.двор_id = Двор.двор_id
#     WHERE сотрудник_id = %s;"""
#     cur.execute(select_query, (employee_id,))
#     employees_adresses_tuple = cur.fetchall()
#     employees_adresses = []
#     for address in employees_adresses_tuple:
#         address = str(address)
#         employees_adresses.append(address)

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

# select()

# auth_main_box = toga.Box(style=Pack(direction=COLUMN))
#
# login_label = toga.Label(
#     "Введите логин: ",
#     style=Pack(padding=(0, 0, 2, 0))
# )
# password_label = toga.Label(
#     "Введите пароль: ",
#     style=Pack(padding=(10, 0, 2, 0))
# )
#
# login_input = toga.TextInput(style=Pack(flex=2, padding=(0, 0, 5, 0)))
# password_input = toga.TextInput(style=Pack(flex=2, padding=(0, 0, 5, 0)))
#
# auth_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
# auth_box.add(login_label, login_input, password_label, password_input)
#
# login_button = toga.Button(
#     "Войти",
#     on_press=insert_journal,
#     style=Pack(padding=5)
# )
#
# auth_main_box.add(auth_box)
# auth_main_box.add(login_button)
#
# auth_window = toga.Window(title=formal_name)
# auth_window.content = auth_main_box
# auth_window.show()

# employee_id = 1
# select_employees_work_types_query = """SELECT название
# FROM Типы_работ
# inner join Должности_и_типы_работ on Типы_работ.тип_работы_id = Должности_и_типы_работ.тип_работы
# inner join Сотрудники on Сотрудники.должность = Должности_и_типы_работ.должность
# where Сотрудники.сотрудник_id = %s;"""
# cur.execute(select_employees_work_types_query, (employee_id,))


# Получение списка номеров выбранной улицы из выбранного города
# select_street_numbers_query = """SELECT Улицы.номер
#           FROM Дворы
#           inner join Улицы on Дворы.улица  = Улицы.улица_id
#           inner join Города on Дворы.город  = Города.город_id
#           inner join Сотрудники_и_дворы on Сотрудники_и_дворы.двор  = Дворы.двор_id
#           WHERE Города.название = %s and Улицы.название = %s and Сотрудники_и_дворы.сотрудник = 1;"""
#
# employee_street_id_result = 'Альметьевск'
# employee_city_id_result = 'Ленина'
# cur.execute(select_street_numbers_query, (employee_street_id_result, employee_city_id_result,))
# all_street_numbers_tuple = cur.fetchall()
# employee_all_street_numbers = []
# for street_number in all_street_numbers_tuple:
#     employee_all_street_numbers.append(str(street_number[0]))
#
# print(employee_all_street_numbers)

# Создание списка всех адресов выбранного города
select_all_street_names_query = """SELECT Улицы.название
       FROM Улицы
       inner join Дворы on Дворы.улица  = Улицы.улица_id
       inner join Города on Дворы.город = Города.город_id
       WHERE Города.город_id = %s;"""

city_selection = 1
cur.execute(select_all_street_names_query, (city_selection,))
all_streets_tuple = cur.fetchall()
all_streets = []

for street in all_streets_tuple:
    all_streets.append(street[0])
print(all_streets)

new_all_streets = []
[new_all_streets.append(item) for item in all_streets if item not in new_all_streets]
print(new_all_streets)
