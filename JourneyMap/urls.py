from django.urls import path

from . import views
from .views import ImageCreateView, ImageDeleteView

urlpatterns = [
    path('', views.home, name='JourneyMap_home'),
    path('privacy_policy/', views.privacy_policy, name='JourneyMap_privacy_policy'),
    path('terms_of_service/', views.terms_of_service, name='JourneyMap_terms_of_service'),
    path('contact_us/', views.contact, name='JourneyMap_contact_us'),
    path('journeys/', views.journeys, name='JourneyMap_journeys'),
    path('journeys/new/images/', ImageCreateView.as_view(), name='JourneyMap_journeys_new_image'),
    path('journeys/delete/', views.delete_journey, name='JourneyMap_journeys_delete'),
    path('image/delete', ImageDeleteView.as_view(), name='JourneyMap_image_delete'),
    path('cdp/<iid>', views.cdp, name='JourneyMap_cdp'),
    path('journey/<jid>', views.journey, name='JourneyMap_journey'),
    path('map/<jid>', views.map, name='JourneyMap_map'),
]
