import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from .models import CVBanque
import os
from django.conf import settings

@csrf_exempt
def search_cv(request):
    title = request.GET.get('title', "").strip()
    cv = CVBanque.objects.filter(title__icontains=title).first()

    if cv and cv.attachments:
        # Assurez-vous que le répertoire existe
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)

        file_path = os.path.join(settings.MEDIA_ROOT, f"{cv.title.strip()}.pptx")

        # Écriture du BLOB dans un fichier
        with open(file_path, 'wb+') as file:
            file.write(cv.attachments)

        # Générer l'URL de téléchargement
        download_url = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, f"{cv.title.strip()}.pptx"))

        return JsonResponse({'url': download_url})
    else:
        return JsonResponse({'error': 'CV not found'}, status=404)

def chat_page(request):
    return render(request, 'chat.html')

@csrf_exempt
def chat_with_rasa(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            sender = data.get('sender', 'default_user')

            if not user_message:
                return JsonResponse({"error": "Message field is required and cannot be empty."}, status=400)

            # Envoyer à Rasa pour traitement
            rasa_url = "http://localhost:5005/webhooks/rest/webhook"
            headers = {'Content-type': 'application/json'}
            response = requests.post(rasa_url, json={"sender": sender, "message": user_message}, headers=headers)

            if response.status_code == 200:
                return JsonResponse(response.json(), safe=False)
            else:
                return JsonResponse({"error": "Failed to connect to Rasa server."}, status=response.status_code)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    elif request.method == "GET":
        return render(request, 'chat.html')
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)
