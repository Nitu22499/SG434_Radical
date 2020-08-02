from django.contrib import admin

# Register your models here.
from teach_staff.models import Teaching_Staff_Info, Teaching_Staff_NonTeachers_Info

admin.site.register(Teaching_Staff_Info)
admin.site.register(Teaching_Staff_NonTeachers_Info)