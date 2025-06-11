from django.contrib import admin
from django.urls import path
from base import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('status', views.status_view),
    path('metrics', views.metrics_view),
    path('version', views.version_view),
]