from django.views.generic import TemplateView, FormView
from .forms import ReportForm
from django.urls import reverse_lazy
from misc.utilities import get_blocks
from schoolinfo.models import SchoolProfile, PhysicalFacilities 
from schoolinfo.models2 import SchoolLibrary,SchoolItems
from profiles.models import Block, District
from misc.utilities import academic_year



class SchoolsByab(FormView):
    template_name = 'reports/schools_by_ab.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:schools_by_ab')
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
        return super(SchoolsByab, self).get(request, *args, **kwargs)

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

        # print(objs)

        total_cbse_schools = 0
        total_icse_schools = 0
        total_both_schools = 0
        total_state_schools = 0
        total_international_schools = 0
        total_other_schools = 0
        total_total_schools = 0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            records = objs.filter(sp_cd=block)      # get schools in particular block
            cbse_schools = records.filter(sp_sec_affi_board='CBSE').count()
            cbse_schools += records.filter(sp_high_sec_affi_board='CBSE').count()
            state_schools = records.filter(sp_sec_affi_board='State Board').count()
            state_schools += records.filter(sp_high_sec_affi_board='State Board').count()
            international_schools = records.filter(sp_sec_affi_board='International Board').count()
            international_schools += records.filter(sp_high_sec_affi_board='International Board').count()
            icse_schools = records.filter(sp_sec_affi_board='ICSE').count()
            icse_schools += records.filter(sp_high_sec_affi_board='ICSE').count()
            other_schools = records.filter(sp_sec_affi_board='Others').count()
            other_schools += records.filter(sp_high_sec_affi_board='Others').count()
            both_schools = records.filter(sp_sec_affi_board='Both CBSE & State Board').count()
            both_schools += records.filter(sp_high_sec_affi_board='Both CBSE & State Board').count()
            total_schools = cbse_schools + state_schools + international_schools + icse_schools + other_schools +both_schools
            table_data.append({
                'block_name':block,
                'cbse_schools':cbse_schools,
                'state_schools':state_schools,
                'international_schools':international_schools,
                'icse_schools':icse_schools,
                'other_schools':other_schools,
                'both_schools':both_schools,
                'total_schools':total_schools
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_cbse_schools += cbse_schools
                total_icse_schools += icse_schools
                total_state_schools += state_schools
                total_international_schools += international_schools
                total_both_schools+=both_schools
                total_other_schools += other_schools
                total_total_schools += total_schools
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'cbse_schools':total_cbse_schools,
                'icse_schools':total_icse_schools,
                'state_schools':total_state_schools,
                'international_schools':total_international_schools,
                'both_schools':total_both_schools,
                'other_schools':total_other_schools,
                'total_schools':total_total_schools
            }
       
        
        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)



class SchoolsByct(FormView):
    template_name = 'reports/schools_by_ct.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:schools_by_ct')
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
        return super(SchoolsByct, self).get(request, *args, **kwargs)

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

        # print(objs)

        total_pri15_schools = 0
        total_pri18_schools = 0
        total_high_sec112_schools = 0
        total_upper_pri68_schools = 0
        total_international_schools = 0
        total_high_sec612_schools = 0
        total_sec110_schools = 0
        total_sec610_schools = 0
        total_sec910_schools = 0
        total_high_sec912_schools = 0
        total_hr1112_schools = 0
        total_total_schools=0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            records = objs.filter(sp_cd=block)      # get schools in particular block
            pri15_schools = records.filter(sp_school_category='Primary only with grades 1 to 5').count()
            pri18_schools = records.filter(sp_school_category='Primary only with grades 1 to 8').count()
            high_sec112_schools = records.filter(sp_school_category='Higher Secondary with grades 1 to 12').count()
            upper_pri68_schools = records.filter(sp_school_category='Upper Primary only with grades 6 to 8').count()
            high_sec612_schools = records.filter(sp_school_category='Higher Secondary with grades 6 to 12').count()
            sec110_schools = records.filter(sp_school_category='Secondary/Sr.Sec. with grades 1 to 10').count()
            sec610_schools = records.filter(sp_school_category='Secondary/Sr.Sec. with grades 6 to 10').count()
            sec910_schools = records.filter(sp_school_category='Secondary/Sr.Sec. with grades 9 and 10').count()
            high_sec912_schools = records.filter(sp_school_category='Higher Secondary with grades 9 to 12').count()
            hr1112_schools = records.filter(sp_school_category='Hr.Sec. /Jr.College only with grades 11 and 12').count()
            total_schools = pri15_schools + pri18_schools + high_sec112_schools + upper_pri68_schools + high_sec612_schools +sec110_schools+sec610_schools +sec910_schools +high_sec912_schools + hr1112_schools
            table_data.append({
                'block_name':block,
                'pri15_schools':pri15_schools,
                'pri18_schools':pri18_schools,
                'high_sec112_schools':high_sec112_schools,
                'upper_pri68_schools':upper_pri68_schools,
                'high_sec612_schools':high_sec612_schools,
                'sec110_schools':sec110_schools,
                'sec610_schools':sec610_schools,
                'sec910_schools':sec910_schools,
                'high_sec912_schools':high_sec912_schools,
                'hr1112_schools':hr1112_schools,
                'total_schools':total_schools
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_pri15_schools += pri15_schools
                total_pri18_schools += pri18_schools
                total_high_sec112_schools += high_sec112_schools
                total_upper_pri68_schools += upper_pri68_schools
                total_high_sec612_schools+=high_sec612_schools
                total_sec110_schools += sec110_schools
                total_sec610_schools += sec610_schools
                total_sec910_schools += sec910_schools
                total_high_sec912_schools += high_sec912_schools
                total_hr1112_schools += hr1112_schools
                total_total_schools += total_schools
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'pri15_schools':total_pri15_schools,
                'pri18_schools':total_pri18_schools,
                'upper_pri68_schools':total_upper_pri68_schools,
                'high_sec112_schools':total_high_sec112_schools,
                'high_sec612_schools':total_high_sec612_schools,
                'sec110_schools':total_sec110_schools,
                'sec610_schools':total_sec610_schools,
                'sec910_schools':total_sec910_schools,
                'high_sec912_schools':total_high_sec912_schools,
                'hr1112_schools':total_hr1112_schools,
                'total_schools':total_total_schools
            }
       
        
        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)


class SchoolsBysb(FormView):
    template_name = 'reports/schools_by_sb.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:schools_by_sb')
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
        return super(SchoolsBysb, self).get(request, *args, **kwargs)

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
        objs1 = PhysicalFacilities.objects.filter(academic_year = self.academic_year_field)
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

        # print(objs)

        total_private_schools = 0
        total_rented_schools = 0
        total_gov_schools = 0
        total_rent_free_schools = 0
        total_no_build_schools = 0
        total_build_schools = 0
        total_const_schools = 0
        total_other_schools = 0
        total_total_schools=0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            records = objs.filter(sp_cd=block) # get schools in particular block
            private_schools=0
            for record in records:
                school=record.sp_school
                if  PhysicalFacilities.objects.filter(pf_school=school,pf_status="Private"):
                    private_schools+=1
                # print(private_schools)
            rented_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_status="Rented"):
                    rented_schools+= 1
            gov_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_status="Government"):
                    gov_schools+= 1
            rent_free_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_status="Government School in a rent free building"):
                    rent_free_schools+= 1
            no_build_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_status="No Building"):
                    no_build_schools+= 1
            build_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_status="Building"):
                    build_schools+= 1
            const_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_status="Under Construction"):
                    const_schools+= 1
            other_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_status="School running in other Department Building"):
                    other_schools+= 1
            total_schools = private_schools + rented_schools + gov_schools + rent_free_schools + no_build_schools +build_schools+const_schools +other_schools 
            table_data.append({
                'block_name':block,
                'private_schools':private_schools,
                'rented_schools':rented_schools,
                'gov_schools':gov_schools,
                'rent_free_schools':rent_free_schools,
                'no_build_schools':no_build_schools,
                'build_schools':build_schools,
                'const_schools':const_schools,
                'other_schools':other_schools,
                'total_schools':total_schools
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_private_schools += private_schools
                total_rented_schools += rented_schools
                total_gov_schools += gov_schools
                total_rent_free_schools += rent_free_schools
                total_no_build_schools+=no_build_schools
                total_build_schools += build_schools
                total_const_schools += const_schools
                total_other_schools += other_schools
                total_total_schools += total_schools
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'private_schools':total_private_schools,
                'rented_schools':total_rented_schools,
                'gov_schools':total_gov_schools,
                'rent_free_schools':total_rent_free_schools,
                'no_build_schools':total_no_build_schools,
                'build_schools':total_build_schools,
                'const_schools':total_const_schools,
                'other_schools':total_other_schools,
                'total_schools':total_total_schools
            }
       
        
        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)




class SchoolsBybw(FormView):
    template_name = 'reports/schools_by_bw.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:schools_by_bw')
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
        return super(SchoolsBybw, self).get(request, *args, **kwargs)

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

        # print(objs)

        total_pucca_schools = 0
        total_broken_schools = 0
        total_wire_schools = 0
        total_hedges_schools = 0
        total_walls_schools = 0
        total_others_schools = 0
        total_partial_schools = 0
        total_const_schools = 0
        total_total_schools=0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            records = objs.filter(sp_cd=block) # get schools in particular block
            pucca_schools=0
            for record in records:
                school=record.sp_school
                if  PhysicalFacilities.objects.filter(pf_school=school,pf_boundary_type="Pucca"):
                    pucca_schools+=1
                # print(private_schools)
            broken_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_boundary_type="Pucca but broken"):
                    broken_schools+= 1
            wire_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_boundary_type="Barbed wire fencing"):
                    wire_schools+= 1
            hedges_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_boundary_type="Hedges"):
                    hedges_schools+= 1
            walls_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_boundary_type="No boundary walls"):
                    walls_schools+= 1
            others_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_boundary_type="others"):
                    others_schools+= 1
            partial_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_boundary_type="Partial"):
                    partial_schools+= 1
            const_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_boundary_type="Under Construction"):
                    const_schools+= 1
            total_schools = pucca_schools + broken_schools + wire_schools + hedges_schools + partial_schools +walls_schools+const_schools +others_schools 
            table_data.append({
                'block_name':block,
                'pucca_schools':pucca_schools,
                'broken_schools':broken_schools,
                'wire_schools':wire_schools,
                'hedges_schools':hedges_schools,
                'walls_schools':walls_schools,
                'others_schools':others_schools,
                'partial_schools':partial_schools,
                'const_schools':const_schools,
                'total_schools':total_schools
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_pucca_schools += pucca_schools
                total_broken_schools += broken_schools
                total_wire_schools += wire_schools
                total_hedges_schools += hedges_schools
                total_walls_schools+=walls_schools
                total_others_schools += others_schools
                total_partial_schools += partial_schools
                total_const_schools += const_schools
                total_total_schools += total_schools
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'pucca_schools':total_pucca_schools,
                'borken_schools':total_broken_schools,
                'wire_schools':total_wire_schools,
                'hedges_schools':total_hedges_schools,
                'walls_schools':total_walls_schools,
                'others_schools':total_others_schools,
                'partial_schools':total_partial_schools,
                'const_schools':total_const_schools,
                'total_schools':total_total_schools
            }
       
        
        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)





class SchoolsByec(FormView):
    template_name = 'reports/schools_by_ec.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:schools_by_ec')
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
        return super(SchoolsByec, self).get(request, *args, **kwargs)

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

        # print(blocks_list)
        total_count_of_primary_one = 0
        total_count_of_primary_two = 0
        total_count_of_higher_sec_one = 0
        total_count_of_upper_primary = 0
        total_count_of_higher_sec_two = 0
        total_count_of_sr_secondary_one = 0
        total_count_of_sr_secondary_two = 0
        total_count_of_sr_secondary_three = 0
        total_count_of_higher_sec_three = 0
        total_count_of_college = 0
        total_total_schools = 0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            objs = objs.filter(sp_cd=block)    # get schools in particular block
            records = objs.filter(sp_school_category='Primary only with grades 1 to 5')
            count_of_primary_one=0
            for record in records:
                school = record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_electricity_connection="Yes"):
                    count_of_primary_one+=1
            records = objs.filter(sp_school_category='Primary only with grades 1 to 8')
            count_of_primary_two=0
            for record in records:
                school = record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_electricity_connection="Yes"):
                    count_of_primary_two+=1
            records = objs.filter(sp_school_category='Higher Secondary with grades 1 to 12')
            count_of_higher_sec_one=0
            for record in records:
                school = record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_electricity_connection="Yes"):
                    count_of_higher_sec_one+=1
            records = objs.filter(sp_school_category='Upper Primary only with grades 6 to 8')
            count_of_upper_primary=0
            for record in records:
                school = record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_electricity_connection="Yes"):
                    count_of_upper_primary+=1
            records = objs.filter(sp_school_category='Higher Secondary with grades 6 to 12')
            count_of_higher_sec_two=0
            for record in records:
                school = record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_electricity_connection="Yes"):
                    count_of_higher_sec_two+=1
            records = objs.filter(sp_school_category='Secondary/Sr.Sec. with grades 1 to 10')
            count_of_sr_secondary_one=0
            for record in records:
                school = record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_electricity_connection="Yes"):
                    count_of_sr_secondary_one+=1
            records = objs.filter(sp_school_category='Secondary/Sr.Sec. with grades 6 to 10')
            count_of_sr_secondary_two=0
            for record in records:
                school = record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_electricity_connection="Yes"):
                    count_of_sr_secondary_two+=1
            records = objs.filter(sp_school_category='Secondary/Sr.Sec. with grades 9 and 10')
            count_of_sr_secondary_three=0
            for record in records:
                school = record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_electricity_connection="Yes"):
                    count_of_sr_secondary_three+=1
            records = objs.filter(sp_school_category='Higher Secondary with grades 9 to 12')
            count_of_higher_sec_three=0
            for record in records:
                school = record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_electricity_connection="Yes"):
                    count_of_higher_sec_three+=1
            records = objs.filter(sp_school_category='Hr.Sec. /Jr.College only with grades 11 and 12')
            count_of_college=0
            for record in records:
                school = record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_electricity_connection="Yes"):
                    count_of_college+=1
            
            total_schools = count_of_primary_one + count_of_primary_two + count_of_higher_sec_one + count_of_upper_primary + count_of_higher_sec_two + count_of_sr_secondary_one + count_of_sr_secondary_two + count_of_sr_secondary_three + count_of_higher_sec_three + count_of_college
            table_data.append({
                'block_name':block,
                'count_of_primary_one':count_of_primary_one,
                'count_of_primary_two':count_of_primary_two,
                'count_of_higher_sec_one':count_of_higher_sec_one,
                'count_of_upper_primary':count_of_upper_primary,
                'count_of_higher_sec_two':count_of_higher_sec_two,
                'count_of_sr_secondary_one':count_of_sr_secondary_one,
                'count_of_sr_secondary_two':count_of_sr_secondary_two,
                'count_of_sr_secondary_three':count_of_sr_secondary_three,
                'count_of_higher_sec_three':count_of_higher_sec_three,
                'count_of_college':count_of_college,
                'total_schools':total_schools
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_count_of_primary_one += count_of_primary_one
                total_count_of_primary_two += count_of_primary_two
                total_count_of_higher_sec_one += count_of_higher_sec_one
                total_count_of_upper_primary += count_of_upper_primary
                total_count_of_higher_sec_two += count_of_higher_sec_two
                total_count_of_sr_secondary_one += count_of_sr_secondary_one
                total_count_of_sr_secondary_two += count_of_sr_secondary_two
                total_count_of_sr_secondary_three += count_of_sr_secondary_three
                total_count_of_higher_sec_three += count_of_higher_sec_three
                total_count_of_college += count_of_college
                total_total_schools += total_schools
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'count_of_primary_one':total_count_of_primary_one,
                'count_of_primary_two':total_count_of_primary_two,
                'count_of_higher_sec_one':total_count_of_higher_sec_one,
                'count_of_upper_primary':total_count_of_upper_primary,
                'count_of_higher_sec_two':total_count_of_higher_sec_two,
                'count_of_sr_secondary_one':total_count_of_sr_secondary_one,
                'count_of_sr_secondary_two':total_count_of_sr_secondary_two,
                'count_of_sr_secondary_three':total_count_of_sr_secondary_three,
                'count_of_higher_sec_three':total_count_of_higher_sec_three,
                'count_of_college':total_count_of_college,
                'total_schools':total_total_schools
            }


        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)





class SchoolsBycwsn(FormView):
    template_name = 'reports/schools_by_cwsn.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:schools_by_cwsn')
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
        return super(SchoolsBycwsn, self).get(request, *args, **kwargs)

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

        # print(blocks_list)
        total_count_of_primary_one = 0
        total_count_of_primary_two = 0
        total_count_of_higher_sec_one = 0
        total_count_of_upper_primary = 0
        total_count_of_higher_sec_two = 0
        total_count_of_sr_secondary_one = 0
        total_count_of_sr_secondary_two = 0
        total_count_of_sr_secondary_three = 0
        total_count_of_higher_sec_three = 0
        total_count_of_college = 0
        total_total_schools = 0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            objs = objs.filter(sp_cd=block)    # get schools in particular block
            records = objs.filter(sp_school_category='Primary only with grades 1 to 5')
            count_of_primary_one=0
            for record in records:
                school = record.sp_school
                if SchoolProfile.objects.filter(sp_school=school,sp_is_cwsn="Yes"):
                    count_of_primary_one+=1
            records = objs.filter(sp_school_category='Primary only with grades 1 to 8')
            count_of_primary_two=0
            for record in records:
                school = record.sp_school
                if SchoolProfile.objects.filter(sp_school=school,sp_is_cwsn="Yes"):
                    count_of_primary_two+=1
            records = objs.filter(sp_school_category='Higher Secondary with grades 1 to 12')
            count_of_higher_sec_one=0
            for record in records:
                school = record.sp_school
                if SchoolProfile.objects.filter(sp_school=school,sp_is_cwsn="Yes"):
                    count_of_higher_sec_one+=1
            records = objs.filter(sp_school_category='Upper Primary only with grades 6 to 8')
            count_of_upper_primary=0
            for record in records:
                school = record.sp_school
                if SchoolProfile.objects.filter(sp_school=school,sp_is_cwsn="Yes"):
                    count_of_upper_primary+=1
            records = objs.filter(sp_school_category='Higher Secondary with grades 6 to 12')
            count_of_higher_sec_two=0
            for record in records:
                school = record.sp_school
                if SchoolProfile.objects.filter(sp_school=school,sp_is_cwsn="Yes"):
                    count_of_higher_sec_two+=1
            records = objs.filter(sp_school_category='Secondary/Sr.Sec. with grades 1 to 10')
            count_of_sr_secondary_one=0
            for record in records:
                school = record.sp_school
                if SchoolProfile.objects.filter(sp_school=school,sp_is_cwsn="Yes"):
                    count_of_sr_secondary_one+=1
            records = objs.filter(sp_school_category='Secondary/Sr.Sec. with grades 6 to 10')
            count_of_sr_secondary_two=0
            for record in records:
                school = record.sp_school
                if SchoolProfile.objects.filter(sp_school=school,sp_is_cwsn="Yes"):
                    count_of_sr_secondary_two+=1
            records = objs.filter(sp_school_category='Secondary/Sr.Sec. with grades 9 and 10')
            count_of_sr_secondary_three=0
            for record in records:
                school = record.sp_school
                if SchoolProfile.objects.filter(sp_school=school,sp_is_cwsn="Yes"):
                    count_of_sr_secondary_three+=1
            records = objs.filter(sp_school_category='Higher Secondary with grades 9 to 12')
            count_of_higher_sec_three=0
            for record in records:
                school = record.sp_school
                if SchoolProfile.objects.filter(sp_school=school,sp_is_cwsn="Yes"):
                    count_of_higher_sec_three+=1
            records = objs.filter(sp_school_category='Hr.Sec. /Jr.College only with grades 11 and 12')
            count_of_college=0
            for record in records:
                school = record.sp_school
                if SchoolProfile.objects.filter(sp_school=school,sp_is_cwsn="Yes"):
                    count_of_college+=1
            
            total_schools = count_of_primary_one + count_of_primary_two + count_of_higher_sec_one + count_of_upper_primary + count_of_higher_sec_two + count_of_sr_secondary_one + count_of_sr_secondary_two + count_of_sr_secondary_three + count_of_higher_sec_three + count_of_college
            table_data.append({
                'block_name':block,
                'count_of_primary_one':count_of_primary_one,
                'count_of_primary_two':count_of_primary_two,
                'count_of_higher_sec_one':count_of_higher_sec_one,
                'count_of_upper_primary':count_of_upper_primary,
                'count_of_higher_sec_two':count_of_higher_sec_two,
                'count_of_sr_secondary_one':count_of_sr_secondary_one,
                'count_of_sr_secondary_two':count_of_sr_secondary_two,
                'count_of_sr_secondary_three':count_of_sr_secondary_three,
                'count_of_higher_sec_three':count_of_higher_sec_three,
                'count_of_college':count_of_college,
                'total_schools':total_schools
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_count_of_primary_one += count_of_primary_one
                total_count_of_primary_two += count_of_primary_two
                total_count_of_higher_sec_one += count_of_higher_sec_one
                total_count_of_upper_primary += count_of_upper_primary
                total_count_of_higher_sec_two += count_of_higher_sec_two
                total_count_of_sr_secondary_one += count_of_sr_secondary_one
                total_count_of_sr_secondary_two += count_of_sr_secondary_two
                total_count_of_sr_secondary_three += count_of_sr_secondary_three
                total_count_of_higher_sec_three += count_of_higher_sec_three
                total_count_of_college += count_of_college
                total_total_schools += total_schools
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'count_of_primary_one':total_count_of_primary_one,
                'count_of_primary_two':total_count_of_primary_two,
                'count_of_higher_sec_one':total_count_of_higher_sec_one,
                'count_of_upper_primary':total_count_of_upper_primary,
                'count_of_higher_sec_two':total_count_of_higher_sec_two,
                'count_of_sr_secondary_one':total_count_of_sr_secondary_one,
                'count_of_sr_secondary_two':total_count_of_sr_secondary_two,
                'count_of_sr_secondary_three':total_count_of_sr_secondary_three,
                'count_of_higher_sec_three':total_count_of_higher_sec_three,
                'count_of_college':total_count_of_college,
                'total_schools':total_total_schools
            }


        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)




class SchoolsByif(FormView):
    template_name = 'reports/schools_by_if.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:schools_by_if')
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
        return super(SchoolsByif, self).get(request, *args, **kwargs)

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

        # print(objs)

        total_toilets_schools = 0
        total_water_schools = 0
        total_ramp_schools = 0
        total_elec_schools = 0
        total_solar_schools = 0
        total_lib_schools = 0
        total_play_schools = 0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            records = objs.filter(sp_cd=block) # get schools in particular block
            toilets_schools=0
            for record in records:
                school=record.sp_school
                if  PhysicalFacilities.objects.filter(pf_school=school,pf_schools_toilet="Yes"):
                    toilets_schools+=1
                # print(private_schools)
            water_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_drinking_water_available="Yes"):
                    water_schools+= 1
            elec_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_electricity_connection="Yes"):
                    elec_schools+= 1
            solar_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_solar_panel="Yes"):
                    solar_schools+= 1
            lib_schools=0
            for record in records:
                school=record.sp_school
                if SchoolLibrary.objects.filter(sli_school_name=school,sli_lib_avai="Yes"):
                    lib_schools+= 1
            play_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_playground_facility="Yes"):
                    play_schools+= 1
            ramp_schools=0
            for record in records:
                school=record.sp_school
                if PhysicalFacilities.objects.filter(pf_school=school,pf_ramp_disabled="Yes"):
                    ramp_schools+= 1

            total_schools = water_schools + solar_schools + lib_schools + ramp_schools + toilets_schools +play_schools+elec_schools  
            table_data.append({
                'block_name':block,
                'toilets_schools':toilets_schools,
                'water_schools':water_schools,
                'elec_schools':elec_schools,
                'solar_schools':solar_schools,
                'lib_schools':lib_schools,
                'play_schools':play_schools,
                'ramp_schools':ramp_schools
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_toilets_schools += toilets_schools
                total_water_schools += water_schools
                total_elec_schools += elec_schools
                total_solar_schools += solar_schools
                total_lib_schools+=lib_schools
                total_play_schools += play_schools
                total_ramp_schools += ramp_schools
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'toilets_schools':total_toilets_schools,
                'water_schools':total_water_schools,
                'elec_schools':total_elec_schools,
                'solar_schools':total_solar_schools,
                'lib_schools':total_lib_schools,
                'play_schools':total_play_schools,
                'ramp_schools':total_ramp_schools
            }
       
        
        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)






class SchoolsByc(FormView):
    template_name = 'reports/schools_by_c.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:schools_by_c')
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
        return super(SchoolsByc, self).get(request, *args, **kwargs)

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

        # print(blocks_list)
        total_count_of_primary_one = 0
        total_count_of_primary_two = 0
        total_count_of_higher_sec_one = 0
        total_count_of_upper_primary = 0
        total_count_of_higher_sec_two = 0
        total_count_of_sr_secondary_one = 0
        total_count_of_sr_secondary_two = 0
        total_count_of_sr_secondary_three = 0
        total_count_of_higher_sec_three = 0
        total_count_of_college = 0
        total_total_schools = 0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            objs = objs.filter(sp_cd=block)    # get schools in particular block
            records = objs.filter(sp_school_category='Primary only with grades 1 to 5')
            count_of_primary_one=0
            for record in records:
                school = record.sp_school
                if SchoolItems.objects.filter(sit_school_name=school,sit_desk_avai="Yes"):
                    count_of_primary_one+=1
            records = objs.filter(sp_school_category='Primary only with grades 1 to 8')
            count_of_primary_two=0
            for record in records:
                school = record.sp_school
                if SchoolItems.objects.filter(sit_school_name=school,sit_desk_avai="Yes"):
                    count_of_primary_two+=1
            records = objs.filter(sp_school_category='Higher Secondary with grades 1 to 12')
            count_of_higher_sec_one=0
            for record in records:
                school = record.sp_school
                if SchoolItems.objects.filter(sit_school_name=school,sit_desk_avai="Yes"):
                    count_of_higher_sec_one+=1
            records = objs.filter(sp_school_category='Upper Primary only with grades 6 to 8')
            count_of_upper_primary=0
            for record in records:
                school = record.sp_school
                if SchoolItems.objects.filter(sit_school_name=school,sit_desk_avai="Yes"):
                    count_of_upper_primary+=1
            records = objs.filter(sp_school_category='Higher Secondary with grades 6 to 12')
            count_of_higher_sec_two=0
            for record in records:
                school = record.sp_school
                if SchoolItems.objects.filter(sit_school_name=school,sit_desk_avai="Yes"):
                    count_of_higher_sec_two+=1
            records = objs.filter(sp_school_category='Secondary/Sr.Sec. with grades 1 to 10')
            count_of_sr_secondary_one=0
            for record in records:
                school = record.sp_school
                if SchoolItems.objects.filter(sit_school_name=school,sit_desk_avai="Yes"):
                    count_of_sr_secondary_one+=1
            records = objs.filter(sp_school_category='Secondary/Sr.Sec. with grades 6 to 10')
            count_of_sr_secondary_two=0
            for record in records:
                school = record.sp_school
                if SchoolItems.objects.filter(sit_school_name=school,sit_desk_avai="Yes"):
                    count_of_sr_secondary_two+=1
            records = objs.filter(sp_school_category='Secondary/Sr.Sec. with grades 9 and 10')
            count_of_sr_secondary_three=0
            for record in records:
                school = record.sp_school
                if SchoolItems.objects.filter(sit_school_name=school,sit_desk_avai="Yes"):
                    count_of_sr_secondary_three+=1
            records = objs.filter(sp_school_category='Higher Secondary with grades 9 to 12')
            count_of_higher_sec_three=0
            for record in records:
                school = record.sp_school
                if SchoolItems.objects.filter(sit_school_name=school,sit_desk_avai="Yes"):
                    count_of_higher_sec_three+=1
            records = objs.filter(sp_school_category='Hr.Sec. /Jr.College only with grades 11 and 12')
            count_of_college=0
            for record in records:
                school = record.sp_school
                if SchoolItems.objects.filter(sit_school_name=school,sit_desk_avai="Yes"):
                    count_of_college+=1
            
            total_schools = count_of_primary_one + count_of_primary_two + count_of_higher_sec_one + count_of_upper_primary + count_of_higher_sec_two + count_of_sr_secondary_one + count_of_sr_secondary_two + count_of_sr_secondary_three + count_of_higher_sec_three + count_of_college
            table_data.append({
                'block_name':block,
                'count_of_primary_one':count_of_primary_one,
                'count_of_primary_two':count_of_primary_two,
                'count_of_higher_sec_one':count_of_higher_sec_one,
                'count_of_upper_primary':count_of_upper_primary,
                'count_of_higher_sec_two':count_of_higher_sec_two,
                'count_of_sr_secondary_one':count_of_sr_secondary_one,
                'count_of_sr_secondary_two':count_of_sr_secondary_two,
                'count_of_sr_secondary_three':count_of_sr_secondary_three,
                'count_of_higher_sec_three':count_of_higher_sec_three,
                'count_of_college':count_of_college,
                'total_schools':total_schools
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_count_of_primary_one += count_of_primary_one
                total_count_of_primary_two += count_of_primary_two
                total_count_of_higher_sec_one += count_of_higher_sec_one
                total_count_of_upper_primary += count_of_upper_primary
                total_count_of_higher_sec_two += count_of_higher_sec_two
                total_count_of_sr_secondary_one += count_of_sr_secondary_one
                total_count_of_sr_secondary_two += count_of_sr_secondary_two
                total_count_of_sr_secondary_three += count_of_sr_secondary_three
                total_count_of_higher_sec_three += count_of_higher_sec_three
                total_count_of_college += count_of_college
                total_total_schools += total_schools
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'count_of_primary_one':total_count_of_primary_one,
                'count_of_primary_two':total_count_of_primary_two,
                'count_of_higher_sec_one':total_count_of_higher_sec_one,
                'count_of_upper_primary':total_count_of_upper_primary,
                'count_of_higher_sec_two':total_count_of_higher_sec_two,
                'count_of_sr_secondary_one':total_count_of_sr_secondary_one,
                'count_of_sr_secondary_two':total_count_of_sr_secondary_two,
                'count_of_sr_secondary_three':total_count_of_sr_secondary_three,
                'count_of_higher_sec_three':total_count_of_higher_sec_three,
                'count_of_college':total_count_of_college,
                'total_schools':total_total_schools
            }


        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)


