from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Person, Connection


@receiver(post_save, sender=Person)
def signal_send_user_email(sender, instance, created, **kwargs):
    if created:  # Check if coming instance was from newly created.
        subject = 'Welcome to Profconn'
        from_email = 'no-reply@profconn.com'
        recipients = [instance.email]
        message = '''
        Thanks for register {user},

        Here is your login credential below.
        username    : {username}
        password    : {password}

        For security reason, please update your password in your profile settings.

        Regards,

        Profconn Team.
        '''.format(user=instance.name,
                   username=instance.user.username,
                   password=instance.plain_password)

        # Send verification email and default password.
        send_mail(subject, message, from_email, recipients, fail_silently=True)

@receiver(post_save, sender=Connection)
def signal_approve_connection(sender, instance, created, **kwargs):
    if not created:  # Check if instance from updated `Connection` instance.
        if instance.status == Connection.APPROVED:
            friend, person = instance.person, instance.friend
            Connection.objects.create(person=person,
                                      friend=friend,
                                      status=Connection.APPROVED)

@receiver(post_delete, sender=Connection)
def signal_unfriend_connection(sender, instance, **kwargs):
    connection = Connection.objects.filter(person=instance.friend,
                                           friend=instance.person,
                                           status=Connection.APPROVED)
    # Check if reversed connection exist then delete it.
    if connection.exists():
        connection.delete()
