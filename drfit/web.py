#-*- coding: utf-8 -*-
import uuid , json , string , random, urllib, base64, os, sys
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
data = {}




def yonetim(request):
    return render(request, "userlist.html", locals())


def sorular(request):
    return render(request, "sorular.html", locals())

def videos(request):
    return render(request, "addnewvideo.html", locals())

def bireyselresimleri(request):
    getbimglist = bimglist.objects.get(id=1)
    return render(request, "bresim.html", locals())

@csrf_exempt
def addnewbimg(request):
    data = {}
    if request.method == 'POST':
        kacincigunicin = request.POST.get('kacincigunicin')
        filez = request.POST.get('file')
        if filez:
            filej = json.loads(filez)
            ftype =  filej['input']['type']
            imgstring = filej['output']['image']
            mylist = imgstring.split(',')
            getjpgorpng = ftype.split('/')
            imgdata = base64.b64decode(mylist[1])
            random_img_name = id_generator(22, "qwertyuopasdfghjklizxcvbnm1234567890")
            filename = '/opt/venv/drfit/drfit/templates/media_cdn/'+random_img_name+'.'+getjpgorpng[1]+''  # I assume you have a way of picking unique filenames
            filenamefordatabase = ''+random_img_name+'.'+getjpgorpng[1]+''
            with open(filename, 'wb') as f:
                f.write(imgdata)
            try:
                getbimg = bimglist.objects.get(id=1)
            except bimglist.DoesNotExist:
                if int(kacincigunicin) == 1:
                    saveimage = bimglist(firstimage=filenamefordatabase)
                    saveimage.save()
                    data['response'] = "ok"
                    return HttpResponse(json.dumps(data), content_type = "application/json")
                elif int(kacincigunicin) == 2:
                    saveimage = bimglist(secondimage=filenamefordatabase)
                    saveimage.save()
                    data['response'] = "ok"
                    return HttpResponse(json.dumps(data), content_type = "application/json")
                elif int(kacincigunicin) == 3:
                    saveimage = bimglist(thirthimage=filenamefordatabase)
                    saveimage.save()
                    data['response'] = "ok"
                    return HttpResponse(json.dumps(data), content_type = "application/json")
                elif int(kacincigunicin) == 4:
                    saveimage = bimglist(fourthimage=filenamefordatabase)
                    saveimage.save()
                    data['response'] = "ok"
                    return HttpResponse(json.dumps(data), content_type = "application/json")
                elif int(kacincigunicin) == 5:
                    saveimage = bimglist(fiveimage=filenamefordatabase)
                    saveimage.save()
                    data['response'] = "ok"
                    return HttpResponse(json.dumps(data), content_type = "application/json")
                else:
                    data['response'] = "non"
                    return HttpResponse(json.dumps(data), content_type = "application/json")
            if int(kacincigunicin) == 1:
                getbimg.firstimage = filenamefordatabase
                getbimg.save()
                data['response'] = "ok"
                return HttpResponse(json.dumps(data), content_type = "application/json")
            elif int(kacincigunicin) == 2:
                getbimg.secondimage = filenamefordatabase
                getbimg.save()
                data['response'] = "ok"
                return HttpResponse(json.dumps(data), content_type = "application/json")
            elif int(kacincigunicin) == 3:
                getbimg.thirthimage = filenamefordatabase
                getbimg.save()
                data['response'] = "ok"
                return HttpResponse(json.dumps(data), content_type = "application/json")
            elif int(kacincigunicin) == 4:
                getbimg.fourthimage =  filenamefordatabase
                getbimg.save()
                data['response'] = "ok"
                return HttpResponse(json.dumps(data), content_type = "application/json")
            elif int(kacincigunicin) == 5:
                getbimg.fiveimage= filenamefordatabase
                getbimg.save()
                data['response'] = "ok"
                return HttpResponse(json.dumps(data), content_type = "application/json")
            else:
                data['response'] = "non"
                return HttpResponse(json.dumps(data), content_type = "application/json")
        else:
            data['info'] = "Resim zorunlu"
            data['response'] = "non"
            return HttpResponse(json.dumps(data), content_type = "application/json")
    else:
        data['response'] = "non"
        return HttpResponse(json.dumps(data), content_type = "application/json")


@csrf_exempt
def addnv(request):
    data = {}
    if request.method == 'POST':
        tlist = request.POST.get('tlist')
        enlist = request.POST.get('enlist')
        fllist = request.POST.get('fllist')
        delist = request.POST.get('delist')
        eslist = request.POST.get('eslist')

        tname = request.POST.get('tname')
        enname = request.POST.get('enname')
        flname = request.POST.get('flname')
        dename = request.POST.get('dename')
        esname = request.POST.get('esname')
        checkfile = request.FILES.get('file', False)
        print (checkfile)
        print (request.FILES)
        if checkfile:
            file = request.FILES['file']
            file_type = file.content_type.split('/')[1]
            print (file_type)
            print (file._size)
            print (file.content_type)
            if file._size > 52428800:
                data['response'] = "Dosya boyutu 50 MB geçemez"
                return HttpResponse(json.dumps(data), content_type = "application/json")

            savevideo = Program(name_en=enname,
            name_tr=tname,
            name_nl=flname,
            name_de=dename,
            name_es=esname,
            video=request.FILES['file'])
            savevideo.save()

            if tlist:
                tlist = json.loads(tlist)
                for x in tlist:
                    addnewstlist = SubtitleList(forwhichprogram=savevideo,
                    subtitle=x,language="tr")
                    addnewstlist.save()
            if enlist:
                enlist = json.loads(enlist)
                for x in enlist:
                    addnewstlist = SubtitleList(forwhichprogram=savevideo,
                    subtitle=x,language="en")
                    addnewstlist.save()
            if fllist:
                fllist = json.loads(fllist)
                for x in fllist:
                    addnewstlist = SubtitleList(forwhichprogram=savevideo,
                    subtitle=x,language="nl")
                    addnewstlist.save()
            if delist:
                delist = json.loads(delist)
                for x in delist:
                    addnewstlist = SubtitleList(forwhichprogram=savevideo,
                    subtitle=x,language="de")
                    addnewstlist.save()
            if eslist:
                eslist = json.loads(eslist)
                for x in eslist:
                    addnewstlist = SubtitleList(forwhichprogram=savevideo,
                    subtitle=x,language="es")
                    addnewstlist.save()




            data['response'] = "ok"
            return HttpResponse(json.dumps(data), content_type = "application/json")
        data['response'] = "non"
        data["message"] = "video eklemeyi unutma!!"
        return HttpResponse(json.dumps(data), content_type = "application/json")
    else:
        data["message"] = "POST RQ ONLY"
        data["response"] = "non"
        return HttpResponse(json.dumps(data), content_type = "application/json")





def kategoriekle(request):
    getkategoris = Category.objects.all()
    return render(request, "kekle.html", locals())

def userlist(request):
    return render(request, "userlist.html", locals())


def altkategoriekle(request):
    getkategoris = Category.objects.all()
    getsubkategoris = SubCategory.objects.all()
    return render(request, "akekle.html", locals())

def kategoriprogrami(request):
    getkategoris = Category.objects.all()
    getvideos = Program.objects.all()
    return render(request, "kprogrami.html", locals())

def bireyselprogram(request):
    getvideos = Program.objects.all()
    return render(request, "bprogram.html", locals())

@csrf_exempt
def getsubcates(request):
    if request.method == 'POST':
        cateid = request.POST.get('cateid')
        selectedcate = Category.objects.get(id=cateid)
        getsubcate  = SubCategory.objects.filter(Ctgry=selectedcate)
        subcatearray = []
        for i in getsubcate:
            print ("sorraki")

            subcatearray.append([i.id, i.name_tr])
        data['subcatearr'] = subcatearray
        data['response'] = "ok"
        return HttpResponse(json.dumps(data), content_type = "application/json")
    else:
        data['response'] = "Err"
        return HttpResponse(json.dumps(data), content_type = "application/json")




@csrf_exempt
def addcategoryfy(request):
    data = {}
    if request.method == 'POST':
        trkateisim = request.POST.get('trkateisim')
        trkateaciklama = request.POST.get('trkateaciklama')

        enkateisim = request.POST.get('enkateisim')
        enkateaciklama = request.POST.get('enkateaciklama')

        flkateisim = request.POST.get('flkateisim')
        flkateaciklama = request.POST.get('flkateaciklama')

        dekateisim = request.POST.get('dekateisim')
        dekateaciklama = request.POST.get('dekateaciklama')

        eskateisim = request.POST.get('eskateisim')
        eskateaciklama = request.POST.get('eskateaciklama')

        filez = request.POST.get('file')
        print (request.POST)
        print (filez)

        if trkateisim and filez:
            filej = json.loads(filez)
            ftype =  filej['input']['type']
            imgstring = filej['output']['image']
            mylist = imgstring.split(',')
            getjpgorpng = ftype.split('/')
            imgdata = base64.b64decode(mylist[1])
            random_img_name = id_generator(22, "qwertyuopasdfghjklizxcvbnm1234567890")
            filename = '/opt/venv/drfit/drfit/templates/media_cdn/'+random_img_name+'.'+getjpgorpng[1]+''  # I assume you have a way of picking unique filenames
            filenamefordatabase = ''+random_img_name+'.'+getjpgorpng[1]+''
            with open(filename, 'wb') as f:
                f.write(imgdata)
            try:
                getcategory = Category.objects.get(name_tr=trkateisim)
            except Category.DoesNotExist:
                savecate = Category(name_en=enkateisim,
                name_tr=trkateisim,
                name_nl=flkateisim,
                name_de=dekateisim,
                name_es=eskateisim,
                explain_en=enkateaciklama,
                explain_tr = trkateaciklama,
                explain_nl = flkateisim,
                explain_de = dekateisim,
                explain_es = eskateisim,
                image=filenamefordatabase)
                savecate.save()
                data["message"] = "Great"
                data['response'] = "ok"
                data["filename"] = filenamefordatabase
                return HttpResponse(json.dumps(data), content_type = "application/json")
            data = {"response":"Bu kategori zaten var"}
            return HttpResponse(json.dumps(data), content_type = "application/json")
        else:
            data['response'] = "non"
            data["message"] = "Boş yer bırakmayın"
            return HttpResponse(json.dumps(data), content_type = "application/json")
    else:
        data["message"] = "POST RQ ONLY"
        data["response"] = "non"
        return HttpResponse(json.dumps(data), content_type = "application/json")


@csrf_exempt
def addaltcategoryfy(request):
    data = {}
    if request.method == 'POST':

        alanbox = request.POST.get('calismaalanialt')
        totaltime = request.POST.get('totaltime')


        trkateisim = request.POST.get('traltkateisim')
        trkateaciklama = request.POST.get('traltkateaciklama')

        enkateisim = request.POST.get('enaltkateisim')
        enkateaciklama = request.POST.get('enaltkateaciklama')

        flkateisim = request.POST.get('flaltkateisim')
        flkateaciklama = request.POST.get('flaltkateaciklama')

        dekateisim = request.POST.get('dealtkateisim')
        dekateaciklama = request.POST.get('dealtkateaciklama')

        eskateisim = request.POST.get('esaltkateisim')
        eskateaciklama = request.POST.get('esaltkateaciklama')

        categoryid = request.POST.get('cateforalt')
        premium = request.POST.get('premium')
        preboool = True
        if premium:
            print("yes it is prem")
            preboool = True
        else:
            print("fuck free")
            preboool = False
        filez = request.POST.get('file')
        print (request.POST)
        print (filez)

        if trkateisim and filez:
            filej = json.loads(filez)
            ftype =  filej['input']['type']
            imgstring = filej['output']['image']
            mylist = imgstring.split(',')
            getjpgorpng = ftype.split('/')
            imgdata = base64.b64decode(mylist[1])
            random_img_name = id_generator(22, "qwertyuopasdfghjklizxcvbnm1234567890")
            filename = '/opt/venv/drfit/drfit/templates/media_cdn/'+random_img_name+'.'+getjpgorpng[1]+''  # I assume you have a way of picking unique filenames
            filenamefordatabase = ''+random_img_name+'.'+getjpgorpng[1]+''
            with open(filename, 'wb') as f:
                f.write(imgdata)
            category = Category.objects.get(id=categoryid)
            try:
                getsubcategory = SubCategory.objects.get(name_tr=trkateisim)
            except SubCategory.DoesNotExist:
                savesubcate = SubCategory(Ctgry=category,
                totaltime=totaltime,
                place=alanbox,
                name_en=enkateisim,
                name_tr=trkateisim,
                name_nl=flkateisim,
                name_de=dekateisim,
                name_es=eskateisim,
                explain_en=enkateaciklama,
                explain_tr = trkateaciklama,
                explain_nl = flkateisim,
                explain_de = dekateisim,
                explain_es = eskateisim,
                image=filenamefordatabase,
                isitpremium=preboool)
                savesubcate.save()
                data["message"] = "Great"
                data['response'] = "ok"
                data["filename"] = filenamefordatabase
                return HttpResponse(json.dumps(data), content_type = "application/json")

            data['response'] = "non"
            data["message"] = "Bu kategori zaten var"
            return HttpResponse(json.dumps(data), content_type = "application/json")
        else:
            data['response'] = "non"
            data["message"] = "Boş yer bırakmayın"
            return HttpResponse(json.dumps(data), content_type = "application/json")
    else:
        data["message"] = "POST RQ ONLY"
        data["response"] = "non"
        return HttpResponse(json.dumps(data), content_type = "application/json")



@csrf_exempt
def addnewstep(request):
    if request.method == 'POST':
        cateid = request.POST.get('cateid')
        subcateid = request.POST.get('subcateid')
        videoid = request.POST.get('videoid')
        tekrarsaytisi = request.POST.get('tekrarsaytisi')
        setsayisi = request.POST.get('setsayisi')
        resttime = request.POST.get('resttime')
        isitduration = request.POST.get('isitduration')
        preboool = True
        if isitduration:
            preboool = True
        else:
            preboool = False
        getsubcate = SubCategory.objects.get(id=int(subcateid))
        if resttime:
            addrest = Programlist(psc=getsubcate,
            duration=int(resttime),
            isitduration=preboool,
            isitrest= True)
            addrest.save()
        else:
            getprogram = Program.objects.get(id=int(videoid))
            addrest = Programlist(psc=getsubcate,
            progrm=getprogram,
            setcount=setsayisi,
            replycount=tekrarsaytisi,
            isitduration=preboool,
            isitrest=False)
            addrest.save()
        data['response'] = "ok"
        return HttpResponse(json.dumps(data), content_type = "application/json")
    else:
        data['response'] = "non"
        return HttpResponse(json.dumps(data), content_type = "application/json")



@csrf_exempt
def searchmusteri(request):
    data = {}
    if request.method == 'POST':
        query = request.POST.get('query')
        try:
            musterilistesi = User.objects.filter(name__icontains=query)[0:25] or User.objects.filter(email__icontains=query)[0:25]
        except User.DoesNotExist:
            data['response'] = "Böyle bir profil bulunamadı"
            return HttpResponse(json.dumps(data), content_type = "application/json")
        userlist = []
        for uzer in musterilistesi:
            userlist.append([uzer.id, uzer.name, uzer.email, uzer.isitpremium])
        data['response'] = userlist
        return HttpResponse(json.dumps(data), content_type = "application/json")
    else:
        data['response'] = "non"
        return HttpResponse(json.dumps(data), content_type = "application/json")

@csrf_exempt
def getlastuyeler(request): #düzenlenexadjaslkdjaomgbbqhax
    data = {}
    if request.method == 'POST':
        try:
            musterilistesi = User.objects.all().order_by('-regdate')[:25]
        except User.DoesNotExist:
            data['response'] = "Üye bulunamadı"
            return HttpResponse(json.dumps(data), content_type = "application/json")
        userlist = []
        for uzer in musterilistesi:
            userlist.append([uzer.id, uzer.name, uzer.email, uzer.isitpremium])
        data['response'] = userlist
        return HttpResponse(json.dumps(data), content_type = "application/json")
    else:
        data['response'] = "non"
        return HttpResponse(json.dumps(data), content_type = "application/json")



@csrf_exempt
def addnewbstep(request):
    if request.method == 'POST':
        hedef = request.POST.get('hedef')
        calismaalani = request.POST.get('calismaalani')
        kilotipi = request.POST.get('kilotipi')
        guctipi = request.POST.get('guctipi')
        guntipi = request.POST.get('guntipi')
        videoid = request.POST.get('videoid')
        whichweek = request.POST.get('whichweek')
        whichday = request.POST.get('whichday')
        tekrarsaytisi = request.POST.get('tekrarsaytisi')
        setsayisi = request.POST.get('setsayisi')
        resttime = request.POST.get('resttime')
        totaltime = request.POST.get('totaltime')
        isitduration = request.POST.get('isitduration')
        preboool = True
        if isitduration:
            print("yes it is prem")
            preboool = True
        else:
            print("fuck free")
            preboool = False


        try:
            #kilotipi cinsiyet olarak degistirildi.
            selectdpro = DailyProgram.objects.get(hedef=hedef, calismaalani=calismaalani,kilotipi=kilotipi,guctipi=guctipi,guntipi=guntipi)
        except DailyProgram.DoesNotExist:
            addnewbpro = DailyProgram(hedef=hedef, calismaalani=calismaalani,kilotipi=kilotipi,guctipi=guctipi,guntipi=guntipi, totaltime=totaltime)
            addnewbpro.save()
            if resttime:
                addrest = Programfordaily(overprogram=addnewbpro,
                duration=int(resttime),
                weeknumber=whichweek,
                daynumber=whichday,
                isitduration=False,
                isitrest= True)
                addrest.save()
            else:
                getprogram = Program.objects.get(id=int(videoid))
                addproxx = Programfordaily(overprogram=addnewbpro,
                progrm=getprogram,
                setcount=setsayisi,
                replycount=tekrarsaytisi,
                weeknumber=whichweek,
                daynumber=whichday,
                isitduration=preboool,
                isitrest=False)
                addproxx.save()
            data['response'] = "ok"
            return HttpResponse(json.dumps(data), content_type = "application/json")
        #elsecontinueplease
        if resttime:
            addrest = Programfordaily(overprogram=selectdpro,
            duration=int(resttime),
            weeknumber=whichweek,
            daynumber=whichday,
            isitduration=False,
            isitrest= True)
            addrest.save()
        else:
            getprogram = Program.objects.get(id=int(videoid))
            addproxx = Programfordaily(overprogram=selectdpro,
            progrm=getprogram,
            setcount=setsayisi,
            replycount=tekrarsaytisi,
            weeknumber=whichweek,
            daynumber=whichday,
            isitduration=preboool,
            isitrest=False)
            addproxx.save()
        data['response'] = "ok"
        return HttpResponse(json.dumps(data), content_type = "application/json")
    else:
        data['response'] = "non"
        return HttpResponse(json.dumps(data), content_type = "application/json")




def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
