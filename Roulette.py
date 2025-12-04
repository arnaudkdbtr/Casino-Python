import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import time
from typing import List, Dict, Tuple

class Jeton:
    """Représente un jeton de casino (repris du blackjack)"""
    def __init__(self, valeur: int):
        self.valeur = valeur
        self.x = 0
        self.y = 0
    
    def __str__(self):
        return f"Jeton({self.valeur})"

class Pari:
    """Représente un pari sur la roulette"""
    def __init__(self, type_pari: str, valeur: int, jetons: int, position: Tuple[int, int] = None, valeur_jeton: int = None):
        self.type_pari = type_pari  # 'rouge', 'noir', 'pair', 'impair', 'manque', 'passe', 'nombre'
        self.valeur = valeur  # Valeur du pari (chiffre, couleur, etc.)
        self.jetons = jetons  # Nombre de jetons
        self.position = position  # Position sur la table (x, y)
        self.valeur_jeton = valeur_jeton  # Valeur du jeton (doit être fournie)
        self.montant_total = self.valeur_jeton * jetons

class Roulette:
    """Classe principale du jeu de roulette"""
    
    def __init__(self):
        # Nombres de la roulette européenne (0-36)
        self.nombres = list(range(37))  # 0 à 36
        self.nombres_rouges = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        self.nombres_noirs = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        
        # Solde et paris
        self.solde_joueur = 1000
        self.paris_actuels = []
        self.paris_precedents = []  # Stocke les paris de la partie précédente
        self.numero_gagnant = None
        self.partie_en_cours = False
        
        # Historique des numéros
        self.historique = []
    
    def placer_pari(self, type_pari: str, valeur_pari: int, valeur_jeton: int, position: Tuple[int, int] = None) -> bool:
        """Place un pari. Retourne True si le pari est valide"""
        montant_total = valeur_jeton * 1  # 1 jeton
        
        if montant_total > self.solde_joueur:
            return False
        
        if not self.partie_en_cours:
            return False
        
        # Créer le pari avec la valeur du pari et le montant du jeton
        pari = Pari(type_pari, valeur_pari, 1, position, valeur_jeton)
        self.paris_actuels.append(pari)
        self.solde_joueur -= montant_total
        return True
    
    def lancer_roulette(self) -> int:
        """Lance la roulette et retourne le numéro gagnant"""
        if not self.partie_en_cours:
            return None
        
        self.numero_gagnant = random.choice(self.nombres)
        self.historique.append(self.numero_gagnant)
        
        # Garder seulement les 20 derniers numéros
        if len(self.historique) > 20:
            self.historique = self.historique[-20:]
        
        return self.numero_gagnant
    
    def calculer_gains(self) -> int:
        """Calcule les gains totaux selon les paris et le numéro gagnant"""
        gains_totaux = 0
        
        for pari in self.paris_actuels:
            if self.verifier_pari_gagnant(pari):
                multiplicateur = self.get_multiplicateur(pari.type_pari)
                gains_totaux += pari.montant_total * multiplicateur
        
        return gains_totaux
    
    def verifier_pari_gagnant(self, pari: Pari) -> bool:
        """Vérifie si un pari est gagnant"""
        numero = self.numero_gagnant
        
        if pari.type_pari == 'rouge':
            return numero in self.nombres_rouges
        elif pari.type_pari == 'noir':
            return numero in self.nombres_noirs
        elif pari.type_pari == 'pair':
            return numero != 0 and numero % 2 == 0
        elif pari.type_pari == 'impair':
            return numero != 0 and numero % 2 == 1
        elif pari.type_pari == 'manque':
            return 1 <= numero <= 18
        elif pari.type_pari == 'passe':
            return 19 <= numero <= 36
        elif pari.type_pari == 'nombre':
            return numero == pari.valeur
        elif pari.type_pari == 'douzaine1':
            return 1 <= numero <= 12
        elif pari.type_pari == 'douzaine2':
            return 13 <= numero <= 24
        elif pari.type_pari == 'douzaine3':
            return 25 <= numero <= 36
        elif pari.type_pari == 'colonne1':
            return numero != 0 and numero % 3 == 1
        elif pari.type_pari == 'colonne2':
            return numero != 0 and numero % 3 == 2
        elif pari.type_pari == 'colonne3':
            return numero != 0 and numero % 3 == 0
        
        return False
    
    def get_multiplicateur(self, type_pari: str) -> int:
        """Retourne le multiplicateur de gain selon le type de pari"""
        multiplicateurs = {
            'rouge': 2,
            'noir': 2,
            'pair': 2,
            'impair': 2,
            'manque': 2,
            'passe': 2,
            'nombre': 36,  # Pari sur un nombre spécifique
            'douzaine1': 3,
            'douzaine2': 3,
            'douzaine3': 3,
            'colonne1': 3,
            'colonne2': 3,
            'colonne3': 3
        }
        return multiplicateurs.get(type_pari, 1)
    
    def nouvelle_partie(self):
        """Commence une nouvelle partie"""
        self.paris_actuels = []
        self.numero_gagnant = None
        self.partie_en_cours = True
    
    def terminer_partie(self):
        """Termine la partie actuelle"""
        if self.numero_gagnant is not None:
            gains = self.calculer_gains()
            self.solde_joueur += gains
            # Sauvegarder les paris actuels avant de les effacer
            self.paris_precedents = self.paris_actuels.copy()
            self.paris_actuels = []
            self.partie_en_cours = False
            return gains
        return 0
    
    def repeter_mises_precedentes(self) -> bool:
        """Répète les mises de la partie précédente. Retourne True si succès"""
        if not self.paris_precedents or not self.partie_en_cours:
            return False
        
        # Vérifier si le joueur a assez d'argent pour tous les paris
        montant_total = sum(pari.montant_total for pari in self.paris_precedents)
        if montant_total > self.solde_joueur:
            return False
        
        # Placer tous les paris précédents
        for pari in self.paris_precedents:
            # Calculer la vraie valeur du jeton (montant total / nombre de jetons)
            vraie_valeur_jeton = pari.montant_total // pari.jetons
            if not self.placer_pari(pari.type_pari, pari.valeur, vraie_valeur_jeton, pari.position):
                # Si un pari échoue, annuler tous les paris déjà placés
                for pari_place in self.paris_actuels:
                    self.solde_joueur += pari_place.montant_total
                self.paris_actuels = []
                return False
        
        return True

class InterfaceRoulette:
    """Interface graphique du jeu de roulette"""
    
    def __init__(self):
        self.jeu = Roulette()
        self.root = tk.Tk()
        self.root.title("Roulette Casino")
        self.root.geometry("1000x800")
        self.root.configure(bg='#0d5016')
        self.root.minsize(900, 700)
        
        # Variables pour l'animation
        self.animation_en_cours = False
        self.angle_rotation = 0
        self.angle_final = 0
        self.temps_animation = 0
        
        # Variables pour les jetons
        self.jetons_places = []
        self.jeton_en_cours_deplacement = None
        self.jeton_selectionne = None
        self.paris_visuels = []  # Pour afficher les jetons placés
        
        self.creer_interface()
        self.nouvelle_partie()
    
    def creer_interface(self):
        """Crée l'interface utilisateur"""
        # Titre
        self.titre = tk.Label(self.root, text="🎰 ROULETTE CASINO 🎰", 
                        font=('Arial', 18, 'bold'), 
                        fg='white', bg='#0d5016')
        self.titre.pack(pady=5)
        
        # Frame principal
        frame_principal = tk.Frame(self.root, bg='#0d5016')
        frame_principal.pack(expand=True, fill='both', padx=5, pady=2)
        
        # Frame gauche - Roue de roulette et infos joueur
        frame_gauche = tk.Frame(frame_principal, bg='#0d5016')
        frame_gauche.pack(side=tk.LEFT, fill='y', padx=(0, 5))
        
        # Titre et infos joueur
        frame_info = tk.Frame(frame_gauche, bg='#0d5016')
        frame_info.pack(pady=2)
        
        self.label_solde = tk.Label(frame_info, 
                                  text=f"Solde: {self.jeu.solde_joueur} jetons", 
                                  font=('Arial', 12, 'bold'), 
                                  fg='white', bg='#0d5016')
        self.label_solde.pack()
        
        self.label_mise_totale = tk.Label(frame_info, 
                                        text="Mise totale: 0 jetons", 
                                        font=('Arial', 10), 
                                        fg='white', bg='#0d5016')
        self.label_mise_totale.pack()
        
        # Canvas pour la roue de roulette
        self.canvas_roue = tk.Canvas(frame_gauche, width=300, height=300, 
                                   bg='#2E7D32', highlightthickness=0)
        self.canvas_roue.pack(pady=5)
        
        # Message du numéro qui vient de tomber
        self.label_numero_actuel = tk.Label(frame_gauche, text="", 
                                           font=('Arial', 14, 'bold'), 
                                           fg='#FFD700', bg='#0d5016')
        self.label_numero_actuel.pack(pady=2)
        
        # Titre de l'historique
        label_historique = tk.Label(frame_gauche, text="Historique des numéros :", 
                                   font=('Arial', 10, 'bold'), 
                                   fg='white', bg='#0d5016')
        label_historique.pack(pady=(5, 2))
        
        # Canvas pour l'historique des numéros
        self.canvas_historique = tk.Canvas(frame_gauche, width=280, height=100, 
                                         bg='#1B5E20', highlightthickness=1, 
                                         relief='sunken', bd=1)
        self.canvas_historique.pack(pady=2)
        
        # Zone de récapitulatif des gains/pertes
        label_recap = tk.Label(frame_gauche, text="Récapitulatif :", 
                              font=('Arial', 10, 'bold'), 
                              fg='white', bg='#0d5016')
        label_recap.pack(pady=(5, 2))
        
        # Canvas pour le récapitulatif
        self.canvas_recap = tk.Canvas(frame_gauche, width=280, height=100, 
                                    bg='#1B5E20', highlightthickness=1, 
                                    relief='sunken', bd=1)
        self.canvas_recap.pack(pady=2)
        
        # Frame droite - Table de paris
        frame_droite = tk.Frame(frame_principal, bg='#0d5016')
        frame_droite.pack(side=tk.RIGHT, fill='both', expand=True, padx=(5, 0))
        
        # Table de paris - Zone de mise principale
        self.creer_table_paris(frame_droite)
        
        # Zone des jetons disponibles (en dessous de la table)
        label_jetons = tk.Label(frame_droite, text="Jetons disponibles :", 
                               font=('Arial', 10, 'bold'), 
                               fg='white', bg='#0d5016')
        label_jetons.pack(pady=(5, 2))
        
        self.frame_jetons = tk.Frame(frame_droite, bg='#0d5016')
        self.frame_jetons.pack(pady=2)
        
        # Boutons de contrôle des jetons
        frame_boutons_jetons = tk.Frame(frame_droite, bg='#0d5016')
        frame_boutons_jetons.pack(pady=2)
        
        self.btn_deselectionner = tk.Button(frame_boutons_jetons, text="Désélectionner", 
                                           command=self.deselectionner_jeton,
                                           font=('Arial', 8, 'bold'),
                                           bg='#4CAF50', fg='#000000',
                                           padx=8, pady=3,
                                           relief='raised', bd=2,
                                           activebackground='#66BB6A',
                                           activeforeground='#000000')
        self.btn_deselectionner.pack(side=tk.LEFT, padx=2)
        
        self.btn_reinitialiser = tk.Button(frame_boutons_jetons, text="Réinitialiser mises", 
                                          command=self.reinitialiser_mises,
                                          font=('Arial', 8, 'bold'),
                                          bg='#FFCDD2', fg='#000000',
                                          padx=8, pady=3,
                                          relief='raised', bd=2,
                                          activebackground='#FFE0E0',
                                          activeforeground='#000000')
        self.btn_reinitialiser.pack(side=tk.LEFT, padx=2)
        
        self.btn_repetir = tk.Button(frame_boutons_jetons, text="Répéter la mise", 
                                    command=self.repetir_mises_precedentes,
                                    font=('Arial', 8, 'bold'),
                                    bg='#4CAF50', fg='#000000',
                                    padx=8, pady=3,
                                    relief='raised', bd=2,
                                    activebackground='#66BB6A',
                                    activeforeground='#000000')
        self.btn_repetir.pack(side=tk.LEFT, padx=2)
        
        # Frame pour les contrôles (en bas)
        frame_controles = tk.Frame(self.root, bg='#0d5016')
        frame_controles.pack(fill='x', pady=2)
        
        # Boutons de contrôle
        frame_boutons = tk.Frame(frame_controles, bg='#0d5016')
        frame_boutons.pack(side=tk.RIGHT, padx=5, pady=2)
        
        self.btn_lancer = tk.Button(frame_boutons, text="TOURNER", 
                                  command=self.lancer_roulette,
                                  font=('Arial', 10, 'bold'),
                                  bg='#FF9800', fg='#000000',
                                  padx=10, pady=5,
                                  relief='raised', bd=2,
                                  activebackground='#FFB74D',
                                  activeforeground='#000000')
        self.btn_lancer.pack(side=tk.LEFT, padx=3)
        
        self.btn_nouvelle_partie = tk.Button(frame_boutons, text="RÉINITIALISER", 
                                           command=self.nouvelle_partie,
                                           font=('Arial', 10, 'bold'),
                                           bg='#FFCDD2', fg='#000000',
                                           padx=10, pady=5,
                                           relief='raised', bd=2,
                                           activebackground='#FFE0E0',
                                           activeforeground='#000000')
        self.btn_nouvelle_partie.pack(side=tk.LEFT, padx=3)
        
        # Affichage des résultats
        self.label_resultat = tk.Label(frame_droite, 
                                     text="Placez vos paris !", 
                                     font=('Arial', 10, 'bold'), 
                                     fg='#ffd700', bg='#0d5016')
        self.label_resultat.pack(pady=2)
        
        # Créer les jetons et la roue
        self.creer_jetons_disponibles()
        self.dessiner_roue()
        self.dessiner_historique()
    
    def creer_table_paris(self, parent_frame):
        """Crée la table de paris de roulette complète"""
        # Frame principal de la table
        table_frame = tk.Frame(parent_frame, bg='#0d5016')
        table_frame.pack(fill='both', expand=True, pady=5)
        
        # Canvas pour la table de paris - taille réduite et mieux proportionnée
        self.canvas_table = tk.Canvas(table_frame, width=600, height=400, 
                                    bg='#1B5E20', highlightthickness=0)
        self.canvas_table.pack(expand=True)
        
        # Dessiner la table de paris
        self.dessiner_table_paris()
        
        # Lier les événements de clic
        self.canvas_table.bind('<Button-1>', self.clic_table_paris)
        
    def clic_table_paris(self, event):
        """Gère les clics sur la table de paris"""
        if not self.jeton_selectionne:
            return
        
        x, y = event.x, event.y
        
        # Déterminer le type de pari selon la position
        type_pari, valeur = self.determiner_type_pari(x, y)
        
        if type_pari:
            # Placer le pari
            if self.jeu.placer_pari(type_pari, valeur, self.jeton_selectionne, (x, y)):
                
                # Ajouter le jeton visuel
                self.ajouter_jeton_visuel(x, y, self.jeton_selectionne)
                self.mettre_a_jour_affichage()
                self.creer_jetons_disponibles()
                
                # Calculer le total des paris de ce type
                total_paris_type = sum(pari.montant_total for pari in self.jeu.paris_actuels 
                                     if pari.type_pari == type_pari)
                if type_pari == 'nombre':
                    self.label_resultat.config(text=f"Pari placé: chiffre {valeur} - Total: {total_paris_type} jetons")
                else:
                    self.label_resultat.config(text=f"Pari placé: {type_pari} - Total: {total_paris_type} jetons")
            else:
                self.label_resultat.config(text="❌ Pas assez de jetons !")
        
        # Le jeton reste sélectionné pour permettre de placer plusieurs paris
    
    def deselectionner_jeton(self):
        """Désélectionne le jeton actuel"""
        self.jeton_selectionne = None
        self.label_resultat.config(text="Jeton désélectionné - Sélectionnez un jeton pour parier")
    
    def reinitialiser_mises(self):
        """Supprime seulement les mises (sans changer de partie)"""
        # Empêcher la réinitialisation pendant l'animation
        if self.animation_en_cours:
            self.label_resultat.config(text="❌ Impossible de réinitialiser pendant que la roue tourne !")
            return
        
        # Rembourser tous les paris
        for pari in self.jeu.paris_actuels:
            self.jeu.solde_joueur += pari.montant_total
        
        # Vider la liste des paris
        self.jeu.paris_actuels = []
        
        # Effacer tous les jetons visuels (redessine automatiquement la table)
        self.effacer_paris_visuels()
        
        # Mettre à jour l'affichage
        self.mettre_a_jour_affichage()
        self.creer_jetons_disponibles()
        self.label_resultat.config(text="Mises supprimées - Argent remboursé")
    
    def repetir_mises_precedentes(self):
        """Répète les mises de la partie précédente"""
        # Empêcher la répétition pendant l'animation
        if self.animation_en_cours:
            self.label_resultat.config(text="❌ Impossible de répéter pendant que la roue tourne !")
            return
        
        # Vérifier s'il y a des paris précédents
        if not self.jeu.paris_precedents:
            self.label_resultat.config(text="❌ Aucune mise précédente à répéter !")
            return
        
        # Vérifier si une partie est en cours
        if not self.jeu.partie_en_cours:
            self.label_resultat.config(text="❌ Aucune partie en cours !")
            return
        
        # Vérifier s'il y a déjà des paris actuels
        if self.jeu.paris_actuels:
            self.label_resultat.config(text="❌ Supprimez d'abord les mises actuelles !")
            return
        
        # Essayer de répéter les mises
        if self.jeu.repeter_mises_precedentes():
            # Afficher visuellement les jetons répétés
            self.afficher_paris_visuels()
            self.mettre_a_jour_affichage()
            self.creer_jetons_disponibles()
            
            montant_total = sum(pari.montant_total for pari in self.jeu.paris_actuels)
            self.label_resultat.config(text=f"✅ Mises répétées ! Total: {montant_total} jetons")
        else:
            self.label_resultat.config(text="❌ Pas assez de jetons pour répéter les mises !")
    
    def afficher_paris_visuels(self):
        """Affiche visuellement tous les paris actuels sur la table"""
        # Effacer d'abord tous les paris visuels existants
        self.effacer_paris_visuels()
        
        # Afficher chaque pari
        for pari in self.jeu.paris_actuels:
            if pari.position:
                # Utiliser valeur_jeton si disponible, sinon calculer à partir du montant
                if hasattr(pari, 'valeur_jeton') and pari.valeur_jeton is not None:
                    valeur_afficher = pari.valeur_jeton
                else:
                    valeur_afficher = pari.montant_total // pari.jetons
                self.ajouter_jeton_visuel(pari.position[0], pari.position[1], valeur_afficher)
    
    def regrouper_paris_identiques(self, paris):
        """Regroupe les paris par type, en séparant les chiffres des autres types"""
        paris_groupes = {}
        
        for pari in paris:
            # Pour les paris sur des chiffres, grouper tous les chiffres ensemble
            if pari.type_pari == 'nombre':
                cle = 'nombres'  # Clé unique pour tous les chiffres
            else:
                # Pour les autres types de paris, garder le regroupement par type
                cle = pari.type_pari
            
            if cle not in paris_groupes:
                paris_groupes[cle] = {
                    'type_pari': pari.type_pari,
                    'valeur': pari.valeur if pari.type_pari != 'nombre' else None,
                    'montant_total': 0,
                    'jetons_total': 0,
                    'position': pari.position,
                    'chiffres': set() if pari.type_pari == 'nombre' else None
                }
            
            # Additionner les montants et jetons
            paris_groupes[cle]['montant_total'] += pari.montant_total
            paris_groupes[cle]['jetons_total'] += pari.jetons
            
            # Pour les chiffres, collecter tous les chiffres misés
            if pari.type_pari == 'nombre':
                paris_groupes[cle]['chiffres'].add(pari.valeur)
        
        return list(paris_groupes.values())
    
    def generer_recapitulatif(self, paris_avant_lancer, numero_gagnant):
        """Génère le récapitulatif des gains et pertes"""
        self.canvas_recap.delete("all")
        
        if not paris_avant_lancer:
            self.canvas_recap.create_text(140, 60, text="Aucun pari", 
                                        font=('Arial', 10), fill='#888888')
            return
        
        # Calculer les dimensions
        y_position = 5
        
        # Regrouper les paris identiques
        paris_groupes = self.regrouper_paris_identiques(paris_avant_lancer)
        
        numero_gagnant = self.jeu.numero_gagnant
        ligne_height = 20
        
        for pari_groupe in paris_groupes:
            # Gestion spéciale pour les paris sur des chiffres
            if pari_groupe['type_pari'] == 'nombre':
                # Vérifier si au moins un chiffre est gagnant
                chiffres_gagnants = []
                chiffres_perdants = []
                
                for chiffre in pari_groupe['chiffres']:
                    # Vérifier directement si le chiffre correspond au numéro gagnant
                    est_gagnant = (chiffre == numero_gagnant)
                    if est_gagnant:
                        chiffres_gagnants.append(chiffre)
                    else:
                        chiffres_perdants.append(chiffre)
                
                # Afficher les gains
                if chiffres_gagnants:
                    multiplicateur = self.jeu.get_multiplicateur('nombre')
                    # Calculer le montant gagnant correctement pour chaque chiffre gagnant
                    montant_gagnant = 0
                    for chiffre in chiffres_gagnants:
                        montant_chiffre = sum(pari.montant_total for pari in paris_avant_lancer 
                                            if pari.type_pari == 'nombre' and pari.valeur == chiffre)
                        montant_gagnant += montant_chiffre
                    
                    gain = montant_gagnant * multiplicateur
                    chiffres_str = ','.join(map(str, sorted(chiffres_gagnants)))
                    message = f"✅ Tu as gagné {gain} jetons sur les chiffres {chiffres_str} (mise: {montant_gagnant} x {multiplicateur})"
                    self.canvas_recap.create_text(10, y_position, text=message, 
                                                font=('Arial', 9), fill='#00FF00', anchor='w')
                    y_position += ligne_height
                
                # Afficher les pertes
                if chiffres_perdants:
                    # Calculer le montant perdu correctement pour chaque chiffre perdant
                    montant_perdant = 0
                    for chiffre in chiffres_perdants:
                        montant_chiffre = sum(pari.montant_total for pari in paris_avant_lancer 
                                            if pari.type_pari == 'nombre' and pari.valeur == chiffre)
                        montant_perdant += montant_chiffre
                    
                    chiffres_str = ','.join(map(str, sorted(chiffres_perdants)))
                    message = f"❌ Tu as perdu {montant_perdant} jetons sur les chiffres {chiffres_str}"
                    self.canvas_recap.create_text(10, y_position, text=message, 
                                                font=('Arial', 9), fill='#FF0000', anchor='w')
                    y_position += ligne_height
            else:
                # Gestion normale pour les autres types de paris
                # Calculer la valeur du jeton à partir du montant total et du nombre de jetons
                valeur_jeton = pari_groupe['montant_total'] // pari_groupe['jetons_total']
                pari_temp = Pari(pari_groupe['type_pari'], pari_groupe['valeur'], 
                               pari_groupe['jetons_total'], pari_groupe['position'], valeur_jeton)
                
                # Définir temporairement le numéro gagnant pour la vérification
                self.jeu.numero_gagnant = numero_gagnant
                est_gagnant = self.jeu.verifier_pari_gagnant(pari_temp)
                
                # Formater le nom du pari
                nom_pari = self.formater_nom_pari(pari_temp)
                
                if est_gagnant:
                    multiplicateur = self.jeu.get_multiplicateur(pari_groupe['type_pari'])
                    gain = pari_groupe['montant_total'] * multiplicateur
                    couleur = '#00FF00'  # Vert pour les gains
                    if pari_groupe['jetons_total'] > 1:
                        message = f"✅ Tu as gagné {gain} jetons sur {nom_pari} ({pari_groupe['jetons_total']} jetons)"
                    else:
                        message = f"✅ Tu as gagné {gain} jetons sur {nom_pari}"
                else:
                    couleur = '#FF0000'  # Rouge pour les pertes
                    if pari_groupe['jetons_total'] > 1:
                        message = f"❌ Tu as perdu {pari_groupe['montant_total']} jetons sur {nom_pari} ({pari_groupe['jetons_total']} jetons)"
                    else:
                        message = f"❌ Tu as perdu {pari_groupe['montant_total']} jetons sur {nom_pari}"
                
                # Afficher le message
                self.canvas_recap.create_text(10, y_position, text=message, 
                                            font=('Arial', 9), fill=couleur, anchor='w')
                y_position += ligne_height
            
            # Si on dépasse la hauteur du canvas, arrêter
            if y_position > 85:
                break
    
    def formater_nom_pari(self, pari):
        """Formate le nom du pari pour l'affichage"""
        if pari.type_pari == 'nombre':
            return f"le chiffre {pari.valeur}"
        elif pari.type_pari == 'rouge':
            return "le rouge"
        elif pari.type_pari == 'noir':
            return "le noir"
        elif pari.type_pari == 'pair':
            return "pair"
        elif pari.type_pari == 'impair':
            return "impair"
        elif pari.type_pari == 'manque':
            return "1-18"
        elif pari.type_pari == 'passe':
            return "19-36"
        elif pari.type_pari == 'douzaine1':
            return "1-12"
        elif pari.type_pari == 'douzaine2':
            return "13-24"
        elif pari.type_pari == 'douzaine3':
            return "25-36"
        elif pari.type_pari == 'colonne1':
            return "colonne 1"
        elif pari.type_pari == 'colonne2':
            return "colonne 2"
        elif pari.type_pari == 'colonne3':
            return "colonne 3"
        else:
            return pari.type_pari
    
    def determiner_type_pari(self, x, y):
        """Détermine le type de pari selon la position du clic"""
        # Zone du 0 (largeur de 12 cellules)
        if 50 <= x <= 470 and 50 <= y <= 95:
            return "nombre", 0
        
        # Grille des nombres 1-36 (disposition horizontale : 3 rangées de 12)
        if 50 <= x <= 470 and 95 <= y <= 230:
            col = (x - 50) // 35
            row = (y - 95) // 45
            if 0 <= col <= 11 and 0 <= row <= 2:
                # Organisation traditionnelle de la roulette :
                # Rangée 1: 1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34
                # Rangée 2: 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35  
                # Rangée 3: 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36
                numero = 1 + col * 3 + row
                return "nombre", numero
        
        # Paris simples (en bas, disposition horizontale)
        if 50 <= x <= 590 and 250 <= y <= 310:
            index = (x - 50) // 90
            paris = ["manque", "pair", "rouge", "noir", "impair", "passe"]
            if 0 <= index < len(paris):
                return paris[index], None
        
        # Douzaines (à droite des colonnes "2to1")
        if 470 <= x <= 550 and 95 <= y <= 230:
            index = (y - 95) // 45
            douzaines = ["douzaine1", "douzaine2", "douzaine3"]
            if 0 <= index < len(douzaines):
                return douzaines[index], None
        
        # Colonnes "2to1" (à droite de la grille)
        if 470 <= x <= 530 and 95 <= y <= 230:
            col_index = (y - 95) // 45
            if 0 <= col_index <= 2:
                return f"colonne{col_index + 1}", None
        
        return None, None
    
    def ajouter_jeton_visuel(self, x, y, valeur):
        """Ajoute un jeton visuel sur la table"""
        # Compter les jetons déjà placés à cette position
        jetons_ici = 0
        for pari in self.jeu.paris_actuels:
            if pari.position and abs(pari.position[0] - x) < 20 and abs(pari.position[1] - y) < 20:
                jetons_ici += 1
        
        # Calculer la position du jeton (empilage)
        offset_x = (jetons_ici % 3) * 6 - 6  # 3 jetons par rangée
        offset_y = (jetons_ici // 3) * 6 - 6  # Empilage vertical
        
        # Dessiner un petit cercle pour représenter le jeton
        jeton_id = self.canvas_table.create_oval(x - 8 + offset_x, y - 8 + offset_y, 
                                    x + 8 + offset_x, y + 8 + offset_y, 
                                    fill='#FFD700', outline='#000000', width=2, tags="jeton")
        texte_id = self.canvas_table.create_text(x + offset_x, y + offset_y, text=str(valeur), 
                                    font=('Arial', 6, 'bold'), fill='#000000', tags="jeton")
        
        # Stocker les IDs pour pouvoir les supprimer
        self.paris_visuels.append((jeton_id, texte_id))
    
    def dessiner_table_paris(self):
        """Dessine la table de paris de roulette complète"""
        self.canvas_table.delete("all")
        
        # Dimensions de la table (ajustées au canvas)
        table_width = 600
        table_height = 400
        
        # Dessiner le fond vert de la table
        self.canvas_table.create_rectangle(0, 0, table_width, table_height, 
                                         fill='#1B5E20', outline='#000000', width=2)
        
        # Zone des nombres (grille 3x12 + 0) - en haut à gauche
        self.dessiner_grille_nombres()
        
        # Zone des colonnes (à droite de la grille)
        self.dessiner_colonnes()
        
        # Zone des paris simples (en bas, disposition horizontale)
        self.dessiner_paris_simples()
        
        # Zone des douzaines (en bas, après les paris simples)
        self.dessiner_douzaines()
    
    def dessiner_grille_nombres(self):
        """Dessine la grille des nombres 1-36 + 0 en disposition horizontale"""
        # Position de la grille (centrée et plus grande)
        start_x = 50
        start_y = 50
        cell_width = 35  # Plus larges pour une meilleure visibilité
        cell_height = 45  # Plus hautes pour une meilleure visibilité
        
        # Dessiner le 0 (en haut, largeur de 12 cellules)
        zero_x = start_x
        zero_y = start_y
        zero_width = 12 * cell_width  # Largeur de 12 cellules
        self.canvas_table.create_rectangle(zero_x, zero_y, zero_x + zero_width, zero_y + cell_height,
                                         fill='#00AA00', outline='#000000', width=1)
        self.canvas_table.create_text(zero_x + zero_width//2, zero_y + cell_height//2, 
                                    text="0", font=('Arial', 14, 'bold'), fill='white')
        
        # Dessiner la grille 3x12 des nombres 1-36 (disposition horizontale)
        nombres_rouges = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        
        # Organisation traditionnelle des rangées de roulette :
        # Rangée 1: 1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34
        # Rangée 2: 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35  
        # Rangée 3: 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36
        for row in range(3):
            for col in range(12):
                numero = 1 + col * 3 + row  # Calcul pour l'organisation traditionnelle
                x = start_x + col * cell_width
                y = start_y + cell_height + row * cell_height  # Commencer directement après le 0
                
                # Couleur selon le numéro
                if numero in nombres_rouges:
                    couleur = '#FF0000'  # Rouge
                else:
                    couleur = '#000000'  # Noir
                
                # Dessiner la cellule
                self.canvas_table.create_rectangle(x, y, x + cell_width, y + cell_height,
                                                 fill=couleur, outline='#000000', width=1)
                
                # Texte du numéro
                couleur_texte = 'white' if couleur == '#000000' else 'white'
                self.canvas_table.create_text(x + cell_width//2, y + cell_height//2, 
                                            text=str(numero), font=('Arial', 12, 'bold'), 
                                            fill=couleur_texte)
    
    
    def dessiner_paris_simples(self):
        """Dessine les zones de paris simples (rouge, noir, pair, impair, etc.)"""
        start_x = 50  # Centré avec la grille
        start_y = 250  # En bas de la grille des nombres
        cell_width = 90  # Plus larges
        cell_height = 60  # Plus hautes
        
        # Paris simples
        paris = [
            ("1-18", "manque"),
            ("Even", "pair"),
            ("Red", "rouge"),
            ("Black", "noir"),
            ("Odd", "impair"),
            ("19-36", "passe")
        ]
        
        for i, (texte, type_pari) in enumerate(paris):
            x = start_x + i * cell_width
            y = start_y
            
            # Couleur de fond selon le type
            if type_pari == "rouge":
                couleur_fond = '#FF0000'
            elif type_pari == "noir":
                couleur_fond = '#000000'
            else:
                couleur_fond = '#2E7D32'
            
            # Dessiner la zone de pari
            self.canvas_table.create_rectangle(x, y, x + cell_width, y + cell_height,
                                             fill=couleur_fond, outline='#000000', width=1)
            
            # Texte
            couleur_texte = 'white'
            self.canvas_table.create_text(x + cell_width//2, y + cell_height//2, 
                                        text=texte, font=('Arial', 14, 'bold'), 
                                        fill=couleur_texte)
    
    def dessiner_douzaines(self):
        """Dessine les zones de paris sur douzaines"""
        start_x = 470  # À droite des colonnes "2to1" (50 + 12*35 = 470)
        start_y = 95   # Alignées avec les colonnes (50 + 45 = 95)
        cell_width = 80  # Plus larges
        cell_height = 45  # Plus hautes
        
        douzaines = [
            ("1-12", "douzaine1"),
            ("13-24", "douzaine2"),
            ("25-36", "douzaine3")
        ]
        
        for i, (texte, type_pari) in enumerate(douzaines):
            x = start_x
            y = start_y + i * cell_height  # Verticalement alignées
            
            # Dessiner la zone de pari
            self.canvas_table.create_rectangle(x, y, x + cell_width, y + cell_height,
                                             fill='#2E7D32', outline='#000000', width=1)
            
            # Texte
            self.canvas_table.create_text(x + cell_width//2, y + cell_height//2, 
                                        text=texte, font=('Arial', 12, 'bold'), 
                                        fill='white')
    
    def dessiner_colonnes(self):
        """Dessine les zones de paris sur colonnes"""
        start_x = 470  # À droite de la grille des nombres (50 + 12*35 = 470)
        start_y = 95  # Commencer après le 0 (50 + 45 = 95)
        cell_width = 60  # Plus larges
        cell_height = 45  # Plus hautes
        
        # 3 colonnes "2to1" - une pour chaque rangée
        for col in range(3):
            x = start_x
            y = start_y + col * cell_height  # Une par rangée
            
            # Dessiner la zone de pari (hauteur d'une rangée)
            self.canvas_table.create_rectangle(x, y, x + cell_width, y + cell_height,
                                             fill='#2E7D32', outline='#000000', width=1)
            
            # Texte "2to1" centré
            self.canvas_table.create_text(x + cell_width//2, y + cell_height//2, 
                                        text="2to1", font=('Arial', 12, 'bold'), 
                                        fill='white')
    
    def creer_jetons_disponibles(self):
        """Crée les jetons disponibles (repris du blackjack)"""
        # Effacer les jetons existants
        for widget in self.frame_jetons.winfo_children():
            widget.destroy()
        
        # Créer des jetons de différentes valeurs
        valeurs_jetons = [5, 10, 25, 50, 100, 500]
        
        # Designs des jetons (même que le blackjack)
        designs_jetons = {
            5: {'couleur_centre': '#FFFFFF', 'couleur_inner': '#4A90E2', 'couleur_outer': '#E8F4FD', 'couleur_texte': '#000000', 'couleur_texte_inner': '#FFFFFF'},
            10: {'couleur_centre': '#FFD700', 'couleur_inner': '#DC143C', 'couleur_outer': '#FFF8DC', 'couleur_texte': '#000000', 'couleur_texte_inner': '#FFFFFF'},
            25: {'couleur_centre': '#32CD32', 'couleur_inner': '#87CEEB', 'couleur_outer': '#F0FFF0', 'couleur_texte': '#000000', 'couleur_texte_inner': '#000000'},
            50: {'couleur_centre': '#4169E1', 'couleur_inner': '#DC143C', 'couleur_outer': '#E6F3FF', 'couleur_texte': '#FFFFFF', 'couleur_texte_inner': '#FFFFFF'},
            100: {'couleur_centre': '#000000', 'couleur_inner': '#FFD700', 'couleur_outer': '#F5F5F5', 'couleur_texte': '#FFFFFF', 'couleur_texte_inner': '#000000'},
            500: {'couleur_centre': '#191970', 'couleur_inner': '#FFFFFF', 'couleur_outer': '#E6F3FF', 'couleur_texte': '#FFFFFF', 'couleur_texte_inner': '#000000'}
        }
        
        for valeur in valeurs_jetons:
            if self.jeu.solde_joueur >= valeur:
                quantite_max = self.jeu.solde_joueur // valeur
                
                design = designs_jetons[valeur]
                
                # Créer un canvas pour le jeton
                canvas = tk.Canvas(self.frame_jetons, 
                                 width=60, height=60,
                                 bg='#0d5016', highlightthickness=0)
                canvas.pack(side=tk.LEFT, padx=3, pady=3)
                
                # Dessiner le jeton
                self.dessiner_jeton(canvas, valeur, design, quantite_max)
                
                # Lier les événements de drag & drop
                canvas.bind('<Button-1>', lambda e, v=valeur: self.commencer_deplacement(e, v))
                canvas.bind('<B1-Motion>', self.deplacer_jeton)
                canvas.bind('<ButtonRelease-1>', self.terminer_deplacement)
    
    def dessiner_jeton(self, canvas, valeur, design, quantite_max):
        """Dessine un jeton réaliste"""
        # Cercle extérieur
        canvas.create_oval(5, 5, 55, 55, 
                          fill=design['couleur_outer'], 
                          outline='#C0C0C0', width=2)
        
        # Cercle intérieur
        canvas.create_oval(10, 10, 50, 50, 
                          fill=design['couleur_inner'], 
                          outline='#A0A0A0', width=1)
        
        # Cercle central
        canvas.create_oval(18, 18, 42, 42, 
                          fill=design['couleur_centre'], 
                          outline='#808080', width=1)
        
        # Texte de la valeur
        canvas.create_text(30, 30, text=f"${valeur}", 
                          font=('Arial', 8, 'bold'),
                          fill=design['couleur_texte'])
        
        # Texte "CASINO"
        canvas.create_text(30, 20, text="CASINO", 
                          font=('Arial', 4, 'bold'),
                          fill=design['couleur_texte_inner'])
        
        # Texte "POKER"
        canvas.create_text(30, 40, text="POKER", 
                          font=('Arial', 4, 'bold'),
                          fill=design['couleur_texte_inner'])
        
        # Indicateur de quantité
        if quantite_max > 1:
            canvas.create_text(30, 50, text=f"max {quantite_max}", 
                              font=('Arial', 3),
                              fill='#666666')
    
    def dessiner_roue(self):
        """Dessine la roue de roulette réaliste"""
        self.canvas_roue.delete("all")
        
        # Centre de la roue
        centre_x, centre_y = 150, 150
        rayon_exterieur = 120
        rayon_interieur = 40
        
        # Dessiner le cercle extérieur (fond vert foncé)
        self.canvas_roue.create_oval(centre_x - rayon_exterieur, centre_y - rayon_exterieur, 
                                   centre_x + rayon_exterieur, centre_y + rayon_exterieur,
                                   fill='#1B5E20', outline='#000000', width=2)
        
        # Disposition réelle des numéros sur une roulette européenne (dans l'ordre)
        numeros_ordre = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
        
        # Dessiner les secteurs
        angle_par_secteur = 360 / 37  # 37 secteurs (0-36)
        
        for i, numero in enumerate(numeros_ordre):
            angle_debut = i * angle_par_secteur
            angle_fin = (i + 1) * angle_par_secteur
            
            # Couleur du secteur selon la roulette européenne
            if numero == 0:
                couleur = '#00AA00'  # Vert pour le 0
            elif numero in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
                couleur = '#CC0000'  # Rouge
            else:
                couleur = '#000000'  # Noir
            
            # Dessiner le secteur
            self.dessiner_secteur_realiste(centre_x, centre_y, rayon_exterieur - 5, rayon_interieur + 5, 
                                angle_debut, angle_fin, couleur, numero)
        
        # Dessiner le centre (cercle blanc)
        self.canvas_roue.create_oval(centre_x - rayon_interieur, centre_y - rayon_interieur, 
                                   centre_x + rayon_interieur, centre_y + rayon_interieur,
                                   fill='#FFFFFF', outline='#000000', width=2)
        
        # Dessiner la boule (au lieu de la flèche)
        self.dessiner_boule(centre_x, centre_y)
    
    def dessiner_historique(self):
        """Dessine l'historique des numéros tombés"""
        self.canvas_historique.delete("all")
        
        if not self.jeu.historique:
            # Afficher un message si aucun historique
            self.canvas_historique.create_text(140, 50, text="Aucun numéro encore", 
                                             font=('Arial', 10), fill='#888888')
            return
        
        # Afficher les 12 derniers numéros (2 rangées de 6)
        derniers_numeros = self.jeu.historique[-12:] if len(self.jeu.historique) >= 12 else self.jeu.historique
        
        # Dimensions des cellules
        cell_width = 40
        cell_height = 30
        start_x = 10
        start_y = 10
        
        for i, numero in enumerate(derniers_numeros):
            # Calculer la position (2 rangées de 6)
            row = i // 6
            col = i % 6
            
            x = start_x + col * cell_width
            y = start_y + row * cell_height
            
            # Couleur selon le numéro
            if numero == 0:
                couleur = '#00AA00'  # Vert
                couleur_texte = 'white'
            elif numero in self.jeu.nombres_rouges:
                couleur = '#CC0000'  # Rouge
                couleur_texte = 'white'
            else:
                couleur = '#000000'  # Noir
                couleur_texte = 'white'
            
            # Dessiner la cellule
            self.canvas_historique.create_rectangle(x, y, x + cell_width, y + cell_height,
                                                 fill=couleur, outline='#000000', width=1)
            
            # Dessiner le numéro
            self.canvas_historique.create_text(x + cell_width//2, y + cell_height//2, 
                                             text=str(numero), font=('Arial', 10, 'bold'), 
                                             fill=couleur_texte)
    
    def dessiner_secteur_realiste(self, centre_x, centre_y, rayon_exterieur, rayon_interieur, angle_debut, angle_fin, couleur, numero):
        """Dessine un secteur réaliste de la roue"""
        # Convertir les angles en radians
        angle_debut_rad = math.radians(angle_debut)
        angle_fin_rad = math.radians(angle_fin)
        
        # Points du secteur (forme de trapèze)
        points = []
        
        # Point intérieur de début
        x1 = centre_x + rayon_interieur * math.cos(angle_debut_rad)
        y1 = centre_y + rayon_interieur * math.sin(angle_debut_rad)
        points.extend([x1, y1])
        
        # Point extérieur de début
        x2 = centre_x + rayon_exterieur * math.cos(angle_debut_rad)
        y2 = centre_y + rayon_exterieur * math.sin(angle_debut_rad)
        points.extend([x2, y2])
        
        # Arc extérieur
        for angle in range(int(angle_debut), int(angle_fin) + 1):
            angle_rad = math.radians(angle)
            x = centre_x + rayon_exterieur * math.cos(angle_rad)
            y = centre_y + rayon_exterieur * math.sin(angle_rad)
            points.extend([x, y])
        
        # Point extérieur de fin
        x3 = centre_x + rayon_exterieur * math.cos(angle_fin_rad)
        y3 = centre_y + rayon_exterieur * math.sin(angle_fin_rad)
        points.extend([x3, y3])
        
        # Point intérieur de fin
        x4 = centre_x + rayon_interieur * math.cos(angle_fin_rad)
        y4 = centre_y + rayon_interieur * math.sin(angle_fin_rad)
        points.extend([x4, y4])
        
        # Dessiner le secteur
        self.canvas_roue.create_polygon(points, fill=couleur, outline='#000000', width=1)
        
        # Dessiner le numéro
        angle_milieu = (angle_debut + angle_fin) / 2
        angle_milieu_rad = math.radians(angle_milieu)
        rayon_texte = (rayon_exterieur + rayon_interieur) / 2
        x_num = centre_x + rayon_texte * math.cos(angle_milieu_rad)
        y_num = centre_y + rayon_texte * math.sin(angle_milieu_rad)
        
        couleur_texte = '#FFFFFF'
        self.canvas_roue.create_text(x_num, y_num, text=str(numero), 
                                   font=('Arial', 8, 'bold'),
                                   fill=couleur_texte)
    
    def dessiner_boule(self, centre_x, centre_y):
        """Dessine la boule de roulette"""
        # Position de la boule (au centre pour commencer)
        self.boule_x = centre_x
        self.boule_y = centre_y
        
        # Dessiner la boule (cercle blanc avec bordure)
        self.canvas_roue.create_oval(self.boule_x - 6, self.boule_y - 6, 
                                   self.boule_x + 6, self.boule_y + 6,
                                   fill='#FFFFFF', outline='#000000', width=1, tags="boule")
    
    def dessiner_secteur(self, centre_x, centre_y, rayon, angle_debut, angle_fin, couleur, numero):
        """Dessine un secteur de la roue"""
        # Convertir les angles en radians
        angle_debut_rad = math.radians(angle_debut)
        angle_fin_rad = math.radians(angle_fin)
        
        # Points du secteur
        points = [centre_x, centre_y]
        
        # Point de début
        x1 = centre_x + rayon * math.cos(angle_debut_rad)
        y1 = centre_y + rayon * math.sin(angle_debut_rad)
        points.extend([x1, y1])
        
        # Arc du secteur
        for angle in range(int(angle_debut), int(angle_fin) + 1):
            angle_rad = math.radians(angle)
            x = centre_x + rayon * math.cos(angle_rad)
            y = centre_y + rayon * math.sin(angle_rad)
            points.extend([x, y])
        
        # Point de fin
        x2 = centre_x + rayon * math.cos(angle_fin_rad)
        y2 = centre_y + rayon * math.sin(angle_fin_rad)
        points.extend([x2, y2])
        
        # Dessiner le secteur
        self.canvas_roue.create_polygon(points, fill=couleur, outline='#000000', width=1)
        
        # Dessiner le numéro
        angle_milieu = (angle_debut + angle_fin) / 2
        angle_milieu_rad = math.radians(angle_milieu)
        x_num = centre_x + (rayon - 40) * math.cos(angle_milieu_rad)
        y_num = centre_y + (rayon - 40) * math.sin(angle_milieu_rad)
        
        couleur_texte = '#FFFFFF' if couleur == '#000000' else '#000000'
        self.canvas_roue.create_text(x_num, y_num, text=str(numero), 
                                   font=('Arial', 10, 'bold'),
                                   fill=couleur_texte)
    
    
    def commencer_deplacement(self, event, valeur):
        """Commence le déplacement d'un jeton"""
        self.jeton_selectionne = valeur
        if hasattr(event.widget, 'configure'):
            try:
                event.widget.configure(bg='#FFD700')
            except:
                pass
        self.label_resultat.config(text=f"Jeton {valeur} sélectionné - Cliquez sur la table pour parier (reste sélectionné)")
    
    def deplacer_jeton(self, event):
        """Déplace le jeton pendant le drag"""
        if self.jeton_selectionne:
            pass  # Pas d'animation nécessaire
    
    def terminer_deplacement(self, event):
        """Termine le déplacement d'un jeton"""
        if self.jeton_selectionne:
            # Remettre le jeton en place visuellement
            if hasattr(event.widget, 'configure'):
                try:
                    event.widget.configure(bg='#0d5016')
                except:
                    pass
            # Le jeton reste sélectionné pour le prochain clic sur la table
    
    def mettre_a_jour_affichage(self):
        """Met à jour l'affichage"""
        self.label_solde.config(text=f"Solde: {self.jeu.solde_joueur} jetons")
        
        # Gérer l'état du bouton "Répéter la mise"
        if (self.jeu.paris_precedents and 
            self.jeu.partie_en_cours and 
            not self.jeu.paris_actuels and 
            not self.animation_en_cours):
            self.btn_repetir.config(state=tk.NORMAL)
        else:
            self.btn_repetir.config(state=tk.DISABLED)
        
        # Afficher les paris actuels
        if self.jeu.paris_actuels:
            total_paris = sum(pari.montant_total for pari in self.jeu.paris_actuels)
            self.label_mise_totale.config(text=f"Mise totale: {total_paris} jetons")
            self.label_resultat.config(text=f"Pari total: {total_paris} jetons\nPrêt à lancer !")
        else:
            self.label_mise_totale.config(text="Mise totale: 0 jetons")
            self.label_resultat.config(text="Placez vos paris !")
    
    def lancer_roulette(self):
        """Lance la roulette avec animation"""
        if not self.jeu.partie_en_cours:
            self.label_resultat.config(text="❌ Aucune partie en cours !")
            return
            
        if not self.jeu.paris_actuels:
            self.label_resultat.config(text="❌ Placez des paris avant de lancer !")
            return
        
        if self.animation_en_cours:
            return
        
        self.animation_en_cours = True
        self.btn_lancer.config(state=tk.DISABLED)
        self.btn_repetir.config(state=tk.DISABLED)
        
        # Calculer un angle final aléatoire (sans choisir le numéro à l'avance)
        tours_extra = random.uniform(3, 6) * 360
        angle_aleatoire = random.uniform(0, 360)
        self.angle_final = tours_extra + angle_aleatoire
        
        self.temps_animation = 0
        
        # Lancer l'animation
        self.animer_roue()
    
    def animer_roue(self):
        """Anime la rotation de la boule"""
        if self.temps_animation == 0:
            # Dessiner la roue une seule fois au début
            self.dessiner_roue()
        
        if self.temps_animation < 100:  # 100 frames d'animation
            # Calculer l'angle actuel avec easing
            progress = self.temps_animation / 100.0
            ease_progress = 1 - (1 - progress) ** 3  # Easing out cubic
            
            angle_actuel = self.angle_final * ease_progress
            
            # Faire tourner la boule autour de la roue
            self.animer_boule(angle_actuel)
            
            self.temps_animation += 1
            self.root.after(50, self.animer_roue)  # 20 FPS
        else:
            # Animation terminée
            self.finir_lancer()
    
    def animer_boule(self, angle):
        """Anime la boule qui tourne autour de la roue"""
        centre_x, centre_y = 150, 150
        
        # Calculer le rayon de l'orbite (la boule se rapproche du centre en ralentissant)
        progress = self.temps_animation / 100.0
        
        # Utiliser l'angle calculé normalement pour toute l'animation
        angle_rad = math.radians(angle)
        
        # Calculer le rayon d'orbite avec ralentissement progressif
        if progress < 0.7:
            # Phase de ralentissement normal
            rayon_orbite = 80 * (1 - progress * 0.3)
        elif progress < 0.9:
            # Phase de ralentissement plus prononcé
            phase_ralentissement = (progress - 0.7) / 0.2
            rayon_orbite = 80 * 0.7 * (1 - phase_ralentissement * 0.5)
        else:
            # Phase finale : position finale dans le secteur
            phase_finale = (progress - 0.9) / 0.1
            rayon_orbite = 80 * 0.7 * 0.5 + (20 * (1 - phase_finale))  # Entre 28 et 48 pixels du centre
        
        # Calculer la position de la boule
        self.boule_x = centre_x + rayon_orbite * math.cos(angle_rad)
        self.boule_y = centre_y + rayon_orbite * math.sin(angle_rad)
        
        # Effacer seulement la boule précédente
        self.canvas_roue.delete("boule")
        
        # Dessiner la nouvelle position de la boule
        self.canvas_roue.create_oval(self.boule_x - 6, self.boule_y - 6, 
                                   self.boule_x + 6, self.boule_y + 6,
                                   fill='#FFFFFF', outline='#000000', width=1, tags="boule")
    
    
    def finir_lancer(self):
        """Termine le lancement de la roulette"""
        # Sauvegarder les paris avant de les effacer pour le récapitulatif
        paris_avant_lancer = self.jeu.paris_actuels.copy()
        
        # Déterminer le numéro gagnant basé sur l'angle final réel
        angle_final_reel = self.angle_final % 360  # Normaliser l'angle entre 0 et 360
        
        # Disposition réelle des numéros sur une roulette européenne
        numeros_ordre = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
        
        # Calculer quel secteur correspond à l'angle final
        angle_par_secteur = 360 / 37
        index_secteur = int(angle_final_reel / angle_par_secteur)
        
        # S'assurer que l'index est dans la plage valide
        if index_secteur >= len(numeros_ordre):
            index_secteur = len(numeros_ordre) - 1
        
        numero_gagnant = numeros_ordre[index_secteur]
        
        # Définir le numéro gagnant dans le jeu
        self.jeu.numero_gagnant = numero_gagnant
        
        # Ajouter le numéro à l'historique
        self.jeu.historique.append(numero_gagnant)
        
        # Garder seulement les 20 derniers numéros
        if len(self.jeu.historique) > 20:
            self.jeu.historique = self.jeu.historique[-20:]
        
        # Calculer les gains et terminer la partie
        gains = self.jeu.terminer_partie()
        
        # Afficher le numéro qui vient de tomber
        couleur_numero = "rouge" if numero_gagnant in self.jeu.nombres_rouges else "noir" if numero_gagnant in self.jeu.nombres_noirs else "vert"
        self.label_numero_actuel.config(text=f"🎯 Numéro tombé: {numero_gagnant} ({couleur_numero})")
        
        # Afficher le résultat
        if gains > 0:
            self.label_resultat.config(text=f"🎉 Gains totaux: {gains} jetons !")
        else:
            self.label_resultat.config(text=f"😞 Aucun gain...")
        
        # Générer le récapitulatif des gains/pertes
        self.generer_recapitulatif(paris_avant_lancer, numero_gagnant)
        
        # Réactiver le bouton et arrêter l'animation
        self.btn_lancer.config(state=tk.NORMAL)
        self.animation_en_cours = False
        
        # Effacer tous les paris visuels de la table
        self.effacer_paris_visuels()
        
        # Commencer une nouvelle partie
        self.jeu.nouvelle_partie()
        
        # Mettre à jour l'affichage (après nouvelle_partie pour que partie_en_cours soit True)
        self.mettre_a_jour_affichage()
        self.dessiner_historique()  # Mettre à jour l'historique visuel
        self.creer_jetons_disponibles()
    
    
    def nouvelle_partie(self):
        """Commence une nouvelle partie complète"""
        # Empêcher la réinitialisation pendant l'animation
        if self.animation_en_cours:
            self.label_resultat.config(text="❌ Impossible de réinitialiser pendant que la roue tourne !")
            return
        
        # Rembourser tous les paris avant de commencer une nouvelle partie
        for pari in self.jeu.paris_actuels:
            self.jeu.solde_joueur += pari.montant_total
        
        # Si le joueur n'a plus d'argent, redémarrer avec 1000 jetons
        if self.jeu.solde_joueur <= 0:
            self.label_resultat.config(text="💸 Vous n'avez plus de jetons !\nRedémarrage avec 1000 jetons.")
            self.jeu.solde_joueur = 1000
        
        # Commencer une nouvelle partie
        self.jeu.nouvelle_partie()
        self.jetons_places = []
        self.jeton_selectionne = None
        self.effacer_paris_visuels()
        self.mettre_a_jour_affichage()
        self.creer_jetons_disponibles()
        self.label_resultat.config(text="Sélectionnez un jeton et cliquez sur la table pour parier !")
    
    def effacer_paris_visuels(self):
        """Efface tous les paris visuels de la table"""
        if hasattr(self, 'canvas_table'):
            # Méthode plus robuste : supprimer tous les éléments avec le tag "jeton"
            self.canvas_table.delete("jeton")
            self.canvas_table.delete("total")
            
            # Supprimer aussi les jetons stockés individuellement
            for jeton_id, texte_id in self.paris_visuels:
                try:
                    self.canvas_table.delete(jeton_id)
                    self.canvas_table.delete(texte_id)
                except:
                    pass  # Ignorer les erreurs si l'élément n'existe plus
        self.paris_visuels = []
        
        # Redessiner la table propre
        self.dessiner_table_paris()
    
    def lancer(self):
        """Lance l'interface du jeu"""
        self.root.mainloop()

if __name__ == "__main__":
    jeu = InterfaceRoulette()
    jeu.lancer()
