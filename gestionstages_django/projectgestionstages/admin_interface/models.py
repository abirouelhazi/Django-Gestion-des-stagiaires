from django.db import models
from django.contrib.auth.models import AbstractUser ,BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)# save sert soit à enregistrer ou à mettre à jour
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('encadrant', 'Encadrant'),
        ('stagiaire', 'Stagiaire'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='stagiaire', verbose_name="Rôle")
    email = models.EmailField(unique=True, verbose_name="Email")
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    telephone = models.CharField(max_length=15, verbose_name="Téléphone")
    photo = models.ImageField(
        upload_to='photos_users/',
        blank=True,
        null=True,
        default='admin_interface/images/admin.png',  
        verbose_name="Photo"
    )

    username = None  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    def save(self, *args, **kwargs):
        if not self.pk:  # si la clé primaire est vide = l'utilisateur est nouveau (pas encore enregistré)
            self.set_password('123456')  # Définir le mot de passe par défaut
        super().save(*args, **kwargs)

class Encadrant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="encadrant", verbose_name="Utilisateur")
    biographie = models.TextField(verbose_name="Biographie")
    specialite = models.CharField(max_length=100, verbose_name="Spécialité")
    direction = models.CharField(max_length=100, verbose_name="Direction")
    nb_stagiaire_encadres = models.PositiveIntegerField(default=0, verbose_name="Nombre de stagiaires encadrés", editable=False)

    def __str__(self):
        return f"{self.user.prenom} {self.user.nom}"

class Sujet(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    encadrant = models.ForeignKey(Encadrant, on_delete=models.CASCADE, related_name='sujets')
    
    def __str__(self):
        return self.titre

class Stagiaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="stagiaire", verbose_name="Utilisateur")
    cin = models.CharField(max_length=8, unique=True, verbose_name="CIN")
    lieu_de_naissance = models.CharField(max_length=100, verbose_name="Lieu de naissance")
    date_de_naissance = models.DateField(verbose_name="Date de naissance")
    adresse = models.CharField(max_length=100, verbose_name="Adresse")
    niveau_etude = models.CharField(max_length=30, verbose_name="Niveau d'étude")
    specialite = models.CharField(max_length=30, verbose_name="Spécialité")
    universite = models.CharField(max_length=30, verbose_name="Université")
    
    def has_stages(self):
        return self.demandes.filter(etat='acceptee').exists()

    def __str__(self):
        return f"{self.user.prenom} {self.user.nom}"

class Stage(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
    ]
    stagiaire = models.ForeignKey(Stagiaire, on_delete=models.CASCADE, related_name='demandes', verbose_name="Stagiaire")  
    sujet = models.ForeignKey(Sujet, on_delete=models.CASCADE, related_name='demandes')  
    type_stage = models.CharField(max_length=100)
    date_debut_stage = models.DateField()
    date_fin_stage = models.DateField()
    date_demande = models.DateTimeField(auto_now_add=True)
    document = models.FileField(upload_to='documents_stages/', null=True, blank=True)  
    etat = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')  # État de la demande
    note_evaluation = models.FloatField(null=True, blank=True) 
    rapport = models.FileField(upload_to='rapports/', null=True, blank=True) 
    etat_stage = models.CharField(max_length=20, default='non concluant')
    attestation = models.FileField(upload_to='attestations/', null=True, blank=True) 
    def __str__(self):
        return f"Demande de stage pour {self.stagiaire.user.prenom} {self.stagiaire.user.nom} - Sujet: {self.sujet.titre}"