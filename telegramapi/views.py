from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render
import os
import json
import requests as notdjangorequests
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import random
import string
import telebot
from telebot import types
import logging
from pathlib import Path
from threading import Thread
from datetime import datetime
import discord
from discord import Webhook, RequestsWebhookAdapter, Embed
from accounts.views import make_username
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives

from first.models import ProfileAddInfo, Gallery, ImagesFromHomeworks, Homework, Lesson, UsersMailTmp
from first.views import resize_image
from telegramapi.models import BugReports

webhook_exception = Webhook.partial(881591145220685836,
                                    "7OgNG_dILPEqsRPyLvn4iDKfUcT3d8hbJ9uc4YhWub3sVl8v3G-VrHlqATieygZ3Isso",
                                    adapter=RequestsWebhookAdapter())

webhook_debug = Webhook.partial(917002643149312031,
                                "ipcG0qXbeTmF9VSZ7cjRpWNyJBJV8mQBgMhpuE7xbtcv9PTTdvyu2IXXb5C5Dai9-Ntn",
                                adapter=RequestsWebhookAdapter())

logging.basicConfig(filename=os.path.join(Path(__file__).resolve().parent.parent, "logs.log"),
                    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
                    datefmt="%d/%b/%Y %H:%M:%S",
                    level=logging.INFO)

token = "1964602793:AAGvfvNqGbQyPqk0RK19CelBUzsFYVc5ffo"
bot = telebot.TeleBot(token)
bot.set_webhook(url="https://mangophoto.club/telegramapi/AAGvfvNqGbQyPqk0RK19CelBUzsFYVc5ffo")

base = f"https://api.telegram.org/bot{token}/"

setWebhookdef = base + "setWebhook?url=https://mangophoto.club/telegramapi/AAGvfvNqGbQyPqk0RK19CelBUzsFYVc5ffo"
checkWebhook = base + "getWebhookInfo"
deleteWebhook = base + "deleteWebhook"
getObject = base + "getUpdates"


@bot.message_handler(commands=['sendtoall'])
def handle_start(message):
    if message.chat.id == -1001187078435:
        bot.send_message(message.chat.id, "Пришлите любое сообщение")
        bot.register_next_step_handler(message, redirect_message)


def redirect_message(message):
    try:
        if message.content_type == "text":
            if str(message.text.split(maxsplit=1)[0].strip().lower()) == "отмена":
                bot.send_message(message.chat.id, "Отменено")
            else:
                accounts = ProfileAddInfo.objects.exclude(telegram_id=0)
                for account in accounts:
                    try:
                        bot.forward_message(account.telegram_id, message.chat.id, message.message_id)
                    except Exception as err:
                        e = Embed(title="Exception!", colour=discord.Colour.red())
                        e.add_field(name="Exception text:", value=err)
                        e.add_field(name="Exception from:", value="Redirect message(for)")
                        webhook_exception.send(embed=e)
                bot.send_message(message.chat.id, "Готово")
        else:
            accounts = ProfileAddInfo.objects.exclude(telegram_id=0)
            for account in accounts:
                bot.forward_message(account.telegram_id, message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "Готово")
    except Exception as err:
        e = Embed(title="Exception!", colour=discord.Colour.red())
        e.add_field(name="Exception text:", value=err)
        e.add_field(name="Exception from:", value="Redirect message")
        webhook_exception.send(embed=e)


@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.chat.id == -1001665894315:
        if ProfileAddInfo.objects.filter(telegram_id=message.from_user.id).exists():
            try:
                user = ProfileAddInfo.objects.get(telegram_id=message.from_user.id).user
                homework_num = len(Lesson.objects.exclude(lesson_status=0))
                th = Thread(target=download_file, args=(message, homework_num, user))
                th.start()
            except Exception as err:
                e = Embed(title="Exception!", colour=discord.Colour.red())
                e.add_field(name="Exception text:", value=err)
                e.add_field(name="Exception from:", value="2nd group document register")
                webhook_exception.send(embed=e)
        else:
            e = Embed(title="Debugging info", colour=discord.Colour.orange())
            e.add_field(name="info text:", value="Unregistered user")
            e.add_field(name="info from:", value="2nd group document unregister")
            webhook_debug.send(embed=e)


@bot.message_handler(commands=['send_random'])
def handle_upload(message):
    if message.chat.id == -502825191:
        pass
        link1 = "https://t.me/joinchat/kdYuaxx5LVhkMjQ6"
        link2 = "https://t.me/joinchat/olP1CBQ3kg8zMzAy"
        link3 = "https://t.me/joinchat/Iob3wfKJ-zFjNDEy"
        # accounts = ProfileAddInfo.objects.exclude(telegram_id=0)
        # for account in accounts:
        #     what_link = random.randint(1, 3)
        #     if what_link == 1:
        #         bot.send_message(account.telegram_id, link1)
        #     elif what_link == 2:
        #         bot.send_message(account.telegram_id, link2)
        #     elif what_link == 3:
        #         bot.send_message(account.telegram_id, link3)


@bot.message_handler(commands=['upload_to_gallery'])
def handle_upload(message):
    if message.chat.type == "private":
        if ProfileAddInfo.objects.filter(telegram_id=message.from_user.id).exists():

            e = Embed(title="Debugging info", colour=discord.Colour.orange())
            e.add_field(name="Info text:", value="upload_to_gallery command used!")
            e.add_field(name="Info from:", value="upload_to_gallery func")
            webhook_debug.send(embed=e)

            user = None
            try:
                user = ProfileAddInfo.objects.get(telegram_id=message.from_user.id).user
            except Exception as err:
                e = Embed(title="Exception!", colour=discord.Colour.red())
                e.add_field(name="Exception text:", value=err)
                e.add_field(name="Exception from:", value="Upload to gallery")
                webhook_exception.send(embed=e)
                logging.exception("Exception at getting name!")
            bot.send_message(message.chat.id, "Пришлите боту нужные фотографии и после напишите \"Готово\""
                                              "\n(Отправляйте фотографии не сжимая и не группируя!"
                                              "\nФотографии большого размера могут не отправиться."
                                              " Рекомендуемое разрешение до 4k и размер до 10МБ.)")
            bot.register_next_step_handler(message, save_file_to_upload, user)
        else:
            bot.send_message(message.chat.id, "Похоже, ты ещё не зарегистрирован.\n\n"
                                              "Это можно исправить с помощью команды /register.\n\n")
    elif message.chat.type == "group":
        bot.send_message(message.chat.id, "Эта команда не поддерживается в группе")


def save_file_to_upload(message, user):
    try:
        if message.content_type == 'document':
            th = Thread(target=download_file_to_upload, args=(message, user))
            th.start()
            bot.register_next_step_handler(message, save_file_to_upload, user)
        elif message.content_type == "text":
            if message.text.split(maxsplit=1)[0].strip().lower() == "готово":
                bot.send_message(message.chat.id, "Готово!")
    except Exception as err:
        e = Embed(title="Exception!", colour=discord.Colour.red())
        e.add_field(name="Exception text:", value=err)
        e.add_field(name="Exception from:", value="Save file to upload")
        webhook_exception.send(embed=e)


def download_file_to_upload(message, user):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = rand_string(15) + ".jpg"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_os = os.path.join(dir_path, f'../media/gallery/{file_name}')
    name_for_db = "gallery/" + file_name
    gallery_obj = Gallery.objects.create(image=name_for_db, user=user)
    pillow_image = resize_image(gallery_obj.image)
    pillow_name = gallery_obj.image.name.replace("gallery/", "")
    gallery_obj.image_compressed.save(pillow_name, InMemoryUploadedFile(
        pillow_image,  # file
        None,  # field_name
        pillow_name,  # file name
        'image/jpeg',  # content_type
        pillow_image.tell,  # size
        None))
    with open(file_os, 'wb') as new_file:
        new_file.write(downloaded_file)
        new_file.close()


@bot.message_handler(commands=['bug_report'])
def bug_report(message):
    if message.chat.type == "private":
        if ProfileAddInfo.objects.filter(telegram_id=message.from_user.id).exists():
            text = "Опишите баг, который вы нашли"
            bot.send_message(message.chat.id, text)
            bot.register_next_step_handler(message, bug_report_message)
    elif message.chat.type == "group":
        bot.send_message(message.chat.id, "Эта команда не поддерживается в группе")


def bug_report_message(message):
    try:
        new_bug_report = BugReports.objects.create(user=message.from_user.id)
        new_bug_report.save()
        bot.forward_message(-596223387, message.chat.id, message.message_id)
        bot.send_message(-596223387, f"Номер заявки: {new_bug_report.id}")
        bot.send_message(message.chat.id, f"Номер заявки: {new_bug_report.id}")
        bot.send_message(message.chat.id, "Готово")
    except Exception as err:
        e = Embed(title="Exception!", colour=discord.Colour.red())
        e.add_field(name="Exception text:", value=err)
        e.add_field(name="Exception from:", value="bug_report_message func")
        webhook_exception.send(embed=e)


@bot.message_handler(commands=['bug_report_answer'])
def bug_report_answer(message):
    if message.chat.type == "group":
        if message.chat.id == -596223387:
            try:
                if not str(message.text).replace("/bug_report_answer", "").strip().isdigit():
                    bot.send_message(message.chat.id, "Пришлите сразу номер заявки!(Пример: /bug_report_answer 3)")
                else:
                    request_num = int(str(message.text).replace("/bug_report_answer", "").strip())
                    if BugReports.objects.filter(id=request_num).exists():
                        text = "Пришлите текст ответа"
                        bot.send_message(message.chat.id, text)
                        bot.register_next_step_handler(message, bug_report_answer_message, request_num=request_num)
                    else:
                        bot.send_message(message.chat.id, "Заявка не найдена!")
            except Exception as err:
                e = Embed(title="Exception!", colour=discord.Colour.red())
                e.add_field(name="Exception text:", value=err)
                e.add_field(name="Exception from:", value="bug_report_answer func")
                webhook_exception.send(embed=e)
    elif message.chat.type == "private":
        bot.send_message(message.chat.id, "Эта команда не поддерживается в группе")


def bug_report_answer_message(message, request_num):
    try:
        bug_report = BugReports.objects.get(id=request_num)
        bot.forward_message(bug_report.user, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, "Готово")
    except Exception as err:
        e = Embed(title="Exception!", colour=discord.Colour.red())
        e.add_field(name="Exception text:", value=err)
        e.add_field(name="Exception from:", value="bug_report_answer func")
        webhook_exception.send(embed=e)


@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.chat.type == "private":
        if ProfileAddInfo.objects.filter(telegram_id=message.from_user.id).exists():
            text = "Я Mango - Бот, отправлю ваши фоточки на проверку.\n\n" \
                   "Сначала подпиши номер задания, которое выполняешь.\n\n" \
                   "Дальше загрузи фото. После фото отправиться на проверку\n\n" \
                   "Держи манго 🥭"
            bot.send_message(message.chat.id, text)
        else:
            text = "Я Mango - Бот, отправлю ваши фоточки на проверку.\n\n" \
                   "Сначала подпиши номер задания, которое выполняешь.\n\n" \
                   "Дальше загрузи фото. После фото отправиться на проверку\n\n" \
                   "Но, кажется, ты ещё не зарегистрирован.\n\n" \
                   "Это можно исправить с помощью команды /register.\n\n" \
                   "Держи манго 🥭"
            bot.send_message(message.chat.id, text)
    elif message.chat.type == "group":
        bot.send_message(message.chat.id, "Эта команда не поддерживается в группе")


@bot.message_handler(commands=['register'])
def handle_register(message):
    if message.chat.type == "private":
        if ProfileAddInfo.objects.filter(telegram_id=message.from_user.id).exists():
            bot.send_message(message.chat.id, "Кажется, ты уже зарегистрирован")
        else:
            bot.send_message(message.chat.id, "Начнём регистрацию, напиши свой email")
            bot.register_next_step_handler(message, reg_email)
    elif message.chat.type == "group":
        bot.send_message(message.chat.id, "Эта команда не поддерживается в группе")


def reg_email(message):
    if "@" in str(message.text):
        bot.send_message(message.chat.id, "Теперь пришлите через пробел фамилию и имя")
        bot.register_next_step_handler(message, reg_name, str(message.text))
    else:
        bot.send_message(message.chat.id, "Проверь корректность введённой почты")
        bot.register_next_step_handler(message, reg_email)


def reg_name(message, email):
    try:
        if 1 < len(str(message.text).split(" ")) < 5:
            bot.send_message(message.chat.id, "Отлично, аккаунт зарегистрирован!"
                                              " Держи ссылку на сайт https://mangophoto.club/")
            tmp = str(message.text).split(" ")
            lastname = tmp[0]
            name = tmp[1]
            password = User.objects.make_random_password()
            user = User.objects.create_user(make_username(name, lastname), email, password)
            user.last_name = lastname
            user.first_name = name
            user.is_active = True
            user.save()
            values_for_update = {'avatar': '../static/images/stock_ava.jpg',
                                 'background': '0', 'user': user,
                                 'telegram_id': message.from_user.id}
            ProfileAddInfo.objects.update_or_create(user=user, defaults=values_for_update)
            email_subject = 'Активация аккаунта'
            message = render_to_string('activate_account.html', {
                'password': password,
                'user': user,
                'domain': 'mangophoto.club',
                'protocol': 'https',
            })
            plain_message = strip_tags(message)
            email = EmailMultiAlternatives(email_subject, plain_message, to=[email])
            email.attach_alternative(message, 'text/html')
            email.send()
            UsersMailTmp.objects.create(password=password, user=user)
        else:
            bot.send_message(message.chat.id, "Проверь корректность введённых данных")
            bot.register_next_step_handler(message, reg_name, email)
    except Exception as err:
        e = Embed(title="Exception!", colour=discord.Colour.red())
        e.add_field(name="Exception text:", value=err)
        e.add_field(name="Exception from:", value="Registration(name)")
        webhook_exception.send(embed=e)


@bot.message_handler(commands=['homework'])
def handle_homework(message):
    if message.chat.type == "private":

        if not str(message.text).replace("/homework", "").strip().isdigit():
            bot.send_message(message.chat.id, "Напиши сразу номер урока!(Пример: /homework 3)")
        else:
            e = Embed(title="Debugging info", colour=discord.Colour.orange())
            e.add_field(name="Info text:", value="homework command used!")
            e.add_field(name="Info from:", value="first homework func")
            webhook_debug.send(embed=e)

            if ProfileAddInfo.objects.filter(telegram_id=message.from_user.id).exists():
                user = None
                try:
                    user = ProfileAddInfo.objects.get(telegram_id=message.from_user.id).user
                except Exception as err:
                    e = Embed(title="Exception!", colour=discord.Colour.red())
                    e.add_field(name="Exception text:", value=err)
                    e.add_field(name="Exception from:", value="Homework(begin)")
                    webhook_exception.send(embed=e)
                    logging.exception("Exception at getting name!")
                text = "Выберите что вы хотите сделать для этого занятия"
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                itembtn1 = types.KeyboardButton('Загрузить ДЗ')
                itembtn2 = types.KeyboardButton('Удалить фотографии из ДЗ')
                itembtn3 = types.KeyboardButton('Показать прикреплённые фотографии')
                markup.add(itembtn1, itembtn2, itembtn3)
                bot.send_message(message.chat.id, text, reply_markup=markup)
                bot.register_next_step_handler(message, what_do_with_files,
                                               str(message.text).replace("/homework", "").strip(), user)
            else:
                bot.send_message(message.chat.id, "Зарегистрируйтесь чтобы использовать эту команду")
    elif message.chat.type == "group":
        bot.send_message(message.chat.id, "Эта команда не поддерживается в группе")


def what_do_with_files(message, homework_num, user):
    if len(Lesson.objects.filter(lesson_num=homework_num).exclude(lesson_status=0)) == 0:
        bot.send_message(message.chat.id, "Урок не найден или ещё не доступен!")
    else:
        try:
            e = Embed(title="Debugging info", colour=discord.Colour.orange())
            e.add_field(name="Info text:",
                        value=f"{message.text.split(maxsplit=1)[0].strip()} chose!")
            e.add_field(name="Info from:", value="second homework func")
            webhook_debug.send(embed=e)
        except Exception as err:
            e = Embed(title="Exception!", colour=discord.Colour.red())
            e.add_field(name="Exception text:", value=err)
            e.add_field(name="Exception from:", value="Debugging homework(second)")
            webhook_exception.send(embed=e)

        if message.text.split(maxsplit=1)[0].strip().lower() == "удалить":
            images = list(ImagesFromHomeworks.objects.filter(lesson_num=homework_num, user=user))

            if images:
                itter = 1
                for image in images:
                    try:
                        photo = open(os.path.join(Path(__file__).resolve().parent.parent,
                                                  "media/" + str(image.homework.image_compressed)),
                                     'rb')
                        bot.send_photo(message.chat.id, photo, caption=f"№{itter}")
                    except Exception as err:
                        e = Embed(title="Exception!", colour=discord.Colour.red())
                        e.add_field(name="Exception text:", value=err)
                        e.add_field(name="Exception from:", value="homework(what to do with files)")
                        webhook_exception.send(embed=e)
                        logging.exception("Exception at trying send photos!")
                    itter += 1
                bot.send_message(message.chat.id, "Пришлите через пробел боту номера картинок которые нужно удалить")
                bot.register_next_step_handler(message, del_file, images)
            else:
                bot.send_message(message.chat.id, "Для этого урока не найдено ДЗ")
        elif message.text.split(maxsplit=1)[0].strip().lower() == "загрузить":
            bot.send_message(message.chat.id, "Пришлите боту нужные фотографии и после напишите \"Готово\""
                                              "\n(Отправляйте фотографии не сжимая и не группируя!"
                                              "\nФотографии большого размера могут не отправиться."
                                              " Рекомендуемое разрешение до 4k и размер до 10МБ.)")
            bot.register_next_step_handler(message, save_file, homework_num, user)
        elif message.text.split(maxsplit=1)[0].strip().lower() == "показать":
            images = ImagesFromHomeworks.objects.filter(lesson_num=homework_num, user=user)
            if images:
                itter = 1
                for image in images:
                    try:
                        photo = open(os.path.join(Path(__file__).resolve().parent.parent,
                                                  "media/" + str(image.homework.image_compressed)),
                                     'rb')
                        bot.send_photo(message.chat.id, photo, caption=f"№{itter}")
                    except Exception as err:
                        e = Embed(title="Exception!", colour=discord.Colour.red())
                        e.add_field(name="Exception text:", value=err)
                        e.add_field(name="Exception from:", value="homework(what to do with files)")
                        webhook_exception.send(embed=e)
                        logging.exception("Exception at trying send photos!")
                    itter += 1
                bot.send_message(message.chat.id, "Готово!")
            else:
                bot.send_message(message.chat.id, "Для этого урока не найдено ДЗ")


def save_file(message, homework_num, user):
    try:
        if message.content_type == 'document':
            th = Thread(target=download_file, args=(message, homework_num, user))
            th.start()
            bot.register_next_step_handler(message, save_file, homework_num, user)
        elif message.content_type == "text":
            if message.text.split(maxsplit=1)[0].strip().lower() == "готово":
                bot.send_message(message.chat.id, "Готово!")
            else:
                bot.send_message(message.chat.id, "Когда закинешь все фотки, напиши \"готово\"")
                bot.register_next_step_handler(message, save_file, homework_num, user)
    except Exception as err:
        e = Embed(title="Exception!", colour=discord.Colour.red())
        e.add_field(name="Exception text:", value=err)
        e.add_field(name="Exception from:", value="Save file")
        webhook_exception.send(embed=e)


def download_file(message, homework_num, user):
    try:
        if message.from_user.id != 1099397450 and message.chat.type == "private":
            bot.forward_message("-1001665894315", message.chat.id, message.message_id)
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = rand_string(15) + ".jpg"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_os = os.path.join(dir_path, f'../media/gallery/{file_name}')
        with open(file_os, 'wb') as new_file:
            new_file.write(downloaded_file)
            new_file.close()
        name_for_db = "gallery/" + file_name
        gallery_obj = Gallery.objects.create(image=name_for_db, user=user)
        pillow_image = resize_image(gallery_obj.image)
        pillow_name = gallery_obj.image.name.replace("gallery/", "")
        gallery_obj.image_compressed.save(pillow_name, InMemoryUploadedFile(
            pillow_image,  # file
            None,  # field_name
            pillow_name,  # file name
            'image/jpeg',  # content_type
            pillow_image.tell,  # size
            None))
        ImagesFromHomeworks.objects.create(homework=gallery_obj, lesson_num=homework_num, user=user)
        values_for_update = {"homework_status": 0}
        Homework.objects.update_or_create(user=user, lesson_num=homework_num, defaults=values_for_update)
    except Exception as err:
        e = Embed(title="Exception!", colour=discord.Colour.red())
        e.add_field(name="Exception text:", value=err)
        e.add_field(name="Exception from:", value="Download file")
        webhook_exception.send(embed=e)


def del_file(message, images):
    answer = str(message.text).split(" ")

    numbers = []
    for number in answer:
        if number.isdigit():
            numbers.append(int(number) - 1)

    for number in sorted(numbers, reverse=True):
        try:
            Gallery.objects.get(image=str(images[number].homework)).delete()
            images[number].delete()
        except Exception as err:
            e = Embed(title="Exception!", colour=discord.Colour.red())
            e.add_field(name="Exception text:", value=err)
            webhook_exception.send(embed=e)
            logging.exception("Exception at trying delete photos!")
    bot.send_message(message.chat.id, "Готово!")


def rand_string(size):
    """
    Функция создающая случайную строку длиной в size

    :param size: длина строки которую нужно сгенерировать
    :return: рандомно сгенерированная строка
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))


@csrf_exempt
def webhook_func(request):
    """
    Главная функция обрабатывающая нужную информацию приходящую на вэбхук

    :param request: детали запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера
    :rtype: :class:`django.http.HttpResponse`
    """
    if request.method == "POST":
        req_out = json.loads(request.body)
        try:
            try:
                json_str = request.body.decode('UTF-8')
                update = types.Update.de_json(json_str)
                bot.process_new_updates([update])
            except Exception as e:
                message = render_to_string('send', {'web2': e})
                email = EmailMessage('Test', message, to=['pvisnakov26@gmail.com'])
                email.send()
        except Exception as e:
            message = render_to_string('send', {'web2': e})
            email = EmailMessage('Test', message, to=['pvisnakov26@gmail.com'])
            email.send()
        return HttpResponse(request, status=200)
    web2 = notdjangorequests.get(checkWebhook)
    return render(request, 'telegram.html', {'web2': web2.content})
