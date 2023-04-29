from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Employee)
admin.site.register(Products)
admin.site.register(Books)
admin.site.register(DVDs)
admin.site.register(CDs)
admin.site.register(Records)