from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from .forms import UserRegister


@never_cache
@csrf_protect
def sign_up(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, _('Account created for') + ' ' + f'{username}')
            return redirect('login')
    else:
        form = UserRegister()

    context = {
        'title': _('Sign Up'),
        'form': form
    }
    return render(request, 'Users/sign_up.html', context)


@login_required
@never_cache
@csrf_protect
def profile(request):
    context = {
        'title': _('Profile'),
    }
    return render(request, 'Users/profile.html', context)
