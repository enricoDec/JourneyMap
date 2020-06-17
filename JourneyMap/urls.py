from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='JourneyMap_home'),
    path('login/', views.sign_in, name='JourneyMap_login'),
    path('register/', views.sign_up, name='JourneyMap_register'),
    path('contact_us/', views.contact, name='JourneyMap_contact_us'),
    path('journeys/', views.journeys, name='JourneyMap_journeys'),
]
