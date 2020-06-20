from django.contrib import messages
from django.core import mail
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _

from .forms import ContactForm


def home(request):
    context = {
        'title': _('Home')
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

    context = {
        'title': _('Contact Us'),
        'form': form
    }
    return render(request, 'JourneyMap/contact_us.html', context)


def contact_thanks(request):
    context = {
        'title': _('Thanks')
    }
    return render(request, 'JourneyMap/contact_us_thanks.html', context)
