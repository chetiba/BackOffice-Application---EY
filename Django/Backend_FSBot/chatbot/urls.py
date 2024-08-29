from django.urls import path
from .views import chat_with_rasa, search_cv, chat_page

urlpatterns = [
    path('', chat_page, name='chat_page'),  # Vue pour afficher la page de chat
    path('chat_with_rasa/', chat_with_rasa, name='chat_with_rasa'),
    path('search_cv/', search_cv, name='search_cv'),
]
