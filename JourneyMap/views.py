import logging
import logging.config
import os
import sys
from json import dumps

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import BadHeaderError
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaultfilters import register
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, DeleteView

from WebApplication import settings
from .forms import ContactForm, ImageForm, AddJourneyForm
from .models import Journey, Image

# from folium.utilities import get_bounds

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

logging.config.dictConfig(LOGGING)


def home(request):
    journeys = None

    if request.user.is_authenticated:
        journeys = Journey.objects.filter(user_id=request.user)

    context = {
        'title': _('Home'),
        'journeys': journeys,
    }

    return render(request, 'JourneyMap/home.html', context)


def privacy_policy(request):
    journeys = None

    if request.user.is_authenticated:
        journeys = Journey.objects.filter(user_id=request.user)

    context = {
        'title': _('Privacy Policy'),
        'journeys': journeys,
    }

    return render(request, 'JourneyMap/privacy_policy.html', context)


def terms_of_service(request):
    journeys = None

    if request.user.is_authenticated:
        journeys = Journey.objects.filter(user_id=request.user)

    context = {
        'title': _('Terms of Service'),
        'journeys': journeys,
    }

    return render(request, 'JourneyMap/terms_of_service.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            user_email = request.POST.get('email', '')

            context_email = {
                'message': request.POST.get('message', ''),
                'name': request.POST.get('name', ''),
                'email': user_email,
            }

            try:
                # Send an email with html template
                # Internal email
                html_email = 'JourneyMap/contact_us_email.html'
                html_message = render_to_string(html_email, context_email)

                message = EmailMessage(_('User send a Contact Form'), html_message, 'contact@journey-map.eu',
                                       ['contact@journey-map.eu'])
                message.content_subtype = 'html'
                message.send()

                # User email
                html_email_user = 'JourneyMap/contact_us_user_email.html'
                html_message_user = render_to_string(html_email_user, context_email)

                message = EmailMessage(_('We received your message'), html_message_user, 'contact@journey-map.eu',
                                       [user_email])
                message.content_subtype = 'html'
                message.send()

                messages.success(request, _('Thank you, your message was send.'))
                return redirect('JourneyMap_home')
            except BadHeaderError:
                messages.warning(request, _('An error occurred, please try again'))
                return redirect('JourneyMap_contact_us')

    else:
        form = ContactForm

    journeys = None
    if request.user.is_authenticated:
        journeys = Journey.objects.filter(user_id=request.user)

    context = {
        'title': _('Contact Us'),
        'form': form,
        'journeys': journeys
    }
    return render(request, 'JourneyMap/contact_us.html', context)


@register.filter
def empty(dict):
    return not bool(dict)


@register.filter
def dictvalue(dict, key):
    return dict.get(key)


@never_cache
@csrf_protect
def journeys(request):
    if request.method == "POST":
        form = AddJourneyForm(request.POST)
        if form.is_valid():
            journey = form.save(commit=False)
            journey.user = request.user
            journey.save()

            return redirect('JourneyMap_journeys')
    else:
        form = AddJourneyForm()

    qs = Journey.objects.filter(user_id=request.user.id)
    images = dict()

    for journey in qs:
        images[journey.id] = Image.objects.filter(journey=journey)[0: 5]

    context = {
        'form': form,
        'journeys': qs,
        'images': images
    }

    return render(request, 'JourneyMap/journeys.html', context)


def delete_journey(request):
    if request.method == "POST":
        qs = Journey.objects.filter(id=int(request.POST.get("id")))

        if qs.count() == 1 and qs.first().user_id == request.user.id:
            qs.first().delete()
        else:
            messages.warning(request, _('You are not allowed to delete this journey!'))

        return redirect('JourneyMap_journeys')
    else:
        if request.user.is_authenticated:
            return redirect('JourneyMap_journeys')
        else:
            return redirect('JourneyMap_home')


def cdp(request, iid):
    qs = Image.objects.filter(id=int(iid))

    if request.user.is_authenticated and qs.count() == 1:
        if qs.first().journey.user.id == request.user.id:
            image = qs.first()
            image_data = open(settings.MEDIA_ROOT + image.get_absolute_url(), 'rb').read()
            return HttpResponse(image_data, content_type='image/jpeg')

    return HttpResponse('')


def journey(request, jid):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = ImageForm(request.POST, request.FILES)
            form.user = request.user
            logging.info(request.FILES)

            if form.is_valid():
                image = form.save(commit=False)
                image.journey = Journey.objects.get(id=jid)
                image.title = os.path.basename(image.image.url).lower()
                logging.info(image.upload_image(image.title))
                upload_file(request.FILES['image'], image.get_file_path(), image.title)
                image.save()

        return redirect('JourneyMap_journey', jid)

    journeys = None
    if request.user.is_authenticated:
        journeys = Journey.objects.filter(user_id=request.user.id)

    qs = Image.objects.filter(journey_id=int(jid))

    context = {
        'journeys': journeys,
        'journey': jid,
        'images': qs
    }

    return render(request, 'JourneyMap/journey.html', context)


def upload_file(f, path, filename):
    logging.info(os.path.join(settings.MEDIA_ROOT, path))
    logging.info(os.path.join(settings.MEDIA_ROOT, path, filename))

    if not os.path.exists(settings.MEDIA_ROOT + '/' + path):
        os.makedirs(settings.MEDIA_ROOT + '/' + path)

    with open(os.path.join(settings.MEDIA_ROOT, path, filename), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def map(request, jid):
    journeys = None
    if request.user.is_authenticated:
        journeys = Journey.objects.filter(user_id=request.user.id)

    images = Image.objects.all().order_by('date_taken').filter(journey_id=jid)
    data = [[int(image.id), [float(image.latitude), float(image.longitude)]] for image in images if image.latitude != float(404.0000) and image.longitude != float(404.0000)]

    context = {
        'title': Journey.objects.get(id=jid).title,
        'all_images': len(images),
        'images': len(data),
        'data': dumps(data),
        'jc': len(journeys),
        'user': request.user,
        'journeys': journeys,
        "no_footer": True
    }

    return render(request, 'JourneyMap/map.html', context)


class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Image
    form_class = ImageForm
    # fields = ['journey', 'title', 'image']
    template_name = 'JourneyMap/image_form.html'
    success_url = ''

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user.id
        return kwargs


class ImageDeleteView(LoginRequiredMixin, DeleteView):
    model = Image
    template_name = 'JourneyMap/image_delete.html'
    success_url = ''
