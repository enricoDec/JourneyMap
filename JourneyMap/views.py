from django.contrib import messages
from django.core.mail import BadHeaderError
from django.core.mail import EmailMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import mail
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaultfilters import register
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, CreateView, DeleteView

from .forms import ContactForm, ImageForm, AddJourneyForm
from .models import Journey, Image


def home(request):
    journeys = None
    if request.user.is_authenticated:
        journeys = Journey.objects.filter(user_id=request.user)
    context = {
        'title': _('Home'),
        'journeys': journeys,
    }
    return render(request, 'JourneyMap/home.html', context)


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
    images = dict();

    for journey in qs:
        images[journey.id] = Image.objects.filter(journey=journey)[0: 5]

    context = {
        'form': form,
        'journeys': qs,
        'images': images
    }

    return render(request, 'JourneyMap/journeys.html', context)


class JourneyListView(LoginRequiredMixin, ListView):
    template_name = 'JourneyMap/journeys.html'
    context_object_name = 'journeys'
    # order journeys by newest to oldest
    ordering = ['-date_posted']

    def get_queryset(self):
        return Journey.objects.filter(user_id=self.request.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = Image.objects.filter(journey__user=self.request.user)
        return context


class JourneyCreateView(LoginRequiredMixin, CreateView):
    model = Journey
    fields = ['title']
    template_name = 'JourneyMap/journey_form.html'
    success_url = ''

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(JourneyCreateView, self).form_valid(form)


class JourneyDeleteView(LoginRequiredMixin, DeleteView):
    model = Journey
    template_name = 'JourneyMap/journey_delete.html'
    success_url = ''


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

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'].fields['journey'].queryset = Journey.objects.filter(user_id=self.request.user.id)
    #     return context
