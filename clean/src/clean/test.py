# -*- coding: windows-1251 -*-
import psycopg2 as db
import datetime
from psycopg2 import sql

try:
    # �������� ������������ � ���� ������
    conn = db.connect(dbname='cleandb', user='postgres', password='123', host='localhost')
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


def list():
    employee_id = 1
    select_query = """SELECT ����� FROM ��������� 
    INNER JOIN ���� ON ���������.����_id = ����.����_id 
    WHERE ���������_id = %s;"""
    cur.execute(select_query, (employee_id,))
    employees_adresses_tuple = cur.fetchall()
    employees_adresses = []
    for address in employees_adresses_tuple:
        address = str(address)
        employees_adresses.append(address)

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

select()