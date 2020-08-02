from django.shortcuts import render
from django.views import generic

from misc.utilities import academic_year

from schoolinfo.models import PhysicalFacilities


def get_percentage(c, n):
    if(n == 0):
        return "{:.2f}".format(0)
    return "{:.2f}".format((float(c)/n)*100)


class DashboardView(generic.TemplateView):
    template_name = 'dashboard/school_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'year' in self.request.GET:
            year = self.request.GET['year']
        else:
            year = academic_year()

        context['no_of_school'] = PhysicalFacilities.objects.filter(academic_year=year).count()
        context['no_of_government_schools'] = PhysicalFacilities.objects.filter(pf_status='Government').filter(academic_year=year).count()
        context['no_of_school_with_drinking_water'] = PhysicalFacilities.objects.filter(pf_drinking_water_available='Yes').filter(academic_year=year).count()
        context['no_of_school_have_playground_facility'] = PhysicalFacilities.objects.filter(pf_playground_facility='Yes').filter(academic_year=year).count()
        context['no_of_school_with_electricity'] = PhysicalFacilities.objects.filter(pf_electricity_connection='Yes').filter(academic_year=year).count()
        context['no_of_school_with_library'] = PhysicalFacilities.objects.filter(pf_librarian='Yes').filter(academic_year=year).count()
        context['no_of_school_with_seperate_girl_common_room'] = PhysicalFacilities.objects.filter(pf_sep_girls_sec='Yes').filter(academic_year=year).count()
        context['no_of_school_with_ramp'] = PhysicalFacilities.objects.filter(pf_ramp_disabled='Yes').filter(academic_year=year).count()
        context['no_of_school_with_toilet'] = PhysicalFacilities.objects.filter(pf_schools_toilet='Yes').filter(academic_year=year).count()

        context['no_of_government_schools'] = get_percentage(context['no_of_government_schools'], context['no_of_school'])
        context['no_of_school_with_drinking_water'] = get_percentage(context['no_of_school_with_drinking_water'], context['no_of_school'])
        context['no_of_school_have_playground_facility'] = get_percentage(context['no_of_school_have_playground_facility'], context['no_of_school'])
        context['no_of_school_with_electricity'] = get_percentage(context['no_of_school_with_electricity'], context['no_of_school'])
        context['no_of_school_with_library'] = get_percentage(context['no_of_school_with_library'], context['no_of_school'])
        context['no_of_school_with_seperate_girl_common_room'] = get_percentage(context['no_of_school_with_seperate_girl_common_room'], context['no_of_school'])
        context['no_of_school_with_ramp'] = get_percentage(context['no_of_school_with_ramp'], context['no_of_school'])
        context['no_of_school_with_toilet'] = get_percentage(context['no_of_school_with_toilet'], context['no_of_school'])
        return context