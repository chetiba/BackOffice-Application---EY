from django.urls import path
from .views import addClient, getClientIds ,getAllClients

urlpatterns = [
    path('add-client/', addClient, name='add-client'),
    path('get-client-ids/', getClientIds, name='get-client-ids'),
    path('get-clients/', getAllClients, name='get-clients'),

]
