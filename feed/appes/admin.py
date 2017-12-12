from django.contrib import admin
from .models import Myfeed, Addfeed


admin.site.register(Addfeed)
admin.site.register(Myfeed)
# admin.site.register(Sublink)