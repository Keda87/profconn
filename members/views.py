from django.views.generic.edit import FormView
from django.shortcuts import render

from .forms import SubscribeForm

from rest_framework import viewsets

from .serializers import PersonSerializer, ConnectionSerializer, \
    ExperienceSerializer

from .models import Person, Connection, Experience


class LandingPage(FormView):
    """ Landing page of profconn apps. """
    template_name = 'members/landing.html'
    form_class = SubscribeForm

    def get(self, request):
        context = {
            'form': self.form_class
        }
        return render(request, self.template_name, context)

    def form_valid(self, form):
        return super(LandingPage, self).form_valid(form)

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
