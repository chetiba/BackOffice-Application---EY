from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.crypto import get_random_string
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
import base64
from missions.models import Mission


class CollabFS(AbstractUser):
    prenom = models.CharField(max_length=50, null=True)
    nom = models.CharField(max_length=50, null=True)
    isActivated = models.BooleanField(default=False, null=True)

    # Override the username and password fields to make them optional
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )

    password = models.CharField(max_length=128, null=True, blank=True)

    poste = models.CharField(max_length=100, choices=[
        ('Junior Consultant', 'Junior Consultant'),
        ('Senior Consultant', 'Senior Consultant'),
        ('Assistant Manager', 'Assistant Manager'),
        ('Manager', 'Manager'),
        ('Senior Manager', 'Senior Manager'),
        ('Partner', 'Partner')
    ])
    departement = models.CharField(max_length=100, default='SSL FS TRANSFORMATION')
    role = models.CharField(max_length=100)
    email = models.EmailField(verbose_name="Personal Email", unique=True)
    image = models.BinaryField(blank=True, null=True)
    cv = models.BinaryField(blank=True, null=True)
    access_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)
    is_authenticated = models.BooleanField(default=True)
    Compétences = models.TextField(blank=True, null=True)
    diplome_obtenu = models.CharField(max_length=255, db_column='diplome obtenu', blank=True, null=True)
    institution = models.CharField(max_length=100, blank=True, null=True)
    date = models.CharField(max_length=100, blank=True, null=True)
    missions = models.ManyToManyField(Mission)
    hours_left = models.IntegerField(
        default=40,
        validators=[MinValueValidator(0), MaxValueValidator(40)],
        help_text="Heures restantes que le collaborateur peut travailler cette semaine",
        blank=True,
        null=True
    )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="collabfs_groups",
        related_query_name="collabfs_group"
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="collabfs_user_permissions",
        related_query_name="collabfs_user_permission"
    )

    def save(self, *args, **kwargs):
        creating = not self.pk
        if creating:
            # Only generate username and password if they are not already set
            if not self.username:
                self.username = self.generate_username(self.prenom, self.nom)
            if not self.password:
                password_plaintext = self.generate_password()
                self.set_password(password_plaintext)  # Set the password for the user
                self.send_welcome_email(password_plaintext)
            self.email = self.email.lower()  # Ensure the email is in lowercase
            if CollabFS.objects.filter(username=self.username).exists():
                raise ValueError("Un utilisateur avec ce nom d'utilisateur existe déjà.")
        super().save(*args, **kwargs)

    @staticmethod
    def generate_password():
        return get_random_string(12, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&+=!')

    @staticmethod
    def generate_username(prenom, nom):
        # Create a username by removing spaces, converting to lower case, and appending the company domain
        username = f"{prenom}.{nom}".replace(' ', '').lower() + "@tn.ey.com"
        return username

    def send_welcome_email(self, password_plaintext):
        message = f"""
    Bonjour {self.prenom} {self.nom}, ({self.poste}) 

    Bienvenue chez EY! Voici vos détails de connexion:

    - Email: {self.username}

    - Mot de passe:  {password_plaintext}

    Vous pouvez vous connecter à notre système en utilisant votre email et ce mot de passe. Pour votre sécurité, nous vous recommandons de changer votre mot de passe après votre première connexion.

    Cordialement,
    L'équipe EY - {self.departement}

    """
        send_mail(
            'Bienvenue chez EY',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=True,
        )

    def send_reset_password_email(self):
        token = default_token_generator.make_token(self)
        # Encodage de l'ID utilisateur en base64
        uid_encoded = base64.urlsafe_b64encode(str(self.pk).encode()).decode()
        reset_url = f"{settings.FRONTEND_URL}/user-pages/change-password"
        message = f"""
        Bonjour {self.prenom} {self.nom},

        Pour réinitialiser votre mot de passe, veuillez utiliser les informations suivantes :
        Lien : {reset_url}
        Code utilisateur (uidb64): {uid_encoded}
        Token: {token}

        Copiez et collez les informations ci-dessus dans les champs appropriés sur la page indiquée.

        Si vous n'avez pas demandé la réinitialisation de votre mot de passe, veuillez ignorer cet email.

        Cordialement,
        L'équipe EY
        """
        send_mail(
            'Réinitialisation de mot de passe',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=True,
        )


class CollabMission(models.Model):
    mission = models.ForeignKey('missions.Mission', on_delete=models.CASCADE)
    delivery_team = models.ForeignKey(
        'collaborateurs.CollabFS',
        on_delete=models.CASCADE,
        limit_choices_to={'poste__in': ['Junior Consultant', 'Senior Consultant', 'Assistant Manager']},
        related_name='delivery_team_members',
        verbose_name='Delivery Team Member',
        null=True,
        blank=True
    )
    manager_responsable = models.ForeignKey(
        'collaborateurs.CollabFS',
        on_delete=models.SET_NULL,
        null=True,
        related_name='collab_missions_managed',  # Nom d'accès inversé unique pour les missions gérées dans CollabMission
        verbose_name='Manager Responsable'
    )
    marge_mission_manager = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(40)],
        help_text="Heures assignées au manager pour cette mission",
        null=True,
        blank=True
    )
    marge_mission = models.IntegerField(
        verbose_name='Marge Mission (heures)',
        validators=[MinValueValidator(0), MaxValueValidator(40)],
        null=True,
        blank=True
    )

    def __str__(self):
        team_member = self.delivery_team if self.delivery_team else 'No Team Member'
        mission_margin = f" - Marge Mission: {self.marge_mission} heures" if self.marge_mission is not None else ''
        return f"{team_member} - {self.mission.nom_projet}{mission_margin}"
