from django.views.generic import TemplateView

class Home(TemplateView):
    template_name = 'base.html'

    def get_template_names(self):
        if self.request.user.is_school_admin:
            self.template_name = 'misc/school_home.html'
        elif self.request.user.is_student:
            self.template_name = 'misc/student_home.html'
        elif self.request.user.is_block_admin:
            self.template_name = 'misc/block_home.html'
        elif self.request.user.is_district_admin:
            self.template_name = 'misc/district_home.html'
        return [self.template_name]