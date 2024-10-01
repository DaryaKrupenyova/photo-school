"""django_sql_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.sitemaps import views as sitemap_views
from django.views.generic import TemplateView

from first.sitemaps import PrivateAccountStaticSitemap, AccountDynamicSitemap
from accounts.sitemaps import AccountStaticSitemap

from accounts.views import login_add
from first import views
from django.conf import settings
from django.conf.urls.static import static

sitemaps = {
    'private_account_static': PrivateAccountStaticSitemap,
    'account_dynamic': AccountDynamicSitemap,
    'account_static': AccountStaticSitemap,
}

handler404 = views.handler404
handler500 = views.handler500

urlpatterns = [
    path('private_account/', include('first.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('streams/', include('streams.urls')),
    path('', views.lending, name='lending'),
    path('authorization/', login_add, name='login'),
    path('telegramapi/', include('telegramapi.urls')),
    path('sitemap.xml', sitemap_views.index, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'sitemap-(?P<section>\w+).xml', sitemap_views.sitemap, {'sitemaps': sitemaps},
            name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain"
    )),
]
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
