from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Student, School, Subject, Block, District
# Register your models here.

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ("username", )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("username", )

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    fieldsets = (
        (None, {'fields': ("username", "first_name", "middle_name", "last_name", "date_of_birth", "gender", "password",
         "is_student", "is_teacher", "is_employee", "is_school_admin", "is_block_admin",
          "is_district_admin", "is_state_admin")}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ("username", "first_name", "middle_name", "last_name", "date_of_birth", "gender", "password1", "password2",
         "is_student", "is_teacher", "is_employee", "is_school_admin", "is_block_admin",
          "is_district_admin", "is_state_admin")}
        ),
    )

admin.site.register(Student)
admin.site.register(School)
admin.site.register(Subject)
admin.site.register(Block)
admin.site.register(District)
admin.site.register(User, CustomUserAdmin)
