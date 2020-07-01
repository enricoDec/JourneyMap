from django.contrib import messages
from django.core import mail
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
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

                messages.success(request, _('Thank you, the message was send.'))
                return redirect('JourneyMap_home')
            except BadHeaderError:
                messages.warning(request, _('An error occurred, please try again'))
                return redirect('JourneyMap_contact_us')

            # # To
            # receiver = mail.settings.EMAIL_HOST_USER
            #
            # # From
            # name = request.POST.get('name', '')
            # sender = request.POST.get('email', '')
            # user_message = request.POST.get('message', '')
            #
            # try:
            #     # Format
            #     subject = name + " has send a Contact Form"
            #     message = (
            #         f"Contact Form was send:\n\n"
            #         f"NAME: {name}.\n"
            #         f"FROM: {sender}.\n"
            #         f"MESSAGE:\n{user_message}.\n"
            #     )
            #
            #     send_mail(
            #         subject,
            #         message,
            #         receiver,
            #         [receiver],
            #         fail_silently=False,
            #     )
            #     messages.success(request, _(f'Contact Form Send!'))
            #     return redirect('JourneyMap_home')
            # except BadHeaderError:
            #     return HttpResponse('Invalid header found.')
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
