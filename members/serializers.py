from rest_framework import serializers

from .models import Person, Experience, Connection

excluded_field = ['created', 'modified', 'is_deleted']

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        exclude = excluded_field + ['user']


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        exclude = excluded_field


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        exlude = excluded_field
