from django.apps import AppConfig


class MemberConfig(AppConfig):
    name = 'members'

    def ready(self):
        import signals