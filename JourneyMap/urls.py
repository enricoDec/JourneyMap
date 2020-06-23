from django.urls import path

from . import views
from .views import JourneyListView, JourneyCreateView, ImageCreateView, JourneyDeleteView

urlpatterns = [
    path('', views.home, name='JourneyMap_home'),
    path('contact_us/', views.contact, name='JourneyMap_contact_us'),
    path('contact_us/thanks', views.contact_thanks, name='JourneyMap_contact_us_thanks'),
    path('journeys/', JourneyListView.as_view(), name='JourneyMap_journeys'),
    path('journeys/new/', JourneyCreateView.as_view(), name='JourneyMap_journeys_new'),
    path('journeys/new/images', ImageCreateView.as_view(), name='JourneyMap_journeys_new_image'),
    path('journeys/delete', JourneyDeleteView.as_view(), name='JourneyMap_journeys_delete'),
]
