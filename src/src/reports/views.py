from django.views.generic import TemplateView, FormView
from .forms import ReportForm
from django.urls import reverse_lazy
from misc.utilities import get_blocks
from schoolinfo.models import SchoolProfile, PhysicalFacilities
from profiles.models import Block, District
from misc.utilities import academic_year


class ReportHome(TemplateView):
    template_name = 'reports/reports_home.html'


class SchoolsByMgmt(FormView):
    from django.views.generic import TemplateView, FormView
from .forms import ReportForm
from django.urls import reverse_lazy
from misc.utilities import get_blocks
from schoolinfo.models import SchoolProfile, PhysicalFacilities
from profiles.models import Block, District
from misc.utilities import academic_year


class ReportHome(TemplateView):
    template_name = 'reports/reports_home.html'


class SchoolsByMgmt(FormView):
    template_name = 'reports/schools_by_mgmt.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:schools_by_mgmt')
    academic_year_field = ''
    districts_field = None
    blocks_field = None
    categories_field = None

    def get(self, request, *args, **kwargs):
        """ Get inputs from form """
        if self.request.GET.get('academic_year_field'):
            self.academic_year_field = self.request.GET.get('academic_year_field')
        else:
            self.academic_year_field = academic_year()
        if self.request.GET.get('districts_field'):
            self.districts_field = int(self.request.GET.get('districts_field'))
        if self.request.GET.get('blocks_field'):
            self.blocks_field = int(self.request.GET.get('blocks_field'))
        if self.request.GET.get('categories_field'):
            self.categories_field = self.request.GET.get('categories_field')
        return super(SchoolsByMgmt, self).get(request, *args, **kwargs)

    def get_initial(self):
        """ Save form state on page reload """
        initial_data = {
            'academic_year_field':self.academic_year_field,
            'districts_field':self.districts_field,
            'blocks_field':self.blocks_field,
            'categories_field':self.categories_field
        }
        return initial_data

    def get_form(self, form_class=None):
        """ override get_form() function to add Block Choices dynamically according to selected district """
        if form_class is None:
            form_class = self.get_form_class()
        form = form_class(**self.get_form_kwargs())
        if self.districts_field:
            form.fields['blocks_field'].choices = (('', 'All'), ) + get_blocks(self.districts_field)
        return form

    def get_context_data(self, **kwargs):
        """ Prepare table content and pass to context """
        blocks_list = []        # get the names of blocks for queried schools
        objs = SchoolProfile.objects.filter(academic_year = self.academic_year_field)
        if self.categories_field:   # filter for school category
            objs = objs.filter(sp_school_category=self.categories_field)
        if self.blocks_field:   # filter out schools for particular single block
            objs = objs.filter(sp_school__school_block = self.blocks_field)
            blocks_list.append(Block.objects.get(id=self.blocks_field).block_name)
        elif self.districts_field:      # filter out schools of all blocks in a particular district
            objs = objs.filter(sp_school__school_district = self.districts_field)
            for block in Block.objects.filter(block_district=self.districts_field):
                blocks_list.append(block.block_name)
        else:
            for block in Block.objects.all():       # all inputs set to all.
                blocks_list.append(block.block_name)

        #print(objs)

        total_state_govt_schools = 0
        total_central_govt_schools = 0
        total_private_schools = 0
        total_local_body_schools = 0
        total_other_schools = 0
        total_total_schools = 0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            records = objs.filter(sp_cd=block)   
            #print(records)
               # get schools in particular block
            state_govt_schools = records.filter(sp_management_code='State Govt.').count()
            central_govt_schools = records.filter(sp_management_code='Central Govt.').count()
            private_schools = records.filter(sp_management_code='Private').count()
            local_body_schools = records.filter(sp_management_code='Local Body').count()
            other_schools = records.filter(sp_management_code='Other').count()
            total_schools = state_govt_schools + central_govt_schools + private_schools + local_body_schools + other_schools
            table_data.append({
                'block_name':block,
                'state_govt_schools':state_govt_schools,
                'central_govt_schools':central_govt_schools,
                'private_schools':private_schools,
                'local_body_schools':local_body_schools,
                'other_schools':other_schools,
                'total_schools':total_schools
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_state_govt_schools += state_govt_schools
                total_central_govt_schools += central_govt_schools
                total_private_schools += private_schools
                total_local_body_schools += local_body_schools
                total_other_schools += other_schools
                total_total_schools += total_schools
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'state_govt_schools':total_state_govt_schools,
                'central_govt_schools':total_central_govt_schools,
                'private_schools':total_private_schools,
                'local_body_schools':total_local_body_schools,
                'other_schools':total_other_schools,
                'total_schools':total_total_schools
            }
        

        kwargs['table_data'] = table_data
        #print(table_data)
        return super().get_context_data(**kwargs)


  