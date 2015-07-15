from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Person


@receiver(post_save, sender=Person)
def signal_send_user_email(sender, instance, created, **kwargs):
    if created:  # Check if coming instance was from newly created.
        subject = 'Welcome to Profconn'
        from_email = 'no-reply@profconn.com'
        recipients = [instance.email]
        message = '''
        Thanks for register {user},

        Here is your login credential.

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
