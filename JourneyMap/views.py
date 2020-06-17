from django.shortcuts import render
from django.utils.translation import gettext as _


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
