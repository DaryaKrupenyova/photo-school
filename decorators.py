from django.shortcuts import redirect
from django.urls import reverse
from first.models import ProfileAddInfo, Courses, SignedUpForCourse


def login_required_custom(func=None):
    def wrapper(request, user="without args"):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        else:
            if user == "without args":
                return func(request)
            else:
                return func(request, user)

    return wrapper


def active_required(func=None):
    def wrapper(request):
        if not request.user.is_active:
            return redirect("/accounts/login")
        else:
            return func(request)

    return wrapper


def can_pay(func=None):
    def wrapper(request):
        if int(ProfileAddInfo.objects.get(user=request.user).wallet) < int(Courses.objects.get(course_num=1).price):
            return redirect(reverse('finances'))
        else:
            return func(request)

    return wrapper


def is_in_course(func=None):
    def wrapper(request):
        if len(SignedUpForCourse.objects.filter(course_num=1, user=request.user)) < 1:
            return redirect(reverse('landing'))
        else:
            return func(request)

    return wrapper
