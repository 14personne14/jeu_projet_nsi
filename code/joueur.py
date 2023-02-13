# Importation des modules... 
import pygame
from fonction_import import import_dossier 
from parametre import *
from entite import Entite 


class Joueur(Entite): # Recupère toutes les propiétées des la classe 'Entite' 
    def __init__(self, position, groupes, objets_obstacle, creer_attaque, supprimer_attaque):
        """
        Creation de l'image du joueur et initialisation de toutes les variables pour le joueur : 
        """
        super().__init__(groupes)

        self.image = pygame.image.load('../graphics/joueur/bas/bas_0.png').convert_alpha() # Image par default 
        self.rect = self.image.get_rect(topleft = position)
        self.collision_box = self.rect.inflate(-26,-26) # Retire 13 pixel tout autour du joueur pour les collisions 
        self.objets_obstacle = objets_obstacle
        
        # Préparation du statut du joueur (direction ; attaque? ; stop?) : 
        self.import_images_joueur()
        self.status = "bas"

        # Paramètre pour l'attaque : 
        self.attaque = False
        self.attaque_temps_recharge = 400
        self.attaque_temps = None
        self.arme = 'épée' 
        self.arme_info = ARME
        self.creer_attaque = creer_attaque
        self.supprimer_attaque = supprimer_attaque
        
        # Stats du joueur (pour l'interface)
        self.stats = {'vie': 100, 'attaque': 10, 'vitesse': 10}
        self.vie = self.stats['vie'] 
        self.score = 0
        self.vitesse = self.stats['vitesse']
        
        # Dégat pour le joueur : 
        self.vulnerable = True
        self.temps_blesser = None
        self.imortalite_temps = 500
    
    def import_images_joueur(self):
        """
        Importe toutes les images du joueur sous différente forme (haut, bas, gauche, droite, attaque & stop)
        """
        chemin_joueur = '../graphics/joueur/'
        self.images = {
            'haut': [],
            'bas': [],
            'gauche': [],
            'droite': [],
			'droite_stop': [],
            'gauche_stop':[],
            'haut_stop':[],
            'bas_stop':[],
			'droite_attaque':[],
            'gauche_attaque':[],
            'haut_attaque':[],
            'bas_attaque':[]
        }

        for nom_status in self.images.keys(): 
            chemin_image = chemin_joueur + nom_status
            self.images[nom_status] = import_dossier(chemin_image)

    def input(self):
        """
        Regarde les touches de clavier appuiée par le joueur pour réaliser ensuite l'action demander par le joueur 
        """
        if not self.attaque:
            keys = pygame.key.get_pressed() # Recupère toutes les touches de clavier appuiée par le joueur (format exemple: 'K_UP = True' 'K_DOWN = False')

            if keys[pygame.K_UP]:
                self.deplacement.y = -1 
                self.status = 'haut'
            elif keys[pygame.K_DOWN]:
                self.deplacement.y = 1 
                self.status = 'bas'
            else: # Si le joueur ne bouge pas en hauteur 
                self.deplacement.y = 0 
            
            if keys[pygame.K_RIGHT]: 
                self.deplacement.x = 1
                self.status = 'droite'
            elif keys[pygame.K_LEFT]:
                self.deplacement.x = -1 
                self.status = 'gauche'
            else: # Si le joueur ne bouge pas largeur 
                self.deplacement.x = 0 
            
            if keys[pygame.K_SPACE]: # Si le joueur attaque 
                self.attaque = True
                self.attaque_temps = pygame.time.get_ticks()
                self.creer_attaque()
    
    def status_actualise(self):
        """
        Actualisation du status du joueur en fonction de son deplacement 
        """
        # Si le joueur ne bouge pas :
        if self.deplacement.x == 0 and self.deplacement.y == 0:
            if not "stop" in self.status and not 'attaque' in self.status:
                self.status = self.status + "_stop" 
        
        # Si le joueur attaque :
        if self.attaque:
            self.deplacement.x = 0
            self.deplacement.y = 0
            if not 'attaque' in self.status:
                if 'stop' in self.status:
                    self.status = self.status.replace('_stop', '_attaque') # '.replace(mot_1, mot_2)' remplace le mot_1 par le mot_2 
                else:
                    self.status = self.status + '_attaque'
        
        # Si le joueur n'attaque pas : 
        else:
            if 'attaque' in self.status:
                self.status = self.status.replace('_attaque', '')

    def recharge(self):
        """
        Verifie si le temps de recharge de l'attaque est fini (si le joueur est en attaque)
        """
        temps_actuel = pygame.time.get_ticks()

        if self.attaque:
            if temps_actuel - self.attaque_temps >= self.attaque_temps_recharge:
                self.attaque = False
                self.supprimer_attaque()

        if not self.vulnerable:
            if temps_actuel - self.temps_blesser >= self.imortalite_temps:
                self.vulnerable = True 

    def change_image_joueur(self):
        """
        Change l'image du joueur pour un effet de mouvement 
        """
        images_liste = self.images[self.status] # Récupére de seulement les images qui nous interresse 

        # Change l'index de l'image 
        self.image_index += self.animation_vitesse
        if self.image_index >= len(images_liste):
            self.image_index = 0
        
        # Change l'image du joueur 
        self.image = images_liste[int(self.image_index)]
        self.rect = self.image.get_rect(center = self.collision_box.center)

        if not self.vulnerable:
            alpha = self.valeur() 
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self): 
        """
        Actualise le joueur (movement, action, style)
        """
        self.input()
        self.recharge()
        self.status_actualise()
        self.change_image_joueur()
        self.mouvement(self.vitesse)
