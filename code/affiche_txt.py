# Importation des modules... 
import pygame

pygame.init()
style_ecriture = pygame.font.Font(None,30)

def affiche_txt(texte, y=10, x=10):
	"""
	((Cette fonction n'ai jamais appeler dans le code mais a servi pour le 'debbugage' du jeu plusieurs fois))
	Affiche le texte à l'écran. 
	Très pratique pour trouver des petits problemes dans le code ;-) 
	"""
	surface_ecran = pygame.display.get_surface()
	ecriture_surface = style_ecriture.render(str(texte), True, 'White')
	ecriture_rect = ecriture_surface.get_rect(topleft = (x, y))
	pygame.draw.rect(surface_ecran,'Black', ecriture_rect)
	surface_ecran.blit(ecriture_surface, ecriture_rect)
