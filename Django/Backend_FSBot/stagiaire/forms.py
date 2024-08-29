from django.forms import ModelForm
from .models import Stagiaire
from collaborateurs.models import CollabFS

class StagiaireForm(ModelForm):
    class Meta:
        model = Stagiaire
        fields = ['nom', 'prenom', 'email', 'sujet_pfe', 'etat_avancement', 'collaborateur']

    def __init__(self, *args, **kwargs):
        super(StagiaireForm, self).__init__(*args, **kwargs)
        self.fields['collaborateur'].required = True

    def save(self, commit=True):
        instance = super(StagiaireForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance
