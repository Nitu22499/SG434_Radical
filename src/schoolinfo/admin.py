from django.contrib import admin

from .modelsk import *
from .models import *
from .models2 import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class ProfileResource(resources.ModelResource):

    class Meta:
        model = SchoolProfile


class ProfileAdmin(ImportExportModelAdmin):
    resource_class = ProfileResource


class LibraryResource(resources.ModelResource):

    class Meta:
        model = SchoolLibrary


class LibraryAdmin(ImportExportModelAdmin):
    resource_class = LibraryResource


class PhysicalResource(resources.ModelResource):

    class Meta:
        model = PhysicalFacilities


class PhysicalAdmin(ImportExportModelAdmin):
    resource_class = PhysicalResource


class EWSResource(resources.ModelResource):

    class Meta:
        model = SchoolEWS


class EWSAdmin(ImportExportModelAdmin):
    resource_class = EWSResource

class AnnualResource(resources.ModelResource):

    class Meta:
        model = SchoolAnnual


class AnnualAdmin(ImportExportModelAdmin):
    resource_class = AnnualResource


class ItemsResource(resources.ModelResource):

    class Meta:
        model = SchoolItems


class ItemsAdmin(ImportExportModelAdmin):
    resource_class = ItemsResource

class RepeatersByGradeResource(resources.ModelResource):

    class Meta:
        model = RepeatersByGrade


class RepeatersByGradeAdmin(ImportExportModelAdmin):
    resource_class = RepeatersByGradeResource


admin.site.register(SchoolProfile,ProfileAdmin)
admin.site.register(PhysicalFacilities,PhysicalAdmin)
admin.site.register(RepeatersByGrade,RepeatersByGradeAdmin)
admin.site.register(SchoolRTE)
admin.site.register(SchoolEWS,EWSAdmin)
admin.site.register(SchoolLibrary,LibraryAdmin)
admin.site.register(SchoolItems,ItemsAdmin)
admin.site.register(SchoolToilet)
admin.site.register(EnrolmentPrePrimary)
admin.site.register(EnrolmentBySocialCategory)
admin.site.register(EnrolmentByAge)
admin.site.register(SchoolSafety)
admin.site.register(SchoolReceipt)
admin.site.register(SchoolIncentives)
admin.site.register(SchoolAnnual,AnnualAdmin)
