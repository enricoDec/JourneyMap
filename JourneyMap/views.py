from django.contrib import messages
from django.core.mail import BadHeaderError
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
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

    context = {
        'title': _('Contact Us'),
        'form': form
    }
    return render(request, 'JourneyMap/contact_us.html', context)
