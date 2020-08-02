from django.core.exceptions import ValidationError
from django.utils.timezone import now as today


def validate_no_future_date(date):
    if date > today().date():
        raise ValidationError("Date cannot be from future")
