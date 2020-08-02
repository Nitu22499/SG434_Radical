from datetime import date
from profiles.models import District

def get_districts():
    districts_choices = tuple()
    for obj in District.objects.all().order_by('district_name'):
        districts_choices += ((obj.id, obj.district_name), )
    return districts_choices

def year_choices():
    today = date.today()
    if (today < date(today.year, 5, 1)):
        year = (today.year - 1)
    else:
        year = today.year

    year_list = list(range(year, 1990, -1))

    temp_list = []
    for e in year_list:
        temp_str = str(e) + "-" + str(e + 1)
        temp_var = (temp_str, temp_str)
        temp_list.append(temp_var)
    return tuple(temp_list)

def academic_year():
    today = date.today()
    if (today < date(today.year, 5, 1)):
        year = (today.year - 1)
        return str(year) + "-" + str(year + 1)
    else:
        year = today.year
        return str(year) + "-" + str(year + 1)

    
