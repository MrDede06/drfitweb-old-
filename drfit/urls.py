# -*- coding: utf-8 -*-
import uuid , json , string , random, urllib, time, datetime
from django.http import *
from django import template
from django.shortcuts import  render
from django.urls import reverse
from django.contrib.auth import logout
from django.conf.urls import url
from django.conf import settings
from django.utils import translation
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from random import randint
from django.db.models import Q
from django.contrib import admin
from django.conf.urls.static import static
import core.views, core.posts, core.timeplus
#import  web 
from .web import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^privacy/', core.views.privacy),
    url(r'^tos/', core.views.tos),
    url(r'^gizlilik/', core.views.gizlilik),
    url(r'^kullanimsartlari/', core.views.tostr),

    url(r'^$', core.views.landing),
    url(r'^api/v1/logmein/$', core.views.logmein, name='logmein'),
    url(r'^api/v1/regmein/$', core.posts.regmein, name='regmein'),
    url(r'^api/v1/editdetails/$', core.posts.editdetails, name='editdetails'),
    url(r'^api/v1/forgotpassword/$', core.posts.forgotpassword, name='forgotpassword'),
    url(r'^api/v1/updateprofilephoto/$', core.posts.updateprofilephoto, name='updateprofilephoto'),
    url(r'^api/v1/getcategories/(?P<lang>\w+)/(?P<userid>\w+)/$', core.views.getcategories, name='getcategories'),
    url(r'^api/v1/gymlasium/$', core.views.gymlasium, name='gymlasium'),
    url(r'^api/v1/collectpersonaldatafromuser/$', core.posts.collectpersonaldatafromuser, name='collectpersonaldatafromuser'),
    url(r'^api/v1/personalprogramcomplated/$', core.timeplus.personalprogramcomplated, name='personalprogramcomplated'),
    url(r'^api/v1/checkOtherLecture/$', core.timeplus.checkOtherLecture, name='checkOtherLecture'),
    url(r'^api/v1/freesubcomplated/$', core.timeplus.freesubcomplated, name='freesubcomplated'),
    url(r'^api/v1/socaialearn/$', core.timeplus.socaialearn, name='socaialearn'),
    url(r'^api/v1/buypremium/$', core.timeplus.buypremium, name='buypremium'),
    url(r'^api/v1/onemoremonth/$', core.posts.onemoremonth, name='onemoremonth'),

    #yonetim
    url(r'^yonetim/$', yonetim, name='yonetim'),
    url(r'^addnv/$', addnv, name='addnv'),
    url(r'^videos/$', videos, name='videos'),
    url(r'^kategoriekle/$', kategoriekle, name='kategoriekle'),
    url(r'^altkategoriekle/$', altkategoriekle, name='altkategoriekle'),
    url(r'^sorular/$', sorular, name='sorular'),

    url(r'^kategoriprogrami/$', kategoriprogrami, name='kategoriprogrami'),
    url(r'^bireyselprogram/$', bireyselprogram, name='bireyselprogram'),
    url(r'^getsubcates/$', getsubcates, name='getsubcates'),
    url(r'^addcategoryfy/$', addcategoryfy, name='addcategoryfy'),
    url(r'^addaltcategoryfy/$', addaltcategoryfy, name='addaltcategoryfy'),
    url(r'^addnewstep/$', addnewstep, name='addnewstep'),
    url(r'^addnewbstep/$', addnewbstep, name='addnewbstep'),
    url(r'^userlist/$', userlist, name='userlist'),
    url(r'^searchmusteri/$', searchmusteri , name='searchmusteri'),
    url(r'^getlastuyeler/$', getlastuyeler, name='getlastuyeler'),
    url(r'^bireyselresimleri/$', bireyselresimleri, name='bireyselresimleri'),
    url(r'^addnewbimg/$', addnewbimg, name='addnewbimg'),
    url(r'^api/v1/getpre/$', core.posts.getpre, name='getpre'),






]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
