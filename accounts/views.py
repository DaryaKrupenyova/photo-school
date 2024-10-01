# Create your views here.
import string

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect
from django.core.mail import BadHeaderError, EmailMessage, EmailMultiAlternatives
from django.views.decorators.csrf import csrf_protect
from transliterate import translit
import random
from django.contrib import messages

from accounts.forms import UserSignUpForm
from accounts.token_generator import account_activation_token
from first.models import ProfileAddInfo, Promo


def make_username(f_name, l_name):
    """
    Создание уникального username включающего в себя имя и фамилию пользователя

    :param f_name: имя пользователя
    :param l_name: фамилия пользователя
    :return: объект ответа сервера
    :rtype: :class:`django.http.HttpResponse`
    """
    username = str(l_name) + str(f_name) + str(random.randint(0, 100000))
    username = translit(username, language_code='ru', reversed=True)
    username = username.replace('\'', '')
    username = username.lower()
    return username


def password_reset_request(request):
    """
    Отправка письма о восстановлении пароля

    :param request: детали запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера
    :rtype: :class:`django.http.HttpResponse`
    """
    context = {}
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    email_subject = "Восстановление пароля"
                    current_site = get_current_site(request)
                    message = render_to_string('registration/pasword_reset_email.html', {
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'domain': current_site.domain,
                        'protocol': request.scheme,
                    })
                    plain_message = strip_tags(message)
                    email = EmailMultiAlternatives(email_subject, plain_message, to=[data])
                    email.attach_alternative(message, 'text/html')
                    email.send()
                    return redirect("password_reset/done/")
            else:
                messages.error(request, 'Название содержит ошибку или почтового адреса нет в базе фотошколы.')
    password_reset_form = PasswordResetForm()
    context["password_reset_form"] = password_reset_form
    return render(request, "registration/password_reset.html", context)


def user_signup(request):
    """
    Регистрация пользователя

    :param request: детали запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера
    :rtype: :class:`django.http.HttpResponse`
    """
    if request.method == 'POST':
        logout(request)
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = make_username(form.data['first_name'], form.data['last_name'])
            password = User.objects.make_random_password()
            user.set_password(password)
            user.is_active = True
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Регистрация аккаунта'
            message = render_to_string('activate_account.html', {
                'password': password,
                'user': user,
                'domain': current_site.domain,
                'protocol': request.scheme,
            })
            plain_message = strip_tags(message)
            to_email = form.cleaned_data.get('email')
            email = EmailMultiAlternatives(email_subject, plain_message, to=[to_email])
            email.attach_alternative(message, 'text/html')
            email.send()
            login(request, user)
            values_for_update = {'avatar': '../static/images/stock_ava.jpg',
                                 'background': '0', 'user': request.user}
            ProfileAddInfo.objects.update_or_create(user=request.user, defaults=values_for_update)
            content = rand_string(10)
            Promo.objects.create(content=content, type="INV", amount=200,
                                 expires="9999-12-31", whose=request.user, times_can_use=100000)
            return redirect('signup_complete')
    else:
        form = UserSignUpForm()
    return render(request, 'signup.html', {'form': form})


def rand_string(size):
    """
    Функция создающая случайную строку длиной в size

    :param size: длина строки которую нужно сгенерировать
    :return: рандомно сгенерированная строка
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))


def deactivate_account(request, uidb64, token):
    """
    Деактивация аккаунта пользователя

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
        user.is_active = False
        user.save()

        return HttpResponse("Success!")
    else:
        return HttpResponse("Invalid link!")


# в этой функции есть повтор но при создании доп функции не работают куки, исправить
@csrf_protect
def login_add(request):
    """
    Надстройка над стоковым логином(можно зайти используя и логин, и почту)

    :param request: детали запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера
    :rtype: :class:`django.http.HttpResponse`
    """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            username_by_email = User.objects.get(email=username)
        except:
            username_by_email = None
        user = authenticate(username=username, password=password)
        user_by_email = authenticate(username=username_by_email, password=password)
        if user is not None:
            # повтор здесь
            if user.is_active:
                login(request, user)
                response = redirect('account', request.user)
                # response.set_cookie(key='background', value=back_color, max_age=10)
                return response
            else:
                return redirect('login')
        elif user_by_email is not None:
            # повтор здесь
            if user_by_email.is_active:
                login(request, user_by_email)
                response = redirect('account', request.user)
                # response.set_cookie(key='background', value=back_color, max_age=10)
                return response
            else:
                return redirect('login')
        else:
            messages.error(request, 'Хм, неверный пароль или логин, почта.<br>Попробуй вновь)')
            return redirect('login')
    elif request.method == "GET":
        if request.user.is_authenticated:
            return redirect('account', request.user)
        else:
            return render(request, 'registration/login.html')


def signup_complete(request):
    """
    Отображение страницы о подтверждении регистрации

    :param request: детали запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера
    :rtype: :class:`django.http.HttpResponse`
    """
    return render(request, "signup_complete.html")


def change_password(request):
    return render(request, "change_password.html")
