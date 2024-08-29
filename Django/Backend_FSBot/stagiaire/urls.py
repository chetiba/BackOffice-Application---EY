from django.urls import path
from .views import CreateStagiaire, RetrieveStagiairesByCollaborateur, UpdateStagiaire, DeleteStagiaire, ListStagiaires

urlpatterns = [
    path('create/', CreateStagiaire.as_view(), name='create_stagiaire'),
    path('list/', ListStagiaires.as_view(), name='list_stagiaires'),
    path('update/<int:id>/', UpdateStagiaire.as_view(), name='update_stagiaire'),
    path('delete/<int:id>/', DeleteStagiaire.as_view(), name='delete_stagiaire'),
    path('retrieve-by-collaborateur/<int:collaborateur_id>/', RetrieveStagiairesByCollaborateur.as_view(), name='retrieve_stagiaires_by_collaborateur'),
]
