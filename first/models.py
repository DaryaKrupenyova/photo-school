from django.contrib.auth.models import User
from django.db import models

# Create your models here.
import datetime


class Transactions(models.Model):
    payment_amount = models.FloatField(default=0)
    was = models.DateField(default=datetime.date.today().strftime("%d/%m/%Y"))
    link = models.CharField(default=0, max_length=300)
    type = models.CharField(default=0, max_length=300)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)
    after_transaction = models.FloatField(default=0)


class UsersMailTmp(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)
    password = models.CharField(max_length=100)


class Courses(models.Model):
    course_num = models.IntegerField(default=0)
    title = models.CharField(default=0, max_length=600)
    price = models.IntegerField(default=0)
    places = models.IntegerField(default=0)


class LessonInfo(models.Model):
    task_title = models.CharField(default=0, max_length=300)
    lesson_num = models.IntegerField(default=0)
    lecture_status = models.IntegerField(default=0)
    homework_status = models.IntegerField(default=0)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)
    course_num = models.ForeignKey(to=Courses, on_delete=models.CASCADE, default=0)


class Promo(models.Model):
    content = models.CharField(default=0, max_length=300)
    type = models.CharField(default=0, max_length=100)
    amount = models.IntegerField(default=0)
    expires = models.DateField(default=datetime.date.today() + datetime.timedelta(1))
    whose = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)
    times_can_use = models.IntegerField(default=1)


class PromoUse(models.Model):
    who_use = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)
    what_promo = models.ForeignKey(to=Promo, on_delete=models.CASCADE, default=1, related_name="promo")


class SignedUpForCourse(models.Model):
    course_num = models.ForeignKey(to=Courses, on_delete=models.CASCADE, default=0)
    group_num = models.IntegerField(default=-1)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)


class ProfileAddInfo(models.Model):
    """
    Дополнительная информация о пользователе

    :param avatar: путь к картинке аватара
    :param background: путь к картинке фона меню
    :param telegram_id: id телеграмм аккаунта пользователя
    :param is_teacher: является ли пользователь учителем
    :param user: ForeignKey к модели :class:`django.contrib.auth.models.User`
    """
    avatar = models.ImageField(upload_to='images', default=0)
    background = models.ImageField(upload_to='images', default=0)
    telegram_id = models.IntegerField(default=0)
    is_teacher = models.IntegerField(default=0)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)
    wallet = models.FloatField(default=0)
    is_invited = models.IntegerField(default=0)
    invited_by = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1, related_name="user_inv")
    invited_count = models.IntegerField(default=0)
    group_num = models.CharField(default=0, max_length=100)
    payment_status = models.IntegerField(default=0)
    about = models.CharField(default="", max_length=600)


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, default=1)
    email = models.EmailField(default=0, max_length=100)


class Course(models.Model):
    """
    Информация о новых пользователях которые хотят записаться на курс

    :param name: имя пользователя
    :param e_mail: электронная почта пользователя
    :param phone: номер телефона пользователя
    """
    name = models.CharField('Имя', max_length=100)
    e_mail = models.EmailField('Электронная почта', max_length=100)
    phone = models.CharField('Телефон', max_length=100)


class Gallery(models.Model):
    """
    Фотографии которые загружает пользователь

    :param user: ForeignKey к модели :class:`django.contrib.auth.models.User`
    :param avatar: путь к картинке которую загрузил пользователь
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='gallery', default=0)
    image_compressed = models.ImageField(upload_to='gallery_compressed', default="")
    is_deleted = models.IntegerField(default=0)


class Lesson(models.Model):
    """
    Содержание урока

    :param header: заголовок урока
    :param text1: первая часть текста(до картинок)
    :param text2: первая часть текста(после картинок)
    :param image1: первая демонстрационная фотография в ДЗ
    :param image2: вторая демонстрационная фотография в ДЗ
    :param image3: третья демонстрационная фотография в ДЗ
    :param image4: четвёртая демонстрационная фотография в ДЗ
    :param lesson_num: номер урока
    """
    header = models.CharField(default=0, max_length=300)
    homework_text = models.CharField(default=0, max_length=6000)
    webinar_url = models.CharField(default=0, max_length=600)
    youtube_url = models.CharField(default=0, max_length=600)
    part = models.IntegerField(default=1)
    lesson_num = models.IntegerField(default=0)
    pdf_route = models.FileField(upload_to='pdf', default=0)
    lesson_status = models.IntegerField(default=0)
    course_num = models.ForeignKey(to=Courses, on_delete=models.CASCADE, default=1)


class CourseParts(models.Model):
    course_num = models.ForeignKey(to=Courses, on_delete=models.CASCADE, default=1)
    part_num = models.IntegerField(default=0)
    part_name = models.CharField(default=0, max_length=500)


class ImagesFromLessons(models.Model):
    """
    Картинки к уроку

    :param image: одна из картинок к уроку
    :param lesson_num: номер урока которому принадлежит картинка
    """
    image = models.ImageField(upload_to='gallery', default=0)
    lesson_num = models.IntegerField(default=0)


class FavoritePhotos(models.Model):
    image = models.ForeignKey(to=Gallery, on_delete=models.CASCADE, default=1, related_name="fav_image")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)


class Homework(models.Model):
    """
    Домашняя работа пользователя

    :param homework: путь к домашнему заданию
    :param user: ForeignKey к модели :class:`django.contrib.auth.models.User`
    """
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)
    homework_status = models.IntegerField(default=0)
    comment = models.CharField(default="", max_length=600)
    lesson_num = models.IntegerField(default=0)


class ImagesFromHomeworks(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, default=1)
    homework = models.ForeignKey(to=Gallery, on_delete=models.CASCADE, default=1)
    lesson_num = models.IntegerField(default=0)
