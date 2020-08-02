from django.http import HttpResponse
from django.shortcuts import render

from .modelsk import EnrolmentPrePrimary,NewAdmissionsInGradeI,EnrolmentBySocialCategory,EnrolmentByAge
import json
from misc.utilities import academic_year, year_choices

# Section 4 (according to Data Capture Format)
#   New Admissions, Enrolment and Repeaters 
#   4.1.1 Total Enrolment in Pre Primary section
#   4.1.2 New Admissions in Grade I
def enrolmentPrePrimaryView(request, ac_year):
    template_name = 'schoolinfo/enrolment-pre-primary.html'

    epp, created = EnrolmentPrePrimary.objects.get_or_create(
        academic_year=ac_year, epp_school=request.user.school
    )
    nag, created = NewAdmissionsInGradeI.objects.get_or_create(
        academic_year=ac_year, nag_school=request.user.school
    )
    context = {
        "epp": epp,
        "nag": nag,
        'academic_year': ac_year
    }
    return render(request, template_name, context)

def saveEnrolmentPrePrimaryView(request, ac_year):
    data = json.loads(request.body)
    
    if not data[2]:
        try:
            epp = EnrolmentPrePrimary.objects.get(academic_year=ac_year,epp_school=request.user.school)
            epp.epp_lkg_b = data[0]["LKG"] or None
            epp.epp_ukg_b = data[0]["UKG"] or None
            epp.epp_lkg_g = data[1]["LKG"] or None
            epp.epp_ukg_g = data[1]["UKG"] or None
            epp.full_clean()
            epp.save()
        except Exception as e:
            return HttpResponse(json.dumps({ "err": str(e) }), content_type="application/json")
    else:
        try:
            nag = NewAdmissionsInGradeI.objects.get(academic_year=ac_year,nag_school=request.user.school)
            nag.nag_below_5_b = data[0]["below_5"] or None
            nag.nag_5_b = data[0]["5"] or None
            nag.nag_6_b = data[0]["6"] or None
            nag.nag_7_b = data[0]["7"] or None
            nag.nag_above_7_b = data[0]["above_7"] or None
            # nag.nag_total_b = data[0]["total"] or None
            nag.nag_same_school_b = data[0]["same_school"] or None
            nag.nag_another_school_b = data[0]["another_school"] or None
            nag.nag_anganwadi_school_b = data[0]["anganwadi_school"] or None
            nag.nag_below_5_g = data[1]["below_5"] or None
            nag.nag_5_g = data[1]["5"] or None
            nag.nag_6_g = data[1]["6"] or None
            nag.nag_7_g = data[1]["7"] or None
            nag.nag_above_7_g = data[1]["above_7"] or None
            # nag.nag_total_g = data[1]["total"] or None
            nag.nag_same_school_g = data[1]["same_school"] or None
            nag.nag_another_school_g = data[1]["another_school"] or None
            nag.nag_anganwadi_school_g = data[1]["anganwadi_school"] or None
            nag.full_clean()
            nag.save()
        except Exception as e:
            return HttpResponse(json.dumps({ "err": str(e) }), content_type="application/json")
    return HttpResponse(json.dumps({ "msg": "success" }), content_type="application/json")


def enrolmentBySocialCategoryView(request, ac_year):
    template_name = 'schoolinfo/enrolment-by-social-category.html'

    class_choices = (
        ('General', 'General'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('OBC', 'OBC')
    )

    response = {}
    context = {
        'class': class_choices,
        'academic_year': ac_year
    }
    
    for choice in class_choices:
        esc, created = EnrolmentBySocialCategory.objects.get_or_create(class_name=choice[0], academic_year=ac_year,
            esc_school = request.user.school
        )
        response.update({
            choice[0]: esc
        })
    context.update({
        'rows': response
    })    
    print(response)
    return render(request, template_name, context)


def saveEnrolmentBySocialCategoryView(request, ac_year):
    data = json.loads(request.body)
    rows = data['table']

    for row in rows:
        try:
            class_val = EnrolmentBySocialCategory.objects.get(academic_year=ac_year, class_name=row['class_name'],
                esc_school = request.user.school
            )
            class_val.class_pre_primary_B = row['boys_pp'] or None
            class_val.class_pre_primary_G = row['girls_pp'] or None
            class_val.class_I_B = row['boys_1'] or None
            class_val.class_I_G = row['girls_1'] or None
            class_val.class_II_B = row['boys_2'] or None
            class_val.class_II_G = row['girls_2'] or None
            class_val.class_III_B = row['boys_3'] or None
            class_val.class_III_G = row['girls_3'] or None
            class_val.class_IV_B = row['boys_4'] or None
            class_val.class_IV_G = row['girls_4'] or None
            class_val.class_V_B = row['boys_5'] or None
            class_val.class_V_G = row['girls_5'] or None
            class_val.class_VI_B = row['boys_6'] or None
            class_val.class_VI_G = row['girls_6'] or None
            class_val.class_VII_B = row['boys_7'] or None
            class_val.class_VII_G = row['girls_7'] or None
            class_val.class_VIII_B = row['boys_8'] or None
            class_val.class_VIII_G = row['girls_8'] or None
            class_val.class_IX_B = row['boys_9'] or None
            class_val.class_IX_G = row['girls_9'] or None
            class_val.class_X_B = row['boys_10'] or None
            class_val.class_X_G = row['girls_10'] or None
            class_val.class_XI_B = row['boys_11'] or None
            class_val.class_XI_G = row['girls_11'] or None
            class_val.class_XII_B = row['boys_12'] or None
            class_val.class_XII_G = row['girls_12'] or None
            # Validating and Saving the new Instance
            class_val.full_clean()
            class_val.save()
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({ "err": str(e) }), content_type="application/json")

    return HttpResponse(json.dumps({ "msg": "success" }), content_type="application/json")

def enrolmentByGradeView(request, ac_year):
    template_name = 'schoolinfo/enrolment-by-grade.html'

    class_choices = (
        ('<5', 'below 5'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
        ('13', '13'),
        ('14', '14'),
        ('15', '15'),
        ('16', '16'),
        ('17', '17'),
        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('>22', 'above 22'),
    )

    response = {}
    context = {
        'class': class_choices,
        'academic_year': ac_year
    }
    
    for choice in class_choices:
        esc, created = EnrolmentByAge.objects.get_or_create(class_name=choice[0], academic_year=ac_year,
            eba_school = request.user.school
        )
        response.update({
            choice[0]: esc
        })
    context.update({
        'rows': response
    })    
    return render(request, template_name, context)


def saveEnrolmentByGradeView(request, ac_year):
    data = json.loads(request.body)
    rows = data['table']

    for row in rows:
        try:
            class_val = EnrolmentByAge.objects.get(academic_year=ac_year, class_name=row['age_grade'],
                eba_school = request.user.school
            )
            class_val.class_I_B = row['boys_1'] or None
            class_val.class_I_G = row['girls_1'] or None
            class_val.class_II_B = row['boys_2'] or None
            class_val.class_II_G = row['girls_2'] or None
            class_val.class_III_B = row['boys_3'] or None
            class_val.class_III_G = row['girls_3'] or None
            class_val.class_IV_B = row['boys_4'] or None
            class_val.class_IV_G = row['girls_4'] or None
            class_val.class_V_B = row['boys_5'] or None
            class_val.class_V_G = row['girls_5'] or None
            class_val.class_VI_B = row['boys_6'] or None
            class_val.class_VI_G = row['girls_6'] or None
            class_val.class_VII_B = row['boys_7'] or None
            class_val.class_VII_G = row['girls_7'] or None
            class_val.class_VIII_B = row['boys_8'] or None
            class_val.class_VIII_G = row['girls_8'] or None
            class_val.class_IX_B = row['boys_9'] or None
            class_val.class_IX_G = row['girls_9'] or None
            class_val.class_X_B = row['boys_10'] or None
            class_val.class_X_G = row['girls_10'] or None
            class_val.class_XI_B = row['boys_11'] or None
            class_val.class_XI_G = row['girls_11'] or None
            class_val.class_XII_B = row['boys_12'] or None
            class_val.class_XII_G = row['girls_12'] or None
            # Validating and Saving the new Instance
            class_val.full_clean()
            class_val.save()
        except Exception as e:
            return HttpResponse(json.dumps({ "err": str(e) }), content_type="application/json")

    return HttpResponse(json.dumps({ "msg": "success" }), content_type="application/json")
    