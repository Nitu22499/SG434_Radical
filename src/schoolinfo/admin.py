from django.contrib import admin
from .models import SchoolProfile, RepeatersByGrade, PhysicalFacilities,SchoolRTE,SchoolEWS,SchoolLibrary,SchoolItems,SchoolToilet

admin.site.register(SchoolProfile)
admin.site.register(PhysicalFacilities)
admin.site.register(RepeatersByGrade)
admin.site.register(SchoolRTE)
admin.site.register(SchoolEWS)
admin.site.register(SchoolLibrary)
admin.site.register(SchoolItems)
admin.site.register(SchoolToilet)
