from django.urls import path

from . import views
from .views import ImageCreateView, ImageDeleteView

urlpatterns = [
    path('', views.home, name='JourneyMap_home'),
    path('contact_us/', views.contact, name='JourneyMap_contact_us'),
    path('journeys/', views.journeys, name='JourneyMap_journeys'),
    path('journeys/new/images/', ImageCreateView.as_view(), name='JourneyMap_journeys_new_image'),
    path('journeys/delete/', views.delete_journey, name='JourneyMap_journeys_delete'),
    path('image/delete', ImageDeleteView.as_view(), name='JourneyMap_image_delete'),
    path('cdp/<iid>', views.cdp, name='JourneyMap_cdp'),
    path('journey/<jid>', views.journey, name='JourneyMap_journey')
]
