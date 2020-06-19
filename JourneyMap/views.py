from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, DeleteView

from .forms import ImageForm
from .models import Journey, Image


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
        self.model = Journey.objects.filter(user_id=self.request.user.id)
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


class JourneyDeleteView(LoginRequiredMixin, DeleteView):
    model = Journey
    template_name = 'JourneyMap/journey_delete.html'
    success_url = ''


class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Image
    form_class = ImageForm
    # fields = ['journey', 'title', 'image']
    template_name = 'JourneyMap/image_form.html'
    success_url = ''

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user.id
        return kwargs

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'].fields['journey'].queryset = Journey.objects.filter(user_id=self.request.user.id)
    #     return context
