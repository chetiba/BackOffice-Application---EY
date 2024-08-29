from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chatbot.urls')),  # Inclut les URL de l'application chatbot
    path('api/', include('chatbot.urls')),   # Inclut les URL de l'application chatbot
    path('', RedirectView.as_view(url='/chat/', permanent=False)),  # Redirige vers /chat/
    path('collaborateurs/', include('collaborateurs.urls')),
    path('client/', include('clients.urls')),  # Assurez-vous que ceci est correct
    path('mission/', include('missions.urls')),
    path('stagiaire/', include('stagiaire.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
