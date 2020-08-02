from django.contrib import admin
from .models import User, Student, School, Subject, Block, District
# Register your models here.

admin.site.register(User)
admin.site.register(Student)
admin.site.register(School)
admin.site.register(Subject)
admin.site.register(Block)
admin.site.register(District)
