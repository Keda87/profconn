import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import EmailValidator
from django.utils.translation import ugettext as _


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
    """
    Model contains registered user basic information.

    This model contains signal to perform task:
    1.  Model       : -
        Type        : post_save
        Location    : members.signals.signal_send_user_email
        Description : Sending email to new registered user to send default
                      password.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=120)
    birth = models.DateField()
    email = models.EmailField(unique=True, validators=[EmailValidator])
    profile_picture = models.ImageField(upload_to=profile_stored, blank=True)
    is_verified = models.BooleanField(default=False)
    connections = models.ManyToManyField('self', through='Connection',
                                         symmetrical=False, blank=True,
                                         through_fields=('person', 'friend',),)
    headline = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)

    def __unicode__(self):
        return self.email

    def save(self, **kwargs):
        # Check if `Person` newly created, then create and assign `User`
        # instance.
        if self.id is None:
            # Create user object.
            user = User.objects.create(**{'email': self.email,
                                          'username': self.email})
            # Create default password user.
            password = User.objects.make_random_password(length=15)
            user.set_password(password)
            user.save()

            self.user = user
            self.email = self.email.lower()
            self.name = self.name.title()
            self.plain_password = password  # extra field (not saved in database).
        super(Person, self).save(**kwargs)


class Connection(CommonInfo):
    """Intermediate table for many to many relationship person for friendship."""
    UNBLOCK, BLOCKED, REQUESTED, APPROVED, DECLINED = range(5)
    FRIENDSHIP_STATUS_CHOICES = (
        (UNBLOCK, _('Unblock')),
        (BLOCKED, _('Blocked')),
        (REQUESTED, _('Requested')),
        (APPROVED, _('Approved')),
        (DECLINED, _('Declined')),
    )

    person = models.ForeignKey(Person, related_name='requester')
    friend = models.ForeignKey(Person, related_name='friend')
    status = models.PositiveSmallIntegerField(choices=FRIENDSHIP_STATUS_CHOICES,
                                              null=True, default=None)

    class Meta:
        unique_together = ('person', 'friend',)

    def __unicode__(self):
        return self.person.name


class Experience(CommonInfo):
    """Model contains professional experience."""
    company = models.ForeignKey('companies.Company', null=True, blank=True,
                                related_name='+')
    role = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    # Determine if user currently working in the company
    is_present = models.BooleanField(default=False)
    person = models.ForeignKey(Person)

    def __unicode__(self):
        return self.company.name

    def save(self, **kwargs):
        self.role = self.role.title()
        # Check if `end_date` not filled, then set as present.
        if self.end_date is None:
            self.is_present = True
        super(Experience, self).save(**kwargs)
