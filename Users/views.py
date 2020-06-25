from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext as _
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from .forms import UserRegister
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

            # Send an email
            mail_subject = 'Activate your account.'
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = "{0}/activate/{1}/{2}".format(current_site, uid, token)
            message = "Hello {0},\n {1}".format(user.username, activation_link)
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
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

            return redirect('login')
        else:
            return HttpResponse('Activation link is invalid!')

    # def post(self, request):
    #     form = PasswordChangeForm(request.user, request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         update_session_auth_hash(request, user)
    #         return HttpResponse('Password changed successfully')


@login_required
@never_cache
@csrf_protect
def profile(request):
    context = {
        'title': _('Profile'),
    }
    return render(request, 'Users/profile.html', context)
