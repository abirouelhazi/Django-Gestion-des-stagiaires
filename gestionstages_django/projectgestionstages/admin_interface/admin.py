from django.contrib import admin
from .models import Stagiaire, Encadrant, User, Sujet, Stage
from django.utils.html import format_html

# Configuration de l'affichage pour le modèle User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'prenom', 'nom', 'role', 'is_active', 'is_staff', 'telephone', 'photo')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'nom', 'prenom')
    ordering = ('nom', 'prenom')

@admin.register(Stagiaire)
class StagiaireAdmin(admin.ModelAdmin):
    """Configuration de l'affichage pour le modèle Stagiaire."""
    
    # Liste des champs à afficher dans la vue de liste.
    list_display = (
        'user', 
        'cin', 
        'specialite', 
        'niveau_etude', 
        'universite'
    )

    # Liste des champs à utiliser pour la recherche.
    search_fields = ('cin', 'user__nom', 'user__prenom', 'user__email', 'user__telephone')

    # Liste des filtres à ajouter pour faciliter la navigation.
    list_filter = ('niveau_etude', 'specialite', 'universite',)

    # Définit l'ordre par défaut des objets affichés.
    ordering = ('user__nom', 'user__prenom')

    def user_email(self, obj):
        """Retourne l'email de l'utilisateur associé au stagiaire."""
        return obj.user.email

    user_email.short_description = 'Email'  # Titre de la colonne dans l'admin

# Configuration de l'affichage pour le modèle Encadrant
@admin.register(Encadrant)
class EncadrantAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialite', 'direction', 'nb_stagiaire_encadres')
    

    def nb_stagiaires(self, obj):
        return obj.nb_stagiaire_encadres  # Appelle la méthode ou propriété du modèle
    nb_stagiaires.short_description = "Nombre de stagiaires"

@admin.register(Sujet)
class SujetAdmin(admin.ModelAdmin):
    list_display = ('titre', 'description', 'encadrant')  # Champs à afficher dans la liste

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('type_stage', 'sujet', 'etat_stage', 'stagiaire', 'date_demande', 'rapport', 'attestation', 'note_evaluation')  # Champs à afficher dans la liste
    list_filter = ('etat_stage',)  # Permet de filtrer par état
    ordering = ('-date_demande',)  # Trie par date de demande décroissante

    def stagiaire(self, obj):
        return obj.stagiaire.user.nom  # Affiche le nom d'utilisateur du stagiaire

    stagiaire.short_description = 'Stagiaire'  # Titre de la colonne

    def rapport(self, obj):
        if obj.rapport:  # Vérifiez si le rapport existe
            return format_html('<a href="{}" target="_blank">Télécharger le Rapport</a>', obj.rapport.url)
        return "Aucun rapport"

    rapport.short_description = 'Rapport'  # Titre de la colonne

    def attestation(self, obj):
        if obj.attestation:  # Vérifiez si l'attestation existe
            return format_html('<a href="{}" target="_blank">Télécharger l\'Attestation</a>', obj.attestation.url)
        return "Aucune attestation"

    attestation.short_description = 'Attestation'  # Titre de la colonne

    def note_evaluation(self, obj):
        return obj.note_evaluation if obj.note_evaluation is not None else "Pas d'évaluation"

    note_evaluation.short_description = 'Note d\'Évaluation'  # Titre de la colonne