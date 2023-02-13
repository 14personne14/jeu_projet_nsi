# Importation des modules...
import pygame


class Arme(pygame.sprite.Sprite):
    def __init__(self, joueur, groupes):
        """
        Création de l'arme...
        """
        super().__init__(groupes)

        direction = joueur.status.split('_')[0] # Renvoie la direction du joueur (droite, gauche, haut, bas)

        # Image de l'arme
        chemin_image = f'../graphics/arme/{direction}.png'
        self.image = pygame.image.load(chemin_image).convert_alpha()

        # Placement de l'image (en fonction la direction du joueur et ajoute un petit decalage en fonction de la position du joueur)
        if direction == 'droite':
            self.rect = self.image.get_rect(midleft = joueur.rect.midright + pygame.math.Vector2(0,16))
        elif direction == 'gauche':
            self.rect = self.image.get_rect(midright = joueur.rect.midleft + pygame.math.Vector2(0,16))
        elif direction == 'bas':
            self.rect = self.image.get_rect(midtop = joueur.rect.midbottom + pygame.math.Vector2(-10,0))
        else:
            self.rect = self.image.get_rect(midbottom = joueur.rect.midtop + pygame.math.Vector2(-10,0))
