from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Stagiaire
from .forms import StagiaireForm
import json
from collaborateurs.models import CollabFS

@method_decorator(csrf_exempt, name='dispatch')
class CreateStagiaire(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            print("Received data:", data)

            # Ajoutez la logique pour gérer l'ID du collaborateur
            collaborateur_id = data.pop('collaborateur_id', None)
            if collaborateur_id:
                try:
                    collaborateur = CollabFS.objects.get(pk=collaborateur_id)
                except CollabFS.DoesNotExist:
                    return JsonResponse({'error': 'Collaborateur with the given ID does not exist'}, status=404)
                data['collaborateur'] = collaborateur  # Directly pass the object

            form = StagiaireForm(data)

            if not form.is_valid():
                print("Form errors:", form.errors)  # Imprimer les erreurs pour diagnostic
                return JsonResponse(form.errors, status=400)

            stagiaire = form.save(commit=False)
            stagiaire.save()

            return JsonResponse({"message": "Stagiaire créé avec succès", "id": stagiaire.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



@method_decorator(csrf_exempt, name='dispatch')
class UpdateStagiaire(View):
    def post(self, request, id):
        stagiaire = Stagiaire.objects.filter(id=id).first()
        if not stagiaire:
            return JsonResponse({"erreur": "Stagiaire non trouvé"}, status=404)

        data = json.loads(request.body)
        collaborateur_id = data.get('collaborateur_id')

        # Remove 'collaborateur_id' from data to prevent issues with form validation
        if 'collaborateur_id' in data:
            del data['collaborateur_id']

        # Fetch the collaborateur instance
        if collaborateur_id:
            try:
                collaborateur = CollabFS.objects.get(pk=collaborateur_id)
                data['collaborateur'] = collaborateur
            except CollabFS.DoesNotExist:
                return JsonResponse({'error': 'Collaborateur with the given ID does not exist'}, status=404)

        form = StagiaireForm(data, instance=stagiaire)
        if form.is_valid():
            stagiaire = form.save(commit=False)
            stagiaire.collaborateur = collaborateur  # Set collaborateur explicitly
            stagiaire.save()
            return JsonResponse({"message": "Stagiaire mis à jour avec succès"}, status=200)
        else:
            return JsonResponse(form.errors, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteStagiaire(View):
    def delete(self, request, id):
        stagiaire = Stagiaire.objects.filter(id=id)
        if stagiaire.exists():
            stagiaire.delete()
            return JsonResponse({"message": "Stagiaire supprimé avec succès"}, status=200)
        else:
            return JsonResponse({"erreur": "Stagiaire non trouvé"}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class ListStagiaires(View):
    def get(self, request):
        stagiaires = Stagiaire.objects.all()
        data = [{
            "id": stagiaire.id,
            "nom": stagiaire.nom,
            "prenom": stagiaire.prenom,
            "email": stagiaire.email,
            "sujet_pfe": stagiaire.sujet_pfe,
            "etat_avancement": stagiaire.get_etat_avancement_display(),
            "fichier": stagiaire.fichier.url if stagiaire.fichier else None,
            "collaborateur_id": stagiaire.collaborateur_id if stagiaire.collaborateur else None  # Include collaborateur_id
        } for stagiaire in stagiaires]
        return JsonResponse(data, safe=False, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class RetrieveStagiairesByCollaborateur(View):
    def get(self, request, collaborateur_id):
        stagiaires = Stagiaire.objects.filter(collaborateur_id=collaborateur_id)
        data = [{
            "id": stagiaire.id,
            "nom": stagiaire.nom,
            "prenom": stagiaire.prenom,
            "email": stagiaire.email,
            "sujet_pfe": stagiaire.sujet_pfe,
            "etat_avancement": stagiaire.get_etat_avancement_display(),
            "collaborateur_id": stagiaire.collaborateur_id ,

            "fichier": stagiaire.fichier.url if stagiaire.fichier else None
        } for stagiaire in stagiaires]

        # If no stagiaires are found, return an empty list with a 200 OK status
        if not data:
            return JsonResponse({"message": "No stagiaires found for this collaborateur", "data": []}, status=200)

        return JsonResponse(data, safe=False, status=200)
