import base64
import io
import os
import random
import string
from io import BytesIO

from django.template.context_processors import csrf
from django.utils.datetime_safe import datetime
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import HttpResponse, QueryDict, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDict
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime
import datetime
from discord import Webhook, RequestsWebhookAdapter, Embed
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile

from accounts.forms import UserLoginResetForm, UserEmailResetForm
from accounts.token_generator import account_activation_token

# Create your views here.
from decorators import login_required_custom
from first.forms import CourseForm, HomeworkForm
from first.models import LessonInfo, ProfileAddInfo, Profile, Course, Gallery, Lesson, ImagesFromLessons, Homework, \
    ImagesFromHomeworks, Transactions, Promo, UsersMailTmp, PromoUse, SignedUpForCourse, Courses, CourseParts, \
    FavoritePhotos

webhook = Webhook.partial(881591145220685836, "7OgNG_dILPEqsRPyLvn4iDKfUcT3d8hbJ9uc4YhWub3sVl8v3G-VrHlqATieygZ3Isso",
                          adapter=RequestsWebhookAdapter())


def handler404(request, exception):
    return render(request, 'error_404.html', status=404)


def handler500(request):
    return render(request, 'error_5XX.html', status=500)


def user_info(context, request):
    """
    Получаем информацию о пользователе

    :param context: дополнительная информация передающаяся на страницу
    :param request: детали запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера
    :rtype: :class:`django.http.HttpResponse`
    """
    try:
        user_info = User.objects.get(username=request.user)
        context['first_name'] = user_info.first_name
        context['last_name'] = user_info.last_name
        context['username'] = user_info.username
        context['ava'] = ProfileAddInfo.objects.get(user=request.user)
        context['signup_for_course'] = SignedUpForCourse.objects.filter(user=request.user)
    except Exception as e:
        print(e)
    return context


def take_courses_info(context, request):
    """
    Получаем информацию о курсах

    :param context: дополнительная информация передающаяся на страницу
    :param request: детали запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера
    :rtype: :class:`django.http.HttpResponse`
    """
    try:
        tasks = LessonInfo.objects.filter(user=request.user)
        context['tasks'] = tasks
    except Exception as e:
        print(e)
    return context


def remangotor(request):
    context = {}
    if request.method == "POST":
        pic64 = request.POST['canvas_img'].split(';base64,')[1]
        data = base64.b64decode(pic64.encode('UTF-8'))
        buf = io.BytesIO(data)
        img = Image.open(buf)
        img.show()
    elif request.method == "GET":
        id_photo = request.GET.get('photo')
        lesson = request.GET.get('lesson')
        context['photo'] = Gallery.objects.get(id=id_photo)
        context['lesson_num'] = lesson
    return render(request, 'reMangotor.html', context)


@login_required_custom
def courses(request):
    context = {}
    take_courses_info(context, request)
    user_info(context, request)
    colmns = []
    for _ in range(len(context['tasks'])):
        colmns.append(_ % 4)

    context['mylist'] = zip(context['tasks'], colmns)
    context['mylist1'] = zip(context['tasks'], colmns)
    context['mylist2'] = zip(context['tasks'], colmns)
    context['mylist3'] = zip(context['tasks'], colmns)
    return render(request, 'private_account.html', context)


@login_required_custom
def dev_page(request):
    if request.user.is_superuser == 1:
        if request.method == "POST":
            pass
        return render(request, 'dev_page.html')
    else:
        return redirect('account', request.user)


@login_required_custom
def private_account_courses(request):
    context = {}
    if request.method == "POST":
        if 'signup_for_course_btn' in request.POST:
            course_tmp = Courses.objects.get(id=1)
            SignedUpForCourse.objects.create(course_num=course_tmp, user=request.user, group_num=1)
            profile_add_info = ProfileAddInfo.objects.get(user=request.user)
            profile_add_info.payment_status = 1

    user_info(context, request)
    lessons = Lesson.objects.all()
    context['parts'] = CourseParts.objects.all()
    homeworks_tmp = Homework.objects.all()
    lessons_homeworks = []
    for lesson in lessons:
        flag = True
        for homework in homeworks_tmp:
            if lesson.lesson_num == homework.lesson_num and request.user.id == homework.user_id:
                lessons_homeworks.append([lesson, homework])
                flag = False
                break
        if flag:
            lessons_homeworks.append([lesson, None])

    context['lessons'] = lessons_homeworks
    transactions = Transactions.objects.filter(user=request.user, type="payment")
    context['transactions'] = transactions

    return render(request, 'empty_kurs.html', context)


@login_required_custom
def prepod_homeworks(request):
    context = {}
    loaded_content_limit = 16
    loaded_content_limit_fav = 16
    cookie_val = request.COOKIES.get('fav_status')
    if cookie_val is not None:
        if cookie_val == 'fav':
            favorite_img_instances = list(
                FavoritePhotos.objects.filter(user=request.user).order_by('-id')[:loaded_content_limit_fav]
            )
            context['fav_images'] = favorite_img_instances
        elif cookie_val == 'no_fav':
            context['fav_images'] = None

    if request.method == 'POST':
        if 'fav_imgs' in request.POST:
            if request.POST.get('fav_imgs') == 'fav':
                favorite_img_instances = list(
                    FavoritePhotos.objects.filter(user=request.user).order_by('-id')[:loaded_content_limit_fav]
                )
                context['fav_images'] = favorite_img_instances
            elif request.POST.get('fav_imgs') == 'no_fav':
                context['fav_images'] = None

        if 'favorite_img' in request.POST:
            favorite_img = request.POST.get('favorite_img')
            img_instance = Gallery.objects.get(id=favorite_img)
            favorite_image, created = FavoritePhotos.objects.get_or_create(image=img_instance, user=request.user)
            if not created:
                favorite_image.delete()
            if cookie_val is not None:
                if cookie_val == 'fav':
                    favorite_img_instances = list(
                        FavoritePhotos.objects.filter(user=request.user).order_by('-id')[:loaded_content_limit_fav]
                    )
                    context['fav_images'] = favorite_img_instances

        if 'load_more_btn_fav' in request.POST:
            loaded_content_limit_fav = int(request.POST.get('loaded_content_limit_fav'))
            loaded_content_limit_fav += 16
            user_info(context, request)
            favorite_img_instances = list(
                FavoritePhotos.objects.filter(user=request.user).order_by('-id')[:loaded_content_limit_fav]
            )
            context['fav_images'] = favorite_img_instances
            context['loaded_content_limit'] = loaded_content_limit
            context['loaded_content_limit_fav'] = loaded_content_limit_fav
            context.update(csrf(request))
            return JsonResponse({'data': render_to_string('prepod_homeworks.html', context=context)})

        if 'load_more_btn' in request.POST:
            loaded_content_limit = int(request.POST.get('loaded_content_limit'))
            loaded_content_limit += 16
            user_info(context, request)
            homeworks = ImagesFromHomeworks.objects.all().order_by('-id')[:loaded_content_limit]
            favorite_img_instances = FavoritePhotos.objects.filter(user=request.user)
            fav_imgs = []
            for homework in homeworks:
                flag = True
                for favorite_img_instance in favorite_img_instances:
                    if homework.homework == favorite_img_instance.image:
                        fav_imgs.append((homework, True))
                        flag = False
                        break
                if flag:
                    fav_imgs.append((homework, False))

            context['homeworks'] = fav_imgs
            context['loaded_content_limit'] = loaded_content_limit
            context['loaded_content_limit_fav'] = loaded_content_limit_fav
            context.update(csrf(request))
            return JsonResponse({'data': render_to_string('prepod_homeworks.html', context=context)})

    user_info(context, request)
    homeworks = ImagesFromHomeworks.objects.all().order_by('-id')[:loaded_content_limit]
    favorite_img_instances = FavoritePhotos.objects.filter(user=request.user)
    fav_imgs = []
    for homework in homeworks:
        flag = True
        for favorite_img_instance in favorite_img_instances:
            if homework.homework == favorite_img_instance.image:
                fav_imgs.append((homework, True))
                flag = False
                break
        if flag:
            fav_imgs.append((homework, False))

    context['homeworks'] = fav_imgs
    context['loaded_content_limit'] = loaded_content_limit
    context['loaded_content_limit_fav'] = loaded_content_limit_fav
    response = render(request, 'prepod_homeworks.html', context)

    # setting cookie
    if request.method == 'POST':
        if 'fav_imgs' in request.POST:
            if request.POST.get('fav_imgs') == 'fav':
                response.set_cookie('fav_status', 'fav')
            elif request.POST.get('fav_imgs') == 'no_fav':
                response.set_cookie('fav_status', 'no_fav')

    return response


def private_account_homework(request, lesson, user):
    context = {}
    if request.method == "POST":
        if ('grade' or 'comment' in request.POST) and request.POST.get('comment') is not None:
            grade = request.POST.get('radio')
            if not grade:
                grade = 1
            comment = request.POST.get('comment')
            comment_rec = Homework.objects.filter(lesson_num=lesson, user=user)
            comment_rec.update(comment=comment, homework_status=grade)

        if 'favorite_img' in request.POST:
            favorite_img = request.POST.get('favorite_img')
            img_instance = Gallery.objects.get(id=favorite_img)
            favorite_image, created = FavoritePhotos.objects.get_or_create(image=img_instance, user=request.user)
            if not created:
                favorite_image.delete()

    context['lesson'] = Homework.objects.get(lesson_num=lesson, user=user)
    images = ImagesFromHomeworks.objects.filter(lesson_num=lesson, user=user)
    favorite_img_instances = FavoritePhotos.objects.filter(user=request.user)
    fav_imgs = []
    for image in images:
        flag = True
        for favorite_img_instance in favorite_img_instances:
            if image.homework == favorite_img_instance.image:
                fav_imgs.append((image, True))
                flag = False
                break
        if flag:
            fav_imgs.append((image, False))

    context['images'] = fav_imgs
    user_info(context, request)
    return render(request, 'homework.html', context)


def private_account_lesson(request, lesson):
    context = {}
    lesson_obj = Lesson.objects.get(lesson_num=lesson)
    prof_add_info_obj = ProfileAddInfo.objects.get(user=request.user)
    try:
        next_lesson = Lesson.objects.get(lesson_num=(lesson + 1))
        if next_lesson.lesson_status <= 1 and prof_add_info_obj.is_teacher == 0:
            next_lesson = None
    except:
        next_lesson = None
    try:
        prev_lesson = Lesson.objects.get(lesson_num=(lesson - 1))
        if prev_lesson.lesson_status <= 1 and prof_add_info_obj.is_teacher == 0:
            prev_lesson = None
    except:
        prev_lesson = None
    context['next_lesson'] = next_lesson
    context['prev_lesson'] = prev_lesson
    if lesson_obj.lesson_status <= 0 and prof_add_info_obj.is_teacher == 0 and not request.user.is_staff:
        return redirect('courses')
    else:
        if request.method == "POST":
            if 'lesson_status_change' in request.POST:
                status = request.POST.get('lesson_status_change')
                current_lesson = Lesson.objects.get(lesson_num=lesson)
                if status == 'Открыть урок':
                    current_lesson.lesson_status = 1
                elif status == 'Открыть ДЗ':
                    current_lesson.lesson_status = 2
                elif status == 'Открыть запись':
                    current_lesson.lesson_status = 3
                elif status == 'Закрыть запись':
                    current_lesson.lesson_status = 2
                elif status == 'Закрыть ДЗ':
                    current_lesson.lesson_status = 1
                elif status == 'Закрыть урок':
                    current_lesson.lesson_status = 0
                current_lesson.save()

            if 'ph_ids' in request.POST:
                for i in request.POST.getlist('ph_ids'):
                    image_fh_obj = ImagesFromHomeworks.objects.get(id=i)
                    gallery_obj = image_fh_obj.homework
                    gallery_obj.is_deleted = 1
                    gallery_obj.save()
                    image_fh_obj.delete()

            if 'homework' in request.FILES:
                form = HomeworkForm(request.POST, request.FILES)
                if form.is_valid():
                    values_for_update = {"homework_status": 1}
                    Homework.objects.update_or_create(user=request.user, lesson_num=lesson, defaults=values_for_update)
                    if form.is_valid():
                        for f in request.FILES.getlist('homework'):
                            gallery_obj = Gallery.objects.create(image=f, user=request.user)
                            pillow_image = resize_image(gallery_obj.image)
                            gallery_obj.image_compressed.save(f.name, InMemoryUploadedFile(
                                pillow_image,  # file
                                None,  # field_name
                                f.name,  # file name
                                'image/jpeg',  # content_type
                                pillow_image.tell,  # size
                                None))
                            ImagesFromHomeworks.objects.create(
                                homework=gallery_obj, lesson_num=lesson, user=request.user)
                return redirect('lesson', lesson)

        context['homeworks'] = Homework.objects.filter(lesson_num=lesson)

        lesson_context = Lesson.objects.get(lesson_num=lesson)
        context['hw_images'] = ImagesFromHomeworks.objects.filter(lesson_num=lesson, user=request.user)
        context['lesson'] = lesson_context
        context['lesson_num'] = lesson
        tmp_2 = Homework.objects.filter(lesson_num=lesson, user_id=request.user)
        if len(tmp_2) != 0:
            context['homework'] = tmp_2[len(tmp_2) - 1]
        user_info(context, request)
        form = HomeworkForm()
        context['form'] = form
        return render(request, 'lesson.html', context)


def resize_image(image_field):
    """
    Resizes an image from a Model.ImageField and returns a new image as a ContentFile
    """
    img = Image.open(image_field)
    max_size = (800, 800)
    img = img.convert('RGB')
    img.thumbnail(max_size, Image.ANTIALIAS)
    buffer = BytesIO()
    img.save(fp=buffer, format='JPEG')
    return ContentFile(buffer.getvalue())


def rand_string(size):
    """
    Функция создающая случайную строку длиной в size

    :param size: длина строки которую нужно сгенерировать
    :return: рандомно сгенерированная строка
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))


def pics_update(request, form_name):
    """
    Запись в БД информации о аватаре/фоне меню пользователя

    :param form_name: название формы
    :param request: детали запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера
    :rtype: :class:`django.http.HttpResponse`
    """
    form_name_val = request.FILES[f'{form_name}']
    tmp = form_name_val.name.split('.')
    if tmp[1] == "jpg" or tmp[1] == "png" or tmp[1] == "jpeg" or tmp[1] == "bmp":
        tmp[0] = tmp[0].replace(' ', '')
        tmp[0] += rand_string(10)
        new_name = tmp[0] + "." + tmp[1]
        form_name_val.name = new_name
        values_for_update = {f'{form_name}': form_name_val, 'user': request.user}
        ProfileAddInfo.objects.update_or_create(user=request.user, defaults=values_for_update)
        return new_name


def user_data_update(request, form_name):
    """
    Обновление информации о пользователе

    :param form_name: название формы
    :param request: детали запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера
    :rtype: :class:`django.http.HttpResponse`
    """
    form_name_val = request.POST[f'{form_name}']
    ava = User.objects.filter(username=request.user)
    if form_name == 'username':
        ava.update(username=form_name_val)
    else:
        ava.update(email=form_name_val)


@login_required_custom
def private_account_settings(request):
    all_photos = Gallery.objects.filter(user=request.user).exclude(is_deleted=1)
    carousel_item = []
    for g in range(0, len(all_photos), 3):
        tmp = []
        for i in range(3):
            if g + i < len(all_photos):
                tmp.append(all_photos[g + i])
        carousel_item.append(tmp)

    context = {'carousel_item': carousel_item, "alert_state": 'none'}
    if request.method == "POST":
        form = UserLoginResetForm(request.POST, instance=User.objects.get(username=request.user))
        form1 = UserEmailResetForm(request.POST, instance=User.objects.get(username=request.user))
        context['form'] = form
        context['form1'] = form1
        if form.is_valid():
            form.save()

        if 'telegram_id' in request.POST:
            values_for_update = {
                'user': request.user, 'telegram_id': request.POST['telegram_id']
            }
            ProfileAddInfo.objects.update_or_create(user=request.user, defaults=values_for_update)
        if 'pic_from_gallery' in request.POST:
            tmp_value = request.POST['pic_from_gallery']
            if "/static/" in str(tmp_value):
                tmp_value = tmp_value.replace("/static/", "../static/")
            elif "/media/" in str(tmp_value):
                tmp_value = tmp_value.replace("/media/", "")

            values_for_update = {
                'avatar': tmp_value, 'user': request.user
            }
            ProfileAddInfo.objects.update_or_create(user=request.user, defaults=values_for_update)
        if 'pic_from_gallery_back' in request.POST:
            tmp_value = request.POST['pic_from_gallery_back']

            if "/static/" in str(tmp_value):
                tmp_value = tmp_value.replace("/static/", "../static/")
            elif "/media/" in str(tmp_value):
                tmp_value = tmp_value.replace("/media/", "")

            values_for_update = {
                'background': tmp_value, 'user': request.user
            }
            ProfileAddInfo.objects.update_or_create(user=request.user, defaults=values_for_update)

        if form1.is_valid():
            try:
                take_user = User.objects.get(username=form.data['username'])
            except:
                take_user = User.objects.get(username=request.user)
            values_for_update = {"user": take_user, "email": form1.data['email']}
            mail, created = Profile.objects.update_or_create(user=take_user, defaults=values_for_update)
            mail.save()

            associated_users = User.objects.filter(Q(username=take_user))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Email Reset Requested"
                    current_site = get_current_site(request)
                    email_template_name = "reset_email"
                    c = {
                        'domain': current_site.domain,
                        "email": user.email,
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'protocol': request.scheme,
                        'token': account_activation_token.make_token(user)
                    }
                    email = render_to_string(email_template_name, c)
                    letter = EmailMessage(subject, email, to=[user.email])
                    letter.send()

        if 'avatar' in request.FILES:
            resp = pics_update(request, 'avatar')
            return JsonResponse({'image_url': resp})
        if 'background' in request.FILES:
            resp = pics_update(request, 'background')
            return JsonResponse({'image_url': resp})
        context['ava'] = ProfileAddInfo.objects.get(user=request.user)
        try:
            if not form.is_valid() and form.data['username'] != "":
                userinfo = User.objects.get(username=request.user)
                alert_state = "block"
            else:
                userinfo = User.objects.get(username=form.data['username'])
                alert_state = "None"
        except MultiValueDictKeyError:
            userinfo = User.objects.get(username=request.user)
            alert_state = "None"

        context['alert_state'] = alert_state
        context['first_name'] = userinfo.first_name
        context['last_name'] = userinfo.last_name
        context['username'] = userinfo.username
        return render(request, 'settings.html', context)
    if request.method == "GET":
        user_info(context, request)
        context['form'] = UserLoginResetForm()
        context['form1'] = UserEmailResetForm()
        context['user'] = request.user
    return render(request, 'settings.html', context)


def change_email_confirm(request, uidb64, token):
    """
    Подтверждение смены почты

    :param uidb64: уникальный закодированный id юзера
    :param token: уникальный токен
    :param request: детали запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера
    :rtype: :class:`django.http.HttpResponse`
    """
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user_tmp = request.user
        email = Profile.objects.get(user=request.user).email
        User.objects.filter(username=user_tmp).update(email=email)
        return HttpResponse('You have confirmed the email.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required_custom
def empty_fin(request):
    context = {}
    if request.method == "POST":
        if 'signup_for_course_btn' in request.POST:
            course_tmp = Courses.objects.get(id=1)
            SignedUpForCourse.objects.create(course_num=course_tmp, user=request.user, group_num=1)
            profile_add_info = ProfileAddInfo.objects.get(user=request.user)
            profile_add_info.payment_status = 1

        if 'promo_place' in request.POST:
            if not PromoUse.objects.filter(who_use=request.user).exists():
                promo_place = request.POST.get('promo_place')
                promo_obj = Promo.objects.filter(content=promo_place)
                if len(promo_obj) == 1:
                    if promo_obj[0].expires > datetime.date.today() and promo_obj[0].times_can_use > 0 \
                            and promo_obj[0].type == "PERCENT":
                        promo_obj[0].times_can_use -= 1
                        promo_obj[0].save()
                        PromoUse.objects.create(who_use=request.user, what_promo=promo_obj[0])
                        return JsonResponse({'promo_invalid': 'correct'})
                    else:
                        return JsonResponse({'promo_invalid': 'invalid'})
                else:
                    return JsonResponse({'promo_invalid': 'invalid'})
            else:
                return JsonResponse({'promo_invalid': 'invalid'})

        if 'friend_promo' in request.POST:
            if not PromoUse.objects.filter(who_use=request.user).exists():
                friend_promo = request.POST.get('friend_promo')
                promo_obj = Promo.objects.filter(content=friend_promo)
                if len(promo_obj) == 1:
                    if promo_obj[0].type == "INV" and promo_obj[0].whose == request.user:
                        return JsonResponse({'friend_promo_invalid': 'invalid'})
                    else:
                        if promo_obj[0].type == "INV":
                            PromoUse.objects.create(who_use=request.user, what_promo=promo_obj[0])
                            return JsonResponse({'friend_promo_invalid': 'correct'})
                else:
                    return JsonResponse({'friend_promo_invalid': 'invalid'})
            else:
                return JsonResponse({'friend_promo_invalid': 'invalid'})

    transactions = Transactions.objects.filter(user=request.user)
    promo = Promo.objects.filter(whose=request.user)
    if promo:
        promo = promo[0]
    promo_use = PromoUse.objects.filter(who_use=request.user)
    if promo_use:
        context['promo_use'] = promo_use[0]
    context['transactions'] = transactions
    context['promo'] = promo
    user_info(context, request)
    return render(request, 'finansi.html', context)


@login_required_custom
def question(request):
    context = {}
    if request.method == "POST":
        if 'signup_for_course_btn' in request.POST:
            course_tmp = Courses.objects.get(id=1)
            SignedUpForCourse.objects.create(course_num=course_tmp, user=request.user, group_num=1)
            profile_add_info = ProfileAddInfo.objects.get(user=request.user)
            profile_add_info.payment_status = 1

    user_info(context, request)
    return render(request, 'question.html', context)


def error_404(request):
    return render(request, 'error_404.html')


def error_5XX(request):
    return render(request, 'error_5XX.html')


def error_invalid_link(request):
    return render(request, 'error_invalid_link.html')


@login_required_custom
def group(request):
    context = {}
    if request.method == "POST":
        if 'signup_for_course_btn' in request.POST:
            course_tmp = Courses.objects.get(id=1)
            SignedUpForCourse.objects.create(course_num=course_tmp, user=request.user, group_num=1)
            profile_add_info = ProfileAddInfo.objects.get(user=request.user)
            profile_add_info.payment_status = 1

    user_info(context, request)
    return render(request, 'group.html', context)


def lending(request):
    return render(request, 'lending.html')


@login_required_custom
def admin_fin(request):
    if request.user.is_staff:
        context = {}
        if request.method == "POST":
            if 'withdraw_payment' in request.POST and request.POST.get("withdraw_payment") == "sure":
                users_to_withdraw = User.objects.filter(is_staff=0)
                for i in range(len(users_to_withdraw)):
                    if SignedUpForCourse.objects.filter(user=users_to_withdraw[i]).exists():
                        profile_add_info = ProfileAddInfo.objects.get(user=users_to_withdraw[i])
                        if profile_add_info.is_teacher == 0:
                            does_use_promo = PromoUse.objects.filter(who_use=users_to_withdraw[i])
                            was = datetime.date.today()
                            if len(does_use_promo) > 0:
                                if does_use_promo[0].what_promo.type == "INV":
                                    profile_add_info.wallet += 200
                                    profile_add_info.save()
                                    profile_add_info_tmp = ProfileAddInfo.objects.get(
                                        user=does_use_promo[0].what_promo.whose)
                                    profile_add_info_tmp.wallet += 400
                                    profile_add_info_tmp.save()

                                if does_use_promo[0].what_promo.type == "PERCENT":
                                    how_much_withdraw = round(4000 - 4000 / 100 * does_use_promo[0].what_promo.amount,
                                                              2)
                                    if profile_add_info.wallet >= how_much_withdraw:
                                        profile_add_info.payment_status = 4
                                        profile_add_info.wallet -= how_much_withdraw
                                        Transactions.objects.create(payment_amount=how_much_withdraw, was=was, link="",
                                                                    type="payment", user=users_to_withdraw[i],
                                                                    after_transaction=profile_add_info.wallet)
                                    else:
                                        profile_add_info.payment_status = 2

                            else:
                                if profile_add_info.wallet >= 4000:
                                    profile_add_info.payment_status = 4
                                    profile_add_info.wallet -= 4000
                                    Transactions.objects.create(payment_amount=4000, was=was, link="", type="payment",
                                                                user=users_to_withdraw[i],
                                                                after_transaction=profile_add_info.wallet)
                                else:
                                    profile_add_info.payment_status = 2

                            profile_add_info.save()
                PromoUse.objects.all().delete()

            if 'before_withdraw' in request.POST and request.POST.get("before_withdraw") == "sure":
                users_to_withdraw = User.objects.filter(is_staff=0)
                for i in range(len(users_to_withdraw)):
                    if SignedUpForCourse.objects.filter(user=users_to_withdraw[i]).exists():
                        profile_add_info = ProfileAddInfo.objects.get(user=users_to_withdraw[i])
                        if profile_add_info.is_teacher == 0:
                            does_use_promo = PromoUse.objects.filter(who_use=users_to_withdraw[i])
                            if len(does_use_promo) > 0:
                                if does_use_promo[0].what_promo.type == "PERCENT":
                                    how_much_withdraw = round(4000 - 4000 / 100 * does_use_promo[0].what_promo.amount,
                                                              2)
                                    if profile_add_info.wallet >= how_much_withdraw:
                                        profile_add_info.payment_status = 4
                                    else:
                                        profile_add_info.payment_status = 3
                            else:
                                if profile_add_info.wallet >= 4000:
                                    profile_add_info.payment_status = 4
                                else:
                                    profile_add_info.payment_status = 3

                            profile_add_info.save()

            if 'promo_id' in request.POST:
                promo_id = request.POST.get("promo_id")
                Promo.objects.get(id=promo_id).delete()

            if 'discount' in request.POST:
                content = rand_string(18)
                amount = request.POST.get("discount")
                expires = request.POST.get("expires")
                count = request.POST.get("count")
                Promo.objects.create(content=content, type="PERCENT", amount=amount,
                                     expires=expires, whose=request.user, times_can_use=count)

            if 'discount_edit' in request.POST:
                amount_edit = request.POST.get("discount_edit")
                expires_edit = datetime.datetime.strptime(request.POST.get("expires_edit"), "%Y-%m-%d")
                count_edit = int(request.POST.get("count_edit"))
                p_id = int(request.POST.get("promo_id_edit"))
                db_promo = Promo.objects.get(id=p_id)
                if expires_edit >= datetime.datetime.now() and count_edit >= db_promo.times_can_use:
                    if "%" in str(amount_edit):
                        db_promo.type = "PERCENT"
                        amount_edit = int(str(amount_edit.replace('%', '')))
                    else:
                        db_promo.type = "RUB"
                    db_promo.amount = amount_edit
                    db_promo.expires = expires_edit
                    db_promo.times_can_use = count_edit
                    db_promo.save()
                elif expires_edit < datetime.datetime.now():
                    return JsonResponse({'promo_status': 'date_invalid'})
                elif count_edit < db_promo.times_can_use:
                    return JsonResponse({'promo_status': 'count_invalid'})

            if 'payment_amount' in request.POST:
                payment_amount = round(float(request.POST.get('payment_amount').replace(',', '.')), 2)
                was = request.POST.get('was')
                link = request.POST.get('link')
                user = request.POST.get('user')
                user_tmp = User.objects.get(username=user)
                db_profile_add_info = ProfileAddInfo.objects.get(user=user_tmp.id)
                after_transaction = round(float(db_profile_add_info.wallet) + float(payment_amount), 2)
                db_profile_add_info.wallet = after_transaction
                db_profile_add_info.save()
                Transactions.objects.create(payment_amount=payment_amount, was=was, link=link,
                                            type="adding", user=user_tmp, after_transaction=after_transaction)

            if 'transaction_del' in request.POST:
                transaction_id = request.POST.get('transaction_del')
                Transactions.objects.get(id=transaction_id).delete()

            if 'payment_amount_change' in request.POST:
                payment_amount_change = round(float(request.POST.get('payment_amount_change').replace(',', '.')), 2)
                was_change = request.POST.get('was_change')
                link_change = request.POST.get('link_change')
                transaction_id = request.POST.get('transaction_id')

                transaction = Transactions.objects.get(id=transaction_id)
                difference = round(float(payment_amount_change) - float(transaction.payment_amount), 2)
                after_transaction_change = round(float(transaction.after_transaction) + difference, 2)

                user = request.POST.get('user')
                user_tmp = User.objects.get(username=user)
                db_profile_add_info = ProfileAddInfo.objects.get(user=user_tmp.id)
                wallet_change = round(float(db_profile_add_info.wallet) + float(difference), 2)
                db_profile_add_info.wallet = wallet_change
                db_profile_add_info.save()

                Transactions.objects.filter(id=transaction_id).update(payment_amount=payment_amount_change,
                                                                      was=was_change, link=link_change,
                                                                      after_transaction=after_transaction_change)

        elif request.method == "GET":
            if 'promoid' in request.GET:
                promo_id = request.GET.get("promoid")
                db_promo = Promo.objects.get(id=promo_id)
                context2 = {
                    'db_promo': db_promo,
                }
                context2.update(csrf(request))
                context2_tmp = {'promo_edit': render_to_string('admin_finansi_promo_edit.html', context2)}
                return JsonResponse(context2_tmp)

            if 'username' in request.GET and 'transaction' not in request.GET \
                    and 'add' not in request.GET:
                username_parsed = request.GET.get("username")
                db_user = User.objects.get(username=username_parsed)
                db_profile_add_info = ProfileAddInfo.objects.get(user=db_user.id)
                db_promo = Promo.objects.filter(whose=db_user.id)
                db_transactions = Transactions.objects.filter(user=db_user.id)
                context2 = {
                    'user_user': db_user,
                    'user_profile_add_info': db_profile_add_info,
                    'user_promo': db_promo,
                    'user_transactions': db_transactions,
                    'earned': "0",
                    'uname_for_link': db_user.username,
                }
                for promo in db_promo:
                    if promo.type == "INV":
                        context2['earned'] = int(promo.amount) * int(db_profile_add_info.invited_count)
                context2.update(csrf(request))
                context2_tmp = {'student_info': render_to_string('admin_finansi_info.html', context2)}
                return JsonResponse(context2_tmp)

            if 'username' in request.GET and 'transaction' in request.GET:
                username_parsed = request.GET.get("username")
                transaction_parsed = request.GET.get("transaction")
                db_user = User.objects.get(username=username_parsed)
                db_transactions = Transactions.objects.get(id=transaction_parsed)
                context2 = {
                    'user_user': db_user,
                    'user_transactions': db_transactions,
                    'uname_for_link': db_user.username,
                }
                context2.update(csrf(request))
                context2_tmp = {'transaction_change': render_to_string('admin_finansi_change.html', context2)}
                return JsonResponse(context2_tmp)

            if 'username' in request.GET and 'add' in request.GET:
                username_parsed = request.GET.get("username")
                db_user = User.objects.get(username=username_parsed)
                context2 = {
                    'user_user': db_user,
                    'uname_for_link': db_user.username,
                }
                context2.update(csrf(request))
                context2_tmp = {'transaction_add': render_to_string('admin_finansi_add.html', context2)}
                return JsonResponse(context2_tmp)
        promo_list = Promo.objects.exclude(type="INV")
        day_lasts = []
        for promo_obj in promo_list:
            last = (promo_obj.expires - datetime.date.today()).days
            day_lasts.append(last)
        promo_list_n_days = zip(promo_list, day_lasts)
        context['promo_list_n_days'] = promo_list_n_days
        all_users = User.objects.all()
        context['users'] = all_users
        profaddinfo_arr = []
        for user in all_users:
            profaddinfo = ProfileAddInfo.objects.get(user=user)
            profaddinfo_arr.append(profaddinfo)
        context['profaddinfo_user_zip'] = zip(all_users, profaddinfo_arr)
        context['uname_for_link'] = " "
        user_info(context, request)
        return render(request, 'admin_finansi.html', context)
    else:
        return redirect('account', request.user)


@login_required_custom
def private_account_account(request, user):
    if User.objects.filter(username=user).exists():
        tmp_id = User.objects.get(username=user).id
        gallery = Gallery.objects.filter(user=tmp_id).exclude(is_deleted=1)
        date_joined = str(User.objects.get(username=user).date_joined).split("-")[0]
        teacher_description = ProfileAddInfo.objects.get(user=tmp_id)
        context = {
            'gallery': gallery,
            'pics_count': len(gallery),
            'date_joined': date_joined,
            'teacher_description': teacher_description.about,
        }
        if request.method == "POST":
            if 'teacher_description' in request.POST:
                teacher_description_val = request.POST.get('teacher_description')
                teacher_description.about = teacher_description_val
                teacher_description.save()
                context['teacher_description'] = teacher_description_val
            if 'pic_name' in request.POST:
                pic = Gallery.objects.get(image=request.POST.get('pic_name').replace("/media/", ""))
                pic.delete()
            for file in request.FILES.getlist('file'):
                gallery_obj = Gallery.objects.create(user=request.user, image=file)
                pillow_image = resize_image(gallery_obj.image)
                gallery_obj.image_compressed.save(file.name, InMemoryUploadedFile(
                    pillow_image,  # file
                    None,  # field_name
                    file.name,  # file name
                    'image/jpeg',  # content_type
                    pillow_image.tell,  # size
                    None))
            context['gallery'] = Gallery.objects.filter(user=request.user).exclude(is_deleted=1)
            context['pics_count'] = len(gallery)
        user_info2 = User.objects.get(username=user)
        transactions = Transactions.objects.filter(user=request.user, type="payment")
        context['transactions'] = transactions
        context['guest_first_name'] = user_info2.first_name
        context['guest_last_name'] = user_info2.last_name
        context['guest_username'] = user_info2.username
        context['guest_ava'] = ProfileAddInfo.objects.get(user=User.objects.get(username=user).id)
        context['guest_signup_for_course'] = SignedUpForCourse.objects.filter(user=tmp_id)
        context['guest_transactions'] = Transactions.objects.filter(user=tmp_id, type="payment")
        user_info(context, request)
        if str(user) != str(request.user):
            context['guest'] = True
        return render(request, 'user.html', context)
    else:
        return HttpResponse('User doesn`t exist!')


@login_required_custom
def prepod_account(request):
    return render(request, "prepod_user.html")


@login_required_custom
def prepod_lesson_redac(request):
    return render(request, "prepod_lesson_redac.html")


@login_required_custom
def admin_people(request):
    if request.user.is_staff:
        context = {}
        if request.method == "POST":
            if "q_user_teach" in request.POST:
                pai_id = request.POST.get("q_user_teach")
                profaddinfo_instance = ProfileAddInfo.objects.get(id=pai_id)
                profaddinfo_instance.is_teacher = 1
                profaddinfo_instance.save()
            if "q_delete_teach" in request.POST:
                pai_id = request.POST.get("q_delete_teach")
                profaddinfo_instance = ProfileAddInfo.objects.get(id=pai_id)
                profaddinfo_instance.is_teacher = 0
                profaddinfo_instance.save()
            if "q_user_admin" in request.POST:
                u_id = request.POST.get("q_user_admin")
                user_instance = User.objects.get(id=u_id)
                user_instance.is_staff = 1
                user_instance.save()
        profaddinfo = ProfileAddInfo.objects.all()
        context['profaddinfo_list'] = profaddinfo
        user_info(context, request)
        return render(request, 'admin_people.html', context)
    else:
        return redirect('account', request.user)


def edit_lesson(request, lesson):
    context = {}
    if request.method == "POST":
        header = request.POST['lesson_header']
        webinar_url = request.POST['webinar_url']
        youtube_url = request.POST['youtube_url']
        homework_text = request.POST['txtarea_homework']
        part_num = request.POST['part_select']
        values_for_update = {
            'header': header, 'webinar_url': webinar_url,
            'youtube_url': youtube_url, 'homework_text': homework_text,
        }

        if part_num.isdigit():
            values_for_update['part'] = part_num

        if 'pdf_file' in request.FILES:
            pdf_file = request.FILES['pdf_file']
            values_for_update['pdf_route'] = pdf_file
        Lesson.objects.update_or_create(lesson_num=lesson, defaults=values_for_update)
        return redirect('lesson', lesson=lesson)
    elif request.method == "GET":
        lesson_context = Lesson.objects.get(lesson_num=lesson)
        context['lesson'] = lesson_context
        context['lesson_num'] = lesson

    user_info(context, request)
    context['parts'] = CourseParts.objects.all()
    return render(request, "prepod_edit_lesson.html", context)


def new_lesson(request):
    context = {}
    if request.method == "POST":
        zoom_url = request.POST['zoom_url']
        txtarea2 = request.POST['txtarea2']
        part_num = request.POST['part_select']
        lesson_num = len(Lesson.objects.all()) + 1
        Lesson.objects.create(lesson_num=lesson_num, header=request.POST['lesson_header'],
                              homework_text=txtarea2, webinar_url=zoom_url, part=part_num)

    user_info(context, request)
    context['parts'] = CourseParts.objects.all()
    return render(request, "prepod_new_lesson.html", context)


def enter_courses(request):
    """
    Лендинг

    :param request: детали запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера
    :rtype: :class:`django.http.HttpResponse`
    """
    error = ''
    flag = True
    free = 5
    if request.method == 'POST':
        form = CourseForm(request.POST)
        name = form.data['name']
        e_mail = form.data['e_mail']
        phone = form.data['phone']
        if form.is_valid():
            if Course.objects.filter(phone=phone).count() > 0 or Course.objects.filter(e_mail=e_mail).count() > 0:
                flag = False
            else:
                form.save()
            if flag:
                subject = "Добро пожаловать в фотошколу 1.4"
                curren_site = get_current_site(request)
                email_template_name = "welcome_to_school_email.html"
                c = {
                    'domain': curren_site.domain,
                    "email": e_mail,
                    'site_name': 'Website',
                    "user": name,
                    'protocol': request.scheme,
                }
                email = render_to_string(email_template_name, c)
                letter = EmailMessage(subject, email, to=[e_mail])
                letter.send()
        else:
            error = 'Что-то пошло не так...'
    number_of_count = Course.objects.count()
    places = free - number_of_count
    if places < 0:
        places = 0
    form = CourseForm()
    if places % 10 == 0 or 4 < places % 10 <= 9:
        place = ' мест'
    elif 1 < places % 10 < 5:
        place = ' места'
    else:
        place = ' место'
    context = {
        'places': place,
        'form': form,
        'error': error,
        'number_of_free': places,
        'flag': flag,
    }
    return render(request, 'main_page.html', context)
