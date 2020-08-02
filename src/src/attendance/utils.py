from django.utils.translation import gettext as _

ERROR_MESSAGES = {
    'future_date_error': {'message': _('Date cannot be from future'), 'code': 'date_future_error'},
    'invalid_date_range': {'message': _('"Start date" cannot be future date of "end date"'),
                           'code': 'invalid_date_range'}
}
