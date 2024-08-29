from django.forms import ModelForm
from .models import Mission

class MissionForm(ModelForm):
    class Meta:
        model = Mission
        fields = ['client', 'code_projet', 'nom_projet', 'date_debut', 'date_fin']
