from django import forms #permet de creer des formulaires
from .models import Stagiaire, User, Encadrant,Stage, Sujet #importe de models.py les modeles necessaires pour creer les formulaires
from django.core.exceptions import ValidationError #pour signaler les erreurs de validations

class SujetForm(forms.ModelForm):
    #On ne redéfinit pas les champs dans SujetForm parce qu'on utilise leur version par défaut définie dans models.py.
    class Meta: #classe interne qui definit les champs de ce formaulaire
        model = Sujet #ce formulaire est basé sur le modele sujet
        fields = ['titre', 'description'] #liste des champs du modele qui seront inclus 

class StagiaireForm(forms.ModelForm):
    #Dans StagiaireForm, on avait besoin de plus de contrôle, d’où la redéfinition de certains champs.
    nom = forms.CharField(max_length=100, label="Nom")
    prenom = forms.CharField(max_length=100, label="Prénom")
    email = forms.EmailField(label="Email")
    telephone = forms.CharField(max_length=15, label="Téléphone")
    photo = forms.ImageField(required=False, label="Photo")
    cin = forms.CharField(max_length=8, label="CIN")
    lieu_de_naissance = forms.CharField(max_length=100, label="Lieu de naissance")  # Utilisez label au lieu de verbose_name
    date_de_naissance = forms.DateField(label="Date de naissance")  # Utilisez label au lieu de verbose_name
    adresse = forms.CharField(max_length=100, label="Adresse")  # Utilisez label au lieu de verbose_name
    niveau_etude = forms.CharField(max_length=30, label="Niveau d'étude")  # Utilisez label au lieu de verbose_name
    specialite = forms.CharField(max_length=30, label="Spécialité")  # Utilisez label au lieu de verbose_name
    universite = forms.CharField(max_length=30, label="Université")  # Utilisez label au lieu de verbose_name

    class Meta:
        model = Stagiaire
        fields = [
            'nom', 'prenom', 'email', 'telephone', 'cin', 'lieu_de_naissance', 'date_de_naissance',
            'adresse', 'niveau_etude', 'specialite', 'universite', 'photo'
        ]

    def clean_cin(self): #fonction pour valider le champ de cin
        #Après que l'utilisateur a rempli le formulaire, Django vérifie et nettoie les données.
        #Une fois validées, elles sont enregistrées sous forme de dictionnaire appelé cleaned_data. On récupère ensuite la valeur du CIN à partir de ce dictionnaire.
        cin = self.cleaned_data.get('cin')
        if cin and Stagiaire.objects.filter(cin=cin).exclude(id=self.instance.id).exists(): #Vérifie si un autre stagiaire a déjà ce cin, sauf l’instance actuelle.   #exclude...: Django ignore le stagiaire actuel et vérifie seulement les autres.
            raise ValidationError("Un stagiaire avec ce CIN existe déjà.") #Si le cin est déjà pris, lève une erreur de validation.
        return cin

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.instance.user if self.instance.pk else None
        if User.objects.filter(email=email).exclude(id=user.id if user else None).exists():
            raise ValidationError("L'email est déjà utilisé. Veuillez en choisir un autre.")
        return email

    def save(self, commit=True):
        if not self.instance.pk:  # Si le stagiaire est nouveau
            user = User(
                email=self.cleaned_data['email'],
                nom=self.cleaned_data['nom'],
                prenom=self.cleaned_data['prenom'],
                telephone=self.cleaned_data['telephone']
            )
            user.set_password('123456')  # Définir un mot de passe par défaut
            user.save()
            self.instance.user = user  # Associer l'utilisateur au stagiaire
        else:
            user = self.instance.user  # Récupérer l'utilisateur existant

        # Mettre à jour les informations de l'utilisateur
        user.email = self.cleaned_data['email']
        user.nom = self.cleaned_data['nom']
        user.prenom = self.cleaned_data['prenom']
        user.telephone = self.cleaned_data['telephone']
        if 'photo' in self.cleaned_data and self.cleaned_data['photo']:
            user.photo = self.cleaned_data['photo']

        if commit:
            user.save()  # Sauvegarder les modifications sur l'utilisateur
            print(f"Photo saved: {user.photo.url}")

        stagiaire = super().save(commit=False)  # Sauvegarder le stagiaire sans engager immédiatement

        if commit:
            stagiaire.save()  # Sauvegarder le stagiaire

        return stagiaire

class EncadrantForm(forms.ModelForm):
    email = forms.EmailField()
    nom = forms.CharField(max_length=100)  
    prenom = forms.CharField(max_length=100)  
    telephone = forms.CharField(max_length=15)
    photo = forms.ImageField(required=False, label="Photo")
    biographie = forms.CharField(widget=forms.Textarea, required=True)  
    specialite = forms.CharField(widget=forms.Textarea, required=True)
    direction = forms.CharField(widget=forms.Textarea, required=True)
    
    class Meta:
        model = Encadrant
        fields = ['nom', 'prenom', 'email', 'telephone', 'specialite', 'direction', 'biographie', 'photo']  # Inclure les champs liés à l'encadrant

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.instance.user if self.instance.pk else None
        if User.objects.filter(email=email).exclude(id=user.id if user else None).exists():
            raise ValidationError("L'email est déjà utilisé. Veuillez en choisir un autre.")
        return email
    
    
    def save(self, commit=True):
        # Mettre à jour l'utilisateur (si modifié)
        user = self.instance.user  # Accéder à l'utilisateur lié à l'encadrant
        user.email = self.cleaned_data['email']
        user.nom = self.cleaned_data['nom']  # Mettre à jour le nom de l'utilisateur
        user.prenom = self.cleaned_data['prenom']  # Mettre à jour le prénom de l'utilisateur
        user.telephone = self.cleaned_data['telephone']
        if 'photo' in self.cleaned_data and self.cleaned_data['photo']:
            user.photo = self.cleaned_data['photo'] 
        else:
            # Si aucune nouvelle photo n'est fournie, ne changez pas la photo
            user.photo = user.photo

        if commit:
            user.save()  # Sauvegarder les modifications sur l'utilisateur
            print(f"Photo saved: {user.photo.url}")

        # Mettre à jour l'encadrant
        encadrant = super().save(commit=False)  # Sauvegarder l'encadrant sans engager immédiatement

        if commit:
            encadrant.save()  # Sauvegarder l'encadrant

        return encadrant

class AdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nom', 'prenom', 'email', 'telephone', 'photo']

class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = [
            'type_stage', 'sujet', 
            'date_debut_stage', 'date_fin_stage', 'document' 
        ]

class ChangerEtatDemandeForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['etat']  # Vous pouvez ajouter d'autres champs si nécessaire
        widgets = {
            'etat': forms.Select(choices=[
                ('en_attente', 'En attente'),
                ('acceptee', 'Acceptée'),
                ('refusee', 'Refusée'),
            ]),
        }