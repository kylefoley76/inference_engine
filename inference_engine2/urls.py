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
from django.conf.urls.static import static
from django.contrib import admin
from inference2 import views
from inference_engine2 import settings

urlpatterns = [

    url(r'^version1/$', views.version1_view, name='version1'),
    url(r'^version1/test_machine/$', views.try_input, name='version1_try_input'),
    url(r'^versions/$', views.version_view, name='versions'),
    url(r'^versions/(?P<version>[0-9]+)/details/$', views.version_details, name='version_details'),
    url(r'^version/(?P<version_item>[0-9]+)/dictionary/$', views.version_dictionary, name='version_dictionary'),

    url(r'^version1/dictionary$', views.dictionary, name='dict-result'),
    url(r'^tested_dictionary$', views.tested_dict, name='result'),
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


    url(r'^$', views.try_input, name='try_input'),
    url(r'^clear_output', views.clear_output, name='clear_output'),
    url(r'^clear', views.clear, name='clear-result'),

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
