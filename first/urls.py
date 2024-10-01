from django.urls import path, re_path

from first import views

urlpatterns = [
    path('courses/', views.private_account_courses, name="courses"),
    path('remangotor/', views.remangotor, name="remangotor"),
    path('lesson/<int:lesson>', views.private_account_lesson, name="lesson"),
    re_path(r'^(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
            views.change_email_confirm, name='change_email_confirm'),
    path('account/<str:user>', views.private_account_account, name="account"),
    path('settings/', views.private_account_settings, name="settings"),
    path('finance/', views.empty_fin, name="finances"),
    path('question/', views.question, name="question"),
    path('group/', views.group, name="group"),
    path('admin_finance/', views.admin_fin, name="admin_fin"),
    path('admin_people/', views.admin_people, name="admin_people"),
    path('courses_2/', views.courses, name="courses_2"),
    path('prepod_account/', views.prepod_account, name="prepod_account"),
    path('prepod_lesson_redac/', views.prepod_lesson_redac, name="prepod_lesson_redac"),
    path('lesson_edit/<int:lesson>', views.edit_lesson, name="lesson_edit"),
    path('new_lesson/', views.new_lesson, name="new_lesson"),
    path('homework/<int:lesson>/<int:user>', views.private_account_homework, name="homework"),
    path('prepod_homeworks/', views.prepod_homeworks, name="prepod_homeworks"),
    path('dev_page/', views.dev_page, name="dev_page"),
    path('error_404/', views.error_404, name="error_404"),
    path('error_5XX/', views.error_5XX, name="error_5XX"),
    path('error_invalid_link/', views.error_invalid_link, name="error_invalid_link"),
]
