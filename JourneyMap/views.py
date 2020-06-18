from django.shortcuts import render
from django.utils.translation import gettext as _
from .models import Journey


def home(request):
    context = {
        'title': _('Home')
    }
    return render(request, 'JourneyMap/home.html', context)


def contact(request):
    context = {
        'title': _('Contact Us')
    }
    return render(request, 'JourneyMap/contact_us.html', context)


def journeys(request):
    context = {
        'title': _('Journeys'),
        'journeys': Journey.objects.all()
    }
    return render(request, 'JourneyMap/journeys.html', context)
