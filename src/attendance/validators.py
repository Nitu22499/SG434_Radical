from django.core.exceptions import ValidationError
from django.forms import ValidationError as FormValidationError
from django.utils.timezone import now as today

from .utils import ERROR_MESSAGES


def validate_no_future_date(date):
    if date > today().date():
        raise ValidationError(**ERROR_MESSAGES.get('future_date_error'))


def validate_no_future_date_form(date):
    if date > today().date():
        raise FormValidationError(**ERROR_MESSAGES.get('future_date_error'))
