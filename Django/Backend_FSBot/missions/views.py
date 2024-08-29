from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from collaborateurs.models import  CollabMission, CollabFS
from .models import Mission
from django.db import transaction
import json

from clients.models import  Client

@method_decorator(csrf_exempt, name='dispatch')
class AssignMission(View):
    def post(self, request, manager_id):
        data = json.loads(request.body)
        manager_id = int(manager_id)  # Conversion pour éviter des problèmes de type
        try:
            manager = CollabFS.objects.get(id=manager_id)
            partner_id = data.get('partner_id')
            partner = CollabFS.objects.get(id=partner_id)

            marge_manager = data.get('marge_mission_manager', 0)

            with transaction.atomic():
                mission = Mission(
                    client_id=data['client_id'],
                    nom_projet=data['nom_projet'],
                    date_debut=data['date_debut'],
                    date_fin=data['date_fin'],
                    responsable_manager=manager,
                    partner_responsable=partner
                )
                mission.save()

                if manager.hours_left >= marge_manager:
                    manager.hours_left -= marge_manager
                    manager.save()
                else:
                    return JsonResponse({"erreur": "Le manager n'a pas suffisamment d'heures disponibles"}, status=400)

                erreurs = []
                for member_id in data.get('delivery_team_ids', []):
                    member = CollabFS.objects.get(id=member_id)
                    marge_mission = data['marges'].get(str(member_id), 0)

                    if member.hours_left < marge_mission:
                        erreurs.append(f"Le collaborateur {member.prenom} {member.nom} n'a pas suffisamment d'heures disponibles.")
                        continue

                    member.hours_left -= marge_mission
                    member.save()

                    CollabMission.objects.create(
                        mission=mission,
                        delivery_team=member,
                        marge_mission=marge_mission,
                        manager_responsable=manager,
                        marge_mission_manager=marge_manager if member.id == manager_id else 0
                    )

                if erreurs:
                    return JsonResponse({"erreur": "Certains collaborateurs n'ont pas pu être assignés", "détails": erreurs}, status=400)

                return JsonResponse({"message": "Mission ajoutée et tous les collaborateurs assignés avec succès !"}, status=201)

        except CollabFS.DoesNotExist:
            return JsonResponse({"erreur": "Manager, partenaire ou collaborateur non trouvé"}, status=404)
        except Exception as e:
            return JsonResponse({"erreur": str(e)}, status=400)



    def assign_mission_to_team_member(self, member, mission, marge_mission, manager_id, marge_manager):
        if member.hours_left >= marge_mission:
            member.hours_left -= marge_mission
            member.save()

            # Création de l'objet CollabMission
            collab_mission = CollabMission.objects.create(
                mission=mission,
                delivery_team=member,
                marge_mission=marge_mission,
                manager_responsable_id=manager_id,
                marge_mission_manager=marge_manager if member.id == int(manager_id) else 0
                # Appliquer la marge_manager uniquement au manager
            )
            return True
        else:
            return False


@method_decorator(csrf_exempt, name='dispatch')
class GetAllMissions(View):
    def get(self, request):
        try:
            # Fetch all missions from the database
            missions = Mission.objects.all()

            # Prepare the data to be returned as JSON
            missions_data = []
            for mission in missions:
                # Retrieve the manager responsible
                manager_info = {
                    'id': mission.responsable_manager.id,
                    'prenom': mission.responsable_manager.prenom,
                    'nom': mission.responsable_manager.nom
                } if mission.responsable_manager else None

                # Retrieve the delivery team and their margin for the mission
                collab_missions = CollabMission.objects.filter(mission=mission)
                delivery_team_info = []
                for collab_mission in collab_missions:
                    delivery_team_info.append({
                        'collaborateur': f"{collab_mission.delivery_team.prenom} {collab_mission.delivery_team.nom}",
                        'marge_mission': collab_mission.marge_mission,
                        'manager_responsable': f"{collab_mission.manager_responsable.prenom} {collab_mission.manager_responsable.nom}" if collab_mission.manager_responsable else 'N/A',
                        'marge_mission_manager': collab_mission.marge_mission_manager
                    })

                mission_info = {
                    'id': mission.id,
                    'nom_projet': mission.nom_projet,
                    'code_projet': mission.code_projet,
                    'date_debut': mission.date_debut,
                    'date_fin': mission.date_fin,
                    'gfis_sub_management_unit': mission.gfis_sub_management_unit,
                    'client': {
                        'nom': mission.client.nom if mission.client else None
                    } if mission.client else None,
                    'manager_responsable': manager_info,
                    'delivery_team': delivery_team_info
                }

                missions_data.append(mission_info)

            return JsonResponse(missions_data, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
def missions_by_client(request, client_id):
    try:
        # Filtrer les missions associées au client
        missions = CollabMission.objects.filter(mission__client__id=client_id).select_related('mission', 'manager_responsable', 'delivery_team')

        # Préparer les données à retourner sous forme de JSON
        missions_data = []
        for collab_mission in missions:
            mission_info = {
                'nom_projet': collab_mission.mission.nom_projet,
                'code_projet': collab_mission.mission.code_projet,
                'date_debut': collab_mission.mission.date_debut,
                'date_fin': collab_mission.mission.date_fin,
                'manager_responsable': {
                    'prenom': collab_mission.manager_responsable.prenom if collab_mission.manager_responsable else None,
                    'nom': collab_mission.manager_responsable.nom if collab_mission.manager_responsable else None,
                },
                'collaborateur': {
                    'prenom': collab_mission.delivery_team.prenom,
                    'nom': collab_mission.delivery_team.nom
                },
                'marge_mission': collab_mission.marge_mission
            }
            missions_data.append(mission_info)

        return JsonResponse(missions_data, safe=False, status=200)

    except Client.DoesNotExist:
        return JsonResponse({'error': 'Client non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
