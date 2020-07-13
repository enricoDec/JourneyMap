from django.urls import path

from . import views
from .views import JourneyListView, ImageCreateView

urlpatterns = [
    path('', views.home, name='JourneyMap_home'),
    path('contact_us/', views.contact, name='JourneyMap_contact_us'),
    path('journeys/', views.journeys, name='JourneyMap_journeys'),
    path('journeys/new/images/', ImageCreateView.as_view(), name='JourneyMap_journeys_new_image'),
    path('journeys/delete/', views.delete_journey, name='JourneyMap_journeys_delete'),
]
