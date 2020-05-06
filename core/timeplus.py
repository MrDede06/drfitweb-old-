    #-*- coding: utf-8 -*-
import uuid , json , string , random, urllib, base64, os, sys
from django.utils.encoding import smart_str
from django.http import *
from django import template
from django.shortcuts import *
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.conf import settings
from django.db.models import Q
import pytz
from core.models import *
from datetime import datetime
from time import time as tmx
import time
#import arrow



@csrf_exempt
def personalprogramcomplated(request):
    data = {}
    if request.method == 'POST':
        userid = request.POST.get('userid')
        acc = User.objects.get(id=int(userid))
        oldtime = arrow.get(acc.lasttenhours).to("Europe/Istanbul").timestamp
        lasttime = arrow.utcnow().to("Europe/Istanbul").timestamp
        if oldtime > lasttime:
            data["status"] = "Bekle..."
            data['point'] = acc.point
        else:
            nowtime = arrow.utcnow().to("Europe/Istanbul").shift(hours=+10).datetime #pytz.timezone("Europe/Istanbul")
            acc.dailyprogramdetail = int(acc.dailyprogramdetail) + 1
            acc.lasttenhours = nowtime
            if acc.point:
                acc.point = int(acc.point) + 100
                acc.save()
                acc.refresh_from_db()
                data['point'] = acc.point
            else:
                acc.point = 100
                acc.save()
                acc.refresh_from_db()
                data['point'] = 100


            #data["nowtime"] = "aktif olacağı zaman :" + nowtime.humanize()
            data["status"] = "Zaman doldu."


        data["oldtime"] = oldtime
        data["lasttime"] = lasttime
        data["name"] = acc.name
        data['response'] = "ok"
        data['info'] = "Post RQ* only(\::/)"
        return HttpResponse(json.dumps(data), content_type = "application/json")
    else:
        data['response'] = "non"
        data['info'] = "Post RQ* only."
        return HttpResponse(json.dumps(data), content_type = "application/json")

@csrf_exempt
def freesubcomplated(request):
    data = {}
    if request.method == 'POST':
        userid = request.POST.get('userid')
        subcateid = request.POST.get('subcateid')
        acc = User.objects.get(id=int(userid))
        subcate = SubCategory.objects.get(id=int(subcateid))
        try:
            xnxx = CateEarn.objects.get(EarnerUser=acc,Subcate=subcate)
        except CateEarn.DoesNotExist:
            if acc.point:
                acc.point = int(acc.point) + 100
            else:
                acc.point = 100
            acc.save()
            acc.refresh_from_db()
            addnewcateearn = CateEarn(EarnerUser=acc,Subcate=subcate)
            addnewcateearn.save()
            data['response'] = "ok"
            data['point'] = acc.point
            return HttpResponse(json.dumps(data), content_type = "application/json")
        data['response'] = "ae"
        data['point'] = acc.point
        return HttpResponse(json.dumps(data), content_type = "application/json")

    else:
        data['response'] = "non"
        data['info'] = "Post RQ* only."
        return HttpResponse(json.dumps(data), content_type = "application/json")


@csrf_exempt
def socaialearn(request):
    data = {}
    if request.method == 'POST':
        userid = request.POST.get('userid')
        try:
            acc = User.objects.get(id=int(userid))
        except User.DoesNotExist:
            data['response'] = "non"
            return HttpResponse(json.dumps(data), content_type = "application/json")
        if acc.point:
            acc.point = int(acc.point) + 10
        else:
            acc.point = 10
        acc.save()
        acc.refresh_from_db()
        data['response'] = "ok"
        data['point'] = acc.point
        return HttpResponse(json.dumps(data), content_type = "application/json")

    else:
        data['response'] = "non"
        data['info'] = "Post RQ* only."
        return HttpResponse(json.dumps(data), content_type = "application/json")



@csrf_exempt
def checkOtherLecture(request):
    data = {}
    if request.method == 'POST':
        userid = request.POST.get('userid')
        acc = User.objects.get(id=int(userid))
        oldtime = arrow.get(acc.lasttenhours).to("Europe/Istanbul").timestamp
        lasttime = arrow.utcnow().to("Europe/Istanbul").timestamp

        if oldtime > lasttime:
            data["status"] = "Bekle..."
        else:
            data["status"] = "Zaman doldu."

        data["oldtime"] = oldtime
        data["lasttime"] = lasttime

        #data["lasttime"] = lasttime.strftime("%Y-%m-%d %H:%M")
        data['response'] = "ok"
        return HttpResponse(json.dumps(data), content_type = "application/json")
    else:
        data['response'] = "non"
        data['info'] = "Post RQ* only."
        return HttpResponse(json.dumps(data), content_type = "application/json")

@csrf_exempt
def buypremium(request):
    data = {}
    if request.method == 'POST':
        lang = request.POST.get('lang')
        rdata  = request.POST.get('rdata')
        userid = request.POST.get('userid')
        product_id = request.POST.get('product_id')
        acc = User.objects.get(id=int(userid))

        if product_id == "1MONTHSUBSCRIPTION":
            onemonthlater = arrow.utcnow().to("Europe/Istanbul").shift(months=+1).datetime
        elif product_id == "3MONTHSUBS":
            onemonthlater = arrow.utcnow().to("Europe/Istanbul").shift(months=+3).datetime
        elif product_id == "1YEARSUBS":
            onemonthlater = arrow.utcnow().to("Europe/Istanbul").shift(years=+1).datetime
        else:
            onemonthlater = arrow.utcnow().to("Europe/Istanbul").shift(months=+1).datetime


        acc.premium = onemonthlater
        acc.isitpremium = True
        acc.save()
        ntr = Transactions(Buyer=acc,receiptData=rdata,TierPrice=product_id)
        ntr.save()
        data['response'] = "ok"
        return HttpResponse(json.dumps(data), content_type = "application/json")
    else:
        data['response'] = "non"
        data['info'] = "Post RQ* only."
        return HttpResponse(json.dumps(data), content_type = "application/json")
