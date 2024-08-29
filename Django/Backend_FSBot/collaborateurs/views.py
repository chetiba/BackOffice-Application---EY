import os
import re
import traceback

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render , redirect
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import CollabFS
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_decode
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from bs4 import BeautifulSoup
from rest_framework.permissions import AllowAny  # Importer AllowAny
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time  # Import time module to manage any needed delays
from django.db.models import Q  # Import correct de Q
from .models import CollabMission

from django.conf import settings
from .forms import AssignMissionForm
import logging
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class SearchCV(View):
    def get(self, request):
        query = request.GET.get('query', "").strip()

        cvs = CollabFS.objects.filter(
            Q(prenom__icontains=query) |
            Q(nom__icontains=query) |
            Q(poste__icontains=query) |
            Q(Compétences__icontains=query) |  # Assurez-vous d'utiliser la bonne casse
            Q(diplome_obtenu__icontains=query) |
            Q(institution__icontains=query)
        )[:25]  # Limite à 25 résultats

        if cvs.exists():  # Vérifier s'il y a des résultats
            results = []
            for cv in cvs:
                if cv.cv:  # Vérifier si l'attribut cv existe pour chaque objet cv
                    if not os.path.exists(settings.MEDIA_ROOT):
                        os.makedirs(settings.MEDIA_ROOT)

                    file_path = os.path.join(settings.MEDIA_ROOT, f"{cv.prenom.strip()}_{cv.nom.strip()}.pptx")
                    with open(file_path, 'wb+') as file:
                        file.write(cv.cv)

                    download_url = request.build_absolute_uri(
                        os.path.join(settings.MEDIA_URL, f"{cv.prenom.strip()}_{cv.nom.strip()}.pptx"))

                    results.append({
                        'prenom': cv.prenom.strip(),
                        'nom': cv.nom.strip(),
                        'url': download_url
                    })

            return JsonResponse({'cvs': results})
        else:
            return JsonResponse({'error': 'No CVs found'}, status=404)


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

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@method_decorator(csrf_exempt, name='dispatch')
class AddCollaborateurView(View):
    def post(self, request):
        try:
            image_file = request.FILES.get('image')
            cv_file = request.FILES.get('cv')

            # Check for required files
            if not image_file or not cv_file:
                return JsonResponse({'error': 'Image and CV files are required'}, status=400)

            # Extract form data
            prenom = request.POST.get('prenom')
            nom = request.POST.get('nom')
            poste = request.POST.get('poste')
            email = request.POST.get('email')
            role = request.POST.get('role')  # Ensure this is retrieved
            competences = request.POST.get('competences')
            diplome_obtenu = request.POST.get('diplome_obtenu')
            institution = request.POST.get('institution')
            date = request.POST.get('date')

            # Check for required fields
            if not all([prenom, nom, poste, email, role, competences, diplome_obtenu, institution, date]):
                return JsonResponse({'error': 'All fields are required, including image and CV'}, status=400)

            # Create and save model instance without username and password
            collaborateur = CollabFS(
                prenom=prenom,
                nom=nom,
                poste=poste,
                email=email,
                role=role,  # Ensure this is assigned
                Compétences=competences,
                diplome_obtenu=diplome_obtenu,
                institution=institution,
                date=date,
                image=image_file.read(),  # Read binary data once
                cv=cv_file.read()  # Read binary data once
            )

            # Validate and save model
            collaborateur.full_clean()
            collaborateur.save()

            return JsonResponse({'message': 'Collaborateur ajouté avec succès.'}, status=201)
        except Exception as e:
            # Log the stack trace for debugging purposes
            traceback_str = traceback.format_exc()
            print(traceback_str)
            return JsonResponse({'error': str(e), 'traceback': traceback_str}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                tokens = get_tokens_for_user(user)
                user.access_token = tokens['access']
                user.refresh_token = tokens['refresh']
                user.is_authenticated = True
                user.save()
                login(request, user)
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'prenom': user.prenom,
                    'nom': user.nom,
                    'poste': user.poste,
                    'departement': user.departement,
                    'email': user.email,
                    'access_token': user.access_token,
                    'refresh_token': user.refresh_token,
                    'role': user.role,  # Ajout du rôle
                    'is_authenticated': user.is_authenticated,  # Statut d'authentification de l'utilisateur
                    'competences': user.Compétences,  # Ajout des compétences
                    'diplome_obtenu': user.diplome_obtenu,  # Ajout du diplôme obtenu
                    'institution': user.institution,  # Ajout de l'institution
                    'date': user.date  # Ajout de la date
                }
                return JsonResponse({'user': user_data}, status=200)
            else:
                return HttpResponse('Ce compte est désactivé.', status=403)
        else:
            return HttpResponse('Identifiants invalides.', status=401)

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            user = CollabFS.objects.get(username=username)

            if user.is_authenticated:
                user.access_token = None
                user.refresh_token = None
                user.is_authenticated = False
                user.save()
                return JsonResponse({'message': 'Vous êtes déconnecté avec succès.'}, status=200)
            else:
                return HttpResponse('Utilisateur non connecté.', status=403)
        except CollabFS.DoesNotExist:
            return HttpResponse('Utilisateur non trouvé.', status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class ResetPasswordView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')

            if not email:
                return JsonResponse({'error': 'Email est obligatoire'}, status=400)

            try:
                user = CollabFS.objects.get(email=email)
                user.send_reset_password_email()
                return JsonResponse({'message': 'Un email de réinitialisation a été envoyé.'}, status=200)
            except CollabFS.DoesNotExist:
                return JsonResponse({'error': 'Utilisateur avec cet email non trouvé'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class ResetPasswordConfirmView(View):
    def post(self, request, uidb64, token):
        try:
            data = json.loads(request.body)
            password = data.get('password')

            if not password:
                return JsonResponse({'error': 'Le nouveau mot de passe est obligatoire'}, status=400)

            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = CollabFS.objects.get(pk=uid)

                if default_token_generator.check_token(user, token):
                    user.set_password(password)
                    user.save()
                    return JsonResponse({'message': 'Le mot de passe a été réinitialisé avec succès.'}, status=200)
                else:
                    return JsonResponse({'error': 'Le lien de réinitialisation est invalide ou a expiré.'}, status=400)

            except CollabFS.DoesNotExist:
                return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class GetImageView(View):
    def get(self, request, user_id):
        try:
            try:
                user = CollabFS.objects.get(pk=user_id)
                if user.image:
                    return HttpResponse(user.image, content_type='image/jpeg')  # Vous pouvez ajuster le type MIME selon le format réel de l'image
                else:
                    return JsonResponse({'error': 'Image non trouvée'}, status=404)

            except CollabFS.DoesNotExist:
                return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class GetAllUsersView(View):
    def get(self, request):
        try:
            # Récupérer tous les utilisateurs de la base de données
            users = CollabFS.objects.all()
            users_data = []
            for user in users:
                user_dict = {
                    'id': user.id,
                    'username': user.username,
                    'prenom': user.prenom,
                    'nom': user.nom,
                    'poste': user.poste,
                    'email': user.email,
                    'role': user.role,
                    'competences': user.Compétences,
                    'diplome_obtenu': user.diplome_obtenu,
                    'institution': user.institution,
                    'date': user.date,
                    'is_authenticated': user.is_authenticated
                }
                users_data.append(user_dict)

            return JsonResponse(users_data, safe=False, status=200)  # safe=False pour permettre la sérialisation de listes

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class GetOneUser(View):
    def get(self, request, user_id):
        try:
            # Récupérer tous les utilisateurs de la base de données, sauf l'utilisateur avec l'ID fourni
            users = CollabFS.objects.exclude(id=user_id)
            users_data = []
            for user in users:
                user_dict = {
                    'id': user.id,
                    'username': user.username,
                    'prenom': user.prenom,
                    'nom': user.nom,
                    'poste': user.poste,
                    'email': user.email,
                    'role': user.role,
                    'competences': user.Compétences,
                    'diplome_obtenu': user.diplome_obtenu,
                    'institution': user.institution,
                    'date': user.date,
                    'is_authenticated': user.is_authenticated
                }
                users_data.append(user_dict)

            return JsonResponse(users_data, safe=False, status=200)  # safe=False pour permettre la sérialisation de listes

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class ScrapeDataAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        url = 'https://www.ilboursa.com/'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        data = {
            'TUNINDEX': self.scrape_tunindex(soup),
            'Hausses': self.scrape_stock_changes(soup, '+ FORTES HAUSSES'),
            'Baisses': self.scrape_stock_changes(soup, '+ FORTES BAISSES')
        }

        return Response(data)

    def scrape_tunindex(self, soup):
        tunindex_div = soup.find('a', text='TUNINDEX')
        if not tunindex_div:
            return {"value": "N/A", "change": "N/A"}

        tunindex_parent = tunindex_div.parent.parent
        index_value = tunindex_parent.find_next('span').text.strip()
        index_change_span = tunindex_parent.find('span', class_='quote_up4') or tunindex_parent.find('span', class_='quote_down4')
        index_change = index_change_span.text.strip() if index_change_span else "No change data"

        return {"value": index_value, "change": index_change}

    def scrape_stock_changes(self, soup, change_type):
        changes_list = []
        if change_type == '+ FORTES HAUSSES':
            changes_div = soup.find('div', text='+ FORTES HAUSSES')
        elif change_type == '+ FORTES BAISSES':
            changes_div = soup.find('div', text='+ FORTES BAISSES')

        if not changes_div:
            return changes_list

        changes_table = changes_div.find_next('table')
        if not changes_table:
            return changes_list

        for row in changes_table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) >= 6:  # Assurer que la ligne a au moins 6 cellules pour 2 entreprises par ligne
                for i in range(0, 6, 3):  # Parcourt chaque bloc de 3 cellules
                    symbol = cells[i].find('a').text.strip() if cells[i].find('a') else "N/A"
                    value = cells[i+1].text.strip()
                    change = cells[i+2].text.strip()
                    changes_list.append({
                        'symbol': symbol,
                        'value': value,
                        'change': change
                    })
        return changes_list
class ScrapeSelectOptionsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        url = 'https://www.ilboursa.com/'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        data = self.scrape_select_options(soup)
        return Response(data)

    def scrape_select_options(self, soup):
        select_options = {}
        selects = soup.find_all('select')
        for select in selects:
            options = []
            for option in select.find_all('option'):
                value = option.get('value')
                text = option.text.strip()
                options.append({'value': value, 'text': text})
            select_options[select.get('id')] = options
        return select_options
import logging

# Configure logging
class ScrapeActuAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        url = 'https://www.ilboursa.com/marches/actualites_bourse_tunis'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return JsonResponse({'error': 'Failed to fetch data from the source.'}, status=response.status_code)

            soup = BeautifulSoup(response.content, 'html.parser')
            data = self.scrape_articles(soup)
            return Response(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def scrape_articles(self, soup):
        articles = []
        table = soup.find('table', id='tabQuotes')
        if not table:
            return articles  # Returning empty list if table is not found

        rows = table.find('tbody').find_all('tr', recursive=False)  # Get rows directly under tbody
        for row in rows:
            date_span = row.find('span', class_='sp1')
            date = date_span.text.strip() if date_span else 'Date not found'

            link_tag = row.find('a')
            title = link_tag.text.strip() if link_tag else 'Title not found'
            link = link_tag['href'] if link_tag else 'Link not found'

            articles.append({'date': date, 'title': title, 'link': link})

        return articles
@method_decorator(csrf_exempt, name='dispatch')
class EditUserView(View):
    def put(self, request, user_id):
        try:
            user = CollabFS.objects.get(pk=user_id)
            data = json.loads(request.body)

            # Update only the specified fields
            user.poste = data.get('poste', user.poste)
            user.Compétences = data.get('competences', user.Compétences)
            user.diplome_obtenu = data.get('diplome_obtenu', user.diplome_obtenu)
            user.institution = data.get('institution', user.institution)
            user.date = data.get('date', user.date)

            user.full_clean()
            user.save()

            return JsonResponse({'message': 'Collaborateur mis à jour avec succès.'}, status=200)
        except CollabFS.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
        except Exception as e:
            # Log the stack trace for debugging purposes
            traceback_str = traceback.format_exc()
            print(traceback_str)
            return JsonResponse({'error': str(e), 'traceback': traceback_str}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteUserView(View):
    def delete(self, request, user_id):
        try:
            user = CollabFS.objects.get(pk=user_id)
            user.delete()
            return JsonResponse({'message': 'Collaborateur supprimé avec succès.'}, status=200)
        except CollabFS.DoesNotExist:
            return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
        except Exception as e:
            # Log the stack trace for debugging purposes
            traceback_str = traceback.format_exc()
            print(traceback_str)
            return JsonResponse({'error': str(e), 'traceback': traceback_str}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
def assign_mission(request):
    if request.method == 'POST':
        # Parsing des données JSON reçues dans la requête POST
        data = json.loads(request.body)
        form = AssignMissionForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Mission assigned successfully!"}, status=201)
        else:
            return JsonResponse(form.errors, status=400)
    return JsonResponse({"error": "Only POST method is allowed"}, status=405)

@method_decorator(csrf_exempt, name='dispatch')
def missions_by_collaborator(request, collab_id):
    missions = CollabMission.objects.filter(collab__id=collab_id)
    data = [{"mission_name": m.mission.nom_projet, "client": m.mission.client.nom} for m in missions]
    return JsonResponse(data, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
def missions_by_client(request, client_id):
    missions = CollabMission.objects.filter(mission__client__id=client_id)
    data = [{"collaborator_name": m.collab.nom, "mission_name": m.mission.nom_projet} for m in missions]
    return JsonResponse(data, safe=False)
@method_decorator(csrf_exempt, name='dispatch')
class GetIdManager(View):
    def get(self, request):
        try:
            # Filtering users where poste is 'Manager' or 'Senior Manager'
            managers = CollabFS.objects.filter(
                Q(poste__icontains='Manager') | Q(poste__icontains='Senior Manager')
            ).values('id', 'prenom', 'nom', 'poste')

            # Check if any managers were found
            if managers.exists():
                manager_list = list(managers)
                return JsonResponse(manager_list, safe=False, status=200)
            else:
                return JsonResponse({'error': 'No managers found'}, status=404)
        except Exception as e:
            # Log the stack trace for debugging purposes
            traceback_str = traceback.format_exc()
            print(traceback_str)
            return JsonResponse({'error': str(e), 'traceback': traceback_str}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class LoadAllCollaborateursView(View):
    def get(self, request):
        try:
            # Filtrer les collaborateurs dont le poste est "Junior Consultant", "Senior Consultant", ou "Assistant Manager"
            collaborateurs = CollabFS.objects.filter(
                Q(poste='Junior Consultant') | Q(poste='Senior Consultant') | Q(poste='Assistant Manager')
            ).values('id', 'prenom', 'nom', 'poste')

            # Vérifier si des collaborateurs ont été trouvés
            if collaborateurs.exists():
                collaborateurs_list = list(collaborateurs)
                return JsonResponse(collaborateurs_list, safe=False, status=200)
            else:
                return JsonResponse({'error': 'Aucun collaborateur trouvé avec les postes spécifiés.'}, status=404)
        except Exception as e:
            # Log the stack trace for debugging purposes
            traceback_str = traceback.format_exc()
            print(traceback_str)
            return JsonResponse({'error': str(e), 'traceback': traceback_str}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class LoadAllPartnersView(View):
    def get(self, request):
        try:
            # Filtrer les collaborateurs dont le poste est "Junior Consultant", "Senior Consultant", ou "Assistant Manager"
            collaborateurs = CollabFS.objects.filter(
                Q(poste='Partner')
            ).values('id', 'prenom', 'nom', 'poste')

            # Vérifier si des collaborateurs ont été trouvés
            if collaborateurs.exists():
                collaborateurs_list = list(collaborateurs)
                return JsonResponse(collaborateurs_list, safe=False, status=200)
            else:
                return JsonResponse({'error': 'Aucun Patner trouvé avec les postes spécifiés.'}, status=404)
        except Exception as e:
            # Log the stack trace for debugging purposes
            traceback_str = traceback.format_exc()
            print(traceback_str)
            return JsonResponse({'error': str(e), 'traceback': traceback_str}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class GetAllCollabMissionsView(View):
    def get(self, request):
        try:
            # Récupérer toutes les missions de collaborateurs
            collab_missions = CollabMission.objects.all()

            # Préparer les données à retourner sous forme de JSON
            missions_data = []
            for collab_mission in collab_missions:
                mission_info = {
                    'collaborator': {
                        'prenom': collab_mission.delivery_team.prenom if collab_mission.delivery_team else None,
                        'nom': collab_mission.delivery_team.nom if collab_mission.delivery_team else None,
                        'poste': collab_mission.delivery_team.poste if collab_mission.delivery_team else None,
                    },
                    'mission': {
                        'nom_projet': collab_mission.mission.nom_projet,
                        'client': collab_mission.mission.client.nom if collab_mission.mission.client else None,
                        'date_debut': collab_mission.mission.date_debut,
                        'date_fin': collab_mission.mission.date_fin,
                    },
                    'marge_mission': collab_mission.marge_mission,
                    'manager_responsable': {
                        'prenom': collab_mission.manager_responsable.prenom if collab_mission.manager_responsable else None,
                        'nom': collab_mission.manager_responsable.nom if collab_mission.manager_responsable else None,
                    }
                }
                missions_data.append(mission_info)

            return JsonResponse(missions_data, safe=False, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
def missions_by_collaborator(request, collab_id):
    try:
        # Fetch all CollabMission entries directly where the specified collaborator is part of the delivery team
        related_missions = CollabMission.objects.filter(delivery_team__id=collab_id).select_related(
            'mission', 'mission__client', 'manager_responsable', 'delivery_team'
        )

        # Assemble the mission data including the CollabMission ID
        missions_data = [{
            'collabmission_id': m.id,  # Directly using the CollabMission ID
            'nom_projet': m.mission.nom_projet,
            'code_projet': m.mission.code_projet,
            'date_debut': m.mission.date_debut,
            'date_fin': m.mission.date_fin,
            'client': m.mission.client.nom if m.mission.client else None,
            'manager_responsable': {
                'prenom': m.manager_responsable.prenom if m.manager_responsable else None,
                'nom': m.manager_responsable.nom if m.manager_responsable else None,
            },
            'collaborateur': {
                'prenom': m.delivery_team.prenom,
                'nom': m.delivery_team.nom,
                'id': m.delivery_team.id

            },
            'marge_mission': m.marge_mission,
            'marge_mission_manager': m.marge_mission_manager
        } for m in related_missions]

        return JsonResponse(missions_data, safe=False, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class GetHoursLeftView(View):
    def get(self, request, collab_id):
        try:
            # Récupérer le collaborateur par son ID
            collaborateur = CollabFS.objects.get(pk=collab_id)

            # Préparer les données à retourner
            data = {
                'id': collaborateur.id,
                'hours_left': collaborateur.hours_left
            }

            return JsonResponse(data, status=200)

        except CollabFS.DoesNotExist:
            return JsonResponse({'error': 'Collaborateur non trouvé'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateCollabMissionMarginView(View):
    def post(self, request, collab_mission_id):
        try:
            # Log the incoming request body for debugging
            data = json.loads(request.body)
            logger.debug(f"Received data for updating mission margin: {data}")

            new_marge_mission = data.get('marge_mission')
            collaborator_id = data.get('collaborator_id')

            # Vérification de la présence des données nécessaires
            if new_marge_mission is None or collaborator_id is None:
                return JsonResponse({'error': 'La marge de mission et l\'ID du collaborateur sont requis'}, status=400)

            # Récupération des instances basées sur les IDs fournis
            collab_mission = CollabMission.objects.get(pk=collab_mission_id)
            collaborator = CollabFS.objects.get(pk=collaborator_id)

            # Vérification de la cohérence des données
            if collab_mission.delivery_team_id != collaborator_id:
                return JsonResponse({'error': 'Le collaborateur spécifié ne fait pas partie de cette mission'}, status=400)

            # Calcul des heures restantes potentielles après mise à jour
            current_marge = collab_mission.marge_mission or 0
            potential_hours_left = collaborator.hours_left + current_marge - new_marge_mission

            if potential_hours_left < 0:
                return JsonResponse({'error': 'Heures insuffisantes pour augmenter la marge de mission'}, status=400)

            # Mise à jour des données
            collab_mission.marge_mission = new_marge_mission
            collab_mission.save()
            collaborator.hours_left = potential_hours_left
            collaborator.save()

            return JsonResponse({
                'message': 'Marge de mission mise à jour avec succès.',
                'nouvelle_marge_mission': new_marge_mission,
                'nouvelles_heures_restantes': collaborator.hours_left
            }, status=200)

        except CollabMission.DoesNotExist:
            return JsonResponse({'error': 'Mission non trouvée'}, status=404)
        except CollabFS.DoesNotExist:
            return JsonResponse({'error': 'Collaborateur non trouvé'}, status=404)
        except Exception as e:
            logger.exception(f"Erreur lors de la mise à jour de la marge de mission pour collab_mission_id={collab_mission_id}.")
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ActivateCollaborateurView(View):
    def post(self, request, collaborateur_id):
        try:
            collaborateur = CollabFS.objects.get(pk=collaborateur_id)

            if collaborateur.isActivated:
                return JsonResponse({'error': 'Collaborateur already activated'}, status=400)

            # Generate username and password
            username = CollabFS.generate_username(collaborateur.prenom, collaborateur.nom)
            password = CollabFS.generate_password()

            # Update collaborateur with username and password
            collaborateur.username = username
            collaborateur.set_password(password)
            collaborateur.isActivated = True
            collaborateur.save()

            # Send email with credentials
            message = f"""
            Bonjour {collaborateur.prenom} {collaborateur.nom},

            Votre inscription a été activée avec succès. Voici vos informations de connexion :

            - Email: {username}
            - Mot de passe: {password}

            Vous pouvez vous connecter en utilisant le lien suivant : http://localhost:4200/user-pages/login

            Cordialement,
            L'équipe EY
            """

            send_mail(
                'Activation de votre compte',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [collaborateur.email],
                fail_silently=True,
            )

            return JsonResponse({'message': 'Collaborateur activé avec succès.'}, status=200)
        except CollabFS.DoesNotExist:
            return JsonResponse({'error': 'Collaborateur non trouvé'}, status=404)
        except Exception as e:
            # Log the stack trace for debugging purposes
            traceback_str = traceback.format_exc()
            print(traceback_str)
            return JsonResponse({'error': str(e), 'traceback': traceback_str}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class GetCollaborateurs(View):
    def get(self, request):
        try:
            # Récupérer tous les utilisateurs de la base de données avec les informations nécessaires
            collaborateurs = CollabFS.objects.all().values('id', 'isActivated', 'prenom', 'nom', 'email', 'poste')

            collaborateurs_data = []
            for collaborateur in collaborateurs:
                collaborateur_dict = {
                    'id': collaborateur['id'],  # Ajout de l'ID du collaborateur
                    'isActivated': collaborateur['isActivated'],
                    'full_name': f"{collaborateur['prenom']} {collaborateur['nom']}",
                    'email': collaborateur['email'],
                    'grade': collaborateur['poste']
                }
                collaborateurs_data.append(collaborateur_dict)

            return JsonResponse(collaborateurs_data, safe=False, status=200)

        except Exception as e:
            # Log the stack trace for debugging purposes
            traceback_str = traceback.format_exc()
            print(traceback_str)
            return JsonResponse({'error': str(e), 'traceback': traceback_str}, status=500)
