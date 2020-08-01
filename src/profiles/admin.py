from django.contrib import admin
from .models import User, Student, Employee, School, Subject
# Register your models here.

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Employee)
admin.site.register(School)
admin.site.register(Subject)
