from django.contrib import admin
#from models import *
from . import models
from .models import *
# Register your models here.






admin.site.register(User)
admin.site.register(Transactions)
admin.site.register(Programfordaily)
admin.site.register(Programlist)
admin.site.register(DailyProgram)
admin.site.register(SubtitleList)
admin.site.register(Program)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(bimglist)
admin.site.register(CateEarn)
