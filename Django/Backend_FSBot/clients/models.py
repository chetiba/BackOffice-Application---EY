from django.db import models


class Client(models.Model):
    nom = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.nom
