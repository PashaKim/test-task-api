from datetime import date
from django.core.exceptions import ValidationError


def over_18(value):
    today = date.today()

    if today.year - 18 < value.year:
        raise ValidationError('You must be over 18 old to register!')
