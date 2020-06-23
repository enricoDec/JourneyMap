from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import mail
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, DeleteView

from .forms import ContactForm, ImageForm
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

            # To
            receiver = mail.settings.EMAIL_HOST_USER

            # From
            name = request.POST.get('name', '')
            sender = request.POST.get('email', '')
            user_message = request.POST.get('message', '')

            try:
                # Format
                subject = name + " has send a Contact Form"
                message = (
                    f"Contact Form was send:\n\n"
                    f"NAME: {name}.\n"
                    f"FROM: {sender}.\n"
                    f"MESSAGE:\n{user_message}.\n"
                )

                send_mail(
                    subject,
                    message,
                    receiver,
                    [receiver],
                    fail_silently=False,
                )
                messages.success(request, _(f'Contact Form Send!'))
                return redirect('JourneyMap_contact_us_thanks')
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        else:
            messages.error(request, _(f'Error !'))
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


def contact_thanks(request):
    context = {
        'title': _('Thanks')
    }
    return render(request, 'JourneyMap/contact_us_thanks.html', context)


class JourneyListView(LoginRequiredMixin, ListView):
    template_name = 'JourneyMap/journeys.html'
    context_object_name = 'journeys'
    # order journeys by newest to oldest
    ordering = ['-date_posted']

    def get_queryset(self):
        self.model = Journey.objects.filter(user_id=self.request.user.id)
        return self.model

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
