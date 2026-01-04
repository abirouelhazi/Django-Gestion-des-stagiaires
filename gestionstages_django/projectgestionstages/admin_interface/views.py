from django.shortcuts import render, get_object_or_404, redirect
from .models import Stagiaire, Encadrant, User, Sujet, Stage
from .forms import StagiaireForm, EncadrantForm, AdminForm, SujetForm, StageForm
from django.urls import reverse_lazy
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

#--------------------------------------------------------------------Page index
def index(request):
    return render(request, 'index/index.html')

def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print('email:', email)
        print('password:', password)

        # Authentifier l'utilisateur
        user = authenticate(request, username=email, password=password)
        print('user:', user)

        if user is not None:
            login(request, user)  # Connecter l'utilisateur
            print(user.role)

            # Redirection en fonction du rôle de l'utilisateur
            if user.role == 'admin':
                print("Je suis Admin")
                return redirect('admin_dashboard')
            elif user.role == 'encadrant':
                return redirect('encadrant_dashboard')
            elif user.role == 'stagiaire':
                return redirect('stagiaire_dashboard')
        else:
            # Afficher un message d'erreur si l'authentification échoue
            messages.error(request, "Identifiants invalides.")
            return render(request, 'index/login.html')

    return render(request, 'index/login.html')

def deconnexion(request):
    logout(request)  # Supprime la session de l'utilisateur
    return redirect('index')  # Redirige vers la page d'accueil ou la page de connexion

#----------------------------------------------------------------Page administrateur


@login_required
def admin_dashboard(request):
    context = {
        'admin': request.user, 
    }
    return render(request, 'admin_dashboard.html', context)

def add_admin(request):
    # Ajouter un admin
    if request.method == 'POST':
        form = AdminForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create(
                email=form.cleaned_data['email'],
                nom=form.cleaned_data['nom'],
                prenom=form.cleaned_data['prenom'],
                role='admin'
            )
            message = f"Administrateur {user.nom} ajouté avec succès."
            return render(request, 'administrateur/ajouter_admin.html', {'form': form, 'message': message})#on recharge la page avec message de succes
        else:
            print(request)
            return render(request, 'administrateur/ajouter_admin.html', {'form': form})
    else:
        form = AdminForm()
    return render(request, 'administrateur/ajouter_admin.html', {'form': form})

def changer_etat_demande(request, demande_id, action):
    # Récupérer la demande de stage ou renvoyer une 404 si elle n'existe pas
    demande = get_object_or_404(Stage, id=demande_id)

    if action == 'accepter':
        # Mettre à jour l'état de la demande à 'acceptee'
        demande.etat = 'acceptee'
        demande.save()  # Enregistrer les modifications

        # Mettre à jour le nombre de stagiaires de l'encadrant
        encadrant = demande.sujet.encadrant
        if encadrant:  # Vérifiez que l'encadrant n'est pas None
            encadrant.nb_stagiaire_encadres += 1  # Incrémentez le nombre de stagiaires
            encadrant.save()  # Sauvegarder les modifications

    elif action == 'refuser':
        demande.etat = 'refusee'
        demande.save()

    else:
        demande.etat = 'en_attente'
    # Rediriger vers la page de gestion des demandes
    return redirect('gestion_demandes_stage')

@login_required
def gestion_demandes_stage(request):
    # Récupérer toutes les demandes qui ne sont pas refusées
    demandes = Stage.objects.exclude(etat='refusee')

    return render(request, 'administrateur/gestion_demandes_stage.html', {'demandes': demandes})

def stagiaire_detail(request, stagiaire_id):
    stagiaire = get_object_or_404(Stagiaire, id=stagiaire_id)
    demandes = stagiaire.demandes.all()  # Assurez-vous que cela renvoie des demandes
    return render(request, 'administrateur/stagiaire_detail.html', {'stagiaire': stagiaire, 'demandes': demandes})

def voir_document(request, demande_id):
    # Récupérer la demande de stage associée à l'ID
    demande = get_object_or_404(Stage, id=demande_id)

    # Vérifier si le document existe
    if demande.document:
        # Ouvrir le fichier en mode binaire
        with open(demande.document.path, 'rb') as fichier:
            response = HttpResponse(fichier.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{demande.document.name.split("/")[-1]}"'  # Affiche le PDF dans le navigateur
            return response
    else:
        return HttpResponse("Aucun document disponible.", status=404)
    
def gestion_encadrants(request):
    encadrants = Encadrant.objects.all()

    # Créer une liste de dictionnaires pour stocker les encadrants et leur nombre de stagiaires
    encadrants_info = []
    for encadrant in encadrants:
        # Récupérer les stagiaires associés à cet encadrant via les demandes de stage acceptées
        nombre_stagiaires = Stagiaire.objects.filter(demandes__sujet__encadrant=encadrant, demandes__etat='acceptee').distinct().count()
        
        encadrants_info.append({
            'encadrant': encadrant,
            'nombre_stagiaires': nombre_stagiaires,  
        })

    return render(request, 'administrateur/gestion_encadrants.html', {'encadrants_info': encadrants_info})

def ajouter_encadrant(request):
    if request.method == "POST":
        form = EncadrantForm(request.POST, request.FILES)
        if not form.is_valid():
            print(form.errors)  

        if form.is_valid():
            # Créer l'utilisateur
            user = User(
                email=form.cleaned_data['email'],
                nom=form.cleaned_data['nom'],
                prenom=form.cleaned_data['prenom'],
                telephone=form.cleaned_data['telephone'],
                role='encadrant'  # Assurez-vous que le champ 'role' existe dans votre modèle User
            )
            user.set_password('123456')  
            user.save()  # Enregistrer l'utilisateur

            # Créer l'encadrant et associer l'utilisateur à l'encadrant
            encadrant = Encadrant(
                user=user,
                biographie=form.cleaned_data['biographie'], 
                specialite=form.cleaned_data['specialite'],
                direction=form.cleaned_data['direction']
            )
            encadrant.save() 
            
            return redirect('gestion_encadrants') 
    else:
        form = EncadrantForm()  

    return render(request, 'administrateur/ajouter_encadrant.html', {'form': form})

def modifier_encadrant(request, id):
    encadrant = get_object_or_404(Encadrant, id=id)
    user = encadrant.user
    
    if request.method == 'POST':
        form = EncadrantForm(request.POST, instance=encadrant)
        if form.is_valid():
            form.save()  
            return redirect('gestion_encadrants') 
    else:
        form = EncadrantForm(
            instance=encadrant,
            initial={
                'nom': user.nom,
                'prenom': user.prenom,
                'email': user.email,
                'telephone': user.telephone,
                'photo': user.photo,
            }
        )
    
    return render(request, 'administrateur/modifier_encadrant.html', {'form': form, 'encadrant': encadrant})
             
def supprimer_encadrant(request, id):
    encadrant = get_object_or_404(Encadrant, id=id)

    # Vérifier si l'encadrant a des stagiaires avec des stages conclus
    if encadrant.sujets.filter(demandes__etat_stage='concluant').exists():
        messages.error(request, "Cet encadrant ne peut pas être supprimé car il a des stagiaires avec des stages conclus.")
        return redirect('gestion_encadrants')

    # Si aucune demande de stage concluant n'est trouvée, supprimer l'encadrant
    encadrant.delete()
    messages.success(request, "L'encadrant a été supprimé avec succès.")
    return redirect('gestion_encadrants')

def gestion_stagiaires(request):
    """
    Affiche la liste des stagiaires avec leurs demandes de stage.
    """
    stagiaires = Stagiaire.objects.prefetch_related('demandes').all()
    return render(request, 'administrateur/gestion_stagiaires.html', {'stagiaires': stagiaires})

def soumettre_attestation(request, demande_id):
    """
    Permet à l'administrateur de soumettre une attestation pour une demande de stage.
    """
    demande = get_object_or_404(Stage, id=demande_id)

    if request.method == 'POST':
        attestation = request.FILES.get('attestation')
        if attestation:
            demande.attestation = attestation  
            demande.save()  
            return redirect('gestion_stagiaires')  
        else:
            # Gérer le cas où l'attestation n'est pas fournie
            return redirect('gestion_stagiaires')  

    return redirect('gestion_stagiaires')  # Redirigez vers la liste des stagiaires si la méthode n'est pas POST

def ajouter_stagiaire(request):
    if request.method == "POST":
        form = StagiaireForm(request.POST, request.FILES)
        if not form.is_valid():
            print(form.errors)  

        if form.is_valid():
            # Créer l'utilisateur
            user = User(
                email=form.cleaned_data['email'],
                nom=form.cleaned_data['nom'],
                prenom=form.cleaned_data['prenom'],
                telephone=form.cleaned_data['telephone'],
            )
            user.set_password('123456')  
            user.save() 

            # Créer le stagiaire et associer l'utilisateur au stagiaire
            stagiaire = Stagiaire(
                user=user,
                lieu_de_naissance = form.cleaned_data['lieu_de_naissance'],  
                date_de_naissance = form.cleaned_data['date_de_naissance'],  
                adresse = form.cleaned_data['adresse'], 
                niveau_etude = form.cleaned_data['niveau_etude'],  
                specialite = form.cleaned_data['specialite'],  
                universite = form.cleaned_data['universite'], 

            )
            stagiaire.save() 
            
            return redirect('gestion_stagiaires')  
    else:
        form = StagiaireForm() 

    return render(request, 'administrateur/ajouter_stagiaire.html', {'form': form})

def modifier_stagiaire(request, id):
    stagiaire = get_object_or_404(Stagiaire, id=id)
    user = stagiaire.user

    if request.method == "POST":
        form = StagiaireForm(request.POST, instance=stagiaire)
        if form.is_valid():
            stagiaire = form.save()  
            return redirect('gestion_stagiaires')  # Redirige vers la page de gestion
    else:
        form = StagiaireForm(instance=stagiaire,
                             initial={
                                'nom': user.nom,
                                'prenom': user.prenom, 'email':user.email, 'telephone': user.telephone, 'photo': user.photo
                                                            })  

    return render(request, 'administrateur/modifier_stagiaire.html', {'form': form})

def supprimer_stagiaire(request, id):
    stagiaire = get_object_or_404(Stagiaire, id=id)
    stagiaire.delete()
    messages.success(request, 'Le stagiaire a été supprimé avec succès.')
    return redirect('gestion_stagiaires') 

#profil_admin
def profil_admin(request):
    context = {
        'admin': request.user,
    }
    return render(request, 'administrateur/profil_admin.html', context)

def modifier_profil_admin(request):
    admin = request.user  # Récupère l'admin connecté
    if request.method == 'POST':
        form = AdminForm(request.POST, request.FILES, instance=admin)
        if form.is_valid():
            form.save()
            return redirect('profil_admin')  
    else:
        form = AdminForm(instance=admin)
    return render(request, 'administrateur/modifier_profil_admin.html', {'form': form})

#----------------------------------------------------------------Page encadrant

@login_required  # Pour assurer que l'utilisateur est connecté
def encadrant_dashboard(request):
    # Récupérer l'encadrant connecté
    encadrant = get_object_or_404(Encadrant, user=request.user)

    # Récupérer la liste des stagiaires associés à cet encadrant via les demandes de stage
    stagiaires = Stagiaire.objects.filter(demandes__sujet__encadrant=encadrant, demandes__etat='acceptee').distinct()

    # Compter le nombre de stagiaires associés
    nombre_stagiaires = stagiaires.count()  

    # Récupérer les sujets associés à cet encadrant
    sujets = Sujet.objects.filter(encadrant=encadrant)

    # Récupérer le nombre de sujets
    nb_sujets = sujets.count()

    context = {
        'encadrant': encadrant,
        'stagiaires': stagiaires,
        'nombre_stagiaires': nombre_stagiaires,
        'sujets': sujets,
        'nb_sujets': nb_sujets,
    }

    return render(request, 'encadrant/page_encadrant.html', context)

#mes_stagiaires
def encadrer_stagiaires(request):
    encadrant = get_object_or_404(Encadrant, user=request.user)  # Récupérer l'encadrant connecté
    # Récupérer les stagiaires associés à cet encadrant via les demandes de stage
    stagiaires = Stagiaire.objects.filter(demandes__sujet__encadrant=encadrant, demandes__etat='acceptee').distinct()

    context = {
        'encadrant': encadrant,
        'stagiaires': stagiaires,
    }
    return render(request, 'encadrant/mes_stagiaires.html', context)

def evaluer_stagiaire(request):
    if request.method == 'POST':
        stagiaire_id = request.POST.get('stagiaire_id')
        note = request.POST.get(f'note_{stagiaire_id}')
        etat_stage = request.POST.get(f'etat_stage_{stagiaire_id}')

        # Récupérer la demande de stage associée au stagiaire
        demande = get_object_or_404(Stage, stagiaire_id=stagiaire_id)

        # Mettre à jour la note d'évaluation et l'état du stage
        if note:
            try:
                demande.note_evaluation = float(note)  # Convertir la note en float
            except ValueError:
                demande.note_evaluation = None  # Si la conversion échoue, mettre à None

        demande.etat_stage = etat_stage  # Mettre à jour l'état du stage
        demande.save()  # Enregistrer les modifications

    return redirect('encadrer_stagiaires')  # Redirigez vers la vue appropriée après la soumission

def enregistrer_etat_stage(request):
    if request.method == 'POST':
        stagiaire_id = request.POST.get('stagiaire_id')
        etat_stage = request.POST.get(f'etat_stage_{stagiaire_id}')
        demande = get_object_or_404(Stage, stagiaire_id=stagiaire_id)

        demande.etat_stage = etat_stage
        demande.save() 

    return redirect('mes_stagiaires') 

#mes_sujets
def gestion_sujets(request):
    encadrant = get_object_or_404(Encadrant, user=request.user)
    sujets = Sujet.objects.filter(encadrant=encadrant)

    # Créer un dictionnaire pour stocker les stagiaires associés à chaque sujet
    sujets_avec_stagiaires = []

    for sujet in sujets:
        # Récupérer les stagiaires associés à ce sujet via les demandes de stage
        stagiaires = Stagiaire.objects.filter(demandes__sujet=sujet, demandes__etat='acceptee').distinct()
        sujets_avec_stagiaires.append({
            'sujet': sujet,
            'stagiaires': stagiaires,
        })

    return render(request, 'encadrant/mes_sujets.html', {'sujets_avec_stagiaires': sujets_avec_stagiaires})

def proposer_sujet(request):
    if request.method == 'POST':
        form = SujetForm(request.POST)
        if form.is_valid():
            sujet = form.save(commit=False)
            sujet.encadrant = Encadrant.objects.get(user=request.user)
            sujet.save()
            print(f"Sujet enregistré : {sujet.titre}")
            return redirect('gestion_sujets')
    else:
        form = SujetForm()
    
    return render(request, 'encadrant/proposer_sujet.html', {'form': form})

def afficher_sujet(request, sujet_id):
    sujet = get_object_or_404(Sujet, id=sujet_id)
    stagiaires = Stagiaire.objects.filter(demandes__sujet=sujet, demandes__etat='acceptee').distinct()  

    return render(request, 'encadrant/afficher_sujet.html', {'sujet': sujet, 'stagiaires': stagiaires})

def modifier_sujet(request, sujet_id):
    sujet = get_object_or_404(Sujet, id=sujet_id)
    if request.method == 'POST':
        form = SujetForm(request.POST, instance=sujet)
        if form.is_valid():
            form.save()
            return redirect('gestion_sujets')  # Redirige vers la liste des sujets
    else:
        form = SujetForm(instance=sujet)
    return render(request, 'encadrant/modifier_sujet.html', {'form': form})

def supprimer_sujet(request, sujet_id):
    sujet = get_object_or_404(Sujet, id=sujet_id)

    if Stage.objects.filter(sujet=sujet).exists():
        # Ajoutez un message d'erreur
        messages.error(request, "Ce sujet ne peut pas être supprimé car il est associé à des demandes de stage.")
        return redirect('gestion_sujets')  # Redirige vers la liste des sujets

    if request.method == 'POST':
        sujet.delete()
        messages.success(request, "Le sujet a été supprimé avec succès.")
        return redirect('gestion_sujets')  # Redirige vers la liste des sujets

    return render(request, 'encadrant/confirmer_suppression.html', {'sujet': sujet})
  
#profil_encadrant
def profil_encadrant(request):
    encadrant = get_object_or_404(Encadrant, user=request.user)  
    print(f"Encadrant: {encadrant.user.prenom}, {encadrant.user.nom}, {encadrant.user.email}, {encadrant.user.telephone}")  # Pour déboguer
    return render(request, 'encadrant/profil_encadrant.html', {'encadrant': encadrant})

def modifier_profil_encadrant(request, encadrant_id):
    # Récupérer l'encadrant par son ID
    encadrant = get_object_or_404(Encadrant, id=encadrant_id)
    
    if request.method == 'POST':
        print(request.FILES) 
        # Créer un formulaire avec les données du POST
        form = EncadrantForm(request.POST, request.FILES, instance=encadrant)

        if form.is_valid():
            print("Form is valid")
            form.save()
            messages.success(request, "Les modifications ont été enregistrées avec succès.")
            return redirect('profil_encadrant')  # Rediriger vers la page de profil

        else:
            print("Form is not valid")
            print(form.errors)
            messages.error(request, "Veuillez corriger les erreurs.")

    else:
        form = EncadrantForm(instance=encadrant)

    return render(request, 'encadrant/modifier_profil_encadrant.html', {'form': form, 'encadrant': encadrant})

#----------------------------------------------------------------Page stagiaire

def register_stagiaire(request):
    if request.method == 'POST':
        form = StagiaireForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre compte a été créé avec succès !')
            return redirect('login')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = StagiaireForm()

    return render(request, 'index/register.html', {'form': form})

@login_required  
def stagiaire_dashboard(request):
    stagiaire = get_object_or_404(Stagiaire, user=request.user)
    return render(request, 'stagiaire/stagiaire_dashboard.html', {'stagiaire': stagiaire})

#les sujets
def les_sujets(request):
    sujets = Sujet.objects.all()  
    return render(request, 'stagiaire/les_sujets.html', {'sujets': sujets})

#demander stage
def demande_stage(request):
    sujets = Sujet.objects.all()  

    if request.method == 'POST':
        form = StageForm(request.POST, request.FILES)  
        if form.is_valid():
            demande_stage = form.save(commit=False)
            
            stagiaire = get_object_or_404(Stagiaire, user=request.user)
            
            demande_stage.stagiaire = stagiaire
            demande_stage.save()  
            
            return redirect('mes_demandes')  
    else:
        form = StageForm()

    context = {
        'form': form,
        'sujets': sujets,
    }

    return render(request, 'stagiaire/demande_stage.html', context)

def mettre_document(request, demande_id):
    if request.method == 'POST':
        demande = get_object_or_404(Stage, id=demande_id)
        document = request.FILES.get('document')

        if document:
            demande.document = document  
            demande.save()  

    return redirect('demande_stage') 

#mes demandes 
def mes_demandes(request):         
    stagiaire = Stagiaire.objects.get (user = request.user)

    demandes = Stage.objects.filter(stagiaire=stagiaire)  
    for demande in demandes:
        print(f"Demande: {demande}, Stagiaire: {demande.stagiaire.user.nom} {demande.stagiaire.user.prenom}, Email: {demande.stagiaire.user.email}")
    
    context = {
        'demandes': demandes,
    }
    return render(request, 'stagiaire/mes_demandes.html', context)

def mettre_rapport(request, demande_id):
    if request.method == 'POST':
        demande = get_object_or_404(Stage, id=demande_id)
        rapport = request.FILES.get('rapport')

        if rapport:
            demande.rapport = rapport 
            demande.save() 

    return redirect('mes_demandes')  

#profil stagiaire
def profil_stagiaire(request):
    # Récupérer le stagiaire associé à l'utilisateur connecté
    stagiaire = get_object_or_404(Stagiaire, user=request.user)

    encadrant = None
    for demande in stagiaire.demandes.filter(etat='acceptee'):
        encadrant = demande.sujet.encadrant
        break  # On prend le premier encadrant trouvé
    context = {
        'stagiaire': stagiaire,
        'encadrant': encadrant,  
    }

    return render(request, 'stagiaire/profil_stagiaire.html', context)


def modifier_profil_stagiaire(request, stagiaire_id):
    stagiaire = get_object_or_404(Stagiaire, id=stagiaire_id)
    user = stagiaire.user
    
    if request.method == 'POST':
        form = StagiaireForm(request.POST, request.FILES, instance=stagiaire)
        
        if form.is_valid():
            form.save()
            user.save() 
            return redirect('profil_stagiaire')  
    else:
        form = StagiaireForm(instance=stagiaire, initial={
            'nom': user.nom,
            'prenom':user.prenom,
            'email':user.email,
            'telephone': user.telephone,
            'photo': user.photo,
            
            })  # Pré-remplir le formulaire avec les données du stagiaire

    return render(request, 'stagiaire/modifier_profil_stagiaire.html', {'form': form, 'stagiaire': stagiaire})
    

