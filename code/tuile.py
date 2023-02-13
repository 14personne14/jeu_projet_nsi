# Importation des modules... 
import pygame 
from parametre import *


class Tuile(pygame.sprite.Sprite):
	def __init__(self, position, groupes, type, surface = pygame.Surface((TAILLETUILE, TAILLETUILE))):
		"""
        Création d'une tuile (64x64) pour l'affiche dans le jeu 
        """
		super().__init__(groupes)

		# Création de l'image et du rect de la tuile 
		self.type = type
		self.image = surface
		if self.type == 'objets':
			self.rect = self.image.get_rect(topleft = (position[0], position[1] - TAILLETUILE))
		else:
			self.rect = self.image.get_rect(topleft = position)
		
		self.collision_tuile = self.rect.inflate(0,-10) # Retire 5 pixel en haut et en bas pour les collisions (effet derrière/devant)
