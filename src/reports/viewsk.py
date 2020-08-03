from django.views.generic import TemplateView, FormView
from .forms import ReportForm
from django.urls import reverse_lazy
from misc.utilities import get_blocks
from schoolinfo.models import SchoolProfile
from profiles.models import Block, District
from employee.models import Teacher
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