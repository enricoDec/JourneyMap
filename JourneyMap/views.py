from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.translation import gettext as _
from .models import Journey, Image
from django.views.generic import ListView, CreateView


def home(request):
    context = {
        'title': _('Home')
    }
    return render(request, 'JourneyMap/home.html', context)


def contact(request):
    context = {
        'title': _('Contact Us')
    }
    return render(request, 'JourneyMap/contact_us.html', context)


class JourneyListView(LoginRequiredMixin, ListView):
    template_name = 'JourneyMap/journeys.html'
    context_object_name = 'journeys'
    # order journeys by newest to oldest
    ordering = ['-date_posted']

    def get_queryset(self):
        self.model = Journey.objects.filter(user=self.request.user.id)
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

