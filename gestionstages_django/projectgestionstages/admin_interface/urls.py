from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import proposer_sujet, afficher_sujet, modifier_sujet, supprimer_sujet,les_sujets, demande_stage, profil_stagiaire, mes_demandes  
from .views import gestion_demandes_stage, changer_etat_demande, stagiaire_detail, voir_document
from .views import register_stagiaire, modifier_profil_stagiaire, evaluer_stagiaire, enregistrer_etat_stage, mettre_rapport 
from .views import soumettre_attestation

urlpatterns = [
    path('add_admin/', views.add_admin, name='add_admin'),

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('gestion_demandes/', gestion_demandes_stage, name='gestion_demandes_stage'),
    path('stagiaire/<int:stagiaire_id>/', stagiaire_detail, name='stagiaire_detail'),
    path('voir_document/<int:demande_id>/', voir_document, name='voir_document'),
    path('changer_etat_demande/<int:demande_id>/<str:action>/', changer_etat_demande, name='changer_etat_demande'),
    path('stagiaires/', views.gestion_stagiaires, name='gestion_stagiaires'),
    path('soumettre_attestation/<int:demande_id>/', soumettre_attestation, name='soumettre_attestation'),  
    path('stagiaires/modifier/<int:id>/', views.modifier_stagiaire, name='modifier_stagiaire'),
    path('stagiaires/supprimer/<int:id>/', views.supprimer_stagiaire, name='supprimer_stagiaire'),
    path('stagiaires/ajouter/', views.ajouter_stagiaire, name='ajouter_stagiaire'),
    path('encadrants/', views.gestion_encadrants, name='gestion_encadrants'),
    path('encadrants/modifier/<int:id>/', views.modifier_encadrant, name='modifier_encadrant'),
    path('encadrants/supprimer/<int:id>/', views.supprimer_encadrant, name='supprimer_encadrant'),
    path('encadrants/ajouter/', views.ajouter_encadrant, name='ajouter_encadrant'),
    path('profil/', views.profil_admin, name='profil_admin'),  # Vérifie cette route
    path('profil/modifier/', views.modifier_profil_admin, name='modifier_profil_admin'),  # Modifier les infos

    
    path('encadrant_dashboard/', views.encadrant_dashboard, name='encadrant_dashboard'),
    path('encadrant/stagiaires/', views.encadrer_stagiaires, name='encadrer_stagiaires'),
    path('evaluer_stagiaire/', evaluer_stagiaire, name='evaluer_stagiaire'),
    path('enregistrer_etat_stage/', enregistrer_etat_stage, name='enregistrer_etat_stage'),
    path('encadrant/sujets/', views.gestion_sujets, name='gestion_sujets'),
    path('proposer_sujet/', proposer_sujet, name='proposer_sujet'),
    path('sujets/modifier/<int:sujet_id>/', modifier_sujet, name='modifier_sujet'),
    path('sujets/supprimer/<int:sujet_id>/', supprimer_sujet, name='supprimer_sujet'),
    path('sujets/<int:sujet_id>/', afficher_sujet, name='afficher_sujet'),
    path('encadrant/profil/', views.profil_encadrant, name='profil_encadrant'),
    path('encadrant/modifier_profil/<int:encadrant_id>', views.modifier_profil_encadrant, name='modifier_profil_encadrant'),

    path('stagiaire_dashboard/', views.stagiaire_dashboard, name='stagiaire_dashboard'),
    path('les_sujets/', les_sujets, name='les_sujets'),
    path('stagiaires/profil/', profil_stagiaire, name='profil_stagiaire'),
    path('stagiaire/modifier_profil/<int:stagiaire_id>/', modifier_profil_stagiaire, name='modifier_profil_stagiaire'),
    path('demande_stage/', demande_stage, name='demande_stage'),
    path('mes_demandes/', mes_demandes, name='mes_demandes'),
    path('mettre_rapport/<int:demande_id>/', mettre_rapport, name='mettre_rapport'),  # Assurez-vous que cette ligne est présente
    

    path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='index/login.html'), name='login'),  # Page de connexion
    path('register/', register_stagiaire, name='register_stagiaire'),
    path('custom_login/',  views.custom_login, name='custom_login'), 
    path('deconnexion/', views.deconnexion, name='deconnexion'),
   
]
