from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic import ListView
from .models import Journey
from django.contrib.auth.decorators import login_required


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


class JourneyListView(ListView):
    model = Journey
    template_name = 'JourneyMap/journeys.html'
    context_object_name = 'journeys'
    # order journeys by newest to oldest
    ordering = ['-date_posted']

# @login_required
# def journeys(request):
#     context = {
#         'title': _('Journeys'),
#         'journeys': Journey.objects.all()
#     }
#     return render(request, 'JourneyMap/journeys.html', context)
