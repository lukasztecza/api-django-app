from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from .health import views

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('health/', views.HealthDetail.as_view(), name='health'),
]
