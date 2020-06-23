"""WebApplication URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from Users import views as user_view
from Users.forms import UserLogin

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('register/', user_view.sign_up, name='register'),
    path('activate/<uidb64>/<token>', user_view.ActivateUser.as_view(), name='activate'),
    # path('login/', user_view.sign_in, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='Users/sign_in.html', authentication_form=UserLogin),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='Users/sign_out.html'), name='logout'),
    path('profile/', user_view.profile, name='profile'),
    path('', include('JourneyMap.urls')),
]

# Needs to be changed before deployed!!
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
