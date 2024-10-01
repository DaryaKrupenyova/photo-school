from django.contrib import sitemaps
from django.urls import reverse


class AccountStaticSitemap(sitemaps.Sitemap):
    priority = 0.6
    changefreq = 'never'

    def items(self):
        return ['signup', 'signup_complete', 'password_reset', 'logout', 'login', 'lending']

    def location(self, item):
        return reverse(item)
