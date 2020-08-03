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



admin.site.register(SchoolProfile,ProfileAdmin)
admin.site.register(PhysicalFacilities)
admin.site.register(RepeatersByGrade)
admin.site.register(SchoolRTE)
admin.site.register(SchoolEWS)
admin.site.register(SchoolLibrary)
admin.site.register(SchoolItems)
admin.site.register(SchoolToilet)
admin.site.register(EnrolmentPrePrimary)
admin.site.register(EnrolmentBySocialCategory)
admin.site.register(EnrolmentByAge)
admin.site.register(SchoolSafety)
admin.site.register(SchoolReceipt)
admin.site.register(SchoolIncentives)
admin.site.register(SchoolAnnual)
