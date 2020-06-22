from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import gettext as _

from .forms import UserRegister


def sign_in(request):
    context = {
        'title': _('Sign In')
    }
    return render(request, 'Users/sign_in.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, _('Account created for') + ' ' + f'{username}')
            return redirect('JourneyMap_home')
    else:
        form = UserRegister()

    context = {
        'title': _('Sign Up'),
        'form': form
    }
    return render(request, 'Users/sign_up.html', context)
