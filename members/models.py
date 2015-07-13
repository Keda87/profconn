import uuid
from django.core.validators import EmailValidator

from django.db import models
from django.contrib.auth.models import User


def profile_stored(instance, filename):
    """Handle storing user profile image to a directory."""
    return u'profile/{email}/%Y/%m/%d/{filename}'.format(email=instance.email,
                                                         filename=filename)


class CommonInfo(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)  # For soft delete.

    class Meta:
        abstract = True


class Person(CommonInfo):
    """Model contains registered user basic information."""
    user = models.OneToOneField(User)
    name = models.CharField(max_length=120)
    birth = models.DateField()
    email = models.EmailField(validators=[EmailValidator])
    profile_picture = models.ImageField(upload_to=profile_stored, blank=True)

    headline = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)

    def __unicode__(self):
        return self.email

    def save(self, **kwargs):
        # Check if `Person` newly created, then create and assign `User`
        # instance.
        if self.id is None:
            user = User.objects.create(**{'email': self.email,
                                          'username': self.email})
            self.user = user
        super(Person, self).save(**kwargs)


class Experience(CommonInfo):
    """Model contains professional experience."""
    company = models.ForeignKey('companies.Company', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    # Determine if user currently working in the company
    is_present = models.BooleanField(default=False)
    person = models.ForeignKey(Person)

    def __unicode__(self):
        return self.company.name

    def save(self, **kwargs):
        # Check if `end_date` not filled, then set as present.
        if self.end_date is None:
            self.is_present = True
        super(Experience, self).save(**kwargs)
