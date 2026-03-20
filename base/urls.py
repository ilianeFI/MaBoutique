from django.urls import path, URLPattern
from .views import Hello

urlpatterns = [
    path('',Hello.as_view(),name='home' ),
]
