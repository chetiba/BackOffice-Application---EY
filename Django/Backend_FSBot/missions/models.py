from django.db import models
from clients.models import Client
import random
from django.conf import settings


class Mission(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    responsable_manager = models.ForeignKey(
        'collaborateurs.CollabFS',
        on_delete=models.SET_NULL,
        null=True,
        related_name='missions_managed',  # Nom d'accès inversé unique pour le manager responsable
        verbose_name='Responsable Manager'
    )
    partner_responsable = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='partnered_missions',
        limit_choices_to={'poste': 'Partner'},  # Assure que le partenaire est obligatoirement assigné
        verbose_name='Partner Responsable'
    )
    code_projet = models.CharField(max_length=20, blank=True, null=True)
    nom_projet = models.CharField(max_length=100, blank=True, null=True)
    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)
    gfis_sub_management_unit = models.CharField(max_length=100, blank=True, default="Transfo FS")

    def __str__(self):
        return f"{self.nom_projet} ({self.code_projet})"

    def save(self, *args, **kwargs):
        if not self.code_projet:
            self.code_projet = f"E-{random.randint(10000000, 99999999)}"
        super().save(*args, **kwargs)
