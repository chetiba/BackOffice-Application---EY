from django import forms
from .models import CollabMission

class AssignMissionForm(forms.ModelForm):
    class Meta:
        model = CollabMission
        fields = ['mission', 'delivery_team', 'marge_mission','marge_mission_manager']
        labels = {
            'mission': 'Mission',
            'delivery_team': 'Membre de l’équipe de livraison',
            'marge_mission': 'Marge '
        }
        help_texts = {
            'mission': 'Sélectionnez la mission assignée.',
            'delivery_team': 'Sélectionnez le membre de l’équipe pour cette mission.',
            'marge_mission': 'Entrez la marge prévue pour ce membre.'
        }
        error_messages = {
            'mission': {
                'required': 'Ce champ est requis.',
            },
            'delivery_team': {
                'required': 'Ce champ est requis.',
            },
            'marge_mission': {
                'required': 'Ce champ est requis.',
                'invalid': 'Veuillez entrer un nombre valide.',
            }
        }
