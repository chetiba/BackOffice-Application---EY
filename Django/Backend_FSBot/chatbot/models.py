from django.db import models

class CVBanque(models.Model):
    title = models.CharField(max_length=100)
    Compétences = models.TextField()
    grade = models.CharField(max_length=100)
    diplome_obtenu = models.CharField(max_length=255, db_column='diplome obtenu')
    institution = models.CharField(max_length=100)
    attachments = models.BinaryField()  # Stocker le CV en tant que BLOB

    class Meta:
        managed = False  # Ne pas gérer cette table avec les migrations Django
        db_table = 'cv fs transformation - banque'  # title de la table existante

    def __str__(self):
        return f"{self.title} - Diplôme: {self.diplome_obtenu}, Institution: {self.institution}"

class CVAssurance(models.Model):
    title = models.CharField(max_length=100)
    Compétences = models.TextField()
    grade = models.CharField(max_length=100)
    diplome_obtenu = models.CharField(max_length=255, db_column='diplome obtenu')
    institution = models.CharField(max_length=100)
    attachments = models.BinaryField()  # Stocker le CV en tant que BLOB

    class Meta:
        managed = False  # Ne pas gérer cette table avec les migrations Django
        db_table = 'cv fs transformation - assurance'  # title de la table existante

    def __str__(self):
        return f"{self.title} - Diplôme: {self.diplome_obtenu}, Institution: {self.institution}"
