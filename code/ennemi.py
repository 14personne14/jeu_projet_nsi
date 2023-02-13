# Importation des modules... 
import pygame
from fonction_import import import_dossier 
from parametre import *
from entite import Entite 


class Ennemi(Entite): # Recupère toutes les propiétées des la classe 'Entite' 
    def __init__(self, nom, position, groupes, objets_obstacle, ennemi_attaque, ajouter_score):
        """
        Creation de l'image de l'ennemi et initialisation de toutes les variables pour l'ennemi : 
        """
        super().__init__(groupes)

        self.type_objet = 'ennemi' # Pour l'actualisation dans le fichier 'level.py' 
        self.objets_obstacle = objets_obstacle
        self.ajouter_score = ajouter_score
        
        # Préparation du statut de l'ennemi (direction ; attaque? ; stop?) et puis l'image : 
        self.import_images(nom)
        self.status = "stop"
        self.image = self.images[self.status][self.image_index]
        self.rect = self.image.get_rect(topleft = position)
        self.collision_box = self.rect.inflate(-26,-26) # Retire 13 pixel tout autour de l'ennemi pour les collisions 

        # Stats de l'ennemi (pour l'interface)
        self.nom_ennemi = nom
        ennemi_info = INFO_ENNEMIS[self.nom_ennemi]
        self.vie = ennemi_info['vie']
        self.score = ennemi_info['score']
        self.vitesse = ennemi_info['vitesse']
        self.degats = ennemi_info['degats']
        self.resistance = ennemi_info['resistance']
        self.attaque_distance_rayon = ennemi_info['attaque_distance_rayon']
        self.notice_rayon = ennemi_info['notice_rayon']
        
        # Paramètre pour l'attaque : 
        self.attaque = False
        self.attaque_temps = None
        self.attaque_temps_recharge = 400 
        self.ennemi_attaque = ennemi_attaque

        # Dégat pour l'ennemi 
        self.vulnerable = True
        self.temps_blesser = None
        self.imortalite_temps = 300

    def import_images(self, nom):
        """
        Importe toutes les images ded l'ennemi sous différente forme (mouvement, attaque & stop)
        """
        chemin_ennemi = f'../graphics/ennemis/{nom}/'
        self.images = {
            'mouvement': [],
			'attaque':[],
            'stop':[]
        }

        for nom_status in self.images.keys(): 
            chemin_image = chemin_ennemi + nom_status
            self.images[nom_status] = import_dossier(chemin_image)

    def change_image_ennemi(self):
        """
        Change l'image de l'ennemi pour un effet de mouvement 
        """
        images_liste = self.images[self.status] # Récupére de seulement les images qui nous interresse 

        # Change l'index de l'image 
        self.image_index += self.animation_vitesse
        if self.image_index >= len(images_liste):
            if self.status == 'attaque':
                self.attaque = True
            self.image_index = 0
        
        # Change l'image de l'ennemi  
        self.image = images_liste[int(self.image_index)]
        self.rect = self.image.get_rect(center = self.collision_box.center)

        if not self.vulnerable:
            alpha = self.valeur() 
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def calcule_distance(self, joueur):
        """
        Calcule de la distance qui sépare le joueur et l'ennemi sur la carte (avec l'aide des vecteurs) 
        """
        vecteur_ennemi = pygame.math.Vector2(self.rect.center)
        vecteur_joueur = pygame.math.Vector2(joueur.rect.center)
        distance = (vecteur_joueur - vecteur_ennemi).magnitude() # Voir 'entite.py' pour fonction magnitude()

        if distance > 0: 
            direction = (vecteur_joueur - vecteur_ennemi).normalize() # Voir 'entite.py' pour fonction normalize()
        else:
            direction = pygame.math.Vector2() # Vecteur vide (l'ennemi ne bouge pas)
        
        return (distance, direction) 

    def status_actualise(self, joueur):
        """
        Actualisation du status de l'ennemi en fonction de son deplacement 
        """
        distance = self.calcule_distance(joueur)[0] # Recupére seulement la distance 

        # Si je joueur est dans le rayon d'attaque de l'ennemi 
        if distance <= self.attaque_distance_rayon and not self.attaque: # Si le joueur est dans la zone d'attaque de l'ennemi (une seule fois le print)
            if self.status != 'attaque': 
                self.image_index = 0
            self.status = 'attaque'
        elif distance <= self.notice_rayon:
            self.status = 'mouvement'
        else: 
            self.status = 'stop'

    def actions(self, joueur):
        """
        Définie le deplacement du joueur en fonction de son status 
        """
        if self.status == 'attaque':
            self.attaque_temps = pygame.time.get_ticks()
            self.ennemi_attaque(self.degats)
        elif self.status == 'mouvement':
            self.deplacement = self.calcule_distance(joueur)[1]
        else: 
            self.deplacement = pygame.math.Vector2() # si le joueur ne bouge pas alors il ne fait aucun mouvement 

    def recharge(self):
        """
        Verifie si l'ennemi peux attaquer ou si il est deja en attaque 
        """
        temps_actuel = pygame.time.get_ticks()

        if self.attaque:
            if temps_actuel - self.attaque_temps >= self.attaque_temps_recharge:
                self.attaque = False

        if not self.vulnerable:
            if temps_actuel - self.temps_blesser >= self.imortalite_temps:
                self.vulnerable = True 
    
    def verification_mort(self):
        """
        Supprim l'ennemi de son groupe si il n'a plus de vie 
        """
        if self.vie <= 0:
            self.kill() # Supprime un element d'un groupe (ici supprime un des ennemis si il a plus de vie)
            self.ajouter_score(self.score)

    def reaction_joueur(self):
        """
        Repousse l'ennemi si le joueur l'attaque 
        """
        if not self.vulnerable:
            self.deplacement = self.deplacement * -self.resistance

    def infige_degat(self, joueur):
        """
        Baisse la vie du joueur en fonction des dégats que lui infige l'ennemi 
        """
        if self.vulnerable:
            self.deplacement = self.calcule_distance(joueur)[1]
            self.vie -= joueur.arme_info['degats']
            self.temps_blesser = pygame.time.get_ticks()
            self.vulnerable = False

    def update(self): 
        """
        Actualise l'ennemi (movement, action, style)
        """
        self.reaction_joueur()
        self.mouvement(self.vitesse)
        self.change_image_ennemi()
        self.recharge()
        self.verification_mort()

    def actualise_ennemi(self, joueur): 
        """
        Actualise les variables de l'ennemi qui ont besoin de la position du joueur (attaque? ; mouvement ; ...)
        """
        self.status_actualise(joueur) 
        self.actions(joueur)
