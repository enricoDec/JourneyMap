from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext as _
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from .forms import UserRegister, ProfileUpdateForm
from .tokens import account_activation_token

User = get_user_model()


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
            return redirect('JourneyMap_home')
    if request.user.is_authenticated:
        return redirect('JourneyMap_home')
    else:
        form = UserRegister()

    context = {
        'title': _('Sign Up'),
        'form': form,
    }
    return render(request, 'Users/sign_up.html', context)


@never_cache
@csrf_protect
def sign_out(request):
    logout(request)
    messages.success(request, _('You have been successfully logged out!'))
    return redirect('JourneyMap_home')


class ActivateUser(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            # activate user and redirect to login:
            user.is_active = True
            user.save()

            messages.success(request, _('Activation successful!'))
            return redirect('login')
        else:
            messages.warning(request, _('Activation link is invalid!'))
            return redirect('JourneyMap_home')


@login_required
@never_cache
@csrf_protect
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        password_form = PasswordChangeForm(request.user, request.POST)

        if 'picture' in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, _(f'Profile picture updated!'))
                return redirect('profile')
            else:
                messages.warning(request, _('Please correct the error below.'))

        elif 'password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, _(f'Password information Updated!'))
                return redirect('profile')
            else:
                messages.warning(request, _('Please correct the error below.'))
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        password_form = PasswordChangeForm(request.user)

    context = {
        'title': _('Profile'),
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'Users/profile.html', context)


def password_done(request):
    messages.success(request, _('An email has been sent'))
    return redirect('JourneyMap_home')


def password_complete(request):
    messages.success(request, _('Your password has been updated.'))
    return redirect('JourneyMap_home')
