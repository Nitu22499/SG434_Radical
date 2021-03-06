from django.views.generic import TemplateView, FormView
from .forms import ReportForm
from django.urls import reverse_lazy
from misc.utilities import get_blocks
from schoolinfo.models import SchoolProfile
from profiles.models import Block, District, Student
from employee.models import Teacher
from schoolinfo.models2 import SchoolIncentives
from misc.utilities import academic_year



class TypeOfSchool(FormView):
    template_name = 'reports/type_of_school.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:type_of_school')
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
        return super(TypeOfSchool, self).get(request, *args, **kwargs)

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

        total_boys_schools = 0
        total_girls_schools = 0
        total_co_educational_schools = 0
        total_total_schools = 0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            records = objs.filter(sp_cd=block)     # get schools in particular block
            boys_school = records.filter(sp_school_type='Boys').count()
            girls_school = records.filter(sp_school_type='Girls').count()
            co_educational_school = records.filter(sp_school_type='Co-educational').count()
            total_schools = boys_school + girls_school + co_educational_school
            table_data.append({
                'block_name':block,
                'boys_school':boys_school,
                'girls_school':girls_school,
                'co_educational_school':co_educational_school,
                'total_schools':total_schools
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_boys_schools += boys_school
                total_girls_schools += girls_school
                total_co_educational_schools += co_educational_school
                total_total_schools += total_schools
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'boys_school':total_boys_schools,
                'girls_school':total_girls_schools,
                'co_educational_school':total_co_educational_schools,
                'total_schools':total_total_schools
            }


        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)


class SchoolsByArea(FormView):
    template_name = 'reports/schools-by-area.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:school_by_area')
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
        return super(SchoolsByArea, self).get(request, *args, **kwargs)

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

        total_urban_schools = 0
        total_rural_schools = 0
        total_total_schools = 0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            records = objs.filter(sp_cd=block)     # get schools in particular block
            urban_school = records.filter(sp_school_located='Urban').count()
            rural_school = records.filter(sp_school_located='Rural').count()
            total_schools = urban_school + rural_school
            table_data.append({
                'block_name':block,
                'urban_school':urban_school,
                'rural_school':rural_school,
                'total_schools':total_schools
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_urban_schools += urban_school
                total_rural_schools += rural_school
                total_total_schools += total_schools
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'urban_school':total_urban_schools,
                'rural_school':total_rural_schools,
                'total_schools':total_total_schools
            }


        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)
         

class TeachersBySchoolCategory(FormView):
    template_name = 'reports/teachers-by-school-category.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:teachers_by_school_category')
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
        return super(TeachersBySchoolCategory, self).get(request, *args, **kwargs)

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
        if self.categories_field:
            total_count_cat_field = 0
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
            temp_obj = objs.filter(sp_cd=block)    # get schools in particular block
            if self.categories_field:
                count_cat_field=0
                teachers_in_current_block = Teacher.objects.filter(teacher_employee__employee_school__school_block__block_name=block)
                for obj in temp_obj:
                    school = obj.sp_school
                    count_cat_field+=teachers_in_current_block.filter(teacher_employee__employee_school=school).count()
            records = temp_obj.filter(sp_school_category='Primary only with grades 1 to 5')
            count_of_primary_one=0
            teachers_in_current_block = Teacher.objects.filter(teacher_employee__employee_school__school_block__block_name=block)
            for record in records:
                school = record.sp_school
                count_of_primary_one+=teachers_in_current_block.filter(teacher_employee__employee_school=school).count()
            records = temp_obj.filter(sp_school_category='Primary only with grades 1 to 8')
            count_of_primary_two=0
            for record in records:
                school = record.sp_school
                count_of_primary_two+=teachers_in_current_block.filter(teacher_employee__employee_school=school).count()
            records = temp_obj.filter(sp_school_category='Higher Secondary with grades 1 to 12')
            count_of_higher_sec_one=0
            for record in records:
                school = record.sp_school
                count_of_higher_sec_one+=teachers_in_current_block.filter(teacher_employee__employee_school=school).count()
            records = temp_obj.filter(sp_school_category='Upper Primary only with grades 6 to 8')
            count_of_upper_primary=0
            for record in records:
                school = record.sp_school
                count_of_upper_primary+=teachers_in_current_block.filter(teacher_employee__employee_school=school).count()
            records = temp_obj.filter(sp_school_category='Higher Secondary with grades 6 to 12')
            count_of_higher_sec_two=0
            for record in records:
                school = record.sp_school
                count_of_higher_sec_two+=teachers_in_current_block.filter(teacher_employee__employee_school=school).count()
            records = temp_obj.filter(sp_school_category='Secondary/Sr.Sec. with grades 1 to 10')
            count_of_sr_secondary_one=0
            for record in records:
                school = record.sp_school
                count_of_sr_secondary_one+=teachers_in_current_block.filter(teacher_employee__employee_school=school).count()
            records = temp_obj.filter(sp_school_category='Secondary/Sr.Sec. with grades 6 to 10')
            count_of_sr_secondary_two=0
            for record in records:
                school = record.sp_school
                count_of_sr_secondary_two+=teachers_in_current_block.filter(teacher_employee__employee_school=school).count()
            records = temp_obj.filter(sp_school_category='Secondary/Sr.Sec. with grades 9 and 10')
            count_of_sr_secondary_three=0
            for record in records:
                school = record.sp_school
                count_of_sr_secondary_three+=teachers_in_current_block.filter(teacher_employee__employee_school=school).count()
            records = temp_obj.filter(sp_school_category='Higher Secondary with grades 9 to 12')
            count_of_higher_sec_three=0
            for record in records:
                school = record.sp_school
                count_of_higher_sec_three+=teachers_in_current_block.filter(teacher_employee__employee_school=school).count()
            records = temp_obj.filter(sp_school_category='Hr.Sec. /Jr.College only with grades 11 and 12')
            count_of_college=0
            for record in records:
                school = record.sp_school
                count_of_college+=teachers_in_current_block.filter(teacher_employee__employee_school=school).count()
            
            total_schools = count_of_primary_one + count_of_primary_two + count_of_higher_sec_one + count_of_upper_primary + count_of_higher_sec_two + count_of_sr_secondary_one + count_of_sr_secondary_two + count_of_sr_secondary_three + count_of_higher_sec_three + count_of_college
            if self.categories_field:
                table_data.append({
                    'block_name':block,
                    'count_cat_field': count_cat_field
                })
            else:
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

            if not self.blocks_field and not self.categories_field:       # total of schools of blocks when more than 1 block
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
            
        if not self.blocks_field and not self.categories_field:       # add to context total tally of schools if more than 1 block.
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

        if self.categories_field:
            kwargs['cat_field_name'] = self.categories_field
        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)



class TeachersBySocialCategory(FormView):
    template_name = 'reports/teachers-by-social-category.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:teachers_by_social_category')
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
        return super(TeachersBySocialCategory, self).get(request, *args, **kwargs)

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
        total_count_OPEN = 0
        total_count_SC = 0
        total_count_ST = 0
        total_count_OBC = 0
        total_count_ORC = 0
        total_count_OTHERS = 0
        total_total_schools = 0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            records = objs.filter(sp_cd=block)    # get schools in particular block
            teachers_in_current_block = Teacher.objects.filter(teacher_employee__employee_school__school_block__block_name=block)
            count_OPEN = 0
            count_SC = 0
            count_ST = 0
            count_OBC = 0
            count_ORC = 0
            count_OTHERS = 0
            for record in records:
                school=record.sp_school
                teachers_in_current_block_and_school = teachers_in_current_block.filter(teacher_employee__employee_school=school)
                count_OPEN += teachers_in_current_block_and_school.filter(teacher_employee__employee_social_category='OPEN').count()
                count_SC += teachers_in_current_block_and_school.filter(teacher_employee__employee_social_category='SC').count()
                count_ST += teachers_in_current_block_and_school.filter(teacher_employee__employee_social_category='ST').count()
                count_OBC += teachers_in_current_block_and_school.filter(teacher_employee__employee_social_category='OBC').count()
                count_ORC += teachers_in_current_block_and_school.filter(teacher_employee__employee_social_category='ORC').count()
                count_OTHERS += teachers_in_current_block_and_school.filter(teacher_employee__employee_social_category='OTHERS').count()
            total_schools = count_OPEN + count_SC + count_ST + count_OBC + count_ORC + count_OTHERS

            table_data.append({
                'block_name':block,
                'count_OPEN':count_OPEN,
                'count_SC':count_SC,
                'count_ST':count_ST,
                'count_OBC':count_OBC,
                'count_ORC':count_ORC,
                'count_OTHERS':count_OTHERS,
                'total_schools':total_schools
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_count_OPEN += count_OPEN
                total_count_SC += count_SC
                total_count_ST += count_ST
                total_count_OBC += count_OBC
                total_count_ORC += count_ORC
                total_count_OTHERS += count_OTHERS
                total_total_schools += total_schools
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'count_OPEN':total_count_OPEN,
                'count_SC':total_count_SC,
                'count_OBC':total_count_OBC,
                'count_ORC':total_count_ORC,
                'count_OTHERS':total_count_OTHERS,
                'total_schools':total_total_schools,
                'count_ST':total_count_ST
            }


        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)  


class TeachersReceivedInServiceTraining(FormView):
    template_name = 'reports/teachers-received-in-service-training.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:teachers_received_in_service_training')
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
            self.districts_field = int(self.request.GET.get('districts_field') or 0)
        if self.request.GET.get('blocks_field'):
            self.blocks_field = int(self.request.GET.get('blocks_field')  or 0)
        if self.request.GET.get('categories_field'):
            self.categories_field = self.request.GET.get('categories_field')
        return super(TeachersReceivedInServiceTraining, self).get(request, *args, **kwargs)

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
        total_state_govt_schools = 0
        total_central_govt_schools = 0
        total_private_schools = 0
        total_local_body_schools = 0
        total_other_schools = 0
        total_total_schools = 0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            temp_obj = objs.filter(sp_cd=block)    # get schools in particular block
            teachers_in_current_block = Teacher.objects.filter( # get teachers in current block
                teacher_employee__employee_school__school_block__block_name=block 
            )
        #   Initialize Count   
            count_state_govt_schools = 0
            count_central_govt_schools = 0
            count_private_schools = 0
            count_local_body_schools = 0
            count_other_schools = 0
            count_total_schools = 0
        #   Start Counting
            records = temp_obj.filter(sp_management_code='State Govt.')            
            for record in records:
                count_state_govt_schools += teachers_in_current_block.filter(teacher_employee__employee_school=record.sp_school).count()
            
            records = temp_obj.filter(sp_management_code='Central Govt.')            
            for record in records:
                count_central_govt_schools += teachers_in_current_block.filter(teacher_employee__employee_school=record.sp_school).count()

            records = temp_obj.filter(sp_management_code='Private')            
            for record in records:
                count_private_schools += teachers_in_current_block.filter(teacher_employee__employee_school=record.sp_school).count()

            records = temp_obj.filter(sp_management_code='Local Body')            
            for record in records:
                count_local_body_schools += teachers_in_current_block.filter(teacher_employee__employee_school=record.sp_school).count()

            records = temp_obj.filter(sp_management_code='Other')            
            for record in records:
                count_other_schools += teachers_in_current_block.filter(teacher_employee__employee_school=record.sp_school).count()

        
            total_schools = count_state_govt_schools + count_central_govt_schools + count_private_schools + count_local_body_schools + count_other_schools

            table_data.append({
                'block_name':block,
                'count_state_govt_schools':count_state_govt_schools,
                'count_central_govt_schools':count_central_govt_schools,
                'count_private_schools':count_private_schools,
                'count_local_body_schools':count_local_body_schools,
                'count_other_schools':count_other_schools,
                'total_schools':total_schools
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_state_govt_schools += count_state_govt_schools
                total_central_govt_schools += count_central_govt_schools
                total_private_schools += count_private_schools
                total_local_body_schools += count_local_body_schools
                total_other_schools += count_other_schools
                total_total_schools += total_schools
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'count_state_govt_schools':total_state_govt_schools,
                'count_central_govt_schools':total_central_govt_schools,
                'count_private_schools':total_private_schools,
                'count_local_body_schools':total_local_body_schools,
                'count_other_schools':total_other_schools,
                'total_schools':total_total_schools
            }

        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)  

class TeachersTrainedForCWSN(FormView):
    template_name = 'reports/teachers-trained-for-cwsn.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:teachers_trained_for_cwsn')
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
            self.districts_field = int(self.request.GET.get('districts_field') or 0)
        if self.request.GET.get('blocks_field'):
            self.blocks_field = int(self.request.GET.get('blocks_field')  or 0)
        if self.request.GET.get('categories_field'):
            self.categories_field = self.request.GET.get('categories_field')
        return super(TeachersTrainedForCWSN, self).get(request, *args, **kwargs)

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
        total_state_govt_schools = 0
        total_central_govt_schools = 0
        total_private_schools = 0
        total_local_body_schools = 0
        total_other_schools = 0
        total_total_schools = 0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            temp_obj = objs.filter(sp_cd=block)    # get schools in particular block
            teachers_in_current_block = Teacher.objects.filter( # get teachers in current block
                teacher_employee__employee_school__school_block__block_name=block,
                teacher_training_received='Knowledge and skills for CWSN'
            )
        #   Initialize Count   
            count_state_govt_schools = 0
            count_central_govt_schools = 0
            count_private_schools = 0
            count_local_body_schools = 0
            count_other_schools = 0
            count_total_schools = 0
        #   Start Counting
            records = temp_obj.filter(sp_management_code='State Govt.')  
            #
            for record in records:
                
                count_state_govt_schools += teachers_in_current_block.filter(teacher_employee__employee_school=record.sp_school).count()
            
            records = temp_obj.filter(sp_management_code='Central Govt.')            
            for record in records:
                count_central_govt_schools += teachers_in_current_block.filter(teacher_employee__employee_school=record.sp_school).count()

            records = temp_obj.filter(sp_management_code='Private')            
            for record in records:
                count_private_schools += teachers_in_current_block.filter(teacher_employee__employee_school=record.sp_school).count()

            records = temp_obj.filter(sp_management_code='Local Body')            
            for record in records:
                count_local_body_schools += teachers_in_current_block.filter(teacher_employee__employee_school=record.sp_school).count()

            records = temp_obj.filter(sp_management_code='Other')            
            for record in records:
                count_other_schools += teachers_in_current_block.filter(teacher_employee__employee_school=record.sp_school).count()

        
            total_schools = count_state_govt_schools + count_central_govt_schools + count_private_schools + count_local_body_schools + count_other_schools

            table_data.append({
                'block_name':block,
                'count_state_govt_schools':count_state_govt_schools,
                'count_central_govt_schools':count_central_govt_schools,
                'count_private_schools':count_private_schools,
                'count_local_body_schools':count_local_body_schools,
                'count_other_schools':count_other_schools,
                'total_schools':total_schools
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_state_govt_schools += count_state_govt_schools
                total_central_govt_schools += count_central_govt_schools
                total_private_schools += count_private_schools
                total_local_body_schools += count_local_body_schools
                total_other_schools += count_other_schools
                total_total_schools += total_schools
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'count_state_govt_schools':total_state_govt_schools,
                'count_central_govt_schools':total_central_govt_schools,
                'count_private_schools':total_private_schools,
                'count_local_body_schools':total_local_body_schools,
                'count_other_schools':total_other_schools,
                'total_schools':total_total_schools
            }

        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)  


class StudentsEnrolmentByMgmtCategory(FormView):
    template_name = 'reports/students-enrolment-by-mgmt-category.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:students_enrolment_by_mgmt_category')
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
            self.districts_field = int(self.request.GET.get('districts_field') or 0)
        if self.request.GET.get('blocks_field'):
            self.blocks_field = int(self.request.GET.get('blocks_field')  or 0)
        if self.request.GET.get('categories_field'):
            self.categories_field = self.request.GET.get('categories_field')
        return super(StudentsEnrolmentByMgmtCategory, self).get(request, *args, **kwargs)

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
        total_state_govt_schools = 0
        total_central_govt_schools = 0
        total_private_schools = 0
        total_local_body_schools = 0
        total_other_schools = 0
        total_total_schools = 0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            temp_obj = objs.filter(sp_cd=block)
            all_schools = Block.objects.filter(block_name=block)[0].school_set.all()
            students_in_current_block = Student.objects.none()
            for school in all_schools:
                students_in_current_block |= Student.objects.filter(stud_school=school)
            
            # students_in_current_block = Student.objects.filter( # get students in current block
            #     stud_school__school_block__block_name=block
            # )
        #   Initialize Count   
            count_state_govt_schools = 0
            count_central_govt_schools = 0
            count_private_schools = 0
            count_local_body_schools = 0
            count_other_schools = 0
            count_total_schools = 0
        #   Start Counting
            records = temp_obj.filter(sp_management_code='State Govt.')            
            for record in records:
                count_state_govt_schools += students_in_current_block.filter(stud_school=record.sp_school).count()
            
            records = temp_obj.filter(sp_management_code='Central Govt.')            
            for record in records:
                count_central_govt_schools += students_in_current_block.filter(stud_school=record.sp_school).count()

            records = temp_obj.filter(sp_management_code='Private')            
            for record in records:
                count_private_schools += students_in_current_block.filter(stud_school=record.sp_school).count()

            records = temp_obj.filter(sp_management_code='Local Body')            
            for record in records:
                count_local_body_schools += students_in_current_block.filter(stud_school=record.sp_school).count()

            records = temp_obj.filter(sp_management_code='Other')            
            for record in records:
                count_other_schools += students_in_current_block.filter(stud_school=record.sp_school).count()

        
            total_schools = count_state_govt_schools + count_central_govt_schools + count_private_schools + count_local_body_schools + count_other_schools

            table_data.append({
                'block_name':block,
                'count_state_govt_schools':count_state_govt_schools,
                'count_central_govt_schools':count_central_govt_schools,
                'count_private_schools':count_private_schools,
                'count_local_body_schools':count_local_body_schools,
                'count_other_schools':count_other_schools,
                'total_schools':total_schools
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_state_govt_schools += count_state_govt_schools
                total_central_govt_schools += count_central_govt_schools
                total_private_schools += count_private_schools
                total_local_body_schools += count_local_body_schools
                total_other_schools += count_other_schools
                total_total_schools += total_schools
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'count_state_govt_schools':total_state_govt_schools,
                'count_central_govt_schools':total_central_govt_schools,
                'count_private_schools':total_private_schools,
                'count_local_body_schools':total_local_body_schools,
                'count_other_schools':total_other_schools,
                'total_schools':total_total_schools
            }

        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)  


class StudentsEnrolmentByGender(FormView):
    template_name = 'reports/students-enrolment-by-gender.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:students_enrolment_by_gender')
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
            self.districts_field = int(self.request.GET.get('districts_field') or 0)
        if self.request.GET.get('blocks_field'):
            self.blocks_field = int(self.request.GET.get('blocks_field')  or 0)
        if self.request.GET.get('categories_field'):
            self.categories_field = self.request.GET.get('categories_field')
        return super(StudentsEnrolmentByGender, self).get(request, *args, **kwargs)

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
        total_boys = 0
        total_girls = 0
        total_boys_and_girls = 0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            temp_obj = objs.filter(sp_cd=block)
            all_schools = Block.objects.filter(block_name=block)[0].school_set.all()
            boys = girls = Student.objects.none()
            for school in all_schools:
                boys |= Student.objects.filter(stud_school=school, user__gender='MALE')
                girls |= Student.objects.filter(stud_school=school, user__gender='FEMALE')
            
            boys = boys.count()
            girls = girls.count()
        
            boys_and_girls = boys + girls

            table_data.append({
                'block_name':block,
                'boys':boys,
                'girls':girls,
                'boys_and_girls':boys_and_girls
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_boys += boys
                total_girls += girls
                total_boys_and_girls += boys_and_girls
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'total_boys':total_boys,
                'total_girls':total_girls,
                'total_boys_and_girls':total_boys_and_girls
            }

        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)  


class StudentsBySocialCategory(FormView):
    template_name = 'reports/students-by-social-category.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:students_by_social_category')
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
        return super(StudentsBySocialCategory, self).get(request, *args, **kwargs)

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
        total_count_OPEN = 0
        total_count_SC = 0
        total_count_ST = 0
        total_count_OBC = 0
        total_count_MBC = 0
        total_count_OTHERS = 0
        total_total_schools = 0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            records = objs.filter(sp_cd=block)    # get schools in particular block
            students_in_current_block = Student.objects.filter(stud_school__school_block__block_name=block)
            count_OPEN = 0
            count_SC = 0
            count_ST = 0
            count_OBC = 0
            count_MBC = 0
            count_OTHERS = 0
            for record in records:
                school=record.sp_school
                students_in_current_block_and_school = students_in_current_block.filter(stud_school=school)
                count_OPEN += students_in_current_block_and_school.filter(stud_socialCategory='GENERAL').count()
                count_SC += students_in_current_block_and_school.filter(stud_socialCategory='SC').count()
                count_ST += students_in_current_block_and_school.filter(stud_socialCategory='ST').count()
                count_OBC += students_in_current_block_and_school.filter(stud_socialCategory='OBC').count()
                count_MBC += students_in_current_block_and_school.filter(stud_socialCategory='MBC').count()
                count_OTHERS += students_in_current_block_and_school.filter(stud_socialCategory='OTHER').count()
            total_schools = count_OPEN + count_SC + count_ST + count_OBC + count_MBC + count_OTHERS

            table_data.append({
                'block_name':block,
                'count_OPEN':count_OPEN,
                'count_SC':count_SC,
                'count_ST':count_ST,
                'count_OBC':count_OBC,
                'count_MBC':count_MBC,
                'count_OTHERS':count_OTHERS,
                'total_schools':total_schools
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_count_OPEN += count_OPEN
                total_count_SC += count_SC
                total_count_ST += count_ST
                total_count_OBC += count_OBC
                total_count_MBC += count_MBC
                total_count_OTHERS += count_OTHERS
                total_total_schools += total_schools
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'count_OPEN':total_count_OPEN,
                'count_SC':total_count_SC,
                'count_OBC':total_count_OBC,
                'count_MBC':total_count_MBC,
                'count_OTHERS':total_count_OTHERS,
                'total_schools':total_total_schools,
                'count_ST':total_count_ST
            }

        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)  


class StudentsEnrolmentByArea(FormView):
    template_name = 'reports/students-enrolment-by-area.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:students_enrolment_by_area')
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
        return super(StudentsEnrolmentByArea, self).get(request, *args, **kwargs)

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

        total_urban_schools = 0
        total_rural_schools = 0
        total_total_schools = 0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            records = objs.filter(sp_cd=block)     # get schools in particular block
            urban_schools = records.filter(sp_school_located='Urban')
            rural_schools = records.filter(sp_school_located='Rural')
            students_in_current_block = Student.objects.filter(stud_school__school_block__block_name=block)
            urban_school = 0
            rural_school = 0
            for sch in urban_schools:
                school=sch.sp_school
                urban_school += students_in_current_block.filter(stud_school=school).count()
            for sch in rural_schools:
                school=sch.sp_school
                rural_school += students_in_current_block.filter(stud_school=school).count()
            
            urban_school = records.filter(sp_school_located='Urban').count()
            rural_school = records.filter(sp_school_located='Rural').count()
            total_schools = urban_school + rural_school
            table_data.append({
                'block_name':block,
                'urban_school':urban_school,
                'rural_school':rural_school,
                'total_schools':total_schools
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_urban_schools += urban_school
                total_rural_schools += rural_school
                total_total_schools += total_schools
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'urban_school':total_urban_schools,
                'rural_school':total_rural_schools,
                'total_schools':total_total_schools
            }


        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)


class StudentsReceivedFreeTextbooks(FormView):
    template_name = 'reports/students-received-free-textbooks.html'
    form_class = ReportForm
    success_url = reverse_lazy('reports:students_received_free_textbooks')
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
        return super(StudentsReceivedFreeTextbooks, self).get(request, *args, **kwargs)

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

        total_students_with_books = 0
        total_total_students = 0

        table_data = []     # compute and add data block wise to this list
        for block in blocks_list:
            records = objs.filter(sp_cd=block)     # get schools in particular block
            students_with_books = 0
            school_inc_block = SchoolIncentives.objects.filter(si_school_name__school_block__block_name=block)
            for record in records:
                school = record.sp_school
                school_inc = school_inc_block.filter(si_school_name=school, class_name='Free textbooks').first()
                # print(school_inc)
                if school_inc:
                    students_with_books += (school_inc.si_boys_total+school_inc.si_girls_total)

            table_data.append({
                'block_name':block,
                'students_with_books':students_with_books
            })

            if not self.blocks_field:       # total of schools of blocks when more than 1 block
                total_total_students += students_with_books
            
        if not self.blocks_field:       # add to context total tally of schools if more than 1 block.
            kwargs['total_tally'] = {
                'block_name':'TOTAL',
                'total_schools':total_total_students
            }

        kwargs['table_data'] = table_data

        return super().get_context_data(**kwargs)