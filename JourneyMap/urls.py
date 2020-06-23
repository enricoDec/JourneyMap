from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='JourneyMap_home'),
    path('contact_us/', views.contact, name='JourneyMap_contact_us'),
    path('contact_us/thanks', views.contact_thanks, name='JourneyMap_contact_us_thanks'),
]
