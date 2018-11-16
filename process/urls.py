from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path, include

from process.views import Convert

urlpatterns = [
    url(r'^upload/(?P<filename>[^/]+)$', Convert.as_view())
]
