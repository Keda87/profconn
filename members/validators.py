from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


def unique_registered_email(value):
    """Validate email must be not registered in database."""
    from .models import Person
    if Person.objects.filter(email=value).exists():
        raise ValidationError(_('Email already registered.'))
