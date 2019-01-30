from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path, include

from process.views import *

urlpatterns = [
    url(r'^text$', Bot.as_view(), name='text'),
    url(r'^webhook', Verify.as_view(), name='webhook'),
    url(r'^privacy', privacy, name='privacy'),

]
