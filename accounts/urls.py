from django.urls import path, re_path

from .views import user_signup, password_reset_request, deactivate_account, login_add, signup_complete, change_password
from django.contrib.auth import views as dj_contrib_views

urlpatterns = [
    path('signup/', user_signup, name='signup'),
    path('signup_complete/', signup_complete, name="signup_complete"),
    path("password_reset", password_reset_request, name="password_reset"),
    path('password_reset/done/', dj_contrib_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_did.html'
    ), name='password_reset_done'),
    path('logout/', dj_contrib_views.LogoutView.as_view(), name='logout'),
    path('change_password/', change_password, name=""),
    re_path(r'^deactivate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
            deactivate_account, name='deactivate'),
    path('reset/<uidb64>/<token>/', dj_contrib_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirmed_base.html"
    ), name='password_reset_confirm'),
    path('reset/done/', dj_contrib_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_confirmed_did.html'
    ), name='password_reset_complete'),
]
