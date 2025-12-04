import tkinter as tk
from tkinter import ttk, messagebox
import random
from typing import List, Tuple

class Carte:
    """Représente une carte à jouer"""
    def __init__(self, valeur: str, couleur: str):
        self.valeur = valeur
        self.couleur = couleur
        self.face_cachee = False
    
    def get_valeur(self) -> int:
        """Retourne la valeur numérique de la carte"""
        if self.valeur in ['J', 'Q', 'K']:
            return 10
        elif self.valeur == 'A':
            return 11  # L'as vaut 11 par défaut, sera ajusté si nécessaire
        else:
            return int(self.valeur)
    
    def __str__(self) -> str:
        if self.face_cachee:
            return "🂠"
        return f"{self.valeur}{self.couleur}"
    
    def afficher_carte(self) -> str:
        """Retourne une représentation visuelle de la carte"""
        if self.face_cachee:
            return "┌─────┐\n│ ░░░ │\n│░░░░░│\n│ ░░░ │\n└─────┘"
        
        # Nouvelle approche avec caractères simples
        valeur = self.valeur
        symbole = self.couleur
        
        # Créer les lignes une par une pour un contrôle parfait
        ligne1 = "┌─────┐"
        ligne2 = f"│{valeur:>2}   │" if len(valeur) == 1 else f"│{valeur}  │"
        ligne3 = f"│  {symbole}  │"
        ligne4 = f"│   {valeur:<2}│" if len(valeur) == 1 else f"│  {valeur}│"
        ligne5 = "└─────┘"
        
        return f"{ligne1}\n{ligne2}\n{ligne3}\n{ligne4}\n{ligne5}"

class JeuBlackjack:
    """Classe principale du jeu de blackjack"""
    
    def __init__(self):
        self.nombre_paquets = 6  # 6 paquets comme dans la plupart des casinos
        self.jeu_cartes = self.creer_jeu()
        self.main_joueur = []
        self.main_croupier = []
        self.points_joueur = 0
        self.points_croupier = 0
        self.jeu_termine = False
        self.solde_joueur = 1000  # Solde initial de 1000 jetons
        self.mise_actuelle = 0
        self.mise_placee = False
        self.double_effectue = False  # Indique si le joueur a doublé
        self.point_coupure = int(len(self.jeu_cartes) * 0.1)  # Coupure à 10% du jeu
    
    def creer_jeu(self) -> List[Carte]:
        """Crée un jeu avec plusieurs paquets de 52 cartes"""
        valeurs = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        couleurs = ['♠', '♥', '♦', '♣']
        jeu = []
        
        # Créer plusieurs paquets de cartes
        for _ in range(self.nombre_paquets):
            for couleur in couleurs:
                for valeur in valeurs:
                    jeu.append(Carte(valeur, couleur))
        
        return jeu
    
    def melanger_jeu(self):
        """Mélange le jeu de cartes"""
        random.shuffle(self.jeu_cartes)
    
    def distribuer_carte(self, main: List[Carte], face_cachee: bool = False) -> Carte:
        """Distribue une carte à une main"""
        # Vérifier si on doit remélanger (point de coupure atteint)
        if len(self.jeu_cartes) <= self.point_coupure:
            self.jeu_cartes = self.creer_jeu()
            self.melanger_jeu()
            self.point_coupure = int(len(self.jeu_cartes) * 0.1)
        
        carte = self.jeu_cartes.pop()
        carte.face_cachee = face_cachee
        main.append(carte)
        return carte
    
    def calculer_points(self, main: List[Carte]) -> int:
        """Calcule les points d'une main en gérant les as"""
        points = 0
        as_count = 0
        
        for carte in main:
            if carte.valeur == 'A':
                as_count += 1
                points += 11
            else:
                points += carte.get_valeur()
        
        # Ajuster les as si nécessaire (11 -> 1)
        while points > 21 and as_count > 0:
            points -= 10
            as_count -= 1
        
        return points
    
    def nouvelle_partie(self):
        """Commence une nouvelle partie"""
        # Ne pas recréer le jeu de cartes - utiliser celui existant
        # Le jeu sera automatiquement remélangé quand il ne restera que 10% des cartes
        self.main_joueur = []
        self.main_croupier = []
        self.jeu_termine = False
        self.mise_actuelle = 0
        self.mise_placee = False
        self.double_effectue = False
        
        # Distribuer les cartes initiales
        self.distribuer_carte(self.main_joueur)
        self.distribuer_carte(self.main_croupier, face_cachee=True)  # Carte cachée du croupier
        self.distribuer_carte(self.main_joueur)
        self.distribuer_carte(self.main_croupier)
        
        self.points_joueur = self.calculer_points(self.main_joueur)
        self.points_croupier = self.calculer_points(self.main_croupier)
    
    def placer_mise(self, montant: int) -> bool:
        """Place une mise. Retourne True si la mise est valide"""
        if montant <= 0 or montant > self.solde_joueur:
            return False
        
        self.mise_actuelle = montant
        self.solde_joueur -= montant
        self.mise_placee = True
        return True
    
    def calculer_gains(self) -> int:
        """Calcule les gains selon les règles du blackjack"""
        if self.points_joueur > 21:
            return 0  # Le joueur a perdu
        
        # Vérifier d'abord si le joueur a un blackjack (21 en 2 cartes)
        joueur_blackjack = self.points_joueur == 21 and len(self.main_joueur) == 2
        croupier_blackjack = self.points_croupier == 21 and len(self.main_croupier) == 2
        
        if joueur_blackjack:
            if croupier_blackjack:
                return self.mise_actuelle  # Égalité de blackjack, la mise est rendue
            else:
                return int(self.mise_actuelle * 2.5)  # Blackjack du joueur gagne 3:2
        
        if self.points_croupier > 21:
            return self.mise_actuelle * 2  # Le joueur gagne 1:1
        
        if self.points_joueur > self.points_croupier:
            return self.mise_actuelle * 2  # Le joueur gagne 1:1
        
        if self.points_joueur == self.points_croupier:
            return self.mise_actuelle  # Égalité, la mise est rendue
        
        return 0  # Le croupier gagne
    
    def finaliser_partie(self):
        """Finalise la partie et met à jour le solde"""
        if self.mise_placee:
            gains = self.calculer_gains()
            self.solde_joueur += gains
            self.mise_actuelle = 0
            self.mise_placee = False
            return gains
        return 0
    
    def joueur_tire(self) -> bool:
        """Le joueur tire une carte. Retourne True si le jeu continue"""
        if self.jeu_termine:
            return False
        
        self.distribuer_carte(self.main_joueur)
        self.points_joueur = self.calculer_points(self.main_joueur)
        
        if self.points_joueur > 21:
            self.jeu_termine = True
            return False
        
        return True
    
    def doubler_mise(self) -> bool:
        """Le joueur double sa mise et tire une seule carte. Retourne True si possible"""
        if self.jeu_termine or self.double_effectue or len(self.main_joueur) != 2:
            return False
        
        # Vérifier si le joueur a assez de jetons pour doubler
        if self.solde_joueur < self.mise_actuelle:
            return False
        
        # Doubler la mise
        self.solde_joueur -= self.mise_actuelle
        self.mise_actuelle *= 2
        self.double_effectue = True
        
        # Tirer une seule carte
        self.distribuer_carte(self.main_joueur)
        self.points_joueur = self.calculer_points(self.main_joueur)
        
        # Ne pas marquer la partie comme terminée ici, laisser le croupier jouer
        return True
    
    def croupier_joue(self):
        """Le croupier joue selon les règles du blackjack"""
        if self.jeu_termine:
            return
        
        # Retourner la carte cachée
        if self.main_croupier:
            self.main_croupier[0].face_cachee = False
        
        # Le croupier tire jusqu'à avoir au moins 17
        while self.points_croupier < 17:
            self.distribuer_carte(self.main_croupier)
            self.points_croupier = self.calculer_points(self.main_croupier)
        
        self.jeu_termine = True
        # Finaliser la partie avec les gains
        self.finaliser_partie()
    
    def determiner_gagnant(self) -> str:
        """Détermine le gagnant de la partie"""
        if self.points_joueur > 21:
            return "Croupier"
        elif self.points_croupier > 21:
            return "Joueur"
        elif self.points_joueur > self.points_croupier:
            return "Joueur"
        elif self.points_croupier > self.points_joueur:
            return "Croupier"
        else:
            return "Égalité"

class InterfaceBlackjack:
    """Interface graphique du jeu de blackjack"""
    
    def __init__(self):
        self.jeu = JeuBlackjack()
        self.root = tk.Tk()
        self.root.title("Blackjack")
        self.root.geometry("1000x800")
        self.root.configure(bg='#0d5016')
        self.root.minsize(900, 700)  # Taille minimale pour s'assurer que tout est visible
        
        self.creer_interface()
        self.nouvelle_partie()
    
    def creer_interface(self):
        """Crée l'interface utilisateur"""
        # Titre avec fonction de triche
        self.titre = tk.Label(self.root, text="🂡 BLACKJACK 🂡", 
                        font=('Arial', 20, 'bold'), 
                        fg='white', bg='#0d5016',
                        cursor='hand2')
        self.titre.pack(pady=5)
        self.titre.bind('<Button-1>', self.tricher)
        
        # Sous-titre avec info sur les paquets (cliquable pour changer)
        self.sous_titre = tk.Label(self.root, text=f"🎰 {self.jeu.nombre_paquets} paquets mélangés (cliquez pour changer)", 
                                  font=('Arial', 10), 
                                  fg='#87CEEB', bg='#0d5016',
                                  cursor='hand2')
        self.sous_titre.pack(pady=2)
        self.sous_titre.bind('<Button-1>', self.changer_nombre_paquets)
        
        # Variable pour suivre l'état de la triche
        self.triche_activee = False
        
        # Affichage du solde et de la mise
        frame_info = tk.Frame(self.root, bg='#0d5016')
        frame_info.pack(pady=5)
        
        self.label_solde = tk.Label(frame_info, 
                                  font=('Arial', 14, 'bold'), 
                                  fg='#ffd700', bg='#0d5016')
        self.label_solde.pack(side=tk.LEFT, padx=20)
        
        self.label_mise = tk.Label(frame_info, 
                                 font=('Arial', 14, 'bold'), 
                                 fg='#ff6b6b', bg='#0d5016')
        self.label_mise.pack(side=tk.LEFT, padx=20)
        
        self.label_cartes_restantes = tk.Label(frame_info, 
                                             font=('Arial', 12), 
                                             fg='#87CEEB', bg='#0d5016')
        self.label_cartes_restantes.pack(side=tk.LEFT, padx=20)
        
        # Frame pour les cartes du croupier
        frame_croupier = tk.Frame(self.root, bg='#0d5016')
        frame_croupier.pack(pady=5)
        
        tk.Label(frame_croupier, text="Croupier", 
                font=('Arial', 16, 'bold'), 
                fg='white', bg='#0d5016').pack()
        
        self.frame_cartes_croupier = tk.Frame(frame_croupier, bg='#0d5016')
        self.frame_cartes_croupier.pack()
        
        self.label_points_croupier = tk.Label(frame_croupier, 
                                            font=('Arial', 12), 
                                            fg='yellow', bg='#0d5016')
        self.label_points_croupier.pack()
        
        # Séparateur
        tk.Label(self.root, text="─" * 50, 
                font=('Courier', 14), 
                fg='white', bg='#0d5016').pack(pady=5)
        
        # Frame pour les cartes du joueur
        frame_joueur = tk.Frame(self.root, bg='#0d5016')
        frame_joueur.pack(pady=5)
        
        tk.Label(frame_joueur, text="Vos cartes", 
                font=('Arial', 16, 'bold'), 
                fg='white', bg='#0d5016').pack()
        
        self.frame_cartes_joueur = tk.Frame(frame_joueur, bg='#0d5016')
        self.frame_cartes_joueur.pack()
        
        self.label_points_joueur = tk.Label(frame_joueur, 
                                          font=('Arial', 12), 
                                          fg='yellow', bg='#0d5016')
        self.label_points_joueur.pack()
        
        # Zone de mise avec jetons
        frame_zone_mise = tk.Frame(self.root, bg='#0d5016')
        frame_zone_mise.pack(pady=5)
        
        # Zone de mise (où déposer les jetons)
        self.zone_mise = tk.Frame(frame_zone_mise, 
                                 bg='#2E7D32', 
                                 width=400, height=80,
                                 relief='solid', bd=3)
        self.zone_mise.pack(pady=3)
        self.zone_mise.pack_propagate(False)
        
        # Label d'instruction (en dehors de la zone de mise)
        tk.Label(frame_zone_mise, text="Zone de mise (glissez-déposez les jetons)", 
                font=('Arial', 9, 'bold'), 
                fg='white', bg='#0d5016').pack(pady=2)
        
        # Label de la mise totale (en dehors de la zone de mise)
        self.label_mise_totale = tk.Label(frame_zone_mise, 
                                         text="Mise: 0 jetons", 
                                         font=('Arial', 12, 'bold'), 
                                         fg='#ffd700', bg='#0d5016')
        self.label_mise_totale.pack()
        
        # Bouton pour confirmer la mise
        self.btn_confirmer_mise = tk.Button(frame_zone_mise, text="Confirmer la mise", 
                                          command=self.confirmer_mise,
                                          font=('Arial', 12, 'bold'),
                                          bg='#FF9800', fg='#000000',
                                          padx=20, pady=8,
                                          relief='raised', bd=3,
                                          activebackground='#FFB74D',
                                          activeforeground='#000000')
        self.btn_confirmer_mise.pack(pady=5)
        
        # Zone des jetons disponibles
        frame_jetons = tk.Frame(self.root, bg='#0d5016')
        frame_jetons.pack(pady=3)
        
        tk.Label(frame_jetons, text="Vos jetons (glissez-déposez dans la zone de mise):", 
                font=('Arial', 10, 'bold'), 
                fg='white', bg='#0d5016').pack()
        
        self.frame_jetons_disponibles = tk.Frame(frame_jetons, bg='#0d5016')
        self.frame_jetons_disponibles.pack(pady=3)
        
        # Variables pour le drag & drop
        self.jetons_places = []  # Liste des jetons placés dans la zone de mise
        self.mise_totale = 0
        self.jeton_en_cours_deplacement = None
        
        # Créer les jetons disponibles
        self.creer_jetons_disponibles()
        
        # Frame pour les boutons
        frame_boutons = tk.Frame(self.root, bg='#0d5016')
        frame_boutons.pack(pady=10)
        
        self.btn_tirer = tk.Button(frame_boutons, text="Tirer une carte", 
                                 command=self.tirer_carte,
                                 font=('Arial', 14, 'bold'),
                                 bg='#4CAF50', fg='#000000',
                                 padx=20, pady=10,
                                 relief='raised', bd=3,
                                 activebackground='#66BB6A',
                                 activeforeground='#000000')
        self.btn_tirer.pack(side=tk.LEFT, padx=8)
        
        self.btn_rester = tk.Button(frame_boutons, text="Rester", 
                                  command=self.rester,
                                  font=('Arial', 14, 'bold'),
                                  bg='#FF9800', fg='#000000',
                                  padx=20, pady=10,
                                  relief='raised', bd=3,
                                  activebackground='#FFB74D',
                                  activeforeground='#000000')
        self.btn_rester.pack(side=tk.LEFT, padx=8)
        
        self.btn_doubler = tk.Button(frame_boutons, text="Doubler", 
                                   command=self.doubler,
                                   font=('Arial', 14, 'bold'),
                                   bg='#2196F3', fg='#000000',
                                   padx=20, pady=10,
                                   relief='raised', bd=3,
                                   activebackground='#42A5F5',
                                   activeforeground='#000000')
        self.btn_doubler.pack(side=tk.LEFT, padx=8)
        
        self.btn_nouvelle_partie = tk.Button(frame_boutons, text="Nouvelle partie", 
                                           command=self.nouvelle_partie,
                                           font=('Arial', 14, 'bold'),
                                           bg='#FFCDD2', fg='#000000',
                                           padx=20, pady=10,
                                           relief='raised', bd=3,
                                           activebackground='#FFE0E0',
                                           activeforeground='#000000')
        self.btn_nouvelle_partie.pack(side=tk.LEFT, padx=8)
        
        # Label pour les messages
        self.label_message = tk.Label(self.root, 
                                    font=('Arial', 12, 'bold'), 
                                    fg='#ffd700', bg='#0d5016')
        self.label_message.pack(pady=5)
    
    def afficher_cartes(self):
        """Affiche les cartes des deux joueurs"""
        # Mettre à jour l'affichage du solde et de la mise
        self.label_solde.config(text=f"💰 Solde: {self.jeu.solde_joueur} jetons")
        if self.jeu.mise_actuelle > 0:
            self.label_mise.config(text=f"🎯 Mise: {self.jeu.mise_actuelle} jetons")
        else:
            self.label_mise.config(text="")
        
        # Afficher le nombre de cartes restantes
        cartes_restantes = len(self.jeu.jeu_cartes)
        total_cartes = self.jeu.nombre_paquets * 52
        pourcentage = (cartes_restantes / total_cartes) * 100
        
        # Couleur selon le pourcentage restant
        if pourcentage > 50:
            couleur = '#87CEEB'  # Bleu clair
        elif pourcentage > 25:
            couleur = '#FFD700'  # Jaune
        else:
            couleur = '#FF6B6B'  # Rouge (proche du remélange)
        
        self.label_cartes_restantes.config(text=f"🃏 Cartes: {cartes_restantes}/{total_cartes} ({pourcentage:.1f}%)", fg=couleur)
        
        # Cartes du croupier
        if self.jeu.main_croupier:
            self.afficher_cartes_avec_couleurs(self.jeu.main_croupier, self.frame_cartes_croupier)
            # Afficher les points du croupier seulement si toutes ses cartes sont visibles ou si on triche
            if not any(carte.face_cachee for carte in self.jeu.main_croupier) or self.triche_activee:
                self.label_points_croupier.config(text=f"Points: {self.jeu.points_croupier}")
            else:
                # Calculer seulement les points des cartes visibles
                cartes_visibles = [carte for carte in self.jeu.main_croupier if not carte.face_cachee]
                points_visibles = self.jeu.calculer_points(cartes_visibles)
                self.label_points_croupier.config(text=f"Points: {points_visibles} + ?")
        
        # Cartes du joueur
        if self.jeu.main_joueur:
            self.afficher_cartes_avec_couleurs(self.jeu.main_joueur, self.frame_cartes_joueur)
            self.label_points_joueur.config(text=f"Points: {self.jeu.points_joueur}")
    
    def afficher_cartes_vides(self):
        """Affiche des cartes vides avant la distribution"""
        # Mettre à jour l'affichage du solde et de la mise
        self.label_solde.config(text=f"💰 Solde: {self.jeu.solde_joueur} jetons")
        if self.jeu.mise_actuelle > 0:
            self.label_mise.config(text=f"🎯 Mise: {self.jeu.mise_actuelle} jetons")
        else:
            self.label_mise.config(text="")
        
        # Afficher le nombre de cartes restantes
        cartes_restantes = len(self.jeu.jeu_cartes)
        total_cartes = self.jeu.nombre_paquets * 52
        pourcentage = (cartes_restantes / total_cartes) * 100
        
        # Couleur selon le pourcentage restant
        if pourcentage > 50:
            couleur = '#87CEEB'  # Bleu clair
        elif pourcentage > 25:
            couleur = '#FFD700'  # Jaune
        else:
            couleur = '#FF6B6B'  # Rouge (proche du remélange)
        
        self.label_cartes_restantes.config(text=f"🃏 Cartes: {cartes_restantes}/{total_cartes} ({pourcentage:.1f}%)", fg=couleur)
        
        # Afficher des cartes vides pour le croupier
        for widget in self.frame_cartes_croupier.winfo_children():
            widget.destroy()
        
        frame_cartes_vides_croupier = tk.Frame(self.frame_cartes_croupier, bg='#0d5016')
        frame_cartes_vides_croupier.pack()
        
        # Afficher 2 cartes face cachée pour le croupier
        for i in range(2):
            carte_vide = tk.Label(frame_cartes_vides_croupier, 
                                text="┌─────┐\n│ ░░░ │\n│░░░░░│\n│ ░░░ │\n└─────┘",
                                font=('Courier New', 12, 'bold'),
                                fg='#2C3E50', bg='#ECF0F1',
                                justify=tk.LEFT,
                                relief='flat',
                                bd=0,
                                padx=0,
                                pady=0)
            carte_vide.pack(side=tk.LEFT, padx=(0, 8))
        
        self.label_points_croupier.config(text="Points: ?")
        
        # Afficher des cartes vides pour le joueur
        for widget in self.frame_cartes_joueur.winfo_children():
            widget.destroy()
        
        frame_cartes_vides_joueur = tk.Frame(self.frame_cartes_joueur, bg='#0d5016')
        frame_cartes_vides_joueur.pack()
        
        # Afficher 2 cartes face cachée pour le joueur
        for i in range(2):
            carte_vide = tk.Label(frame_cartes_vides_joueur, 
                                text="┌─────┐\n│ ░░░ │\n│░░░░░│\n│ ░░░ │\n└─────┘",
                                font=('Courier New', 12, 'bold'),
                                fg='#2C3E50', bg='#ECF0F1',
                                justify=tk.LEFT,
                                relief='flat',
                                bd=0,
                                padx=0,
                                pady=0)
            carte_vide.pack(side=tk.LEFT, padx=(0, 8))
        
        self.label_points_joueur.config(text="Points: ?")
    
    def afficher_cartes_triche(self):
        """Affiche les cartes qui seront distribuées en mode triche"""
        # Mettre à jour l'affichage du solde et de la mise
        self.label_solde.config(text=f"💰 Solde: {self.jeu.solde_joueur} jetons")
        if self.jeu.mise_actuelle > 0:
            self.label_mise.config(text=f"🎯 Mise: {self.jeu.mise_actuelle} jetons")
        else:
            self.label_mise.config(text="")
        
        # Afficher le nombre de cartes restantes
        cartes_restantes = len(self.jeu.jeu_cartes)
        total_cartes = self.jeu.nombre_paquets * 52
        pourcentage = (cartes_restantes / total_cartes) * 100
        
        # Couleur selon le pourcentage restant
        if pourcentage > 50:
            couleur = '#87CEEB'  # Bleu clair
        elif pourcentage > 25:
            couleur = '#FFD700'  # Jaune
        else:
            couleur = '#FF6B6B'  # Rouge (proche du remélange)
        
        self.label_cartes_restantes.config(text=f"🃏 Cartes: {cartes_restantes}/{total_cartes} ({pourcentage:.1f}%)", fg=couleur)
        
        # Simuler la distribution des cartes pour la triche
        cartes_joueur = []
        cartes_croupier = []
        
        # Prendre les 4 premières cartes du jeu (sans les retirer)
        if len(self.jeu.jeu_cartes) >= 4:
            cartes_joueur = [self.jeu.jeu_cartes[-1], self.jeu.jeu_cartes[-3]]  # 1ère et 3ème carte
            cartes_croupier = [self.jeu.jeu_cartes[-2], self.jeu.jeu_cartes[-4]]  # 2ème et 4ème carte
            cartes_croupier[0].face_cachee = True  # Première carte du croupier cachée
        
        # Afficher les cartes du croupier
        for widget in self.frame_cartes_croupier.winfo_children():
            widget.destroy()
        
        if cartes_croupier:
            self.afficher_cartes_avec_couleurs(cartes_croupier, self.frame_cartes_croupier)
            # Calculer les points du croupier
            points_croupier = self.jeu.calculer_points(cartes_croupier)
            if cartes_croupier[0].face_cachee:
                points_visibles = self.jeu.calculer_points([cartes_croupier[1]])
                self.label_points_croupier.config(text=f"Points: {points_visibles} + ?")
            else:
                self.label_points_croupier.config(text=f"Points: {points_croupier}")
        else:
            self.label_points_croupier.config(text="Points: ?")
        
        # Afficher les cartes du joueur
        for widget in self.frame_cartes_joueur.winfo_children():
            widget.destroy()
        
        if cartes_joueur:
            self.afficher_cartes_avec_couleurs(cartes_joueur, self.frame_cartes_joueur)
            # Calculer les points du joueur
            points_joueur = self.jeu.calculer_points(cartes_joueur)
            self.label_points_joueur.config(text=f"Points: {points_joueur}")
        else:
            self.label_points_joueur.config(text="Points: ?")
    
    def creer_jetons_disponibles(self):
        """Crée les jetons disponibles pour le drag & drop"""
        # Effacer les jetons existants
        for widget in self.frame_jetons_disponibles.winfo_children():
            widget.destroy()
        
        # Créer des jetons de différentes valeurs avec design réaliste de casino
        valeurs_jetons = [5, 10, 25, 50, 100, 500]
        
        # Couleurs authentiques des jetons de casino (inspirées de la photo)
        designs_jetons = {
            5: {
                'couleur_centre': '#FFFFFF',
                'couleur_inner': '#4A90E2',  # Bleu
                'couleur_outer': '#E8F4FD',
                'couleur_texte': '#000000',
                'couleur_texte_inner': '#FFFFFF',
                'symbole': '●'
            },
            10: {
                'couleur_centre': '#FFD700',  # Jaune
                'couleur_inner': '#DC143C',  # Rouge
                'couleur_outer': '#FFF8DC',
                'couleur_texte': '#000000',
                'couleur_texte_inner': '#FFFFFF',
                'symbole': '●'
            },
            25: {
                'couleur_centre': '#32CD32',  # Vert
                'couleur_inner': '#87CEEB',  # Bleu clair
                'couleur_outer': '#F0FFF0',
                'couleur_texte': '#000000',
                'couleur_texte_inner': '#000000',
                'symbole': '●'
            },
            50: {
                'couleur_centre': '#4169E1',  # Bleu royal
                'couleur_inner': '#DC143C',  # Rouge
                'couleur_outer': '#E6F3FF',
                'couleur_texte': '#FFFFFF',
                'couleur_texte_inner': '#FFFFFF',
                'symbole': '●'
            },
            100: {
                'couleur_centre': '#000000',  # Noir
                'couleur_inner': '#FFD700',  # Jaune
                'couleur_outer': '#F5F5F5',
                'couleur_texte': '#FFFFFF',
                'couleur_texte_inner': '#000000',
                'symbole': '●'
            },
            500: {
                'couleur_centre': '#191970',  # Bleu marine
                'couleur_inner': '#FFFFFF',  # Blanc
                'couleur_outer': '#E6F3FF',
                'couleur_texte': '#FFFFFF',
                'couleur_texte_inner': '#000000',
                'symbole': '●'
            }
        }
        
        for valeur in valeurs_jetons:
            if self.jeu.solde_joueur >= valeur:  # Seulement si on peut se permettre au moins un jeton
                # Calculer combien de jetons de cette valeur on peut se permettre
                quantite_max = self.jeu.solde_joueur // valeur
                
                design = designs_jetons[valeur]
                
                # Créer un canvas pour dessiner le jeton réaliste
                canvas = tk.Canvas(self.frame_jetons_disponibles, 
                                 width=60, height=60,
                                 bg='#0d5016', highlightthickness=0)
                canvas.pack(side=tk.LEFT, padx=3, pady=3)
                
                # Dessiner le jeton avec des cercles concentriques
                self.dessiner_jeton_realiste(canvas, valeur, design, quantite_max)
                
                # Lier les événements de drag & drop
                canvas.bind('<Button-1>', lambda e, v=valeur: self.commencer_deplacement(e, v))
                canvas.bind('<B1-Motion>', self.deplacer_jeton)
                canvas.bind('<ButtonRelease-1>', self.terminer_deplacement)
    
    def dessiner_jeton_realiste(self, canvas, valeur, design, quantite_max):
        """Dessine un jeton réaliste avec des cercles concentriques"""
        # Cercle extérieur (bordure)
        canvas.create_oval(5, 5, 55, 55, 
                          fill=design['couleur_outer'], 
                          outline='#C0C0C0', width=2)
        
        # Cercle intérieur (bande avec texte)
        canvas.create_oval(10, 10, 50, 50, 
                          fill=design['couleur_inner'], 
                          outline='#A0A0A0', width=1)
        
        # Cercle central (valeur)
        canvas.create_oval(18, 18, 42, 42, 
                          fill=design['couleur_centre'], 
                          outline='#808080', width=1)
        
        # Texte de la valeur au centre
        canvas.create_text(30, 30, text=f"${valeur}", 
                          font=('Arial', 8, 'bold'),
                          fill=design['couleur_texte'])
        
        # Texte "CASINO" dans la bande intérieure
        canvas.create_text(30, 20, text="CASINO", 
                          font=('Arial', 4, 'bold'),
                          fill=design['couleur_texte_inner'])
        
        # Texte "POKER" dans la bande intérieure
        canvas.create_text(30, 40, text="POKER", 
                          font=('Arial', 4, 'bold'),
                          fill=design['couleur_texte_inner'])
        
        # Indicateur de quantité si plus d'un jeton possible
        if quantite_max > 1:
            canvas.create_text(30, 50, text=f"max {quantite_max}", 
                              font=('Arial', 3),
                              fill='#666666')
    
    def commencer_deplacement(self, event, valeur):
        """Commence le déplacement d'un jeton"""
        self.jeton_en_cours_deplacement = valeur
        # Pour les canvas, on peut changer la couleur de fond pour indiquer la sélection
        if hasattr(event.widget, 'configure'):
            try:
                event.widget.configure(bg='#FFD700')  # Jaune pour indiquer la sélection
            except:
                pass
    
    def deplacer_jeton(self, event):
        """Déplace le jeton pendant le drag"""
        if self.jeton_en_cours_deplacement:
            # Mettre à jour la position du curseur
            pass
    
    def terminer_deplacement(self, event):
        """Termine le déplacement d'un jeton"""
        if self.jeton_en_cours_deplacement:
            # Vérifier si le jeton est dans la zone de mise
            x, y = event.x_root, event.y_root
            zone_x = self.zone_mise.winfo_rootx()
            zone_y = self.zone_mise.winfo_rooty()
            zone_width = self.zone_mise.winfo_width()
            zone_height = self.zone_mise.winfo_height()
            
            if (zone_x <= x <= zone_x + zone_width and 
                zone_y <= y <= zone_y + zone_height):
                # Le jeton est dans la zone de mise
                self.ajouter_jeton_a_la_mise(self.jeton_en_cours_deplacement)
            else:
                # Le jeton n'est pas dans la zone de mise, le remettre en place
                if hasattr(event.widget, 'configure'):
                    try:
                        event.widget.configure(bg='#0d5016')  # Remettre la couleur normale
                    except:
                        pass
            
            self.jeton_en_cours_deplacement = None
    
    def ajouter_jeton_a_la_mise(self, valeur):
        """Ajoute un jeton à la mise"""
        if self.jeu.solde_joueur >= valeur:  # Vérifier qu'on peut encore se permettre ce jeton
            self.jetons_places.append(valeur)
            self.mise_totale += valeur
            self.jeu.solde_joueur -= valeur
            self.mettre_a_jour_affichage_mise()
            self.creer_jetons_disponibles()  # Recréer les jetons avec le nouveau solde
        else:
            self.label_message.config(text="❌ Pas assez de jetons pour cette valeur !")
    
    def retirer_jeton_de_la_mise(self, valeur):
        """Retire un jeton de la mise"""
        if valeur in self.jetons_places:
            self.jetons_places.remove(valeur)
            self.mise_totale -= valeur
            self.jeu.solde_joueur += valeur
            self.mettre_a_jour_affichage_mise()
            self.creer_jetons_disponibles()
            self.afficher_cartes()  # Mettre à jour l'affichage du solde
            self.label_message.config(text=f"Jeton de {valeur} retiré de la mise")
    
    def mettre_a_jour_affichage_mise(self):
        """Met à jour l'affichage de la mise"""
        self.label_mise_totale.config(text=f"Mise: {self.mise_totale} jetons")
        
        # Afficher les jetons placés
        # Détruire tous les widgets de la zone de mise
        for widget in self.zone_mise.winfo_children():
            widget.destroy()
        
        if self.jetons_places:
            # Compter les jetons par valeur
            compteur_jetons = {}
            for valeur in self.jetons_places:
                compteur_jetons[valeur] = compteur_jetons.get(valeur, 0) + 1
            
            # Afficher les piles de jetons
            frame_jetons_places = tk.Frame(self.zone_mise, bg='#2E7D32')
            frame_jetons_places.pack(pady=5)
            
            # Ajouter un label d'instruction
            tk.Label(frame_jetons_places, text="Cliquez sur un jeton pour le retirer:", 
                    font=('Arial', 8, 'bold'), 
                    fg='white', bg='#2E7D32').pack(pady=2)
            
            # Designs des jetons (même que pour les jetons disponibles)
            designs_jetons = {
                5: {
                    'couleur_centre': '#FFFFFF',
                    'couleur_inner': '#4A90E2',  # Bleu
                    'couleur_outer': '#E8F4FD',
                    'couleur_texte': '#000000',
                    'couleur_texte_inner': '#FFFFFF',
                    'symbole': '●'
                },
                10: {
                    'couleur_centre': '#FFD700',  # Jaune
                    'couleur_inner': '#DC143C',  # Rouge
                    'couleur_outer': '#FFF8DC',
                    'couleur_texte': '#000000',
                    'couleur_texte_inner': '#FFFFFF',
                    'symbole': '●'
                },
                25: {
                    'couleur_centre': '#32CD32',  # Vert
                    'couleur_inner': '#87CEEB',  # Bleu clair
                    'couleur_outer': '#F0FFF0',
                    'couleur_texte': '#000000',
                    'couleur_texte_inner': '#000000',
                    'symbole': '●'
                },
                50: {
                    'couleur_centre': '#4169E1',  # Bleu royal
                    'couleur_inner': '#DC143C',  # Rouge
                    'couleur_outer': '#E6F3FF',
                    'couleur_texte': '#FFFFFF',
                    'couleur_texte_inner': '#FFFFFF',
                    'symbole': '●'
                },
                100: {
                    'couleur_centre': '#000000',  # Noir
                    'couleur_inner': '#FFD700',  # Jaune
                    'couleur_outer': '#F5F5F5',
                    'couleur_texte': '#FFFFFF',
                    'couleur_texte_inner': '#000000',
                    'symbole': '●'
                },
                500: {
                    'couleur_centre': '#191970',  # Bleu marine
                    'couleur_inner': '#FFFFFF',  # Blanc
                    'couleur_outer': '#E6F3FF',
                    'couleur_texte': '#FFFFFF',
                    'couleur_texte_inner': '#000000',
                    'symbole': '●'
                }
            }
            
            for valeur, quantite in compteur_jetons.items():
                design = designs_jetons.get(valeur, designs_jetons[5])  # Fallback au jeton de 5
                
                # Créer un canvas rond pour chaque jeton (comme les vrais jetons de casino)
                canvas_jeton = tk.Canvas(frame_jetons_places, 
                                       width=40, height=40,
                                       bg='#2E7D32', highlightthickness=0)
                canvas_jeton.pack(side=tk.LEFT, padx=2, pady=2)
                
                # Dessiner le jeton rond avec des cercles concentriques
                self.dessiner_jeton_place_ronde(canvas_jeton, valeur, design, quantite)
                
                # Lier l'événement de clic pour retirer le jeton
                canvas_jeton.bind('<Button-1>', lambda e, v=valeur: self.retirer_jeton_de_la_mise(v))
                canvas_jeton.bind('<Enter>', lambda e: e.widget.configure(cursor='hand2'))
                canvas_jeton.bind('<Leave>', lambda e: e.widget.configure(cursor=''))
    
    def dessiner_jeton_place_ronde(self, canvas, valeur, design, quantite):
        """Dessine un jeton rond placé dans la zone de mise"""
        # Cercle extérieur (bordure)
        canvas.create_oval(2, 2, 38, 38, 
                          fill=design['couleur_outer'], 
                          outline='#C0C0C0', width=1)
        
        # Cercle intérieur (bande avec texte)
        canvas.create_oval(6, 6, 34, 34, 
                          fill=design['couleur_inner'], 
                          outline='#A0A0A0', width=1)
        
        # Cercle central (valeur)
        canvas.create_oval(12, 12, 28, 28, 
                          fill=design['couleur_centre'], 
                          outline='#808080', width=1)
        
        # Texte de la valeur au centre
        canvas.create_text(20, 20, text=f"${valeur}", 
                          font=('Arial', 6, 'bold'),
                          fill=design['couleur_texte'])
        
        # Texte "CASINO" dans la bande intérieure
        canvas.create_text(20, 15, text="CASINO", 
                          font=('Arial', 2, 'bold'),
                          fill=design['couleur_texte_inner'])
        
        # Texte "POKER" dans la bande intérieure
        canvas.create_text(20, 25, text="POKER", 
                          font=('Arial', 2, 'bold'),
                          fill=design['couleur_texte_inner'])
        
        # Indicateur de quantité si plus d'un jeton
        if quantite > 1:
            canvas.create_text(20, 32, text=f"×{quantite}", 
                              font=('Arial', 3, 'bold'),
                              fill='#FF0000')  # Rouge pour indiquer qu'on peut cliquer
        
        # Ajouter un indicateur de clic
        canvas.create_text(20, 35, text="CLIC", 
                          font=('Arial', 2, 'bold'),
                          fill='#FF0000')
    
    def dessiner_jeton_place(self, canvas, valeur, design, quantite):
        """Dessine un jeton placé dans la zone de mise (ancienne version)"""
        # Cercle extérieur (bordure)
        canvas.create_oval(3, 3, 47, 47, 
                          fill=design['couleur_outer'], 
                          outline='#C0C0C0', width=2)
        
        # Cercle intérieur (bande avec texte)
        canvas.create_oval(8, 8, 42, 42, 
                          fill=design['couleur_inner'], 
                          outline='#A0A0A0', width=1)
        
        # Cercle central (valeur)
        canvas.create_oval(15, 15, 35, 35, 
                          fill=design['couleur_centre'], 
                          outline='#808080', width=1)
        
        # Texte de la valeur au centre
        canvas.create_text(25, 25, text=f"${valeur}", 
                          font=('Arial', 7, 'bold'),
                          fill=design['couleur_texte'])
        
        # Texte "CASINO" dans la bande intérieure
        canvas.create_text(25, 18, text="CASINO", 
                          font=('Arial', 3, 'bold'),
                          fill=design['couleur_texte_inner'])
        
        # Texte "POKER" dans la bande intérieure
        canvas.create_text(25, 32, text="POKER", 
                          font=('Arial', 3, 'bold'),
                          fill=design['couleur_texte_inner'])
        
        # Indicateur de quantité si plus d'un jeton
        if quantite > 1:
            canvas.create_text(25, 40, text=f"×{quantite}", 
                              font=('Arial', 4, 'bold'),
                              fill='#FF0000')  # Rouge pour indiquer qu'on peut cliquer
        
        # Ajouter un indicateur de clic
        canvas.create_text(25, 45, text="CLIC", 
                          font=('Arial', 2, 'bold'),
                          fill='#FF0000')
    
    def confirmer_mise(self):
        """Confirme la mise et commence le jeu"""
        if self.mise_totale > 0:
            self.jeu.mise_actuelle = self.mise_totale
            self.jeu.mise_placee = True
            
            # Distribuer les cartes initiales maintenant
            self.jeu.distribuer_carte(self.jeu.main_joueur)
            self.jeu.distribuer_carte(self.jeu.main_croupier, face_cachee=True)  # Carte cachée du croupier
            self.jeu.distribuer_carte(self.jeu.main_joueur)
            self.jeu.distribuer_carte(self.jeu.main_croupier)
            
            self.jeu.points_joueur = self.jeu.calculer_points(self.jeu.main_joueur)
            self.jeu.points_croupier = self.jeu.calculer_points(self.jeu.main_croupier)
            
            # Afficher les cartes distribuées
            self.afficher_cartes()
            
            if self.triche_activee:
                self.label_message.config(text="🔍 Mode triche activé ! Mise confirmée ! Tirez une carte ou restez !")
            else:
                self.label_message.config(text="Mise confirmée ! Tirez une carte, restez ou doublez !")
            self.btn_tirer.config(state=tk.NORMAL)
            self.btn_rester.config(state=tk.NORMAL)
            self.btn_doubler.config(state=tk.NORMAL)
            self.btn_confirmer_mise.config(state=tk.DISABLED)
            # Désactiver les jetons
            for widget in self.frame_jetons_disponibles.winfo_children():
                widget.config(state=tk.DISABLED)
        else:
            self.label_message.config(text="❌ Placez au moins un jeton avant de confirmer !")
    
    def creer_affichage_cartes(self, main: List[Carte]) -> str:
        """Crée un affichage multi-lignes pour les cartes"""
        if not main:
            return ""
        
        # Diviser chaque carte en lignes
        lignes_cartes = []
        for carte in main:
            lignes_cartes.append(carte.afficher_carte().split('\n'))
        
        # Combiner les lignes horizontalement
        resultat = []
        for i in range(5):  # 5 lignes par carte
            ligne_combinee = "  ".join([carte[i] for carte in lignes_cartes])
            resultat.append(ligne_combinee)
        
        return '\n'.join(resultat)
    
    def afficher_cartes_avec_couleurs(self, main: List[Carte], label_widget):
        """Affiche les cartes avec des couleurs appropriées"""
        if not main:
            return
        
        # Effacer le contenu précédent
        for widget in label_widget.winfo_children():
            widget.destroy()
        
        # Créer un frame pour contenir les cartes
        frame_cartes = tk.Frame(label_widget, bg='#0d5016')
        frame_cartes.pack()
        
        for carte in main:
            # Si la triche est activée, montrer toutes les cartes
            if carte.face_cachee and not self.triche_activee:
                # Carte cachée avec design réaliste
                carte_label = tk.Label(frame_cartes, 
                                     text=carte.afficher_carte(),
                                     font=('Courier New', 12, 'bold'),
                                     fg='#2C3E50', bg='#ECF0F1',
                                     justify=tk.LEFT,
                                     relief='flat',
                                     bd=0,
                                     padx=0,
                                     pady=0)
                carte_label.pack(side=tk.LEFT, padx=(0, 8))
            else:
                # Carte visible - déterminer la couleur
                couleur_rouge = carte.couleur in ['♥', '♦']
                couleur_texte = '#E74C3C' if couleur_rouge else '#2C3E50'
                couleur_fond = '#FFFFFF'
                
                # Si c'est une carte cachée révélée par la triche, la marquer
                if carte.face_cachee and self.triche_activee:
                    couleur_texte = '#F39C12'  # Couleur spéciale pour les cartes triché
                    couleur_fond = '#FFF3CD'
                
                carte_label = tk.Label(frame_cartes, 
                                     text=carte.afficher_carte(),
                                     font=('Courier New', 12, 'bold'),
                                     fg=couleur_texte, bg=couleur_fond,
                                     justify=tk.LEFT,
                                     relief='flat',
                                     bd=0,
                                     padx=0,
                                     pady=0)
                carte_label.pack(side=tk.LEFT, padx=(0, 8))
    
    def nouvelle_partie(self):
        """Commence une nouvelle partie"""
        # Supprimer le message de fin s'il existe
        if hasattr(self, '_message_fin_ajoute'):
            self._message_fin_ajoute.destroy()
            delattr(self, '_message_fin_ajoute')
        
        if self.jeu.solde_joueur <= 0:
            self.label_message.config(text="💸 Vous n'avez plus de jetons ! Cliquez sur 'Nouvelle partie' pour recommencer avec 1000 jetons.")
            self.jeu.solde_joueur = 1000  # Redonner 1000 jetons
            self.afficher_cartes()
            self.creer_jetons_disponibles()
            return
        
        # Réinitialiser le jeu sans distribuer les cartes
        # Ne pas recréer le jeu de cartes - utiliser celui existant
        # Le jeu sera automatiquement remélangé quand il ne restera que 10% des cartes
        self.jeu.main_joueur = []
        self.jeu.main_croupier = []
        self.jeu.points_joueur = 0
        self.jeu.points_croupier = 0
        self.jeu.jeu_termine = False
        self.jeu.mise_actuelle = 0
        self.jeu.mise_placee = False
        self.jeu.double_effectue = False
        
        # Réinitialiser les jetons
        self.jetons_places = []
        self.mise_totale = 0
        self.mettre_a_jour_affichage_mise()
        
        # Afficher des cartes vides
        self.afficher_cartes_vides()
        self.creer_jetons_disponibles()
        self.label_message.config(text="Glissez-déposez vos jetons dans la zone de mise, puis confirmez !")
        self.btn_tirer.config(state=tk.DISABLED)
        self.btn_rester.config(state=tk.DISABLED)
        self.btn_doubler.config(state=tk.DISABLED)
        self.btn_confirmer_mise.config(state=tk.NORMAL)
    
    def tirer_carte(self):
        """Le joueur tire une carte"""
        if self.jeu.joueur_tire():
            self.afficher_cartes()
            # Désactiver le bouton doubler après avoir tiré une carte
            self.btn_doubler.config(state=tk.DISABLED)
            
            if self.jeu.points_joueur == 21:
                if len(self.jeu.main_joueur) == 2:
                    self.label_message.config(text="Blackjack ! Vous avez 21 en 2 cartes !")
                else:
                    self.label_message.config(text="21 points ! Vous avez 21 points !")
                # Ne pas marquer la partie comme terminée ici, laisser le croupier jouer
                self.croupier_joue()
            elif self.jeu.points_joueur > 21:
                self.label_message.config(text="Bust ! Vous avez dépassé 21 points !")
                # Le joueur a perdu, mais on fait quand même jouer le croupier pour montrer ses cartes
                self.croupier_joue()
        else:
            # Le joueur a perdu, mais on fait quand même jouer le croupier pour montrer ses cartes
            self.croupier_joue()
    
    def rester(self):
        """Le joueur reste avec ses cartes actuelles"""
        self.croupier_joue()
    
    def doubler(self):
        """Le joueur double sa mise et tire une carte"""
        if self.jeu.doubler_mise():
            self.afficher_cartes()
            # Désactiver le bouton doubler après utilisation
            self.btn_doubler.config(state=tk.DISABLED)
            
            if self.jeu.points_joueur > 21:
                self.label_message.config(text="Bust après double ! Vous avez dépassé 21 points !")
            elif self.jeu.points_joueur == 21:
                self.label_message.config(text="21 points après double !")
            else:
                self.label_message.config(text=f"Double effectué ! Vous avez {self.jeu.points_joueur} points.")
            
            # Après un double, le croupier joue automatiquement
            self.croupier_joue()
        else:
            if self.jeu.double_effectue:
                self.label_message.config(text="❌ Vous avez déjà doublé !")
            elif len(self.jeu.main_joueur) != 2:
                self.label_message.config(text="❌ Vous ne pouvez doubler qu'avec exactement 2 cartes !")
            elif self.jeu.solde_joueur < self.jeu.mise_actuelle:
                self.label_message.config(text="❌ Pas assez de jetons pour doubler !")
            else:
                self.label_message.config(text="❌ Impossible de doubler maintenant !")
    
    def croupier_joue(self):
        """Fait jouer le croupier"""
        # Vérifier si la partie n'est pas déjà terminée
        if not self.jeu.jeu_termine:
            self.jeu.croupier_joue()
            self.afficher_cartes()
            # Appeler fin_partie() pour désactiver les boutons et afficher le résultat
            self.fin_partie()
        else:
            # Si la partie est déjà terminée, juste afficher les cartes et finir
            self.afficher_cartes()
            self.fin_partie()
    
    def fin_partie(self):
        """Termine la partie et affiche le résultat"""
        # Désactiver tous les boutons de jeu
        self.btn_tirer.config(state=tk.DISABLED)
        self.btn_rester.config(state=tk.DISABLED)
        self.btn_doubler.config(state=tk.DISABLED)
        self.btn_confirmer_mise.config(state=tk.DISABLED)
        
        # Désactiver tous les jetons
        for widget in self.frame_jetons_disponibles.winfo_children():
            widget.config(state=tk.DISABLED)
        
        # Vérifier si la partie n'est pas déjà terminée pour éviter le double calcul
        if not self.jeu.jeu_termine:
            gagnant = self.jeu.determiner_gagnant()
            mise_perdue = self.jeu.mise_actuelle
            gains = self.jeu.finaliser_partie()
            
            # Mettre à jour l'affichage du solde
            self.afficher_cartes()
            
            if gagnant == "Joueur":
                if self.jeu.points_joueur == 21 and len(self.jeu.main_joueur) == 2:
                    self.label_message.config(text=f"🎉 BLACKJACK ! Vous avez gagné {gains} jetons ! 🎉")
                else:
                    self.label_message.config(text=f"🎉 Félicitations ! Vous avez gagné {gains} jetons ! 🎉")
            elif gagnant == "Croupier":
                self.label_message.config(text=f"😞 Le croupier a gagné ! Vous perdez {mise_perdue} jetons.")
            else:
                self.label_message.config(text=f"🤝 Égalité ! Votre mise de {gains} jetons vous est rendue.")
        else:
            # La partie est déjà terminée, les gains ont déjà été calculés
            # Juste mettre à jour l'affichage et déterminer le message
            self.afficher_cartes()
            
            # Déterminer le gagnant pour afficher le bon message
            gagnant = self.jeu.determiner_gagnant()
            if gagnant == "Joueur":
                if self.jeu.points_joueur == 21 and len(self.jeu.main_joueur) == 2:
                    self.label_message.config(text="🎉 BLACKJACK ! Vous avez gagné ! 🎉")
                else:
                    self.label_message.config(text="🎉 Félicitations ! Vous avez gagné ! 🎉")
            elif gagnant == "Croupier":
                self.label_message.config(text="😞 Le croupier a gagné !")
            else:
                self.label_message.config(text="🤝 Égalité ! Votre mise vous est rendue.")
        
        # Ajouter un message pour indiquer qu'il faut cliquer sur "Nouvelle partie"
        if not hasattr(self, '_message_fin_ajoute'):
            message_fin = tk.Label(self.root, 
                                 text="🎯 Partie terminée ! Cliquez sur 'Nouvelle partie' pour recommencer",
                                 font=('Arial', 12, 'bold'), 
                                 fg='#ffd700', bg='#0d5016')
            message_fin.pack(pady=5)
            self._message_fin_ajoute = message_fin
    
    def tricher(self, event):
        """Active/désactive le mode triche en cliquant sur le titre"""
        if not self.jeu.jeu_termine:
            self.triche_activee = not self.triche_activee
            
            if self.triche_activee:
                self.titre.config(text="🂡 TRICHE ACTIVÉE! 🂡", fg='#ff6b6b')
                if not self.jeu.mise_placee:
                    self.label_message.config(text="🔍 Mode triche activé ! Vous pouvez voir les cartes qui seront distribuées !")
                    # Afficher les cartes qui seront distribuées
                    self.afficher_cartes_triche()
                else:
                    self.label_message.config(text="🔍 Mode triche activé ! Vous pouvez voir les cartes cachées du croupier !")
                    # Rafraîchir l'affichage des cartes
                    self.afficher_cartes()
            else:
                self.titre.config(text="🂡 BLACKJACK 🂡", fg='white')
                if not self.jeu.mise_placee:
                    self.label_message.config(text="Glissez-déposez vos jetons dans la zone de mise, puis confirmez !")
                    # Revenir aux cartes vides
                    self.afficher_cartes_vides()
                else:
                    self.label_message.config(text="Tirez une carte ou restez !")
                    # Rafraîchir l'affichage des cartes
                    self.afficher_cartes()
        else:
            # Si la partie est terminée, indiquer qu'il faut commencer une nouvelle partie
            self.label_message.config(text="🎯 Partie terminée ! Cliquez sur 'Nouvelle partie' pour recommencer")
    
    def changer_nombre_paquets(self, event):
        """Change le nombre de paquets utilisés"""
        if not self.jeu.jeu_termine and not self.jeu.mise_placee:
            # Créer une fenêtre de dialogue pour choisir le nombre de paquets
            dialog = tk.Toplevel(self.root)
            dialog.title("Choisir le nombre de paquets")
            dialog.geometry("300x200")
            dialog.configure(bg='#0d5016')
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Centrer la fenêtre
            dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
            
            tk.Label(dialog, text="Nombre de paquets de cartes :", 
                    font=('Arial', 12, 'bold'), 
                    fg='white', bg='#0d5016').pack(pady=10)
            
            # Variable pour le nombre de paquets
            var_paquets = tk.IntVar(value=self.jeu.nombre_paquets)
            
            # Options de paquets
            options = [1, 2, 4, 6, 8]
            for paquets in options:
                tk.Radiobutton(dialog, text=f"{paquets} paquet{'s' if paquets > 1 else ''} ({paquets * 52} cartes)", 
                             variable=var_paquets, value=paquets,
                             font=('Arial', 10), 
                             fg='white', bg='#0d5016',
                             selectcolor='#2E7D32').pack(anchor='w', padx=20)
            
            def confirmer():
                nouveau_nombre = var_paquets.get()
                if nouveau_nombre != self.jeu.nombre_paquets:
                    self.jeu.nombre_paquets = nouveau_nombre
                    self.jeu.jeu_cartes = self.jeu.creer_jeu()
                    self.jeu.melanger_jeu()
                    self.jeu.point_coupure = int(len(self.jeu.jeu_cartes) * 0.1)
                    self.sous_titre.config(text=f"🎰 {self.jeu.nombre_paquets} paquets mélangés (cliquez pour changer)")
                    self.afficher_cartes_vides()
                    self.label_message.config(text=f"Jeu remélangé avec {nouveau_nombre} paquet{'s' if nouveau_nombre > 1 else ''} !")
                dialog.destroy()
            
            def annuler():
                dialog.destroy()
            
            # Boutons
            frame_boutons = tk.Frame(dialog, bg='#0d5016')
            frame_boutons.pack(pady=20)
            
            tk.Button(frame_boutons, text="Confirmer", command=confirmer,
                     font=('Arial', 10, 'bold'),
                     bg='#4CAF50', fg='#000000',
                     padx=15, pady=5,
                     relief='raised', bd=3,
                     activebackground='#66BB6A',
                     activeforeground='#000000').pack(side=tk.LEFT, padx=5)
            
            tk.Button(frame_boutons, text="Annuler", command=annuler,
                     font=('Arial', 10, 'bold'),
                     bg='#FFCDD2', fg='#000000',
                     padx=15, pady=5,
                     relief='raised', bd=3,
                     activebackground='#FFE0E0',
                     activeforeground='#000000').pack(side=tk.LEFT, padx=5)
        else:
            self.label_message.config(text="❌ Vous ne pouvez changer le nombre de paquets qu'avant de placer une mise !")
    
    def lancer(self):
        """Lance l'interface du jeu"""
        self.root.mainloop()

if __name__ == "__main__":
    jeu = InterfaceBlackjack()
    jeu.lancer()
