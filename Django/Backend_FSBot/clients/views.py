from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ClientForm
import json
from .models import Client  # Import your Client model

@csrf_exempt
def addClient(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        form = ClientForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Client added successfully!"}, status=201)
        else:
            return JsonResponse(form.errors, status=400)
    return JsonResponse({"error": "Only POST method is allowed"}, status=405)

@csrf_exempt
def getClientIds(request):
    if request.method == 'GET':
        try:
            # Retrieve all clients and their IDs and names
            clients = Client.objects.all().values('id', 'nom')  # Adjust 'nom' to the actual field name for the client name
            client_list = list(clients)
            return JsonResponse(client_list, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Only GET method is allowed"}, status=405)
@csrf_exempt
def getAllClients(request):
    if request.method == 'GET':
        try:
            # Retrieve all client details
            clients = Client.objects.all().values()  # Get all fields for clients
            client_list = list(clients)
            return JsonResponse(client_list, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "This endpoint supports only GET requests"}, status=405)
