from django.urls import path
from .views import AddCollaborateurView, LoginView, LogoutView, ResetPasswordView, ResetPasswordConfirmView ,GetImageView, GetAllUsersView ,ScrapeDataAPIView ,ScrapeSelectOptionsAPIView , ScrapeActuAPIView,EditUserView,DeleteUserView,SearchCV,chat_with_rasa,GetOneUser,GetIdManager,LoadAllCollaborateursView,LoadAllPartnersView,GetAllCollabMissionsView,missions_by_collaborator,GetHoursLeftView,UpdateCollabMissionMarginView,ActivateCollaborateurView,GetCollaborateurs
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('add/', AddCollaborateurView.as_view(), name='add_collaborateur'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset-confirm/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('image/<int:user_id>/', GetImageView.as_view(), name='image'),  # Ajouter cette ligne
    path('scrape/', ScrapeDataAPIView.as_view(), name='scrape-api'),
    path('scrapeOptions/', ScrapeSelectOptionsAPIView.as_view(), name='scrape_select_options'),
    path('actu/', ScrapeActuAPIView.as_view(), name='scrapeActu'),
    path('edit-user/<int:user_id>/', EditUserView.as_view(), name='edit-user'),
    path('delete-user/<int:user_id>/', DeleteUserView.as_view(), name='delete-user'),
    path('getusers/', GetAllUsersView.as_view(), name='getusers'),
    path('getusers/<int:user_id>/', GetOneUser.as_view(), name='GetOneUser'),
    path('search/', SearchCV.as_view(), name='search_cv_banque'),
    path('chat_with_rasa/', chat_with_rasa, name='chat_with_rasa'),
    path('assign-mission/', views.assign_mission, name='assign-mission'),
    path('missions/collaborator/<int:collab_id>/', views.missions_by_collaborator, name='missions-by-collaborator'),
    path('missions/client/<int:client_id>/', views.missions_by_client, name='missions-by-client'),
    path('get-id-manager/', GetIdManager.as_view(), name='get-id-manager'),
    path('load-collaborateurs/', LoadAllCollaborateursView.as_view(), name='load-collaborateurs'),
    path('load-Partners/', LoadAllPartnersView.as_view(), name='load-collaborateurs'),
    path('collab-missions/', GetAllCollabMissionsView.as_view(), name='get_all_collab_missions'),
    path('missions-by-collaborator/<int:collab_id>/', missions_by_collaborator, name='missions_by_collaborator'),
    path('<int:collab_id>/hours-left/', GetHoursLeftView.as_view(), name='get_hours_left'),
    path('update-mission-margin/<int:collab_mission_id>/', UpdateCollabMissionMarginView.as_view(),
         name='update-mission-margin'),
    path('valider-inscription/<int:collaborateur_id>/', ActivateCollaborateurView.as_view(),
         name='valider_inscription'),
    path('getCollaborateurs/', GetCollaborateurs.as_view(),
             name='get_collaborateurs'),

]
