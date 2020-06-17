from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.contrib import messages
from .forms import UserRegister
from django.contrib.auth.decorators import login_required


#
# def sign_in(request):
#     context = {
#         'title': _('Sign In')
#     }
#     return render(request, 'Users/sign_in.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, _(f'Account created for {username}! You can now log in'))
            return redirect('login')
    else:
        form = UserRegister()

    context = {
        'title': _('Sign Up'),
        'form': form
    }
    return render(request, 'Users/sign_up.html', context)


@login_required
def profile(request):
    context = {
        'title': _('Profile'),
    }
    return render(request, 'Users/profile.html', context)
