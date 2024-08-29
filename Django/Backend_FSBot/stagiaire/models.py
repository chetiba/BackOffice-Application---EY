from django.db import models
from django.conf import settings

from collaborateurs.models import CollabFS

class Stagiaire(models.Model):
    collaborateur = models.ForeignKey('collaborateurs.CollabFS', on_delete=models.CASCADE, null=True, blank=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    sujet_pfe = models.CharField(max_length=255)
    etat_avancement = models.IntegerField(choices=[
        (0, '0% - 25%'),
        (25, '26% - 50%'),
        (50, '51% - 75%'),
        (75, '76% - 100%'),
        (100, 'Terminé')
    ], default=0)
    fichier = models.FileField(upload_to='fichiers_stagiaires/', blank=True,
                               null=True)  # Rendre le champ fichier optionnel

    def __str__(self):
        return f"{self.prenom} {self.nom}"
