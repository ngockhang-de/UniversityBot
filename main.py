import telebot
import sqlite3
import re
import datetime
import os

token = ''

bot = telebot.TeleBot(token)

def execute_query(sql, params = None):
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        if params is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, params)
        conn.commit()
        return cursor.fetchall()
    except Exception as ex:
        print(ex)

def get_state(message):
    uid = int(message.from_user.id)
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        cursor.execute("select status from USER us join STATE st on status_id = st.id where us.id = ?", [uid])
        conn.commit()
        return cursor.fetchone()[0]
    except Exception as ex:
        print(ex)

def set_state(message, state):
    uid = int(message.from_user.id)
    try:
        state_id = execute_query("select id from state where status = ?", [state])[0][0]
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        cursor.execute("update user set status_id = ? where id = ?", [state_id, uid])
        conn.commit()
        if state == 'Chill':
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            role = get_role(message)
            if role in ('Admin', 'Student', 'Teacher'):
                markup.row('Инструкция', 'Курсы', 'Занятия')
                if role in ('Admin', 'Teacher'):
                    markup.row('Добавить курс', 'Изменить курс', 'Удалить курс')
                    markup.row('Добавить занятие', 'Изменить занятие', 'Удалить занятие')
                    if role in ('Admin'):
                            markup.row('Добавить преподавателя', 'Изменить пользователя', 'Удалить преподавателей')
            markup.row('Просмотреть преподавателей', 'Изменить личные данные')
            bot.send_message(message.chat.id, 'Укажите действие из списка ниже', reply_markup=markup)
    except Exception as ex:
        print(ex)

def set_name(message, name):
    uid = int(message.from_user.id)
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        cursor.execute("update user set name = ? where id = ?", [name, uid])
        conn.commit()
    except Exception as ex:
        print(ex)

def set_surname(message, surname):
    uid = int(message.from_user.id)
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        cursor.execute("update user set surname = ? where id = ?", [surname, uid])
        conn.commit()
    except Exception as ex:
        print(ex)

def set_number(message, num):
    uid = int(message.from_user.id)
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        cursor.execute("update user set tel_no = ? where id = ?", [num, uid])
        conn.commit()
    except Exception as ex:
        print(ex)

def set_email(message, email):
    uid = int(message.from_user.id)
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        cursor.execute("update user set email = ? where id = ?", [email, uid])
        conn.commit()
    except Exception as ex:
        print(ex)

def set_role(message, role):
    uid = int(message.from_user.id)
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        rl = execute_query("select id from role where role = ?", [role])[0][0]
        cursor.execute("update user set role = ? where id = ?", [rl, uid])
        conn.commit()
    except Exception as ex:
        print(ex)

def set_role_by_id(id, role):
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        rl = execute_query("select id from role where role = ?", [role])[0][0]
        cursor.execute("update user set role = ? where id = ?", [rl, id])
        conn.commit()
    except Exception as ex:
        print(ex)

def get_role(message):
    uid = int(message.from_user.id)
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        cursor.execute("select role.role from user join role on user.role = role.id where user.id = ?", [uid])
        conn.commit()
        return cursor.fetchone()[0]
    except Exception as ex:
        print(ex)

def get_role_by_id(id):
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        cursor.execute("select role.role from user join role on user.role = role.id where user.id = ?", [id])
        conn.commit()
        return cursor.fetchone()[0]
    except Exception as ex:
        print(ex)

def is_teacher(id):
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        cursor.execute("select role.role from user join role on user.role = role.id where user.id = ?", [id])
        conn.commit()
        return cursor.fetchone()[0] == 'Teacher'
    except Exception as ex:
        print(ex)

def in_system(id):
    return bool(execute_query("select count(*) from user where id = ?", [id])[0][0])

def get_teachers_info():
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        cursor.execute("select name, surname, telegram_id, user.id from user join role on user.role = role.id where role.role = 'Teacher' order by name")
        conn.commit()
        return cursor.fetchall()
    except Exception as ex:
        print(ex)

def get_users_info():
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        cursor.execute("select role.role, name, surname, telegram_id, user.id from user join role on user.role = role.id order by role.role, name")
        conn.commit()
        return cursor.fetchall()
    except Exception as ex:
        print(ex)

def get_teacher(name, surname, t_id, id):
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        cursor.execute("select name, surname, telegram_id, email, tel_no from user where name = ? and surname = ? and telegram_id = ? and id = ?", [name, surname, t_id, id])
        conn.commit()
        return cursor.fetchall()
    except Exception as ex:
        print(ex)

def get_user(id):
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        cursor.execute("select name, surname, telegram_id, tel_no, email from user where id = ?", [id])
        conn.commit()
        return cursor.fetchall()
    except Exception as ex:
        print(ex)

def get_additional_data(message):
    uid = int(message.from_user.id)
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        cursor.execute("select data from tempdata where user_id = ?", [uid])
        conn.commit()
        return cursor.fetchall()[0]
    except Exception as ex:
        print(ex)

def set_additional_data(message, data):
    uid = int(message.from_user.id)
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        cursor.execute("insert into tempdata (user_id, data) values (?, ?)", [uid, data])
        conn.commit()
    except Exception as ex:
        print(ex)
        
def del_additional_data(message):
    uid = int(message.from_user.id)
    try:
        conn = sqlite3.connect("database.db3")
        cursor = conn.cursor()
        cursor.execute("delete from tempdata where user_id = ?", [uid])
        conn.commit()
    except Exception as ex:
        print(ex)