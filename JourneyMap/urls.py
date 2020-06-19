from django.urls import path
from . import views
from .views import JourneyListView, JourneyCreateView

urlpatterns = [
    path('', views.home, name='JourneyMap_home'),
    path('contact_us/', views.contact, name='JourneyMap_contact_us'),
    path('journeys/', JourneyListView.as_view(), name='JourneyMap_journeys'),
    path('journeys/new/', JourneyCreateView.as_view(), name='JourneyMap_journeys_new'),
]
