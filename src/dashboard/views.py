from django.shortcuts import render
from django.views import generic
from django.db.models import Count, Q
from django.http import JsonResponse

from misc.utilities import academic_year, year_choices, get_districts, get_blocks

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
            if self.request.GET['year'] != "":
                year = Q(academic_year = self.request.GET['year'])
                context['year'] = self.request.GET['year']
            else: 
                year = Q()
        else:
            year = Q()

        if 'district' in self.request.GET:
            if self.request.GET['district'] != "":
                district = Q(pf_school__school_district = int(self.request.GET['district']))
                context['district_id'] = self.request.GET['district']
            else: 
                district = Q()
        else:
            district = Q()

        if 'block' in self.request.GET:
            if self.request.GET['block'] != "":
                block = Q(pf_school__school_block = int(self.request.GET['block']))
                context['block_id'] = self.request.GET['block']
            else: 
                block = Q()
        else:
            block = Q()

        context['years'] = year_choices()
        context['blocks'] = get_blocks()
        context['districts'] = get_districts()
        
        context['no_of_school'] = PhysicalFacilities.objects.filter(year).filter(district).filter(block).count()
        context['no_of_government_schools'] = PhysicalFacilities.objects.filter(pf_status='Government').filter(year).filter(district).filter(block).count()
        context['no_of_school_with_drinking_water'] = PhysicalFacilities.objects.filter(pf_drinking_water_available='Yes').filter(year).filter(district).filter(block).count()
        context['no_of_school_have_playground_facility'] = PhysicalFacilities.objects.filter(pf_playground_facility='Yes').filter(year).filter(district).filter(block).count()
        context['no_of_school_with_electricity'] = PhysicalFacilities.objects.filter(pf_electricity_connection='Yes').filter(year).filter(district).filter(block).count()
        context['no_of_school_with_library'] = PhysicalFacilities.objects.filter(pf_librarian='Yes').filter(year).filter(district).filter(block).count()
        context['no_of_school_with_seperate_girl_common_room'] = PhysicalFacilities.objects.filter(pf_sep_girls_sec='Yes').filter(year).filter(district).filter(block).count()
        context['no_of_school_with_ramp'] = PhysicalFacilities.objects.filter(pf_ramp_disabled='Yes').filter(year).filter(district).filter(block).count()
        context['no_of_school_with_toilet'] = PhysicalFacilities.objects.filter(pf_schools_toilet='Yes').filter(year).filter(district).filter(block).count()

        context['no_of_government_schools'] = get_percentage(context['no_of_government_schools'], context['no_of_school'])
        context['no_of_school_with_drinking_water'] = get_percentage(context['no_of_school_with_drinking_water'], context['no_of_school'])
        context['no_of_school_have_playground_facility'] = get_percentage(context['no_of_school_have_playground_facility'], context['no_of_school'])
        context['no_of_school_with_electricity'] = get_percentage(context['no_of_school_with_electricity'], context['no_of_school'])
        context['no_of_school_with_library'] = get_percentage(context['no_of_school_with_library'], context['no_of_school'])
        context['no_of_school_with_seperate_girl_common_room'] = get_percentage(context['no_of_school_with_seperate_girl_common_room'], context['no_of_school'])
        context['no_of_school_with_ramp'] = get_percentage(context['no_of_school_with_ramp'], context['no_of_school'])
        context['no_of_school_with_toilet'] = get_percentage(context['no_of_school_with_toilet'], context['no_of_school'])
        return context


def chart(request, *args, **kwargs):
    label = []
    data = []
    query = {}
    
    if 'year' in request.GET and request.GET['year'] != '':
        query['academic_year'] = request.GET['year']
    if 'district' in request.GET and request.GET['district'] != '':
        query['pf_school__school_district'] = int(request.GET['district'])
    if 'block' in request.GET and request.GET['block'] != '':
        query['pf_school__school_block'] = int(request.GET['block'])
    if 'field' in request.GET and request.GET['value'] != '' and request.GET['field'] != '':
        query[request.GET['field']] = request.GET['value']
    
    values = PhysicalFacilities.objects.filter(**query).values_list('academic_year').annotate(freq=Count('academic_year'))
    for value in values:
        label.append(value[0])
        data.append(value[1])
    return JsonResponse(data = {
        'label': label,
        'data' : data
    })
    

def get_blocks_by_district(request):
    blocks = None
    if 'district_id' in request.GET:
        if request.GET['district_id'] == "":
            blocks = get_blocks()
        else:
            district_id = int(request.GET['district_id'])
            blocks = get_blocks(district_id)
    return JsonResponse(data = {
        'blocks' : blocks
    })
