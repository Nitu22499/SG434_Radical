from django.contrib import admin
from .models import User, Student, School, Subject
# Register your models here.

admin.site.register(User)
admin.site.register(Student)
admin.site.register(School)
admin.site.register(Subject)
