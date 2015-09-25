from django.views.generic import TemplateView
from django.shortcuts import render

from rest_framework import viewsets

from .serializers import PersonSerializer, ConnectionSerializer, \
    ExperienceSerializer

from .models import Person, Connection, Experience


class LandingPage(TemplateView):
    """ Index page of profconn apps. """
    template_name = 'members/index.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


# ---------------------------- Rest API views ----------------------------------
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
