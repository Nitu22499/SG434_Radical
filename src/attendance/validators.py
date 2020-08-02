from django.core.exceptions import ValidationError
from django.forms import ValidationError as FormValidationError
from django.utils.timezone import now as today
from django.utils.translation import gettext as _

error_messages = {
    'future_date_error': {'message': _('Date cannot be from future'), 'code': 'date_future_error'}
}


def validate_no_future_date(date):
    if date > today().date():
        raise ValidationError(**error_messages.get('future_date_error'))


def validate_no_future_date_form(date):
    if date > today().date():
        raise FormValidationError(**error_messages.get('future_date_error'))
