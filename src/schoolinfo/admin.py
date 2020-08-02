from django.contrib import admin
from .models import SchoolProfile, RepeatersByGrade, PhysicalFacilities

admin.site.register(SchoolProfile)
admin.site.register(PhysicalFacilities)
admin.site.register(RepeatersByGrade)
