#-*- coding: utf-8 -*-
import uuid , json , string , random, urllib, base64, os, arrow 
from django.utils.encoding import smart_str
from django.http import *
from django import template
from django.shortcuts import *
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from core.models import *
from django.conf import settings
from datetime import datetime
import pytz
from django.db.models import Q
from time import time as tmx
import time
data = {}




@csrf_exempt
def collectpersonaldatafromuser(request):
    data = {}
    if request.method == 'POST':
        step = request.POST.get('step')
        infotype = request.POST.get('type')
        lang = request.POST.get('lang')
        userid = request.POST.get('userid')
        userwidth = request.POST.get('userwidth')
        userheight = request.POST.get('userheight')
        userpower = request.POST.get('userpower')



        response = "Great"
        data["response"] = "ok"

        if lang != "en" and lang != "tr" and lang != "nl" and lang != "de" and lang != "es":
            data["info"] = "only5lang"
            data["response"] = "non"
            return HttpResponse(json.dumps(data), content_type = "application/json")
        acc = User.objects.get(id=int(userid))
        if int(step) == 1:
            #adam eğer buradaysa estetik performans veya hipertropi seçebilir.
            print ("Birinci steptesiniz")
            if infotype == "1" or infotype == "2" or infotype == "3":
                try:
                    acc = User.objects.get(id=userid)
                except User.DoesNotExist:
                    data["response"] = "non"
                    response = "Böyle bir kullanıcı bulamadım."
                acc.goal = infotype
                acc.save()
                response = ("1. stepte sorun yok %s sectiniz."% infotype)
            else:
                data["response"] = "non"
                response = "yanlış tip seçimi step (1) veya tip hatalı olabilir."
        elif int(step) == 2:
            if infotype == "1" or infotype == "2" or infotype == "3":
                try:
                    acc = User.objects.get(id=userid)
                except User.DoesNotExist:
                    data["response"] = "non"
                    response = "Böyle bir kullanıcı bulamadım."
                acc.place = infotype
                acc.save()
                response = ("2. steptede sorun yok %s sectiniz."% infotype)
            else:
                data["response"] = "non"
                response = "yanlış tip seçimi step (2) veya tip hatalı olabilir."
        elif int(step) == 3:
            if int(infotype) == 3 or int(infotype) == 4 or int(infotype) == 5:
                try:
                    acc = User.objects.get(id=userid)
                except User.DoesNotExist:
                    data["response"] = "non"
                    response = "Böyle bir kullanıcı bulamadım."
                acc.traindayinweek = infotype
                acc.save()
                response = ("ucuncu steptede sorun yok %s sectiniz."% infotype)
            else:
                data["response"] = "non"
                response = ("hatali tip secimi step (3) veya tip hatali olabilir. %s"% infotype)
        elif int(step) == 4:
            if userwidth and userheight:
                try:
                    acc = User.objects.get(id=userid)
                except User.DoesNotExist:
                    data["response"] = "non"
                    response = "Böyle bir kullanıcı bulamadım."
                acc.height = int(userheight)
                acc.kilo = int(userwidth)
                acc.usertype =  int(calculeta(userwidth, userheight))

                data["extra"] = calculeta(userwidth, userheight)
                acc.save()
                response = ("Dont hava any problem user width is : %s and user height is %s"% (userwidth,userheight))
            else:
                data["response"] = "non"
                response = ("hatali tip secimi step (4) veya tip hatali olabilir. %s"% infotype)
        elif int(step) == 5:
            if int(infotype) == 1 or int(infotype) == 2 or int(infotype) == 3:
                try:
                    acc = User.objects.get(id=userid)
                except User.DoesNotExist:
                    data["response"] = "non"
                    response = "Böyle bir kullanıcı bulamadım."
                acc.btype = infotype
                acc.save()
                response = ("Besinci steptede sorun yok %s sectiniz."% infotype)
            else:
                data["response"] = "non"
                response = ("hatali tip secimi step (5) veya tip hatali olabilir. %s"% infotype)
        elif int(step) == 6:
            if userpower:
                try:
                    acc = User.objects.get(id=userid)
                except User.DoesNotExist:
                    data["response"] = "non"
                    response = "Böyle bir kullanıcı bulamadım."
                acc.setsayisi = "0"
                acc.suresayisi = "0"
                acc.strongorlight = userpower
                acc.dailyprogramdetail = 1

                acc.lasttenhours = arrow.utcnow().to("Europe/Istanbul").datetime
                acc.onemonthlater =arrow.utcnow().to("Europe/Istanbul").shift(months=+1).datetime # arrow.utcnow().to("Europe/Istanbul").datetime
                acc.save()
                response = ("Besinci steptede sorun yok %s sectiniz."% infotype)
            else:
                data["response"] = "non"
                response = ("hatali tip secimi step (5) veya tip hatali olabilir. %s"% infotype)

        data["info"] = response
        return HttpResponse(json.dumps(data), content_type = "application/json")
    else:
        return HttpResponse("err")




@csrf_exempt
def getpre(request):
    data = {}
    if request.method == 'POST':
        userid = request.POST.get('userid')
        try:
            acc = User.objects.get(id=int(userid))
        except User.DoesNotExist:
            data["response"] = "non"
            data["info"] = "Böyle bir kullanıcı bulamadım."
            return HttpResponse(json.dumps(data), content_type = "application/json")
        if(acc.isitpremium):
            data["response"] = "ok"
            data["premium"] = True
            data["info"] = "Kullanıcı premium."
            return HttpResponse(json.dumps(data), content_type = "application/json")
        else:
            data["response"] = "ok"
            data["premium"] = False
            data["info"] = "Kullanıcı premium. değil"
            return HttpResponse(json.dumps(data), content_type = "application/json")
    else:
        data["response"] = "non"
        data["info"] = "POST only"
        return HttpResponse(json.dumps(data), content_type = "application/json")



def calculeta(userwidth, userheight):
    htype = "1"
    wtype = "1"
    usertype = "N"

    print ("user width is : %s"% userwidth)
    print ("user height is: %s"% userheight)

    userheight = int (userheight)
    userwidth = int(userwidth)

    if(userheight < 140):
        htype = "1"
    elif(userheight > 140 and userheight < 155):
        htype = "2"
    elif(userheight > 155 and userheight < 170):
        htype = "3"
    elif(userheight > 170 and userheight < 185):
        htype = "4"
    elif(userheight >= 185):
        htype = "5"


    if(userwidth <= 45):
        wtype = "1"
    elif(userwidth > 45 and userwidth < 55):
        wtype = "2"
    elif(userwidth > 55 and userwidth < 75):
        wtype = "3"
    elif(userwidth > 75 and userwidth < 95):
        wtype = "4"
    elif(userwidth >= 95):
        wtype = "5"
    ourcombination = ("%s%s"% (wtype,htype))

    print ("YOUR_CODE %s"% ourcombination)
    #zayif : 1,  normal 2, fazla kilo :3
    if(ourcombination == "11"):
        usertype = "2"
    elif(ourcombination == "12"):
        usertype = "2"
    elif(ourcombination == "13"):
        usertype = "2"
    elif(ourcombination == "14"):
        usertype = "1"
    elif(ourcombination == "15"):
        usertype = "1"
    elif(ourcombination == "21"):
        usertype = "3"
    elif(ourcombination == "22"):
        usertype = "2"
    elif(ourcombination == "23"):
        usertype = "2"
    elif(ourcombination == "24"):
        usertype = "1"
    elif(ourcombination == "25"):
        usertype = "1"
    elif(ourcombination == "31"):
        usertype = "3"
    elif(ourcombination == "32"):
        usertype = "3"
    elif(ourcombination == "33"):
        usertype = "2"
    elif(ourcombination == "34"):
        usertype = "2"
    elif(ourcombination == "35"):
        usertype = "1"
    elif(ourcombination == "41"):
        usertype = "3"
    elif(ourcombination == "42"):
        usertype = "3"
    elif(ourcombination == "43"):
        usertype = "3"
    elif(ourcombination == "44"):
        usertype = "2"
    elif(ourcombination == "45"):
        usertype = "2"
    elif(ourcombination == "51"):
        usertype = "3"
    elif(ourcombination == "52"):
        usertype = "3"
    elif(ourcombination == "53"):
        usertype = "3"
    elif(ourcombination == "54"):
        usertype = "3"
    elif(ourcombination == "55"):
        usertype = "3"
    else:
        usertype = "FAIL"

    #return combination
    return usertype


@csrf_exempt
def regmein(request):
    data = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('gender')
        facebookid = request.POST.get('facebookid')
        googleid = request.POST.get('googleid')
        phonetype = request.POST.get('phonetype')
        lang = request.POST.get('lang')
        notif = request.POST.get('notif')


        if name and surname and email and password and birthday and gender and phonetype:
            try:
                acc = User.objects.get(email=email)
            except User.DoesNotExist:
                regmeinplease = User(name=name,
                surname=surname,
                email=email,
                password=password,
                birthday=birthday,
                gender=gender,
                facebookid=facebookid,
                gmailid=googleid,
                phonetype=phonetype,
                isitpremium=False)
                regmeinplease.save()
                data['info'] = "Kayıt Başarılı"
                data['response'] = "ok"
                return HttpResponse(json.dumps(data), content_type = "application/json")
            data['info'] = "Bu email ile kayıtlı bir üye zaten mevcut"
            data['response'] = "non"
            return HttpResponse(json.dumps(data), content_type = "application/json")
        else:
            print(name, email, password, birthday, gender, gender, phonetype)
            data['response'] = "non"
            data['info'] = "Boş alan bırakmayın."
            return HttpResponse(json.dumps(data), content_type = "application/json")



@csrf_exempt
def forgotpassword(request):
    if request.method == 'POST':
        data = {}
        email = request.POST.get('email')
        lang = request.POST.get('lang')
        if lang != "en" and lang != "tr" and lang != "nl" and lang != "de" and lang != "es":
            data["info"] = "only5lang"
            data["response"] = "non"
            return HttpResponse(json.dumps(data), content_type = "application/json")
        data["info"] = "Your new password has been send."
        data["response"] = "ok"
        return HttpResponse(json.dumps(data), content_type = "application/json")

@csrf_exempt
def onemoremonth(request):
    if request.method == 'POST':
        data = {}
        userid = request.POST.get('id')
        try:
            acc = User.objects.get(id=int(userid))
        except User.DoesNotExist:
            data["message"] = "User id girmek zorunludur."
            data["response"] = "non"
            return HttpResponse(json.dumps(data), content_type = "application/json")
        acc.onemonthlater =arrow.utcnow().to("Europe/Istanbul").shift(months=+1).datetime
        acc.save()
        data["message"] = "Bir ay daha başarı ile eklendi"
        data["response"] = "ok"
        return HttpResponse(json.dumps(data), content_type = "application/json")





@csrf_exempt
def editdetails(request):
    if request.method == 'POST':
        data = {}
        lang = request.POST.get('lang')
        userid = request.POST.get('userid')
        name = request.POST.get('name').encode('utf-8')
        email = request.POST.get('email').encode('utf-8')
        password = request.POST.get('password').encode('utf-8')
        gender = request.POST.get('gender')
        birthdayy = request.POST.get('birthday')
        surname = request.POST.get('surname').encode('utf-8')

        notification = request.POST.get('notification')
        print(notification)
        print(userid)
        print(name)
        print(surname)
        print(password)
        print(birthdayy)
        print(gender)

        if lang != "en" and lang != "tr" and lang != "nl" and lang != "de" and lang != "es":
            data["info"] = "only5lang"
            data["response"] = "non"
            return HttpResponse(json.dumps(data), content_type = "application/json")
        if userid:
            try:
                acc = User.objects.get(id=int(userid))
            except User.DoesNotExist:
                data['response'] = "non"
                data['info'] = "Kullanıcı bulunamadı"
                return HttpResponse(json.dumps(data), content_type = "application/json")
            acc.name = name
            acc.surname = surname
            acc.email = email
            if password:
                acc.password = password
            acc.birthday = birthdayy
            acc.gender = gender
            acc.notification = notification
            acc.save()
            acc.refresh_from_db()
            getmoresweet = {"id" : acc.id,
                 "facebookid": acc.facebookid,
                 "name": acc.name,
                 "surname": acc.surname,
                 "notification": acc.notification,
                 "email": acc.email,
                 "profileimg": ("http://drfit.training/media/%s"% acc.profilephoto.name),
                 "password": acc.password,
                 "gender": acc.gender,
                 "deviceid":acc.deviceid,
                 "birthday":acc.birthday.strftime("%Y-%m-%d")}
            data['details'] = getmoresweet
            data['response'] = "ok"
            data['info'] = "Bilgileriniz başarıyla güncellendi."
            return HttpResponse(json.dumps(data), content_type = "application/json")
        else:
            data["info"] = "Userid bulunamadı..."
            data["response"] = "non"
            return HttpResponse(json.dumps(data), content_type = "application/json")

    else:
        data["info"] = "ONLY POST RQ*"
        data["response"] = "non"
        return HttpResponse(json.dumps(data), content_type = "application/json")


@csrf_exempt
def updateprofilephoto(request):
    if request.method == 'POST':
        data = {}
        checkfile = request.FILES.get('file', False)
        lang = request.POST.get('lang')
        userid = request.POST.get('userid')
        file = request.FILES['file']
        file_type = file.content_type.split('/')[1]
        if checkfile:
            file = request.FILES['file']
            file_type = file.content_type.split('/')[1]
            print (file_type)
            print (file._size)
            print (file.content_type)
            if file._size > 5000000 and file2._size > 5000000 and file3._size > 5000000:
                data['response'] = "non"
                data['info'] = "Bir resmin boyutu 2 MB geçemez"
                return HttpResponse(json.dumps(data), content_type = "application/json")
            if userid:
                acc = User.objects.get(id=userid)
                acc.profilephoto = request.FILES['file']
                acc.save()
                data['response'] = "ok"
                data['info'] = "Profil fotoğrafınız başarıyla güncellendi."
                data["profileimg"] = ("http://drfit.training/media/%s"% acc.profilephoto.name) #acc.profilephoto.name
                return HttpResponse(json.dumps(data), content_type = "application/json")
        else:
            data['response'] = "non"
            data['info'] = "Resim ve id göndermek zorundasın."
            return HttpResponse(json.dumps(data), content_type = "application/json")
    else:
        data['response'] = "non"
        data['info'] = "Post RQ* only."
        return HttpResponse(json.dumps(data), content_type = "application/json")
