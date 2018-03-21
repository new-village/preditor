from django.urls import path
from umap import views

urlpatterns = [
    path('', views.index, name='index'),
]
