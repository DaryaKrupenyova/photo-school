from django.contrib import sitemaps
from django.contrib.auth.models import User
from django.urls import reverse


class PrivateAccountStaticSitemap(sitemaps.Sitemap):
    priority = 0.6
    changefreq = 'never'

    def items(self):
        return ['courses', 'settings', 'finances', 'question', 'group', 'admin_fin', 'new_lesson']

    def location(self, item):
        return reverse(item)


class AccountDynamicSitemap(sitemaps.Sitemap):
    priority = 0.6
    changefreq = 'always'

    def items(self):
        return User.objects.all()

    def location(self, obj):
        return reverse('account', args=[obj.username])

    def lastmod(self, obj):
        return obj.last_login
