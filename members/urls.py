from django.conf.urls import patterns, url

from .views import LandingPage

urlpatterns = [
    url(r'^$', LandingPage.as_view(), name='landing_page'),
]
