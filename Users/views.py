from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext as _
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from .forms import UserRegister
from .tokens import account_activation_token

User = get_user_model()


def sign_in(request):
    context = {
        'title': _('Sign In')
    }
    return render(request, 'Users/sign_in.html', context)


@never_cache
@csrf_protect
def sign_up(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            form.save()

            # One time token to confirm email
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = "http://{0}/activate/{1}/{2}".format(current_site, uid, token)

            context_email = {
                'subject': 'Activate your account',
                'link': activation_link,
                'name': user.first_name + ' ' + user.last_name,
            }

            # Send an email with html template
            to_email = form.cleaned_data.get('email')
            html_email = 'Users/sign_up_email.html'
            html_message = render_to_string(html_email, context_email)

            message = EmailMessage(_('Activate your account'), html_message, 'auth@journey-map.eu', [to_email])
            message.content_subtype = 'html'
            message.send()

            messages.success(request, _('Please confirm your email address to complete the registration'))
            return redirect("JourneyMap_home")
    else:
        form = UserRegister()

    context = {
        'title': _('Sign Up'),
        'form': form
    }
    return render(request, 'Users/sign_up.html', context)


class ActivateUser(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            # activate user and login:
            user.is_active = True
            user.save()
            login(request, user)

            messages.success(request, _('Activation successful!'))
            return redirect('JourneyMap_home')
        else:
            messages.warning(request, _('Activation link is invalid!'))
            return redirect('JourneyMap_home')
