"""profconn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from companies.views import CompanyViewSet
from members.views import PersonViewSet, ExperienceViewSet, ConnectionViewSet

# REST API
router = DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'experiences', ExperienceViewSet)
router.register(r'connections', ConnectionViewSet)
router.register(r'companies', CompanyViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    # Normal view routes.
    url(r'^', include('members.urls', namespace='member')),

    # REST API
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api-docs/', include('rest_framework_swagger.urls'))
]
