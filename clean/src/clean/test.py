# -*- coding: windows-1251 -*-
import psycopg2 as db
import datetime
from psycopg2 import sql

try:
    # �������� ������������ � ���� ������
    conn = db.connect(dbname='postgres', user='postgres', password='123', host='localhost')
    print('Established connection to database')
    # �������� ������� ������� ��� ���������� SQL-��������
    cur = conn.cursor()
except Exception as e:
    # � ������ ���� ����������� ����� �������� ��������� � �������
    print(e)
    print('Can`t establish connection to database')


def print_all():
    # ���������� SQL-�������
    # SQL-������ ��� ������� ������ �� ��������������
    journal_id = 1

    select_query = """SELECT ������_������.����_�_�����_������,
           ����.�����,
           ���������.�������,
           ���������.���,
           ���������.��������,
           ���_������.��������,
           ������_������.�����������
    FROM ������_������
    INNER JOIN ���� ON ������_������.����_id = ����.����_id
    INNER JOIN ��������� ON ������_������.���������_id = ���������.���������_id
    INNER JOIN ���_������ ON ������_������.���_������ = ���_������.���_������_id
    WHERE ������_������.������_id = %s;"""

    # ���������� SQL-������� � �������������� ���������
    cur.execute(select_query, (journal_id,))

    # ��������� �����������
    result = cur.fetchone()

    # ����� ������
    if result:
        date, address, surname, name, patronymic, clean_type, comments = result
        print("���� � ����� ������:", date)
        print("���������:", surname, name, patronymic)
        print("����:", address)
        print("��� ������:", clean_type)
        print("�����������:", comments)
    else:
        print("������ � ��������� ��������������� �� �������.")

    # ������������� ��������� � �������� ����������
    conn.commit()
    conn.close()

#
# def list():
#     employee_id = 1
#     select_query = """SELECT ����� FROM ���������
#     INNER JOIN ���� ON ���������.����_id = ����.����_id
#     WHERE ���������_id = %s;"""
#     cur.execute(select_query, (employee_id,))
#     employees_adresses_tuple = cur.fetchall()
#     employees_adresses = []
#     for address in employees_adresses_tuple:
#         address = str(address)
#         employees_adresses.append(address)

    # selection = toga.Selection(items=employees_adresses)


def select():
    employee_id = 24
    select_query = """SELECT ����.����_id FROM ���� 
        INNER JOIN ��������� ON ���������.����_id = ����.����_id 
        WHERE ���������_id = %s;"""
    cur.execute(select_query, (employee_id,))
    employees_adresses = cur.fetchone()
    address_result = employees_adresses[0]
    print(address_result)

    #
    # select_query = """SELECT �������, ���, �������� FROM ���������
    #             INNER JOIN ���� ON ���������.����_id = ����.����_id
    #             WHERE ���������_id = %s;"""
    # cur.execute(select_query, (employee_id,))
    # employees_name = cur.fetchone()
    # print(employees_name)
    # # if employees_name:
    # #     surname, name, patronymic = employees_name
    # #
    # #     emploeee = employees_name[0] + " " + employees_name[1] + " " + employees_name[2]
    #
    # select_query = """SELECT ���������_id FROM ��������� WHERE ������� = %s AND ��� = %s AND �������� = %s;"""
    # cur.execute(select_query, (employees_name[0], employees_name[1], employees_name[2], ))
    # employee_id = cur.fetchone()
    # employee_id = employee_id[0]
    #
    # print(employee_id)

# select()

# auth_main_box = toga.Box(style=Pack(direction=COLUMN))
#
# login_label = toga.Label(
#     "������� �����: ",
#     style=Pack(padding=(0, 0, 2, 0))
# )
# password_label = toga.Label(
#     "������� ������: ",
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
#     "�����",
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
# select_employees_work_types_query = """SELECT ��������
# FROM ����_�����
# inner join ���������_�_����_����� on ����_�����.���_������_id = ���������_�_����_�����.���_������
# inner join ���������� on ����������.��������� = ���������_�_����_�����.���������
# where ����������.���������_id = %s;"""
# cur.execute(select_employees_work_types_query, (employee_id,))


# ��������� ������ ������� ��������� ����� �� ���������� ������
# select_street_numbers_query = """SELECT �����.�����
#           FROM �����
#           inner join ����� on �����.�����  = �����.�����_id
#           inner join ������ on �����.�����  = ������.�����_id
#           inner join ����������_�_����� on ����������_�_�����.����  = �����.����_id
#           WHERE ������.�������� = %s and �����.�������� = %s and ����������_�_�����.��������� = 1;"""
#
# employee_street_id_result = '�����������'
# employee_city_id_result = '������'
# cur.execute(select_street_numbers_query, (employee_street_id_result, employee_city_id_result,))
# all_street_numbers_tuple = cur.fetchall()
# employee_all_street_numbers = []
# for street_number in all_street_numbers_tuple:
#     employee_all_street_numbers.append(str(street_number[0]))
#
# print(employee_all_street_numbers)

# �������� ������ ���� ������� ���������� ������
select_all_street_names_query = """SELECT �����.��������
       FROM �����
       inner join ����� on �����.�����  = �����.�����_id
       inner join ������ on �����.����� = ������.�����_id
       WHERE ������.�����_id = %s;"""

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
