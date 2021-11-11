import os

import telebot
import sqlite3
import re
import datetime
from telebot import types
from email_validator import validate_email


token = '2014696218:AAH2DXNBSeViA0nm5j6Cx5WC9SbIdUwdAvg'

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


@bot.message_handler(commands=['start'])
def start_message(message):
    uid =  int(message.from_user.id)
    chat_id = message.chat.id
    username = message.from_user.username
    if username is None:
        username = 'None'
    in_system = bool(execute_query("select count(*) from user where id = ?", [uid])[0][0])
    if (not in_system):
        status_id = execute_query("select id from state where status = 'Not registered'")[0][0]
        role = execute_query("select id from role where role = 'NRG'")[0][0]
        execute_query('insert into user (id, role, chat_id, status_id, telegram_id) values (?, ?, ?, ?, ?)', [uid, role, chat_id, status_id, username])
        bot.send_message(chat_id, '✅Приветствуем Вас в системе дистанционного обучения😊\n' +
                         '✅Чтобы использоавние системы было более усшпеным, предлагаем пройти короткую регистрацию\n' +
                         '✅Это займёт всего минуту⏳')
        bot.send_message(chat_id, 'Введите имя\n\n'+
                                    '✅Правильно: Владислав, Андрей, Artem\n'+
                                    '❌Неправильно: Влад1слав, Andrey2020')
    else:
        bot.send_message(message.chat.id, 'С возвращением в систему дистанционного обучения🧑‍🎓')


@bot.message_handler(content_types=['text'])
def start_message(message):
    state = get_state(message)
    print('State:', state, "|", datetime.datetime.now(), '| Message:', message.text)
    num = -1
    try:
        num = execute_query('select count(*) from user where id = ?', [int(message.from_user.id)])[0][0]
    except Exception as Ex:
        pass
    if num == 0:
        bot.send_message(message.chat.id, 'Укажите команду "/start" в чат')
    elif state == "Not registered":
        text = message.text
        if re.fullmatch('[A-Za-zА-Яа-яёЁЇїЄєІіҐґ]{2,25}( [A-Za-zА-Яа-яеЁЇїЄєІіҐґ]{2,25})?', text):
            bot.send_message(message.chat.id, 'Отправьте фамилию\n\n'+
                                             '✅Правильно: Соловьёв, Колодяжный, Gadjzhiev\n' +
                                             '❌Неправильно: Соловьёв1234, Gorsk1y')
            set_state(message, 'Surname')
            set_name(message, text)
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, исправьте ошибки в написании имени\n'+
                                             '✅Правильно: Владислав, Андрей, Artem\n' +
                                             '❌Неправильно: Влад1слав, Andrey2020')
    elif state == "Surname":
        text = message.text
        if re.fullmatch('[A-Za-zА-Яа-яёЁЇїЄєІіҐґ]{2,25}( [A-Za-zА-Яа-яеЁЇїЄєІіҐґ]{2,25})?', text):
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            for kaf in execute_query('select depart_name from depart order by depart_name'):
                markup.row(kaf[0])
            bot.send_message(message.chat.id,
                             'Выберите кафедру\n\n' +
                             '✅Пример: СТ, ПИ, ИУС\n', reply_markup=markup)
            set_state(message, 'kaf')
            set_surname(message, text)
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, исправьте ошибки в написании фамилии\n' +
                                             '✅Правильно: Соловьёв, Колодяжный, Gadjzhiev\n' +
                                             '❌Неправильно: Соловьёв1234, Gorsk1y')
    elif state == 'kaf':
        text = message.text
        result = None
        try:
            result = execute_query("select depart_name from depart where depart_name = ?", [text])
            print(result)
        except:
            pass
        if result is None:
            result = []
        if text in [item[0].upper() for item in result]:
            depart_id = execute_query('select id from depart where depart_name = ?', [text])[0][0]
            execute_query("update user set depart_id = ? where id = ?", [depart_id, int(message.from_user.id)])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            for group in execute_query('select name from group_table order by name'):
                markup.row(group[0])
            bot.send_message(message.chat.id,
                             'Выберите группу\n\n'
                             '✅Пример: ІТКН-18-3, ІТКН-18-4\n', reply_markup=markup)
            set_state(message, 'group')
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            for kaf in execute_query('select depart_name from depart order by depart_name'):
                markup.row(kaf[0])
            bot.send_message(message.chat.id,
                             '⚠Такой кафедры не существует, выберите другую или укажите пункт списка\n' +
                             '✅Пример: СТ, ПИ, ИУС\n', reply_markup=markup)
    elif state == 'group':
        text = message.text
        if text.upper() in [item[0].upper() for item in execute_query("select name from group_table")]:
            names = [(item[0], item[1].upper()) for item in execute_query("select id, name from group_table")]
            group = None
            for i in names:
                if i[1] == text.upper():
                    group = i[0]
                    break
            execute_query("update user set group_id = ? where id = ?", [group, int(message.from_user.id)])
            markup = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Отправьте номер\n\n' +
                             '✅Правильно: +380506213214\n' +
                             '❌Неправильно: 132211аф21кф\n' +
                             '⚠Для пропуска шага отправьте "-"', reply_markup=markup)
            set_state(message, 'Number')
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            for group in execute_query('select name from group_table order by name'):
                markup.row(group[0])
            bot.send_message(message.chat.id,
                             '❌Такой группы не существует. Выберите другую или укажите пункт из списка\n', reply_markup=markup)
    elif state == "Number":
        text = message.text
        rule = re.compile(r'^(?:\+?380)\d{9,13}$')
        if text == '-':
            set_number(message, '+380XXXXXXXXX')
            bot.send_message(message.chat.id, 'Отправьте почту\n\n' +
                             '✅Правильно: slavik.gorskiy@nure.ua\n' +
                             '❌Неправильно: 132211аф21кф.ua\n')
            set_state(message, 'Email')
        elif rule.search(text):
            bot.send_message(message.chat.id, 'Отправьте почту\n\n' +
                             '✅Правильно: slavik.gorskiy@nure.ua\n' +
                             '❌Неправильно: 132211аф21кф.ua\n')
            set_state(message, 'Email')
            set_number(message, text)
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, исправьте ошибки в номере телефона\n' +
                                             '✅Правильно: +380506213214\n' +
                                             '❌Неправильно: 132211аф21кф\n' +
                                            '⚠Для пропуска шага отправьте "-"')
    elif state == "Email":
        text = message.text
        try:
            valid = validate_email(text)
            email = valid.email
            bot.send_message(message.chat.id, '✅Вы прошли регистрацию\n')
            if int(message.from_user.id) == 386150219:
                set_role(message, 'Admin')
            else:
                    set_role(message, 'Student')
            set_state(message, 'Chill')
            set_email(message, email)
        except:
            bot.send_message(message.chat.id, 'Пожалуйста, исправьте ошибки в почте\n' +
                             '✅Правильно: slavik.gorskiy@nure.ua\n' +
                             '❌Неправильно: 132211аф21кф.ua\n')
    elif state == 'add_teacher_reply':
        if message.text == "-":
            bot.send_message(message.chat.id, "✅Действие отменено")
            set_state(message, 'Chill')
        else:
            if message.forward_from is None:
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.row("-")
                bot.send_message(message.chat.id,
                                 '⚠️Перешлите ОДНО сообщение от человека, которого требуется назначить преподавателем. Отправьте "-" для отмены добалвения.', reply_markup = markup)
            else:
                if message.forward_from is not None and in_system(message.forward_from.id):
                    if message.forward_from.id != message.chat.id:
                        if not is_teacher(message.forward_from.id) and get_role_by_id(message.forward_from.id) != 'Admin':
                            set_role_by_id(message.forward_from.id, 'Teacher')
                            bot.send_message(message.chat.id, "✅" + message.forward_from.first_name + " назначен(а) преподавателем\n"
                                                                                                      "Если вы увидели что-то, кроме этого сообщения - не беспокойтесь, причиной этого стало большое количество пересланных сообщений.")
                            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                            markup.row("-")
                            bot.send_message(message.chat.id,
                                             'Перешлите ОДНО сообщение от человека, которого требуется назначить преподавателем.\n⚠️Отправьте "-" для отмены добалвения.', reply_markup = markup)
                            set_state(message, 'add_teacher_reply')
                        else:
                            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                            markup.row("-")
                            bot.send_message(message.chat.id, "❌Данный человек уже является преподавателем или администратором! Отправьте сообщение другого человека. Если вы передумали добавлять преподавателя пропишите отравьте '-'", reply_markup = markup)
                    else:
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                        markup.row("-")
                        bot.send_message(message.chat.id, "❌Вы переслали своё сообщение. Если вы передумали добавлять преподавателя отправьте '-'", reply_markup = markup)
                elif message.forward_from is not None and not in_system(message.forward_from.id):
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    markup.row("-")
                    bot.send_message(message.chat.id, "❌Данный человек не имеет чата со мной. Мы не можем его добавить. Если вы передумали добавлять преподавателя отправьте '-'", reply_markup = markup)
    elif state == 'show_teacher_list':
        text = message.text
        text = text.split(' ')
        if text[0] == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            set_state(message, 'Chill')
        elif len(text) == 4:
            text[2] = text[2][1:]
            if len(text[3]) > 2:
                try:
                    text[3] = int(text[3][1:len(text[3])-1])
                    text = tuple(text)
                    if text in get_teachers_info():
                        data = get_teacher(*text)
                        msg = "Информация по преподавателю\n" \
                              "✅Имя: {}\n" \
                              "✅Фамилия: {}\n" \
                              "✅Аккаунт телеграмм: @{}\n" \
                              "✅Почта: {}\n" \
                              "✅Номер телефона: {}".format(*data[0])
                        bot.send_message(message.chat.id, msg)
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                        markup.row("-")
                        for name, surname, t_id, chat_id in get_teachers_info():
                            markup.row("{} {} @{} ({})".format(name, surname, t_id, chat_id))
                        bot.send_message(message.chat.id,
                                         'Укажите преподавателя из списка ниже\n' +
                                         '⚠ Отправьте "-" для отмены.',
                                         reply_markup=markup)
                        set_state(message, 'show_teacher_list')
                    else:
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                        markup.row("-")
                        for name, surname, t_id, chat_id in get_teachers_info():
                            markup.row("{} {} @{} ({})".format(name, surname, t_id, chat_id))
                        bot.send_message(message.chat.id, "❌У нас нет такого преподавателя.")
                        bot.send_message(message.chat.id,
                                         'Укажите другого преподавателя\n' +
                                         '⚠ Отправьте "-" для отмены.',
                                         reply_markup=markup)
                except Exception as ex:
                    print(ex)
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    markup.row("-")
                    for name, surname, t_id, chat_id in get_teachers_info():
                        markup.row("{} {} @{} ({})".format(name, surname, t_id, chat_id))
                    bot.send_message(message.chat.id, "❌У нас нет такого преподавателя.")
                    bot.send_message(message.chat.id,
                                     'Укажите другого преподавателя\n' +
                                     '⚠ Отправьте "-" для отмены.',
                                     reply_markup=markup)
            else:
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.row("-")
                for name, surname, t_id, chat_id in get_teachers_info():
                    markup.row("{} {} @{} ({})".format(name, surname, t_id, chat_id))
                bot.send_message(message.chat.id, "❌У нас нет такого преподавателя.")
                bot.send_message(message.chat.id,
                                 'Укажите другого преподавателя\n' +
                                 '⚠ Отправьте "-" для отмены.',
                                 reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            for name, surname, t_id, chat_id in get_teachers_info():
                markup.row("{} {} @{} ({})".format(name, surname, t_id, chat_id))
            bot.send_message(message.chat.id, "❌У нас нет такого преподавателя.")
            bot.send_message(message.chat.id,
                             'Укажите другого преподавателя\n'+
                             '⚠ Отправьте "-" для отмены.',
            reply_markup = markup)
    elif state == 'change_user_start':
        text = message.text
        text = text.split(' ')
        if text[0] == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            set_state(message, 'Chill')
        elif len(text) == 6:
            text[4] = text[4][1:]
            if len(text[5]) > 2:
                try:
                    text[5] = int(text[5][1:len(text[5]) - 1])
                    del text[1]
                    text = tuple(text)
                    if text in get_users_info() and text[0] != 'NRG':
                        set_state(message, 'change_user_answer')
                        set_additional_data(message, text[4])
                        data = get_user(text[4])
                        msg = "Информация пользователя\n" \
                              "✅Имя: {}\n" \
                              "✅Фамилия: {}\n" \
                              "✅Аккаунт телеграмм: @{}\n" \
                              "✅Номер телефона: {}\n" \
                              "✅Почта: {}".format(*data[0])
                        bot.send_message(message.chat.id, msg)
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                        markup.row("Имя", "Фамилия", "@id")
                        markup.row("Номер телефона", "Электронная почта")
                        markup.row("-")
                        bot.send_message(message.chat.id, 'Укажите пункт для изменения\n' +
                                                          '⚠ Отправьте "-" для отмены.', reply_markup=markup)
                    else:
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                        markup.row("-")
                        for role, name, surname, t_id, chat_id in get_users_info():
                            if role != 'NRG':
                                markup.row("{} | {} {} @{} ({})".format(role, name, surname, t_id, chat_id))
                        bot.send_message(message.chat.id, "❌У нас нет такого пользователя.")
                        bot.send_message(message.chat.id,
                                         'Укажите другого пользователя\n' +
                                         '⚠ Отправьте "-" для отмены.',
                                         reply_markup=markup)
                except Exception as ex:
                    print(ex)
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    markup.row("-")
                    for role, name, surname, t_id, chat_id in get_users_info():
                        if role != 'NRG':
                            markup.row("{} | {} {} @{} ({})".format(role, name, surname, t_id, chat_id))
                    bot.send_message(message.chat.id, "❌У нас нет такого пользователя.")
                    bot.send_message(message.chat.id,
                                     'Укажите другого пользователя\n' +
                                     '⚠ Отправьте "-" для отмены.',
                                     reply_markup=markup)
            else:
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.row("-")
                for role, name, surname, t_id, chat_id in get_users_info():
                    markup.row("{} | {} {} @{} ({})".format(role, name, surname, t_id, chat_id))
                bot.send_message(message.chat.id, "❌У нас нет такого пользователя.")
                bot.send_message(message.chat.id,
                                 'Укажите другого пользователя\n' +
                                 '⚠ Отправьте "-" для отмены.',
                                 reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            for role, name, surname, t_id, chat_id in get_users_info():
                markup.row("{} | {} {} @{} ({})".format(role, name, surname, t_id, chat_id))
            bot.send_message(message.chat.id, "❌У нас нет такого пользователя.")
            bot.send_message(message.chat.id,
                             'Укажите другого пользователя\n' +
                             '⚠ Отправьте "-" для отмены.',
                             reply_markup=markup)
    elif state == 'change_user_answer':
        if message.text == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            del_additional_data(message)
            set_state(message, 'change_user_start')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            for role, name, surname, t_id, chat_id in get_users_info():
                if role != 'NRG':
                    markup.row("{} | {} {} @{} ({})".format(role, name, surname, t_id, chat_id))
            bot.send_message(message.chat.id,
                             'Укажите пользователя из списка ниже\n' +
                             '⚠ Отправьте "-" для отмены.',
                             reply_markup=markup)
        elif (message.text).upper() == 'ИМЯ':
            set_state(message, 'change_user_name')
            data = execute_query('select name from user where id = ?', [get_additional_data(message)[0]])[0][0]
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            bot.send_message(message.chat.id, "ℹСтарое имя пользователя: {}\n".format(data)+
                             "Отправьте новое имя\n" +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
        elif (message.text).upper()  == 'ФАМИЛИЯ':
            set_state(message, 'change_user_surname')
            data = execute_query('select surname from user where id = ?', [get_additional_data(message)[0]])[0][0]
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            bot.send_message(message.chat.id, "ℹСтарая фамилия пользователя: {}\n".format(data)+
                             "Отправьте новую фамилию\n" +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
        elif (message.text).upper()  == '@ID':
            set_state(message, 'change_user_telegram')
            data = execute_query('select telegram_id from user where id = ?', [get_additional_data(message)[0]])[0][0]
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            bot.send_message(message.chat.id, "ℹСтарая ссылка на телеграмм пользователя: @{}\n".format(data)+
                             "Отправьте новую ссылку\n" +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
        elif (message.text).upper()  == 'НОМЕР ТЕЛЕФОНА':
            set_state(message, 'change_user_telno')
            data = execute_query('select tel_no from user where id = ?', [get_additional_data(message)[0]])[0][0]
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            bot.send_message(message.chat.id, "ℹСтарый номер телефона пользователя: {}\n".format(data)+
                             "Отправьте новый номер\n" +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
        elif (message.text).upper()  == 'ЭЛЕКТРОННАЯ ПОЧТА':
            set_state(message, 'change_user_email')
            data = execute_query('select email from user where id = ?', [get_additional_data(message)[0]])[0][0]
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            bot.send_message(message.chat.id, "ℹСтарая почта пользователя: {}\n".format(data)+
                             "Отправьте новую почту\n" +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Номер телефона", "Электронная почта")
            markup.row("-")
            bot.send_message(message.chat.id,
                             'Неправильный пункт! Укажите пункт из списка ниже\n' +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
    elif state == 'change_user_name':
        text = message.text
        if text == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            set_state(message, 'change_user_answer')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Номер телефона", "Электронная почта")
            markup.row("-")
            bot.send_message(message.chat.id,
                             'Укажите пункт для изменения\n' +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
        elif re.fullmatch('[A-Za-zА-Яа-яёЁЇїЄєІіҐґ]{2,25}( [A-Za-zА-Яа-яеЁЇїЄєІіҐґ]{2,25})?', text):
            id = int(get_additional_data(message)[0])
            execute_query("update user set name = ? where id = ?", [text, id])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Номер телефона", "Электронная почта")
            markup.row("-")
            bot.send_message(message.chat.id,
                             '✅Имя записано! Укажите пункт для изменения\n' +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
            set_state(message, 'change_user_answer')
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, исправьте ошибки в написании имени\n' +
                             '✅Правильно: Владислав, Андрей, Artem\n' +
                             '❌Неправильно: Влад1слав, Andrey2020')
    elif state == 'change_user_surname':
        text = message.text
        if text == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            set_state(message, 'change_user_answer')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Номер телефона", "Электронная почта")
            markup.row("-")
            bot.send_message(message.chat.id,
                             'Укажите пункт для изменения\n' +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
        elif re.fullmatch('[A-Za-zА-Яа-яёЁЇїЄєІіҐґ]{2,25}( [A-Za-zА-Яа-яеЁЇїЄєІіҐґ]{2,25})?', text):
            id = int(get_additional_data(message)[0])
            execute_query("update user set surname = ? where id = ?", [text, id])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Номер телефона", "Электронная почта")
            markup.row("-")
            bot.send_message(message.chat.id,
                             '✅Фамилия записана! Укажите пункт для изменения\n' +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
            set_state(message, 'change_user_answer')
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, исправьте ошибки в написании фамилии\n' +
                             '✅Правильно: Соловьёв, Колодяжный, Gadjzhiev\n' +
                             '❌Неправильно: Соловьёв1234, Gorsk1y')
    elif state == 'change_user_telegram':
        text = message.text
        if text == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            set_state(message, 'change_user_answer')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Номер телефона", "Электронная почта")
            markup.row("-")
            bot.send_message(message.chat.id,
                             'Укажите пункт для изменения\n' +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
        elif len(text.split(' ')) == 1 and text[0] == '@' and re.fullmatch('[A-Za-z0-9_]{2,25}?', text[1:]) and len(text) >= 6:
            id = int(get_additional_data(message)[0])
            execute_query("update user set telegram_id = ? where id = ?", [text[1:], id])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Номер телефона", "Электронная почта")
            markup.row("-")
            bot.send_message(message.chat.id,
                             '✅Ссылка записана! Укажите пункт для изменения\n' +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
            set_state(message, 'change_user_answer')
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, исправьте ошибки в написании ссылки\n' +
                             '✅Правильно: @the_fenrir, @nure_ua, @darude\n' +
                             '❌Неправильно: link231, https')
    elif state == 'change_user_telno':
        text = message.text
        rule = re.compile(r'^(?:\+?380)\d{9,13}$')
        if text == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            set_state(message, 'change_user_answer')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Номер телефона", "Электронная почта")
            markup.row("-")
            bot.send_message(message.chat.id,
                             'Укажите пункт для изменения\n' +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
        elif rule.search(text):
            id = int(get_additional_data(message)[0])
            execute_query("update user set tel_no = ? where id = ?", [text, id])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Номер телефона", "Электронная почта")
            markup.row("-")
            bot.send_message(message.chat.id,
                             '✅Номер телефона записан! Укажите пункт для изменения\n' +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
            set_state(message, 'change_user_answer')
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, исправьте ошибки в номере телефона\n' +
                             '✅Правильно: +380506213214\n' +
                             '❌Неправильно: 132211аф21кф\n' +
                             'Для пропуска шага отправьте "-"')
    elif state == 'change_user_email':
        text = message.text
        if text == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            set_state(message, 'change_user_answer')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Номер телефона", "Электронная почта")
            markup.row("-")
            bot.send_message(message.chat.id,
                             'Укажите пункт для изменения\n' +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
        else:
            try:
                valid = validate_email(text)
                email = valid.email
                id = int(get_additional_data(message)[0])
                execute_query("update user set email = ? where id = ?", [email, id])
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.row("Имя", "Фамилия", "@id")
                markup.row("Номер телефона", "Электронная почта")
                markup.row("-")
                bot.send_message(message.chat.id,
                                 '✅Почта записана! Укажите пункт для изменения\n' +
                                 '⚠ Отправьте "-" для отмены.', reply_markup=markup)
                set_state(message, 'change_user_answer')
            except:
                bot.send_message(message.chat.id, 'Пожалуйста, исправьте ошибки в почте\n' +
                                 '✅Правильно: slavik.gorskiy@nure.ua\n' +
                                 '❌Неправильно: 132211аф21кф.ua\n')
    elif state == 'edit_myself':
        text = message.text
        if text == "-":
            bot.send_message(message.chat.id, "✅Действие отменено")
            set_state(message, 'Chill')
        elif text.upper() == "ИМЯ":
            data = execute_query('select name from user where id = ?', [int(message.from_user.id)])[0][0]
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            bot.send_message(message.chat.id, "ℹВаше старое имя: {}\n".format(data) +
                             "Отправьте новое имя\n" +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
            set_state(message, 'change_self_name')
        elif text.upper() == "ФАМИЛИЯ":
            data = execute_query('select surname from user where id = ?', [int(message.from_user.id)])[0][0]
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            bot.send_message(message.chat.id, "ℹВаша старая фамилия: {}\n".format(data) +
                             "Отправьте новую фамилию\n" +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
            set_state(message, 'change_self_surname')
        elif text.upper() == "@ID":
            data = execute_query('select telegram_id from user where id = ?', [int(message.from_user.id)])[0][0]
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            bot.send_message(message.chat.id, "ℹВаша старая ссылка в телеграмм: @{}\n".format(data) +
                             "Отправьте новую ссылку\n" +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
            set_state(message, 'change_self_link')
        elif text.upper() == 'EMAIL':
            data = execute_query('select email from user where id = ?', [int(message.from_user.id)])[0][0]
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            bot.send_message(message.chat.id, "ℹВаша старая почта: {}\n".format(data) +
                             "Отправьте новую почту\n" +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
            set_state(message, 'change_self_email')
        elif text.upper() == 'НОМЕР ТЕЛЕФОНА':
            data = execute_query('select tel_no from user where id = ?', [int(message.from_user.id)])[0][0]
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            bot.send_message(message.chat.id, "ℹВаша старый номер телефона: {}\n".format(data) +
                             "Отправьте новый номер\n" +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
            set_state(message, 'change_self_telno')
        elif text.upper() == 'КАФЕДРА':
            data = execute_query('select depart_name from user join depart on depart_id = depart.id where user.id = ?', [int(message.from_user.id)])[0][0]
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            for kaf in execute_query('select depart_name from depart order by depart_name'):
                markup.row(kaf[0])
            bot.send_message(message.chat.id, "ℹВаша старая кафедра: {}\n".format(data) +
                             "Укажите новую кафедру\n" +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
            set_state(message, 'change_self_kaf')
        elif text.upper() == 'ГРУППА':
            data = execute_query('select group_table.name from user join group_table on group_id = group_table.id where user.id = ?', [int(message.from_user.id)])[0][0]
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            for group in execute_query('select name from group_table order by name'):
                markup.row(group[0])
            bot.send_message(message.chat.id, "ℹВаша старая группа: {}\n".format(data) +
                             "Укажите новую группу\n" +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
            set_state(message, 'change_self_group')
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Email", "Номер телефона", "Кафедра")
            markup.row("Группа")
            markup.row("-")
            bot.send_message(message.chat.id,
                             '❌Неправильный пункт. Укажите другой пункт для изменения\n⚠Отправьте "-" для отмены',
                             reply_markup=markup)
    elif state == 'change_self_name':
        text = message.text
        if text == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Email", "Номер телефона", "Кафедра")
            markup.row("Группа")
            markup.row("-")
            bot.send_message(message.chat.id,
                             'Укажите пункт для изменения\n⚠Отправьте "-" для отмены добалвения.',
                             reply_markup=markup)
            set_state(message, 'edit_myself')
        elif re.fullmatch('[A-Za-zА-Яа-яёЁЇїЄєІіҐґ]{2,25}( [A-Za-zА-Яа-яеЁЇїЄєІіҐґ]{2,25})?', text):
            id = int(message.from_user.id)
            execute_query("update user set name = ? where id = ?", [text, id])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Email", "Номер телефона", "Кафедра")
            markup.row("Группа")
            markup.row("-")
            bot.send_message(message.chat.id,
                             '✅Имя записано! Укажите пункт для изменения\n' +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
            set_state(message, 'edit_myself')
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, исправьте ошибки в написании имени\n' +
                             '✅Правильно: Владислав, Андрей, Artem\n' +
                             '❌Неправильно: Влад1слав, Andrey2020')
    elif state == 'change_self_surname':
        text = message.text
        if text == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Email", "Номер телефона", "Кафедра")
            markup.row("Группа")
            markup.row("-")
            bot.send_message(message.chat.id,
                             'Укажите пункт для изменения\n⚠Отправьте "-" для отмены добалвения.',
                             reply_markup=markup)
            set_state(message, 'edit_myself')
        elif re.fullmatch('[A-Za-zА-Яа-яёЁЇїЄєІіҐґ]{2,25}( [A-Za-zА-Яа-яеЁЇїЄєІіҐґ]{2,25})?', text):
            id = int(message.from_user.id)
            execute_query("update user set surname = ? where id = ?", [text, id])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Email", "Номер телефона", "Кафедра")
            markup.row("Группа")
            markup.row("-")
            bot.send_message(message.chat.id,
                             '✅Фамилия записана! Укажите пункт для изменения\n' +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
            set_state(message, 'edit_myself')
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, исправьте ошибки в написании фамилии\n' +
                             '✅Правильно: Соловьёв, Колодяжный, Gadjzhiev\n' +
                             '❌Неправильно: Соловьёв1234, Gorsk1y')
    elif state == 'change_self_link':
        text = message.text
        if text == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Email", "Номер телефона", "Кафедра")
            markup.row("Группа")
            markup.row("-")
            bot.send_message(message.chat.id,
                             'Укажите пункт для изменения\n⚠Отправьте "-" для отмены добалвения.',
                             reply_markup=markup)
            set_state(message, 'edit_myself')
        elif len(text.split(' ')) == 1 and text[0] == '@' and re.fullmatch('[A-Za-z0-9_]{2,25}?', text[1:]) and len(text) >= 6:
            id = int(message.from_user.id)
            execute_query("update user set telegram_id = ? where id = ?", [text[1:], id])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Email", "Номер телефона", "Кафедра")
            markup.row("Группа")
            markup.row("-")
            bot.send_message(message.chat.id,
                             '✅Ссылка записана! Укажите пункт для изменения\n' +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
            set_state(message, 'edit_myself')
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, исправьте ошибки в написании ссылки\n' +
                             '✅Правильно: @the_fenrir, @nure_ua, @darude\n' +
                             '❌Неправильно: link231, https')
    elif state == 'change_self_email':
        text = message.text
        if text == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Email", "Номер телефона", "Кафедра")
            markup.row("Группа")
            markup.row("-")
            bot.send_message(message.chat.id,
                             'Укажите пункт для изменения\n⚠Отправьте "-" для отмены добалвения.',
                             reply_markup=markup)
            set_state(message, 'edit_myself')
        else:
            try:
                valid = validate_email(text)
                email = valid.email
                id = int(message.from_user.id)
                execute_query("update user set email = ? where id = ?", [email, id])
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.row("Имя", "Фамилия", "@id")
                markup.row("Email", "Номер телефона", "Кафедра")
                markup.row("Группа")
                markup.row("-")
                bot.send_message(message.chat.id,
                                 '✅Почта записана! Укажите пункт для изменения\n' +
                                 '⚠Отправьте "-" для отмены.', reply_markup=markup)
                set_state(message, 'edit_myself')
            except:
                bot.send_message(message.chat.id, 'Пожалуйста, исправьте ошибки в почте\n' +
                                 '✅Правильно: slavik.gorskiy@nure.ua\n' +
                                 '❌Неправильно: 132211аф21кф.ua\n')
    elif state == 'change_self_telno':
        text = message.text
        rule = re.compile(r'^(?:\+?380)\d{9,13}$')
        if text == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Email", "Номер телефона", "Кафедра")
            markup.row("Группа")
            markup.row("-")
            bot.send_message(message.chat.id,
                             'Укажите пункт для изменения\n⚠Отправьте "-" для отмены добалвения.',
                             reply_markup=markup)
            set_state(message, 'edit_myself')
        elif rule.search(text):
            id = int(message.from_user.id)
            execute_query("update user set tel_no = ? where id = ?", [text, id])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Email", "Номер телефона", "Кафедра")
            markup.row("Группа")
            markup.row("-")
            bot.send_message(message.chat.id,
                             '✅Номер телефона записан! Укажите пункт для изменения\n' +
                             '⚠ Отправьте "-" для отмены.', reply_markup=markup)
            set_state(message, 'edit_myself')
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, исправьте ошибки в номере телефона\n' +
                             '✅Правильно: +380506213214\n' +
                             '❌Неправильно: 132211аф21кф\n' +
                             'Для пропуска шага отправьте "-"')
    elif state == 'change_self_kaf':
        text = message.text
        if text == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Email", "Номер телефона", "Кафедра")
            markup.row("Группа")
            markup.row("-")
            bot.send_message(message.chat.id,
                             'Укажите пункт для изменения\n⚠Отправьте "-" для выхода.',
                             reply_markup=markup)
            set_state(message, 'edit_myself')
        elif text in [item[0].upper() for item in execute_query("select depart_name from depart")]:
            depart_id = execute_query('select id from depart where depart_name = ?', [text])[0][0]
            execute_query("update user set depart_id = ? where id = ?", [depart_id, int(message.from_user.id)])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Email", "Номер телефона", "Кафедра")
            markup.row("Группа")
            markup.row("-")
            bot.send_message(message.chat.id,
                             '✅Кафедра записана\nУкажите пункт для изменения\n⚠Отправьте "-" для выхода.', reply_markup=markup)
            set_state(message, 'edit_myself')
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            for kaf in execute_query('select depart_name from depart order by depart_name'):
                markup.row(kaf[0])
            bot.send_message(message.chat.id,
                             '⚠Такой кафедры не существует, перепроверьте написание или выберите её из списка\n' +
                             '✅Пример: СТ, ПИ, ИУС\n' +
                             'Для пропуска шага отправьте "-"', reply_markup=markup)
    elif state == 'change_self_group':
        text = message.text
        if text == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Email", "Номер телефона", "Кафедра")
            markup.row("Группа")
            markup.row("-")
            bot.send_message(message.chat.id,
                             'Укажите пункт для изменения\n⚠Отправьте "-" для выхода.',
                             reply_markup=markup)
            set_state(message, 'edit_myself')
        elif text.upper() in [item[0].upper() for item in execute_query("select name from group_table")]:
            names = [(item[0], item[1].upper()) for item in execute_query("select id, name from group_table")]
            group = None
            for i in names:
                if i[1] == text.upper():
                    group = i[0]
                    break
            execute_query("update user set group_id = ? where id = ?", [group, int(message.from_user.id)])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Email", "Номер телефона", "Кафедра")
            markup.row("Группа")
            markup.row("-")
            bot.send_message(message.chat.id,
                             '✅Группа записана\nУкажите пункт для изменения\n⚠Отправьте "-" для выхода.', reply_markup=markup)
            set_state(message, 'edit_myself')
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            for group in execute_query('select name from group_table order by name'):
                markup.row(group[0])
            bot.send_message(message.chat.id,
                             '❌Такой группы не существует. Выберите другую группу\n' +
                             'Для пропуска шага отправьте "-"', reply_markup=markup)
    elif state == 'del_teacher_start':
        text = message.text
        text = text.split(' ')
        if text[0] == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            set_state(message, 'Chill')
        elif len(text) == 4:
            text[2] = text[2][1:]
            if len(text[3]) > 2:
                try:
                    text[3] = int(text[3][1:len(text[3]) - 1])
                    text = tuple(text)
                    if text in get_teachers_info():
                        data = get_teacher(*text)
                        msg = ''
                        msg += "Информация по преподавателю\n" \
                              "✅Имя: {}\n" \
                              "✅Фамилия: {}\n" \
                              "✅Аккаунт телеграмм: @{}\n" \
                              "✅Почта: {}\n" \
                              "✅Номер телефона: {}".format(*data[0])
                        bot.send_message(message.chat.id, msg)
                        set_additional_data(message, text[3])
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                        markup.row("Да", "Нет")
                        set_state(message, 'del_teacher_submit')
                        bot.send_message(message.chat.id, '⚠⚠⚠Вы действительно хотите удалить преподавателя? (Да/Нет) ', reply_markup=markup)
                    else:
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                        markup.row("-")
                        for name, surname, t_id, chat_id in get_teachers_info():
                            markup.row("{} {} @{} ({})".format(name, surname, t_id, chat_id))
                        bot.send_message(message.chat.id, "❌У нас нет такого преподавателя.")
                        bot.send_message(message.chat.id,
                                         'Укажите другого преподавателя\n' +
                                         '⚠ Отправьте "-" для отмены.',
                                         reply_markup=markup)
                except Exception as ex:
                    print(ex)
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    markup.row("-")
                    for name, surname, t_id, chat_id in get_teachers_info():
                        markup.row("{} {} @{} ({})".format(name, surname, t_id, chat_id))
                    bot.send_message(message.chat.id, "❌У нас нет такого преподавателя.")
                    bot.send_message(message.chat.id,
                                     'Укажите другого преподавателя\n' +
                                     '⚠ Отправьте "-" для отмены.',
                                     reply_markup=markup)
            else:
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.row("-")
                for name, surname, t_id, chat_id in get_teachers_info():
                    markup.row("{} {} @{} ({})".format(name, surname, t_id, chat_id))
                bot.send_message(message.chat.id, "❌У нас нет такого преподавателя.")
                bot.send_message(message.chat.id,
                                 'Укажите другого преподавателя\n' +
                                 '⚠ Отправьте "-" для отмены.',
                                 reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            for name, surname, t_id, chat_id in get_teachers_info():
                markup.row("{} {} @{} ({})".format(name, surname, t_id, chat_id))
            bot.send_message(message.chat.id, "❌У нас нет такого преподавателя.")
            bot.send_message(message.chat.id,
                             'Укажите другого преподавателя\n' +
                             '⚠ Отправьте "-" для отмены.',
                             reply_markup=markup)
    elif state == 'del_teacher_submit':
        text = message.text
        if text.upper() == "ДА":
            id = int(get_additional_data(message)[0])
            set_role_by_id(id, 'Student')
            bot.send_message(message.chat.id, '✅Вы выбрали "да", преподаватель удалён, хотите удалить кого-то ещё?')
            set_state(message, 'del_teacher_start')
            del_additional_data(message)
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            for name, surname, t_id, chat_id in get_teachers_info():
                markup.row("{} {} @{} ({})".format(name, surname, t_id, chat_id))
            bot.send_message(message.chat.id,
                             'Список преподавателей показан ниже, если вы хотите удалить одного из них, нажмите на него.\n' +
                             '⚠ Отправьте "-" для отмены.',
                             reply_markup=markup)
        elif text.upper() == "НЕТ":
            bot.send_message(message.chat.id, '✅Вы выбрали "нет", хотите удалить кого-то другого?')
            set_state(message, 'del_teacher_start')
            del_additional_data(message)
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            for name, surname, t_id, chat_id in get_teachers_info():
                markup.row("{} {} @{} ({})".format(name, surname, t_id, chat_id))
            bot.send_message(message.chat.id,
                             'Список преподавателей показан ниже, если вы хотите удалить одного из них, нажмите на него.\n' +
                             '⚠ Отправьте "-" для отмены.',
                             reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Да", "Нет")
            set_state(message, 'del_teacher_submit')
            bot.send_message(message.chat.id, '⚠⚠⚠Вы действительно хотите удалить преподавателя? (Да/Нет) ',
                             reply_markup=markup)
    elif state == 'add_course_name':
        text = message.text
        if text == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            set_state(message, 'Chill')
        elif all([re.fullmatch('[A-Za-zА-Яа-яёЁЇїЄєІіҐґ]{1,25}', i) for i in text.split(' ')]) and text != 'Недоступно':
            id = str(datetime.datetime.now())
            id = id.split(' ')
            id = '_'.join(id)
            execute_query('insert into course(id, name) values (?, ?)', [id, text])
            set_additional_data(message, id)
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            for group in execute_query('select name from group_table order by name'):
                markup.row(group[0])
            bot.send_message(message.chat.id,
                             '✅Название курса сохранено!\nℹВыберите группы для добавления в курс или напишите их в чат.\n' +
                             '⚠Этот шаг обязательный', reply_markup=markup)
            depart_id = execute_query('select depart_id from user where id = ?', [message.from_user.id])[0][0]
            execute_query('update course set depart_id = ? where id = ?', [depart_id, get_additional_data(message)[0]])
            set_state(message, 'add_course_groups')
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            bot.send_message(message.chat.id, 'Исправьте ошибки в написании курса (запрещённые символы &%$#)\n' +
                             '✅Пример: Методы оптимизации и исследования операций\n' +
                             '✅Пример: Дискретная математика\n' +
                             '⚠Отправьте "-" для отмены.', reply_markup=markup)
    elif state == 'add_course_groups':
        text = message.text
        if text == '+':
            groups = \
            execute_query('select count(*) from course_group where course_id = ?', [get_additional_data(message)][0])[
                0][0]
            if groups == 0:
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                for group in execute_query('select name from group_table order by name'):
                    markup.row(group[0])
                bot.send_message(message.chat.id,
                                 '❌Вы не добавили ни одной группы. Выберите группу из списка или напишите её в чат.\n' +
                                 '⚠Этот шаг обязательный', reply_markup=markup)
            else:
                markup = types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id,
                                 '✅Группы записаны\nℹНапишите количество кредитов для курса (1 число)\n' +
                                 '✅Правильно: 4\n' +
                                 '❌Неправильно: аф\n' +
                                 '⚠Этот шаг обязательный', reply_markup=markup)
                set_state(message, 'add_course_credits')
        elif text.upper() in [item[0].upper() for item in execute_query("select name from group_table")]:
            names = [(item[0], item[1].upper()) for item in execute_query("select id, name from group_table")]
            group = None
            for i in names:
                if i[1] == text.upper():
                    group = i[0]
                    break
            if (group,) not in execute_query('select group_id from course_group where course_id = ?',
                                             [get_additional_data(message)[0]]):
                execute_query('insert into course_group(course_id, group_id) values (?, ?)',
                              [get_additional_data(message)[0], group])
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.row("+")
                for group in execute_query('select name from group_table order by name'):
                    markup.row(group[0])
                bot.send_message(message.chat.id,
                                 '✅Группа добавлена. \n' +
                                 'ℹУкажите ещё одну группу или выберите её из списка\n' +
                                 '⚠Если вы уверены что добавили все группы, отправьте "+"', reply_markup=markup)
            else:
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.row("+")
                for group in execute_query('select name from group_table order by name'):
                    markup.row(group[0])
                bot.send_message(message.chat.id,
                                 '❌Группа уже была добавлена. \n' +
                                 'ℹЕсли хотите добавить другую группу, выберите её из списка или напишите в чат.\n' +
                                 '⚠Если вы уверены что добавили все группы, отправьте "+"', reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("+")
            for group in execute_query('select name from group_table order by name'):
                markup.row(group[0])
            bot.send_message(message.chat.id,
                             '❌Такой группы не существует. Выберите группу которую хотите добавить в курс из списка ниже или напишите её в чат.\n' +
                             '⚠Этот шаг обязательный', reply_markup=markup)
    elif state == 'add_course_credits':
        text = message.text
        check = True
        data = None
        if len(text.split(' ')) != 1:
            check = False
        if check is not False:
            try:
                data = int(text)
            except Exception:
                data = None
                check = False
        if data is not None:
            check = data >= 0
        if check and text != 'Недоступно':
            execute_query('update course set practical_n = ?, labs_n = ?, lections_n = ?, credits = ? where id = ?',
                          [0, 0, 0, data, get_additional_data(message)[0]])
            bot.send_message(message.chat.id,
                             '✅Информация сохранена. Осталось совсем немного! Отправьте описание курса (длинна не более 2000 символов)\n' +
                             '⚠Этот шаг обязательный')
            set_state(message, 'add_course_description')
        else:
            bot.send_message(message.chat.id,
                             '⚠Вы допустили ошибку. Введите одно число (кол-во кредитов)\n' +
                             '✅Правильно:  4\n' +
                             '❌Неправильно: -18 аф')
    elif state == 'add_course_description':
        text = message.text
        if len(text) > 2000:
            bot.send_message(message.chat.id,
                             '❌Описание слишком длинное, опишите курс немного короче (до 2000 символов)')
        elif text != 'Недоступно':
            execute_query('update course set description = ? where id = ?', [text, get_additional_data(message)[0]])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            data_set = execute_query(
                'select name, depart_name, practical_n, lections_n, labs_n, credits, description from course join depart on course.depart_id = depart.id where course.id = ?',
                [get_additional_data(message)[0]])[0]
            groups = [item[0] for item in execute_query(
                'select name from group_table join course_group on group_table.id = course_group.group_id where course_id = ?',
                [get_additional_data(message)[0]])]
            del_additional_data(message)
            bot.send_message(message.chat.id, 'ℹНазвание курса: {}\n' \
                                              'ℹКафедра которая преподаёт курс: {}\n' \
                                              'ℹКол-во практических занятий: {}\n' \
                                              'ℹКол-во лекционных занятий: {}\n' \
                                              'ℹКол-во лабораторных занятий: {}\n' \
                                              'ℹКол-во кредитов курса: {}\n'.format(*data_set[:6]) +
                             'ℹГруппы прикреплённые к курсу: ' + ', '.join(
                groups) + '\n' + 'ℹОписание курса: {}\n'.format(data_set[6]), reply_markup=markup)
            bot.send_message(message.chat.id, 'Если хотите добавить ещё один курс, отправьте название\n' +
                             '✅Пример: Методы оптимизации и исследования операций\n' +
                             '✅Пример: Дискретная математика\n' +
                             '⚠Отправьте "-" для отмены.', reply_markup=markup)
            set_state(message, 'add_course_name')
        else:
            bot.send_message(message.chat.id,
                             '❌Запрещённое описание')
    elif state == 'watch_course_choise':
        text = message.text
        text = text.split(' ')
        if text[0] == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            set_state(message, 'Chill')
        else:
            try:
                text[0] = text[0][1:len(text[0]) - 1]
                if text[0] == execute_query(
                        'select id from course where id = ? and description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"',
                        [text[0]])[0][0]:
                    data = None
                    data_set = execute_query(
                        'select name, depart_name, practical_n, lections_n, labs_n, credits, description from course join depart on course.depart_id = depart.id where course.id = ?',
                        [text[0]])[0]
                    groups = [item[0] for item in execute_query(
                        'select name from group_table join course_group on group_table.id = course_group.group_id where course_id = ?',
                        [text[0]])]
                    if get_role(message) == 'Admin':
                        data = execute_query(
                            'select id, name from course where description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"')
                        bot.send_message(message.chat.id, 'ℹНазвание курса: {}\n' \
                                                          'ℹКафедра которая преподаёт курс: {}\n' \
                                                          'ℹКол-во практических занятий: {}\n' \
                                                          'ℹКол-во лекционных занятий: {}\n' \
                                                          'ℹКол-во лабораторных занятий: {}\n' \
                                                          'ℹКол-во кредитов курса: {}\n'.format(*data_set[:6]) +
                                         'ℹГруппы прикреплённые к курсу: ' + ', '.join(
                            groups) + '\n' + 'ℹОписание курса: {}\n'.format(data_set[6]))
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                        markup.row("-")
                        for id, name in data:
                            markup.row("({}) {}".format(id, name))
                        bot.send_message(message.chat.id,
                                         'Выберите курс, список показан ниже\n' +
                                         '⚠ Отправьте "-" для отмены.',
                                         reply_markup=markup)
                    elif get_role(message) == 'Teacher':
                        depart = \
                        execute_query('select depart_id from user where id = ?', [int(message.from_user.id)])[0][0]
                        data = execute_query(
                            'select id, name from course where depart_id = ? and description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"',
                            [depart])
                        if (text[0],) in execute_query('select id from course where depart_id = ?', [depart]):
                            bot.send_message(message.chat.id, 'ℹНазвание курса: {}\n' \
                                                              'ℹКафедра которая преподаёт курс: {}\n' \
                                                              'ℹКол-во практических занятий: {}\n' \
                                                              'ℹКол-во лекционных занятий: {}\n' \
                                                              'ℹКол-во лабораторных занятий: {}\n' \
                                                              'ℹКол-во кредитов курса: {}\n'.format(*data_set[:6]) +
                                             'ℹГруппы прикреплённые к курсу: ' + ', '.join(
                                groups) + '\n' + 'ℹОписание курса: {}\n'.format(data_set[6]))
                        else:
                            bot.send_message(message.chat.id, '❌Курс создан преподавателем другой кафедры.\n')
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                        markup.row("-")
                        for id, name in data:
                            markup.row("({}) {}".format(id, name))
                        bot.send_message(message.chat.id,
                                         'Если вы хотите узнать информацию ещё по одному курсу, выберите его из списка.\n' +
                                         '⚠ Отправьте "-" для отмены.',
                                         reply_markup=markup)

                    elif get_role(message) == 'Student':
                        group = execute_query('select group_id from user where id = ?', [int(message.from_user.id)])[0][
                            0]
                        data = execute_query(
                            'select id, name from course join course_group on id = course_id where group_id = ? and description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"',
                            [group])
                        if (text[0],) in execute_query(
                                'select id from course join course_group on id = course_id where group_id = ?',
                                [group]):
                            bot.send_message(message.chat.id, 'ℹНазвание курса: {}\n' \
                                                              'ℹКафедра которая преподаёт курс: {}\n' \
                                                              'ℹКол-во практических занятий: {}\n' \
                                                              'ℹКол-во лекционных занятий: {}\n' \
                                                              'ℹКол-во лабораторных занятий: {}\n' \
                                                              'ℹКол-во кредитов курса: {}\n'.format(*data_set[:6]) +
                                             'ℹГруппы прикреплённые к курсу: ' + ', '.join(
                                groups) + '\n' + 'ℹОписание курса: {}\n'.format(data_set[6]))
                        else:
                            bot.send_message(message.chat.id, '❌Ваша группа не прикреплена к курсу.\n')
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                        markup.row("-")
                        for id, name in data:
                            markup.row("({}) {}".format(id, name))
                        bot.send_message(message.chat.id,
                                         'Если вы хотите узнать информацию ещё по одному курсу, выберите его из списка.\n' +
                                         '⚠ Отправьте "-" для отмены.',
                                         reply_markup=markup)
                else:
                    data = None
                    if get_role(message) == 'Admin':
                        data = execute_query(
                            'select id, name from course where description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"')
                    elif get_role(message) == 'Teacher':
                        depart = \
                            execute_query('select depart_id from user where id = ?', [int(message.from_user.id)])[0][0]
                        data = execute_query(
                            'select id, name from course where depart_id = ? and description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"',
                            [depart])
                    elif get_role(message) == 'Student':
                        group = execute_query('select group_id from user where id = ?', [int(message.from_user.id)])[0][
                            0]
                        print(group)
                        data = execute_query(
                            'select id, name from course join course_group on id = course_id where group_id = ? and description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"',
                            [group])
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    markup.row("-")
                    for id, name in data:
                        markup.row("({}) {}".format(id, name))
                    bot.send_message(message.chat.id, "❌У нас нет такого курса.")
                    bot.send_message(message.chat.id,
                                     'Список курсов показан ниже, если вы хотите получить информацию по одному из них, нажмите на него.\n' +
                                     '⚠ Отправьте "-" для отмены.',
                                     reply_markup=markup)
            except Exception as ex:
                data = None
                if get_role(message) == 'Admin':
                    data = execute_query('select id, name from course')
                elif get_role(message) == 'Teacher':
                    depart = execute_query('select depart_id from user where id = ?', [int(message.from_user.id)])[0][0]
                    data = execute_query('select id, name from course where depart_id = ?', [depart])
                elif get_role(message) == 'Student':
                    group = execute_query('select group_id from user where id = ?', [int(message.from_user.id)])[0][0]
                    print(group)
                    data = execute_query(
                        'select id, name from course join course_group on id = course_id where group_id = ?', [group])
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.row("-")
                for id, name in data:
                    markup.row("({}) {}".format(id, name))
                bot.send_message(message.chat.id, "❌У нас нет такого курса.")
                bot.send_message(message.chat.id,
                                 'Список курсов показан ниже, если вы хотите получить информацию по одному из них, нажмите на него.\n' +
                                 '⚠ Отправьте "-" для отмены.',
                                 reply_markup=markup)
    elif state == 'del_course_choise':
        text = message.text
        text = text.split(' ')
        if text[0] == '-':
            bot.send_message(message.chat.id, "✅Действие отменено")
            set_state(message, 'Chill')
        else:
            try:
                text[0] = text[0][1:len(text[0]) - 1]
                if text[0] == execute_query(
                        'select id from course where id = ? and description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"',
                        [text[0]])[0][0]:
                    data = None
                    data_set = execute_query(
                        'select name, depart_name, practical_n, lections_n, labs_n, credits, description from course join depart on course.depart_id = depart.id where course.id = ? and description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"',
                        [text[0]])[0]
                    groups = [item[0] for item in execute_query(
                        'select name from group_table join course_group on group_table.id = course_group.group_id where course_id = ?',
                        [text[0]])]
                    if get_role(message) == 'Admin':
                        data = execute_query('select id, name from course')
                        bot.send_message(message.chat.id, 'ℹНазвание курса: {}\n' \
                                                          'ℹКафедра которая преподаёт курс: {}\n' \
                                                          'ℹКол-во практических занятий: {}\n' \
                                                          'ℹКол-во лекционных занятий: {}\n' \
                                                          'ℹКол-во лабораторных занятий: {}\n' \
                                                          'ℹКол-во кредитов курса: {}\n'.format(*data_set[:6]) +
                                         'ℹГруппы прикреплённые к курсу: ' + ', '.join(
                            groups) + '\n' + 'ℹОписание курса: {}\n'.format(data_set[6]))
                        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                        markup.row("Да", "Нет")
                        bot.send_message(message.chat.id, "Вы уверены что хотите удалить курс?", reply_markup=markup)
                        set_additional_data(message, text[0])
                        set_state(message, 'del_course_confirm')
                    elif get_role(message) == 'Teacher':
                        depart = \
                            execute_query('select depart_id from user where id = ?', [int(message.from_user.id)])[0][0]
                        data = [i[0] for i in execute_query(
                            'select id, name from course where depart_id = ? and description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"',
                            [depart])]
                        if text[0] in data:
                            bot.send_message(message.chat.id, 'ℹНазвание курса: {}\n' \
                                                              'ℹКафедра которая преподаёт курс: {}\n' \
                                                              'ℹКол-во практических занятий: {}\n' \
                                                              'ℹКол-во лекционных занятий: {}\n' \
                                                              'ℹКол-во лабораторных занятий: {}\n' \
                                                              'ℹКол-во кредитов курса: {}\n'.format(*data_set[:6]) +
                                             'ℹГруппы прикреплённые к курсу: ' + ', '.join(
                                groups) + '\n' + 'ℹОписание курса: {}\n'.format(data_set[6]))
                            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                            markup.row("Да", "Нет")
                            bot.send_message(message.chat.id, "Вы уверены что хотите удалить курс?",
                                             reply_markup=markup)
                            set_additional_data(message, text[0])
                            set_state(message, 'del_course_confirm')
                        else:
                            depart = \
                            execute_query('select depart_id from user where id = ?', [int(message.from_user.id)])[0][0]
                            data = execute_query(
                                'select id, name from course where depart_id = ? and description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"',
                                [depart])
                            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                            markup.row("-")
                            for id, name in data:
                                markup.row("({}) {}".format(id, name))
                            bot.send_message(message.chat.id,
                                             '❌Курс создан другой кафедрой, его нельзя удалить. Выберите другой курс.\n' +
                                             '⚠Отправьте "-" для отмены.',
                                             reply_markup=markup)
                else:
                    data = None
                    if get_role(message) == 'Admin':
                        data = execute_query(
                            'select id, name from course where description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"')
                    elif get_role(message) == 'Teacher':
                        depart = \
                            execute_query('select depart_id from user where id = ?', [int(message.from_user.id)])[0][0]
                        data = execute_query(
                            'select id, name from course where depart_id = ? and description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"',
                            [depart])
                    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    markup.row("-")
                    for id, name in data:
                        markup.row("({}) {}".format(id, name))
                    bot.send_message(message.chat.id,
                                     '❌У нас нет такого курса. Выберите курс который вы хотели бы удалить из списка ниже.\n' +
                                     '⚠Отправьте "-" для отмены.',
                                     reply_markup=markup)
            except Exception as ex:
                data = None
                if get_role(message) == 'Admin':
                    data = execute_query(
                        'select id, name from course where description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"')
                elif get_role(message) == 'Teacher':
                    depart = execute_query('select depart_id from user where id = ?', [int(message.from_user.id)])[0][0]
                    data = execute_query(
                        'select id, name from course where depart_id = ? and description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"',
                        [depart])
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.row("-")
                for id, name in data:
                    markup.row("({}) {}".format(id, name))
                bot.send_message(message.chat.id,
                                 '❌У нас нет такого курса. Выберите курс который вы хотели бы удалить из списка ниже.\n' +
                                 '⚠Отправьте "-" для отмены.',
                                 reply_markup=markup)
    elif state == 'del_course_confirm':
        text = message.text
        if text.upper() == "ДА":
            id = get_additional_data(message)[0]
            files = execute_query(
                'select path from file join lesson on file.lesson_id = lesson.id where lesson.course_id = ?',
                [get_additional_data(message)[0]])
            for file in files:
                os.remove(file[0])
            execute_query(
                'delete from file where lesson_id in (select id from lesson where course_id = ?)',
                [get_additional_data(message)[0]])
            execute_query('delete from file where lesson_id = ?', [get_additional_data(message)[0]])
            execute_query('delete from lesson where course_id = ?', [id])
            execute_query('delete from course where id = ?', [id])
            execute_query('delete from course_group where course_id = ?', [id])
            set_state(message, 'del_course_choise')
            del_additional_data(message)
            data = None
            if get_role(message) == 'Admin':
                data = execute_query(
                    'select id, name from course where description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"')
            elif get_role(message) == 'Teacher':
                depart = execute_query('select depart_id from user where id = ?', [int(message.from_user.id)])[0][0]
                data = execute_query(
                    'select id, name from course where depart_id = ? and description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"',
                    [depart])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            for id, name in data:
                markup.row("({}) {}".format(id, name))
            bot.send_message(message.chat.id,
                             '✅Вы выбрали "да", курс удалён, хотите удалить ещё один?\n' +
                             '⚠Отправьте "-" для отмены.',
                             reply_markup=markup)
        elif text.upper() == "НЕТ":
            set_state(message, 'del_course_choise')
            del_additional_data(message)
            data = None
            if get_role(message) == 'Admin':
                data = execute_query(
                    'select id, name from course where description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"')
            elif get_role(message) == 'Teacher':
                depart = execute_query('select depart_id from user where id = ?', [int(message.from_user.id)])[0][0]
                data = execute_query(
                    'select id, name from course where depart_id = ? and description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"',
                    [depart])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            for id, name in data:
                markup.row("({}) {}".format(id, name))
            bot.send_message(message.chat.id,
                             '✅Вы выбрали "нет", хотите другой курс?\n' +
                             '⚠Отправьте "-" для отмены.',
                             reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Да", "Нет")
            bot.send_message(message.chat.id, '⚠⚠⚠Вы действительно хотите удалить курс? (Да/Нет) ',
                             reply_markup=markup)
    elif state == "Chill":
        text = message.text
        if text.upper() == "ИНСТРУКЦИЯ":
            msg = ''
            role = get_role(message)
            if role in ('Admin', 'Student', 'Teacher'):
                msg += "✏️'Курсы' — просмотр всех доступных курсов\n"
                msg += "✏️'Занятия' — просмотр всех доступных занятий в курсе\n"
                msg += "✏️'Изменить личные данные' — изменение личных данных (имя, фамилия и т.д)\n"
                if role in ('Admin', 'Teacher'):
                    msg += "✏️'Добавить курс' — добавление нового курса\n"
                    msg += "✏️'Изменить курс' — изменение информации о курсе\n"
                    msg += "✏️'Удалить курс' — полное удаление курса\n"
                    msg += "✏️'Добавить занятие' — добавление занятия в курс\n"
                    msg += "✏️'Изменить занятие' — изменение информации о занятии\n"
                    msg += "✏️'Удалить занятие' — полное удаление занятия из курса\n"
                    if role in ('Admin'):
                        msg += "✏️'Добавить преподавателя' — добавление нового преподавателя в систему\n"
                        msg += "✏️'Изменить пользователя' — изменение информации о преподавателе\n"
                        msg += "✏️'Удалить преподавателей' — удаление преподавателя из системы\n"
            msg += "✏️'Просмотреть преподавателей' — просмотр информации о преподавателях\n"
            msg += "\nДля выполнения действия укажите одну из команд в чат"
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
            bot.send_message(message.chat.id, msg, reply_markup=markup)
        elif text.upper() == "ДОБАВИТЬ ПРЕПОДАВАТЕЛЯ" and get_role(message) == 'Admin':
            set_state(message, 'add_teacher_reply')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            bot.send_message(message.chat.id,
                             'Перешлите ОДНО сообщение от человека, которого требуется назначить преподавателем.\n⚠Отправьте "-" для отмены добалвения.',
                             reply_markup=markup)
        elif text.upper() == "ИЗМЕНИТЬ ЛИЧНЫЕ ДАННЫЕ":
            set_state(message, 'edit_myself')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("Имя", "Фамилия", "@id")
            markup.row("Email", "Номер телефона", "Кафедра")
            markup.row("Группа")
            markup.row("-")
            bot.send_message(message.chat.id,
                             'Укажите пункт для изменения\n⚠Отправьте "-" для отмены',
                             reply_markup=markup)
        elif text.upper() == "ПРОСМОТРЕТЬ ПРЕПОДАВАТЕЛЕЙ":
            set_state(message, 'show_teacher_list')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            for name, surname, t_id, chat_id in get_teachers_info():
                markup.row("{} {} @{} ({})".format(name, surname, t_id, chat_id))
            bot.send_message(message.chat.id,
                             'Укажите преподавателя из списка ниже\n' +
                             '⚠Отправьте "-" для отмены.',
                             reply_markup=markup)
        elif text.upper() == "ИЗМЕНИТЬ ПОЛЬЗОВАТЕЛЯ" and get_role(message) == 'Admin':
            set_state(message, 'change_user_start')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            for role, name, surname, t_id, chat_id in get_users_info():
                if role != 'NRG':
                    markup.row("{} | {} {} @{} ({})".format(role, name, surname, t_id, chat_id))
            bot.send_message(message.chat.id,
                             'Укажите пользователя из списка ниже\n' +
                             '⚠Отправьте "-" для отмены.',
                             reply_markup=markup)
        elif text.upper() == "УДАЛИТЬ ПРЕПОДАВАТЕЛЕЙ" and get_role(message) == 'Admin':
            set_state(message, 'del_teacher_start')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            for name, surname, t_id, chat_id in get_teachers_info():
                markup.row("{} {} @{} ({})".format(name, surname, t_id, chat_id))
            bot.send_message(message.chat.id,
                             'Укажите преподавателя для удаления\n' +
                             '⚠Отправьте "-" для отмены.',
                             reply_markup=markup)
        elif text.upper() == "ДОБАВИТЬ КУРС" and get_role(message) in ('Admin', 'Teacher'):
            set_state(message, 'add_course_name')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            bot.send_message(message.chat.id, 'Укажите название курса\n' +
                             '✅Пример: Методы оптимизации и исследования операций\n' +
                             '✅Пример: Дискретная математика\n' +
                             '⚠Отправьте "-" для отмены\n' +
                             '⚠После написания названия вы должны будете заполнить всю информацию по курсу\n⚠Это действие нельзя отменить!',
                             reply_markup=markup)
        elif text.upper() == "КУРСЫ":
            data = None
            if get_role(message) == 'Admin':
                data = execute_query(
                    'select id, name from course where description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"')
            elif get_role(message) == 'Teacher':
                depart = execute_query('select depart_id from user where id = ?', [int(message.from_user.id)])[0][0]
                data = execute_query(
                    'select id, name from course where depart_id = ? and description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"',
                    [depart])
            elif get_role(message) == 'Student':
                group = execute_query('select group_id from user where id = ?', [int(message.from_user.id)])[0][0]
                data = execute_query(
                    'select id, name from course join course_group on id = course_id where group_id = ? and description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"',
                    [group])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            for id, name in data:
                markup.row("({}) {}".format(id, name))
            bot.send_message(message.chat.id,
                             'Выберите курс, список показан ниже\n' +
                             '⚠Отправьте "-" для отмены.',
                             reply_markup=markup)
            set_state(message, 'watch_course_choise')
        elif text.upper() == "УДАЛИТЬ КУРС" and get_role(message) in ('Admin', 'Teacher'):
            data = None
            if get_role(message) == 'Admin':
                data = execute_query(
                    'select id, name from course where description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"')
            elif get_role(message) == 'Teacher':
                depart = execute_query('select depart_id from user where id = ?', [int(message.from_user.id)])[0][0]
                data = execute_query(
                    'select id, name from course where depart_id = ? and description != "Недоступно" and practical_n != "Недоступно" and lections_n != "Недоступно" and credits != "Недоступно" and depart_id != "Недоступно"',
                    [depart])
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row("-")
            for id, name in data:
                markup.row("({}) {}".format(id, name))
            bot.send_message(message.chat.id,
                             'Укажите курс\n' +
                             '⚠Отправьте "-" для отмены.',
                             reply_markup=markup)
            set_state(message, 'del_course_choise')
        else:
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
            bot.send_message(message.chat.id, "Извините, я вас не понимаю, напишите другую команду или выберите её из списка ниже",
                             reply_markup=markup)

bot.polling()