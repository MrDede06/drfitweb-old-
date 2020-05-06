#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import force_text
from django.db import models
import datetime
from django.utils import timezone
import pytz, datetime

class User(models.Model):
    facebookid = models.CharField(max_length=1000,blank=True , null=True)
    gmailid = models.CharField(max_length=1000,blank=True , null=True)
    phonetype = models.CharField(max_length=1000,blank=True , null=True)
    name = models.CharField(max_length=1000,blank=True , null=True)
    surname = models.CharField(max_length=1000,blank=True , null=True)
    notification = models.CharField(max_length=1000,blank=True , null=True)
    email = models.EmailField(max_length=1000,blank=True , null=True)
    password = models.CharField(max_length=1000,blank=True , null=True)
    gender = models.CharField(max_length=1000,blank=True , null=True)
    kilo = models.IntegerField(blank=True , null=True)
    height = models.IntegerField(blank=True , null=True)
    btype = models.IntegerField(blank=True , null=True)
    usertype = models.IntegerField(blank=True , null=True)
    point = models.IntegerField(blank=True , null=True)
    goal =  models.CharField(max_length=1000,blank=True , null=True)
    place = models.CharField(max_length=1000,blank=True , null=True)
    traindayinweek = models.CharField(max_length=1000,blank=True , null=True)
    profilephoto = models.FileField(blank=True, null=True)
    birthday = models.DateTimeField(null=True)
    deviceid = models.CharField(max_length=1000,blank=True , null=True)
    premium = models.DateTimeField(null=True, blank=True)
    setsayisi = models.IntegerField(blank=True , null=True)
    suresayisi = models.IntegerField(blank=True , null=True)
    strongorlight = models.IntegerField(blank=True , null=True)
    isitpremium = models.BooleanField('premium')
    dailyprogramdetail = models.IntegerField(blank=True , null=True)
    lasttenhours = models.DateTimeField(null=True)
    onemonthlater = models.DateTimeField(null=True)
    regdate = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return '%s %s' % (self.id, self.name)

class Category(models.Model):
    name_en = models.TextField(max_length=1000,blank=True , null=True)
    name_tr = models.TextField(max_length=1000,blank=True , null=True)
    name_nl = models.TextField(max_length=1000,blank=True , null=True)
    name_de = models.TextField(max_length=1000,blank=True , null=True)
    name_es = models.TextField(max_length=1000,blank=True , null=True)
    explain_en = models.TextField(max_length=1000,blank=True , null=True)
    explain_tr = models.TextField(max_length=1000,blank=True , null=True)
    explain_nl = models.TextField(max_length=1000,blank=True , null=True)
    explain_de = models.TextField(max_length=1000,blank=True , null=True)
    explain_es = models.TextField(max_length=1000,blank=True , null=True)
    image = models.TextField(max_length=1000,blank=True , null=True)
    def __unicode__(self):
        return u'Category name : %s ' % (self.id)


class SubCategory(models.Model):
    Ctgry = models.ForeignKey(Category,blank=True, on_delete=models.CASCADE  , null=True)
    image = models.TextField(max_length=1000,blank=True , null=True)
    totaltime = models.TextField(max_length=1000,blank=True , null=True)
    place = models.TextField(max_length=1000,blank=True , null=True)
    isitpremium = models.BooleanField('premium')
    name_en = models.TextField(max_length=1000,blank=True , null=True)
    name_tr = models.TextField(max_length=1000,blank=True , null=True)
    name_nl = models.TextField(max_length=1000,blank=True , null=True)
    name_de = models.TextField(max_length=1000,blank=True , null=True)
    name_es = models.TextField(max_length=1000,blank=True , null=True)
    explain_en = models.TextField(max_length=1000,blank=True , null=True)
    explain_tr = models.TextField(max_length=1000,blank=True , null=True)
    explain_nl = models.TextField(max_length=1000,blank=True , null=True)
    explain_de = models.TextField(max_length=1000,blank=True , null=True)
    explain_es = models.TextField(max_length=1000,blank=True , null=True)

    def __unicode__(self):
        return u'%s' % (self.id)


class Program(models.Model):
    name_en = models.TextField(max_length=1000,blank=True , null=True)
    name_tr = models.TextField(max_length=1000,blank=True , null=True)
    name_nl = models.TextField(max_length=1000,blank=True , null=True)
    name_de = models.TextField(max_length=1000,blank=True , null=True)
    name_es = models.TextField(max_length=1000,blank=True , null=True)
    explain_en = models.TextField(max_length=1000,blank=True , null=True)
    explain_tr = models.TextField(max_length=1000,blank=True , null=True)
    explain_nl = models.TextField(max_length=1000,blank=True , null=True)
    explain_de = models.TextField(max_length=1000,blank=True , null=True)
    explain_es = models.TextField(max_length=1000,blank=True , null=True)
    video = models.FileField(blank=True, null=True)
    def __unicode__(self):
        return u"name : %s "% (self.name_en)

class SubtitleList(models.Model):
    forwhichprogram = models.ForeignKey(Program, on_delete=models.CASCADE)
    subtitle = models.TextField(max_length=1000,blank=True , null=True)
    language = models.TextField(max_length=1000,blank=True , null=True)
    def __unicode__(self):
        return u"%s'ın %s "% (self.forwhichprogram.name_en, self.subtitle)



class Programlist(models.Model):
    psc = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=False , null=False)
    progrm = models.ForeignKey(Program, on_delete=models.CASCADE  ,blank=True , null=True)
    setcount = models.IntegerField(blank=True , null=True)
    replycount = models.IntegerField(blank=True , null=True)
    duration = models.IntegerField(blank=True , null=True)
    orderlist = models.IntegerField(blank=True , null=True)
    isitduration = models.BooleanField('isitduration', default=True ) #eğer set değlide saniye şeklindeyse...
    isitrest = models.BooleanField('isitrest')

    def __unicode__(self):
        return u'%s' % (self.id)



class DailyProgram(models.Model):
    hedef = models.IntegerField(blank=True ,null=True)
    totaltime = models.TextField(max_length=1000,blank=True , null=True)
    calismaalani = models.IntegerField(blank=True, null=True)
    kilotipi = models.IntegerField(blank=True, null=True)
    guctipi = models.IntegerField(blank=True, null=True)
    guntipi = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return u"%s%s%s%s%s"% (self.hedef,self.calismaalani,self.kilotipi,self.guctipi,self.guntipi)


class Programfordaily(models.Model):
    overprogram = models.ForeignKey(DailyProgram, on_delete=models.CASCADE, blank=False , null=False)
    progrm = models.ForeignKey(Program, on_delete=models.CASCADE, blank=True, null=True)
    setcount = models.IntegerField(blank=True, null=True)
    replycount = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    isitrest = models.BooleanField('isitrest')
    isitduration = models.BooleanField('isitduration')   #eğer set değlide saniye şeklindeyse...
    orderlist = models.IntegerField(blank=True, null=True)
    weeknumber = models.IntegerField(blank=True, null=True)
    daynumber = models.IntegerField(blank=True, null=True)
    def __unicode__(self):
        return u"%s'in %s.inci haftasının %s.inci gün programı"% (self.overprogram.id,str(self.weeknumber),str(self.daynumber))


class bimglist(models.Model):
    image = models.TextField(max_length=1000,blank=True , null=True)
    firstimage = models.TextField(max_length=1000,blank=True , null=True)
    secondimage = models.TextField(max_length=1000,blank=True , null=True)
    thirthimage = models.TextField(max_length=1000,blank=True , null=True)
    fourthimage = models.TextField(max_length=1000,blank=True , null=True)
    fiveimage = models.TextField(max_length=1000,blank=True , null=True)
    def __unicode__(self):
        return u"good"


class CateEarn(models.Model):
    EarnerUser = models.ForeignKey(User, on_delete=models.CASCADE,  blank=True , null=True)
    Subcate = models.ForeignKey(SubCategory, on_delete=models.CASCADE,  blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.EarnerUser.name)


class Transactions(models.Model):
    Buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    receiptData = models.TextField(max_length=1000,blank=True , null=True)
    TierPrice = models.TextField(max_length=1000,blank=True , null=True)
    regdate = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return u'%s' % (self.Buyer.name)
