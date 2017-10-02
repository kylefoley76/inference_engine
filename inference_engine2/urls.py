"""inference_engine2 URL Configuration

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
from inference2 import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^dictionary$', views.dictionary, name='result'),
    url(r'^prove$', views.prove, name='prove'),
    url(r'^export_xlsx/(?P<archives_id>[0-9]+)$',
        views.export_xlsx, name='export_xlsx'),
    url(r'^progress$', views.progress, name='progress'),
    url(r'^archives$', views.archives, name='archives'),
    url(r'^files$', views.download_files, name='archives'),
    url(r'^archives/(?P<num>[0-9]+)$',
        views.assign_archives, name='assign_archives'),
    url(r'^archives/(?P<num>[0-9]+)/(?P<type>[a-z]+)$',
        views.assign_archives, name='assign_archives_type'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^getdict$', views.getdict, name='getdict'),
    url(r'^author', views.author, name='author'),
    url(r'^tested_dict', views.tested_dictionary, name='tested_dictionary'),
    url(r'^try_input', views.try_input, name='try_input'),
    url(r'^clear', views.clear, name='clear-result'),


]
