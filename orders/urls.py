from django.urls import path
from . import views
urlpatterns = [
    path('commande/creer/',views.create_order,name='create_order'),
    path('commande/resume/<str:order_number>/',views.order_page,name='order_page'),
    path('commande/valider/<int:order_id>/',views.valider_order,name='valider_order'),
    #paiment

]