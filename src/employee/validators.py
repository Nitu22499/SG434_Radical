from django.core.exceptions import ValidationError
from django.forms import ValidationError as FormValidationError

from .utils import ERROR_MESSAGES


def validate_phone_number(phone_number):
    if len(str(phone_number)) != 10:
        raise ValidationError(**ERROR_MESSAGES['invalid_phone_number'])


def validate_phone_number_form(phone_number):
    if len(str(phone_number)) != 10:
        raise FormValidationError(**ERROR_MESSAGES['invalid_phone_number'])
