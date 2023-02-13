# Importation des modules... 
import pygame
from math import sin 


class Entite(pygame.sprite.Sprite):
    def __init__(self, groupes): 
        """
        Création des variables appartenant au joueur mais aussi aux ennemis (les 2 sont des entites)
        """
        super().__init__(groupes)

        self.image_index = 0 # Index de l'image à prendre dans le dossier (pour un effet de mouvement de l'entite quand elle avance). 
        self.animation_vitesse = 0.15 
        self.deplacement = pygame.math.Vector2() # Creation d'un vecteur vide du déplacement du joueur 
    
    def mouvement(self, vitesse): 
        """
        Changement de la position de l'image de l'entite sur l'écran 
        """
        if self.deplacement.magnitude() != 0: # '.magnitude()' -> calcule la longueur du vecteur 'deplacement' sqrt(x**2 + y**2) 
            self.deplacement = self.deplacement.normalize() # Normalize le vecteur 
        
        # Change les coordonnées de l'entite
        self.collision_box.x += self.deplacement.x * vitesse
        self.collision('horizontal')
        self.collision_box.y += self.deplacement.y * vitesse
        self.collision('vertical')

        # Applique les changements des coordonnées de l'entite 
        self.rect.center = self.collision_box.center
    
    def collision(self, direction_info): 
        """
        Change encore les coordonnées de l'entite si celle-ci touche un obstacle 
        """
        
        # Verifie en 'x' 
        if direction_info == 'horizontal': 
            for obstacle in self.objets_obstacle: 
                if obstacle.collision_tuile.colliderect(self.collision_box): # 'colliderect(collision_box)' -> test si 2 rectangles s'intersectent 
                    if self.deplacement.x > 0: # Replace l'entite à droite
                        self.collision_box.right = obstacle.collision_tuile.left
                    if self.deplacement.x < 0: # Replace l'entite à gauche 
                        self.collision_box.left = obstacle.collision_tuile.right
        
        # Verifie en 'y' 
        if direction_info == 'vertical': 
            for obstacle in self.objets_obstacle: 
                if obstacle.collision_tuile.colliderect(self.collision_box): # //idem// 
                    if self.deplacement.y > 0: # Replace l'entite en bas 
                        self.collision_box.bottom = obstacle.collision_tuile.top
                    if self.deplacement.y < 0: # Replace l'entite en haut
                        self.collision_box.top = obstacle.collision_tuile.bottom

    def valeur(self):
        valeur = sin(pygame.time.get_ticks())
        if valeur >= 0: 
            return 255
        else:
            return 0 
