from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
    path('auth/', include('authsys.urls')),
    path('', RedirectView.as_view(url='/main/my_companies'))
]
