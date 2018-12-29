from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from umap import views

router = routers.DefaultRouter()
router.register(r'race', views.RaceViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
