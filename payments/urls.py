from django.urls import path
from . import views
urlpatterns = [
    path('paiment/<int:order_id>/',views.paiment_choix,name='paiment'),
    path('paiment/selection/<int:order_id>/',views.paiment_selection,name='paiment_selection'),
    path('paiment/success/<int:order_id>/',views.paiment_success,name='paiment_success'),
    path('payments/failed/',views.payment_failed,name='payment_failed'),
]