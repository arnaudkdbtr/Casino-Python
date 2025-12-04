import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Importer les jeux existants
try:
    from Blackjack import InterfaceBlackjack, JeuBlackjack
    from Roulette import InterfaceRoulette, Roulette
except ImportError as e:
    print(f"Erreur d'importation: {e}")
    print("Assurez-vous que les fichiers Blackjack.py et Roulette.py sont dans le même dossier.")
    sys.exit(1)

class CasinoHub:
    """Hub principal du casino avec solde partagé dans une seule fenêtre"""
    
    def __init__(self):
        self.solde_partage = 1000  # Solde initial partagé entre les jeux
        self.root = tk.Tk()
        self.root.title("🎰 CASINO HUB 🎰")
        self.root.geometry("1000x850")
        self.root.configure(bg='#0d5016')
        self.root.minsize(900, 750)
        
        # Frame principal pour contenir tous les écrans
        self.frame_principal = tk.Frame(self.root, bg='#0d5016')
        self.frame_principal.pack(fill='both', expand=True)
        
        # Variables pour les instances de jeux
        self.interface_blackjack = None
        self.interface_roulette = None
        self.ecran_actuel = "hub"  # "hub", "blackjack", "roulette"
        
        self.creer_interface()
    
    def creer_interface(self):
        """Crée l'interface du hub principal"""
        # Créer le frame du hub
        self.frame_hub = tk.Frame(self.frame_principal, bg='#0d5016')
        
        # Titre principal
        titre_principal = tk.Label(self.frame_hub, 
                                 text="🎰 CASINO HUB 🎰", 
                                 font=('Arial', 24, 'bold'), 
                                 fg='#FFD700', bg='#0d5016')
        titre_principal.pack(pady=20)
        
        # Sous-titre
        sous_titre = tk.Label(self.frame_hub, 
                            text="Choisissez votre jeu de casino", 
                            font=('Arial', 14), 
                            fg='white', bg='#0d5016')
        sous_titre.pack(pady=5)
        
        # Affichage du solde partagé
        frame_solde = tk.Frame(self.frame_hub, bg='#0d5016')
        frame_solde.pack(pady=20)
        
        self.label_solde = tk.Label(frame_solde, 
                                 text=f"💰 Solde partagé: {self.solde_partage} jetons", 
                                 font=('Arial', 16, 'bold'), 
                                 fg='#FFD700', bg='#0d5016')
        self.label_solde.pack()
        
        # Bouton pour réinitialiser le solde
        btn_reset_solde = tk.Button(frame_solde, 
                                  text="🔄 Réinitialiser le solde (1000 jetons)", 
                                  command=self.reinitialiser_solde,
                                  font=('Arial', 10, 'bold'),
                                  bg='#FF9800', fg='#000000',
                                  padx=15, pady=8,
                                  relief='raised', bd=3,
                                  activebackground='#FFB74D',
                                  activeforeground='#000000')
        btn_reset_solde.pack(pady=10)
        
        # Frame pour les jeux
        frame_jeux = tk.Frame(self.frame_hub, bg='#0d5016')
        frame_jeux.pack(expand=True, fill='both', padx=60, pady=40)
        
        # Container pour les boutons avec espacement
        boutons_container = tk.Frame(frame_jeux, bg='#0d5016')
        boutons_container.pack(expand=True, fill='both')
        
        # Bouton Blackjack avec design moderne et compact
        btn_blackjack = tk.Button(boutons_container, 
                                text="🂡 BLACKJACK 🂡\n\nApprochez-vous de 21 sans dépasser\nBattez le croupier pour gagner", 
                                command=self.lancer_blackjack,
                                font=('Arial', 11, 'bold'),
                                bg='#4CAF50', fg='#000000',
                                padx=20, pady=12,
                                relief='raised', bd=2,
                                activebackground='#66BB6A',
                                activeforeground='#000000',
                                cursor='hand2',
                                width=18, height=4,
                                justify='center')
        btn_blackjack.pack(side=tk.LEFT, padx=20, expand=True, fill='both')
        
        # Bouton Roulette avec design moderne et compact
        btn_roulette = tk.Button(boutons_container, 
                               text="🎰 ROULETTE 🎰\n\nPariez sur des numéros ou couleurs\nMultiplicateurs selon le risque", 
                               command=self.lancer_roulette,
                               font=('Arial', 11, 'bold'),
                               bg='#2196F3', fg='#000000',
                               padx=20, pady=12,
                               relief='raised', bd=2,
                               activebackground='#42A5F5',
                               activeforeground='#000000',
                               cursor='hand2',
                               width=18, height=4,
                               justify='center')
        btn_roulette.pack(side=tk.RIGHT, padx=20, expand=True, fill='both')
        
        # Informations en bas
        frame_info = tk.Frame(self.frame_hub, bg='#0d5016')
        frame_info.pack(fill='x', pady=10)
        
        info_text = tk.Label(frame_info, 
                           text="💡 Conseil: Utilisez le bouton 'Retour au Hub' dans chaque jeu pour changer de jeu.\nVotre solde sera automatiquement synchronisé entre les jeux.", 
                           font=('Arial', 10), 
                           fg='#87CEEB', bg='#0d5016',
                           wraplength=700)
        info_text.pack()
        
        # Bouton quitter
        btn_quitter = tk.Button(frame_info, 
                               text="🚪 Quitter le Casino", 
                               command=self.quitter,
                               font=('Arial', 12, 'bold'),
                               bg='#FFCDD2', fg='#000000',
                               padx=20, pady=8,
                               relief='raised', bd=3,
                               activebackground='#FFE0E0',
                               activeforeground='#000000')
        btn_quitter.pack(pady=10)
        
        # Afficher le hub par défaut
        self.frame_hub.pack(fill='both', expand=True)
        self.ecran_actuel = "hub"
    
    def afficher_ecran(self, ecran):
        """Affiche l'écran spécifié et cache les autres"""
        # Cacher tous les frames
        for widget in self.frame_principal.winfo_children():
            widget.pack_forget()
        
        # Afficher l'écran demandé
        if ecran == "hub":
            self.frame_hub.pack(fill='both', expand=True)
            self.ecran_actuel = "hub"
        elif ecran == "blackjack" and hasattr(self, 'interface_blackjack') and self.interface_blackjack:
            self.interface_blackjack.frame_jeu.pack(fill='both', expand=True)
            self.ecran_actuel = "blackjack"
        elif ecran == "roulette" and hasattr(self, 'interface_roulette') and self.interface_roulette:
            self.interface_roulette.frame_jeu.pack(fill='both', expand=True)
            self.ecran_actuel = "roulette"
        
        # Forcer la mise à jour de l'affichage
        self.root.update_idletasks()
    
    def reinitialiser_solde(self):
        """Réinitialise le solde partagé à 1000 jetons"""
        self.solde_partage = 1000
        self.mettre_a_jour_affichage_solde()
        messagebox.showinfo("Solde réinitialisé", "Votre solde a été réinitialisé à 1000 jetons.")
    
    def mettre_a_jour_affichage_solde(self):
        """Met à jour l'affichage du solde"""
        self.label_solde.config(text=f"💰 Solde partagé: {self.solde_partage} jetons")
    
    def synchroniser_solde_depuis_jeu(self, nouveau_solde):
        """Synchronise le solde depuis un jeu vers le hub"""
        self.solde_partage = nouveau_solde
        self.mettre_a_jour_affichage_solde()
    
    def lancer_blackjack(self):
        """Lance le jeu de blackjack avec le solde partagé"""
        try:
            # Créer une nouvelle instance de blackjack avec le solde partagé
            self.interface_blackjack = InterfaceBlackjackAvecSolde(self.solde_partage, self, self.frame_principal)
            self.afficher_ecran("blackjack")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer le blackjack: {e}")
    
    def lancer_roulette(self):
        """Lance le jeu de roulette avec le solde partagé"""
        try:
            # Créer une nouvelle instance de roulette avec le solde partagé
            self.interface_roulette = InterfaceRouletteAvecSolde(self.solde_partage, self, self.frame_principal)
            self.afficher_ecran("roulette")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer la roulette: {e}")
    
    def retour_au_hub(self):
        """Retourne au hub principal"""
        # Cacher tous les frames
        for widget in self.frame_principal.winfo_children():
            widget.pack_forget()
        
        # Nettoyer les messages de fin de partie des jeux
        if hasattr(self, 'interface_blackjack') and self.interface_blackjack:
            # Supprimer le message de fin de partie du blackjack s'il existe
            if hasattr(self.interface_blackjack, '_message_fin_ajoute'):
                try:
                    self.interface_blackjack._message_fin_ajoute.destroy()
                    delattr(self.interface_blackjack, '_message_fin_ajoute')
                except:
                    pass
        
        if hasattr(self, 'interface_roulette') and self.interface_roulette:
            # Réinitialiser le message de résultat de la roulette
            if hasattr(self.interface_roulette, 'label_resultat'):
                self.interface_roulette.label_resultat.config(text="Placez vos paris !")
        
        # Afficher le hub
        self.frame_hub.pack(fill='both', expand=True)
        self.ecran_actuel = "hub"
        
        # Forcer la mise à jour de l'affichage
        self.root.update_idletasks()
    
    def quitter(self):
        """Quitte l'application"""
        if messagebox.askyesno("Quitter", "Êtes-vous sûr de vouloir quitter le casino ?"):
            self.root.quit()
            self.root.destroy()

class InterfaceBlackjackAvecSolde(InterfaceBlackjack):
    """Interface Blackjack modifiée pour utiliser un solde partagé dans le hub"""
    
    def __init__(self, solde_initial, hub_parent, parent_frame):
        # Initialiser le jeu avec le solde partagé
        self.jeu = JeuBlackjackAvecSolde(solde_initial)
        self.hub_parent = hub_parent
        self.root = hub_parent.root  # Utiliser la même fenêtre que le hub
        
        # Créer le frame du jeu dans le parent_frame
        self.frame_jeu = tk.Frame(parent_frame, bg='#0d5016')
        
        # Variables pour l'interface (copiées de l'original)
        self.triche_activee = False
        self.jetons_places = []
        self.mise_totale = 0
        self.jeton_en_cours_deplacement = None
        
        # Créer l'interface
        self.creer_interface()
        self.nouvelle_partie()
    
    def creer_interface(self):
        """Crée l'interface utilisateur (version modifiée pour le hub)"""
        # Titre avec bouton retour
        frame_titre = tk.Frame(self.frame_jeu, bg='#0d5016')
        frame_titre.pack(fill='x', pady=5)
        
        # Bouton retour au hub
        btn_retour = tk.Button(frame_titre, text="🏠 Retour au Hub", 
                             command=self.retour_au_hub,
                             font=('Arial', 12, 'bold'),
                             bg='#FF9800', fg='#000000',
                             padx=15, pady=5,
                             relief='raised', bd=3,
                             activebackground='#FFB74D',
                             activeforeground='#000000')
        btn_retour.pack(side=tk.LEFT, padx=10)
        
        # Titre du jeu
        self.titre = tk.Label(frame_titre, text="🂡 BLACKJACK 🂡", 
                        font=('Arial', 20, 'bold'), 
                        fg='white', bg='#0d5016',
                        cursor='hand2')
        self.titre.pack(side=tk.LEFT, padx=20)
        self.titre.bind('<Button-1>', self.tricher)
        
        # Sous-titre avec info sur les paquets (cliquable pour changer)
        self.sous_titre = tk.Label(self.frame_jeu, text=f"🎰 {self.jeu.nombre_paquets} paquets mélangés (cliquez pour changer)", 
                                  font=('Arial', 10), 
                                  fg='#87CEEB', bg='#0d5016',
                                  cursor='hand2')
        self.sous_titre.pack(pady=2)
        self.sous_titre.bind('<Button-1>', self.changer_nombre_paquets)
        
        # Affichage du solde et de la mise
        frame_info = tk.Frame(self.frame_jeu, bg='#0d5016')
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
        frame_croupier = tk.Frame(self.frame_jeu, bg='#0d5016')
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
        tk.Label(self.frame_jeu, text="─" * 50, 
                font=('Courier', 14), 
                fg='white', bg='#0d5016').pack(pady=5)
        
        # Frame pour les cartes du joueur
        frame_joueur = tk.Frame(self.frame_jeu, bg='#0d5016')
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
        frame_zone_mise = tk.Frame(self.frame_jeu, bg='#0d5016')
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
        frame_jetons = tk.Frame(self.frame_jeu, bg='#0d5016')
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
        frame_boutons = tk.Frame(self.frame_jeu, bg='#0d5016')
        frame_boutons.pack(pady=5)
        
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
        
        # Label pour les messages avec plus d'espace
        self.label_message = tk.Label(self.frame_jeu, 
                                    font=('Arial', 12, 'bold'), 
                                    fg='#ffd700', bg='#0d5016',
                                    wraplength=800,
                                    justify='center')
        self.label_message.pack(pady=10, fill='x')
    
    def retour_au_hub(self):
        """Retourne au hub principal"""
        # Nettoyer les messages de fin de partie
        if hasattr(self, '_message_fin_ajoute'):
            try:
                self._message_fin_ajoute.destroy()
                delattr(self, '_message_fin_ajoute')
            except:
                pass
        
        # Réinitialiser le message principal
        if hasattr(self, 'label_message'):
            self.label_message.config(text="Glissez-déposez vos jetons dans la zone de mise, puis confirmez !")
        
        # Synchroniser le solde avec le hub
        self.hub_parent.synchroniser_solde_depuis_jeu(self.jeu.solde_joueur)
        self.hub_parent.retour_au_hub()
    
    def nouvelle_partie(self):
        """Commence une nouvelle partie (version modifiée)"""
        # Supprimer le message de fin s'il existe
        if hasattr(self, '_message_fin_ajoute'):
            self._message_fin_ajoute.destroy()
            delattr(self, '_message_fin_ajoute')
        
        if self.jeu.solde_joueur <= 0:
            self.label_message.config(text="💸 Vous n'avez plus de jetons ! Retournez au hub pour réinitialiser votre solde.")
            return
        
        # Réinitialiser le jeu sans distribuer les cartes
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

class JeuBlackjackAvecSolde(JeuBlackjack):
    """Jeu Blackjack modifié pour utiliser un solde externe"""
    
    def __init__(self, solde_initial):
        # Initialiser avec le solde fourni
        self.nombre_paquets = 6
        self.jeu_cartes = self.creer_jeu()
        self.main_joueur = []
        self.main_croupier = []
        self.points_joueur = 0
        self.points_croupier = 0
        self.jeu_termine = False
        self.solde_joueur = solde_initial  # Utiliser le solde fourni
        self.mise_actuelle = 0
        self.mise_placee = False
        self.double_effectue = False
        self.point_coupure = int(len(self.jeu_cartes) * 0.1)

class InterfaceRouletteAvecSolde(InterfaceRoulette):
    """Interface Roulette modifiée pour utiliser un solde partagé dans le hub"""
    
    def __init__(self, solde_initial, hub_parent, parent_frame):
        # Initialiser le jeu avec le solde partagé
        self.jeu = RouletteAvecSolde(solde_initial)
        self.hub_parent = hub_parent
        self.root = hub_parent.root  # Utiliser la même fenêtre que le hub
        
        # Créer le frame du jeu dans le parent_frame
        self.frame_jeu = tk.Frame(parent_frame, bg='#0d5016')
        
        # Variables pour l'animation
        self.animation_en_cours = False
        self.angle_rotation = 0
        self.angle_final = 0
        self.temps_animation = 0
        
        # Variables pour les jetons
        self.jetons_places = []
        self.jeton_en_cours_deplacement = None
        self.jeton_selectionne = None
        self.paris_visuels = []
        
        # Créer l'interface
        self.creer_interface()
        self.nouvelle_partie()
    
    def creer_interface(self):
        """Crée l'interface utilisateur (version modifiée pour le hub)"""
        # Titre avec bouton retour
        frame_titre = tk.Frame(self.frame_jeu, bg='#0d5016')
        frame_titre.pack(fill='x', pady=5)
        
        # Bouton retour au hub
        btn_retour = tk.Button(frame_titre, text="🏠 Retour au Hub", 
                             command=self.retour_au_hub,
                             font=('Arial', 12, 'bold'),
                             bg='#FF9800', fg='#000000',
                             padx=15, pady=5,
                             relief='raised', bd=3,
                             activebackground='#FFB74D',
                             activeforeground='#000000')
        btn_retour.pack(side=tk.LEFT, padx=10)
        
        # Titre du jeu
        self.titre = tk.Label(frame_titre, text="🎰 ROULETTE CASINO 🎰", 
                        font=('Arial', 18, 'bold'), 
                        fg='white', bg='#0d5016')
        self.titre.pack(side=tk.LEFT, padx=20)
        
        # Frame principal
        frame_principal = tk.Frame(self.frame_jeu, bg='#0d5016')
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
        frame_controles = tk.Frame(self.frame_jeu, bg='#0d5016')
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
    
    def retour_au_hub(self):
        """Retourne au hub principal"""
        # Réinitialiser le message de résultat
        if hasattr(self, 'label_resultat'):
            self.label_resultat.config(text="Placez vos paris !")
        
        # Synchroniser le solde avec le hub
        self.hub_parent.synchroniser_solde_depuis_jeu(self.jeu.solde_joueur)
        self.hub_parent.retour_au_hub()
    
    def nouvelle_partie(self):
        """Commence une nouvelle partie complète (version modifiée)"""
        # Empêcher la réinitialisation pendant l'animation
        if self.animation_en_cours:
            self.label_resultat.config(text="❌ Impossible de réinitialiser pendant que la roue tourne !")
            return
        
        # Rembourser tous les paris avant de commencer une nouvelle partie
        for pari in self.jeu.paris_actuels:
            self.jeu.solde_joueur += pari.montant_total
        
        # Si le joueur n'a plus d'argent, afficher un message
        if self.jeu.solde_joueur <= 0:
            self.label_resultat.config(text="💸 Vous n'avez plus de jetons ! Retournez au hub pour réinitialiser votre solde.")
            return
        
        # Commencer une nouvelle partie
        self.jeu.nouvelle_partie()
        self.jetons_places = []
        self.jeton_selectionne = None
        self.effacer_paris_visuels()
        self.mettre_a_jour_affichage()
        self.creer_jetons_disponibles()
        self.label_resultat.config(text="Sélectionnez un jeton et cliquez sur la table pour parier !")

class RouletteAvecSolde(Roulette):
    """Jeu Roulette modifié pour utiliser un solde externe"""
    
    def __init__(self, solde_initial):
        # Initialiser avec le solde fourni
        self.nombres = list(range(37))
        self.nombres_rouges = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        self.nombres_noirs = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        
        # Solde et paris
        self.solde_joueur = solde_initial  # Utiliser le solde fourni
        self.paris_actuels = []
        self.paris_precedents = []
        self.numero_gagnant = None
        self.partie_en_cours = False
        
        # Historique des numéros
        self.historique = []

if __name__ == "__main__":
    hub = CasinoHub()
    hub.root.mainloop()
