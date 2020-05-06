#-*- coding: utf-8 -*-
import uuid , json , string , random, urllib, base64, os, sys, math, pytz, time
from django.utils.encoding import smart_str
from django.http import *
from django import template
from django.shortcuts import *
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from core.models import *
from django.conf import settings
from django.db.models import Q
from time import time as tmx
from datetime import datetime
#import arrow
data = {}


def landing(request):
    return render(request, "index.html", locals())


def privacy(request):
    return render(request, "privacy.html", locals())

def gizlilik(request):
    return render(request, "privacytr.html", locals())

def tos(request):
    return render(request, "tos.html", locals())

def tostr(request):
    return render(request, "tostr.html", locals())

@csrf_exempt
def logmein(request):
    data = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        facebookid = request.POST.get('facebookid')
        googleid = request.POST.get('googleid')
        deviceid = request.POST.get('deviceid')

        lang = request.POST.get('lang')
        if lang != "en" and lang != "tr" and lang != "nl" and lang != "de" and lang != "es":
            data["info"] = "only5lang"
            data["response"] = "non"
            return HttpResponse(json.dumps(data), content_type = "application/json")
        spesificname = "name_%s"% lang
        spesificexp = "explain_%s"% lang



        if facebookid:
            try:
                acc = User.objects.get(facebookid=facebookid)
                email = acc.email
                password = acc.password
            except User.DoesNotExist:
                data['response'] = "nof"
                data['info'] = "Hatalı kullanıcı adı veya şifre"
                return HttpResponse(json.dumps(data), content_type = "application/json")
        elif googleid:
            try:
                acc = User.objects.get(gmailid=googleid)
                email = acc.email
                password = acc.password
            except User.DoesNotExist:
                data['response'] = "nof"
                data['info'] = "Hatalı kullanıcı adı veya şifre"
                return HttpResponse(json.dumps(data), content_type = "application/json")

        if email and password:
            try:
                acc = User.objects.get(email=email)
            except User.DoesNotExist:
                data['response'] = "nof"
                data['info'] = "Hatalı kullanıcı adı veya şifre"
                return HttpResponse(json.dumps(data), content_type = "application/json")
            if deviceid:
                acc.notification = deviceid
                acc.save()
            step = "goal"
            alltestsarecomplated = False
            if acc.password == password:
                if acc.goal:
                    print ("Kullanıcının hedefi belli first step complated.")
                    step = "place"
                    if acc.place:
                        print ("Kullanıcının mekanı belli second step complated.")
                        step = ("traindayinweek")
                        if acc.traindayinweek:
                            print ("Kullanıcın haftada kaç gün çalışacağı belli -third step has been complated.")
                            step = "kilo"
                            if acc.height:
                                print ("Kullanıcının yüksekliği belli -fourth step has been complated.")
                                step = "kilo"
                                if acc.kilo:
                                    print ("Kullanıcın kilosu belli  -fourth step has been complated.")
                                    step = "btype"
                                    if acc.btype:
                                        print ("Kullanıcın kilosu belli  -fourth step has been complated.")
                                        step = "video"
                                        if acc.strongorlight:
                                            print ("Everything are working correctly.")
                                            step = "ok"
                                            alltestsarecomplated = True
                                        else:
                                            step = "video"
                                            alltestsarecomplated = False
                data['response'] = "ok"
                data['premium'] = acc.isitpremium
                data['alltestsarecomplated'] = alltestsarecomplated
                data['step'] =  step
                data['info'] = "Giriş başarılı"
                mypoint = 0
                if acc.point:
                    mypoint = acc.point

                acc.refresh_from_db()
                if acc.facebookid:
                    proimg = ("https://graph.facebook.com/%s/picture?type=large"% acc.facebookid)
                else:
                    proimg = ("http://drfit.training/media/%s"% acc.profilephoto.name)
                getmoresweet = {"id" : acc.id,
                     "facebookid": acc.facebookid,
                     "name": acc.name,
                     "surname": acc.surname,
                     "userpoint":mypoint,
                     "notification": acc.notification,
                     "email": acc.email,
                     "profileimg": proimg,
                     "password": acc.password,
                     "gender": acc.gender,
                     "deviceid":acc.deviceid,
                     "birthday":acc.birthday.strftime("%Y-%m-%d")}
                data['details'] = getmoresweet
                #data['details'] = [acc.id, acc.name, acc.lastname, acc.username, acc.image.name[2:]]
                return HttpResponse(json.dumps(data), content_type = "application/json")
            else:
                data['info'] = "Hatalı email veya şifre"
                data['response'] = "non"
                return HttpResponse(json.dumps(data), content_type = "application/json")
        else:
            data['response'] = "non"
            data['info'] = "Boş Alan Bırakmayın"
            return HttpResponse(json.dumps(data), content_type = "application/json")
    data['response'] = "Err"
    data['info'] = "Post RQ* only"
    return HttpResponse(json.dumps(data), content_type = "application/json")




@csrf_exempt
def getcategories(request, lang, userid):
    if request.method == 'GET':
        data = {}
        allofarray = []
        if lang != "en" and lang != "tr" and lang != "nl" and lang != "de" and lang != "es":
            data["info"] = "only5lang"
            data["response"] = "non"
            return HttpResponse(json.dumps(data), content_type = "application/json")
        spesificname = "name_%s"% lang
        spesificexp = "explain_%s"% lang
        print(userid)
        getkategoris = Category.objects.all()
        cate = []
        print (getkategoris.count())
        for y in getkategoris:
            suncates = []

            suncatezz = SubCategory.objects.filter(Ctgry=y)
            for jj in suncatezz:
                getprosfromplist = Programlist.objects.filter(psc=jj)
                plistify = []
                videolist = []
                movecount = 0
                for np in getprosfromplist:
                    if np:
                        if np.isitrest:
                            plistify.append({"isim": "rest", "duration": np.duration, "altyazi": [], "video" : "", "setcount": 0, "replycount": 0,"movecount": 0})
                        else:
                            movecount += 1
                            name = getattr(np.progrm, spesificname)
                            exp = getattr(np.progrm, spesificexp)
                            if not np.progrm.video.name in videolist:
                                videolist.append(np.progrm.video.name)
                                #tümvideolarıgösteren array için var!
                            subtitlexz = []
                            getsubtitles = SubtitleList.objects.filter(forwhichprogram=np.progrm,language=lang)
                            for x in getsubtitles:
                                subtitlexz.append(x.subtitle)

                            plistify.append({"isim": name, "duration": 0, "altyazi": subtitlexz, "video" : np.progrm.video.name, "setcount": np.setcount, "replycount": np.replycount,"movecount":movecount,"isitduration":np.isitduration})
                    else:
                        print ("oş")
                name = getattr(jj, spesificname)
                exp = getattr(jj, spesificexp)
                suncates.append({"isim": name, "id":jj.id, "aciklama": exp, "resim": "http://drfit.training/media/"+jj.image, "premium": jj.isitpremium,"totaltime":jj.totaltime,"place":jj.place,
                "programdetails": plistify, "allvideos": videolist })
            name = getattr(y, spesificname)
            exp  = getattr(y, spesificexp)
            cate.append({"isim": name, "aciklama": exp, "resim": "http://drfit.training/media/"+y.image, "subcate": suncates })
        #eğer her şey okeyse artık trainingini seçebilirsin demektir..

        try:
            acc = User.objects.get(id=int(userid))
        except User.DoesNotExist:
            data["message"] = "User id girmek zorunludur."
            data["response"] = "ok"
            return HttpResponse(json.dumps(data), content_type = "application/json")
        if acc.traindayinweek and acc.dailyprogramdetail:
            userselecteday = int(acc.traindayinweek)
            whereami = int(acc.dailyprogramdetail)
            mydprogram =  DailyProgram.objects.get(hedef=int(acc.goal),calismaalani=int(acc.place),kilotipi=int(acc.gender),guctipi=int(acc.strongorlight),guntipi=userselecteday)
            if acc.dailyprogramdetail:
                data['istestcomplated']= True

                getweek = math.ceil(int(acc.dailyprogramdetail)/userselecteday)
                if getweek == 0:
                    getweek = 1
                for j in range(1,(userselecteday+1)):
                    daylist = []
                    movecount = 0
                    dailyvideolist = []
                    getweeklyprograms = Programfordaily.objects.filter(overprogram=mydprogram,weeknumber=getweek,daynumber=j)
                    for x in getweeklyprograms:
                        if x:
                            getsubtitles = SubtitleList.objects.filter(forwhichprogram=x.progrm,language=lang)
                            if x.isitrest:
                                daylist.append({"isim": "rest", "duration": x.duration, "whichday":0, "altyazi":[],
                                "video" : "", "setcount":0, "replycount":0,"isitduration":"" })
                            else:
                                movecount += 1
                                subtitlexz = []
                                for j in getsubtitles:
                                    subtitlexz.append(j.subtitle)
                                name = getattr(x.progrm , spesificname)
                                exp = getattr(x.progrm , spesificexp)
                                if not x.progrm.video.name in dailyvideolist:
                                    dailyvideolist.append(x.progrm.video.name)
                                    #tümvideolarıgösteren array için var!

                                daylist.append({"isim": name, "duration":0, "whichday":x.daynumber, "altyazi": subtitlexz,
                                "video" : x.progrm.video.name, "setcount": x.setcount, "replycount": x.replycount, "isitduration" :x.isitduration})


                    allofarray.append({"daylist": daylist, "dailyvideolist":dailyvideolist,"movecount":movecount,"totaltime":mydprogram.totaltime,"place":mydprogram.calismaalani})
                    apdetail = 1
                    if acc.onemonthlater:
                        oldtime = arrow.get(acc.onemonthlater).to("Europe/Istanbul").timestamp
                        lasttime = arrow.utcnow().to("Europe/Istanbul").timestamp
                        if oldtime > lasttime:
                            data["recheck"] = False
                        else:
                            data["recheck"] = True
                    if acc.goal:
                        if lang == "tr":
                            if int(acc.goal) == 1:
                                data["usergoal"] = "Estetik & Atletik Vücut"
                            elif int(acc.goal) == 2:
                                data["usergoal"] = "Performans & Yağ Yakımı"
                            else:
                                data["usergoal"] = "Kuvvet & Hacim"
                        else:
                            if int(acc.goal) == 1:
                                data["usergoal"] = "Aesthetic & Fit Body"
                            elif int(acc.goal) == 2:
                                data["usergoal"] = "Performance & Fat Burn"
                            else:
                                data["usergoal"] = "Strength & Bulking"


                    if acc.place:
                        if lang == "tr":
                            if int(acc.place) == 1:
                                data["userplace"] = "Vücut Ağırlığı"
                            else:
                                data["userplace"] = "Serbest Ağırlık"
                        else:
                            if int(acc.goal) == 1:
                                data["userplace"] = "Body Weight"
                            else:
                                data["userplace"] = "Free Weight"


                    oldtime = arrow.get(acc.lasttenhours).to("Europe/Istanbul").timestamp
                    lasttime = arrow.utcnow().to("Europe/Istanbul").timestamp
                    if oldtime > lasttime:
                        apdetail = int(acc.dailyprogramdetail) - 1
                        data["isnextvideoavailable"] = "waiting"
                    else:
                        apdetail = acc.dailyprogramdetail
                        data["isnextvideoavailable"] = "programisready"
                    data['apdetail'] = apdetail
                    data['userselecteday'] = userselecteday
                    if userselecteday == 3:
                        data['isitokey'] = "Kullanıcı 3 günlükte"
                        if apdetail == 0:
                            data['dayinweekforarray']= 1

                        elif apdetail % 3 == 0:
                            data['dayinweekforarray']= 2
                        elif apdetail % 3 == 1:
                            data['dayinweekforarray']= 0
                        elif apdetail % 3 == 2:
                            data['dayinweekforarray']= 1
                    elif userselecteday == 4:
                        data['isitokey'] = "Kullanıcı 4 günlükte"
                        if apdetail == 0:
                            data['dayinweekforarray']= 1
                        elif apdetail % 4 == 0:
                            data['dayinweekforarray']= 3
                        elif apdetail % 4 == 1:
                            data['dayinweekforarray']= 0
                        elif apdetail % 4 == 2:
                            data['dayinweekforarray']= 1
                        elif apdetail % 4 == 3:
                            data['dayinweekforarray']= 2
                    elif userselecteday == 5:
                        data['isitokey'] = "Kullanıcı 5 günlükte"
                        if apdetail == 0:
                            data['dayinweekforarray']= 1
                        elif apdetail % 5 == 0:
                            data['dayinweekforarray']= 4
                        elif apdetail % 5 == 1:
                            data['dayinweekforarray']= 0
                        elif apdetail % 5 == 2:
                            data['dayinweekforarray']= 1
                        elif apdetail % 5 == 3:
                            data['dayinweekforarray']= 2
                        elif apdetail % 5 == 4:
                            data['dayinweekforarray']= 3



                    bimgs = []
                    images = bimglist.objects.get(id=1)
                    bimgs.append("http://drfit.training/media/"+images.firstimage)
                    bimgs.append("http://drfit.training/media/"+images.secondimage)
                    bimgs.append("http://drfit.training/media/"+images.thirthimage)
                    bimgs.append("http://drfit.training/media/"+images.fourthimage)
                    bimgs.append("http://drfit.training/media/"+images.fiveimage)
                    data["imagelist"] = bimgs
            else:
                data['istestcomplated']= False
        else:
            data['istestcomplated']= False
        data["category"] = cate
        data['personalprogram'] = allofarray
        data["isuserpremium"] = acc.isitpremium
        data["response"] = "ok"
        return HttpResponse(json.dumps(data), content_type = "application/json")

@csrf_exempt
def gymlasium(request):
    if request.method == 'GET':
        data = {}
        getpersons = User.objects.all().order_by('point')[::-1][0:10]
        glist = []
        for x in getpersons:
            mypoint = 0
            if x.point:
                mypoint = x.point
            if x.facebookid:
                proimg = ("https://graph.facebook.com/%s/picture?type=large"% x.facebookid)
            else:
                proimg = ("http://drfit.training/media/%s"% x.profilephoto.name)
            glist.append({"isim": x.name, "puan": mypoint, "resim": proimg, "premium": x.isitpremium})
        data["gymlasium"] = glist
        data["response"] = "ok"
        return HttpResponse(json.dumps(data), content_type = "application/json")
