from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Student, School, Subject, Block, District
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.hashers import make_password

class UserResource(resources.ModelResource):

    class Meta:
        model = User
    
    def before_import_row(self,row, **kwargs):
        value = row['password']
        row['password'] = make_password(value)

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ("username", )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("username", )

class CustomUserAdmin(UserAdmin, ImportExportModelAdmin):
    resource_class = UserResource
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


class SubjectResource(resources.ModelResource):

    class Meta:
        model = Subject


class SubjectAdmin(ImportExportModelAdmin):
    resource_class = SubjectResource

class StudentResource(resources.ModelResource):

    class Meta:
        model = Student


class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource

class SchoolResource(resources.ModelResource):

    class Meta:
        model = School


class SchoolAdmin(ImportExportModelAdmin):
    resource_class = SchoolResource


admin.site.register(Student, StudentAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Block)
admin.site.register(District)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Subject, SubjectAdmin)

