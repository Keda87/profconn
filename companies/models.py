import uuid

from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import EmailValidator, URLValidator


class CommonInfo(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)  # For soft delete.

    class Meta:
        abstract = True


class Company(CommonInfo):
    """Model contains company information."""

    EXTRA_SMALL, SMALL, MEDIUM, LARGE, X_LARGE, XX_LARGE = range(6)
    EMPLOYEE_RANGE_CHOICES = (
        (EXTRA_SMALL, '1-10  {employee}'.format(employee=_('employees'))),
        (SMALL, '10-50 {employee}'.format(employee=_('employees'))),
        (MEDIUM, '50-500 {employee}'.format(employee=_('employees'))),
        (LARGE, '500-1000 {employee}'.format(employee=_('employees'))),
        (X_LARGE, '1000-5000 {employee}'.format(employee=_('employees'))),
        (XX_LARGE, '5000-... {employee}'.format(employee=_('employees')))
    )

    name = models.CharField(max_length=120)
    employee_range = models.SmallIntegerField(choices=EMPLOYEE_RANGE_CHOICES)
    founded = models.DateField()
    address = models.TextField()
    email = models.EmailField(validators=[EmailValidator])
    phone = models.CharField(max_length=30)
    website = models.URLField(validators=[URLValidator])
    logo = models.ImageField(height_field=50, width_field=50,
                             upload_to=u'logos/%Y/%m/%d', blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'companies'
