from .utilities import academic_year

def default_academic_year(request):
    current_academic_year = academic_year()
    return {'current_academic_year': current_academic_year}