# Importation des modules... 
import pygame
from parametre import * 


class Interface:
    def __init__(self):
        """
        Prépare les éléments pour l'interface du joueur (aussi dit 'interface utilisateur')
        """
        self.surface_ecran = pygame.display.get_surface()
        self.ecriture = pygame.font.Font(POLICE_ECRITURE, TAILLE_ECRITURE)
        
        # Création des variables pour les barre de vie 
        self.barre_vie_rect = pygame.Rect(10, 10, LARGEUR_BARRE_VIE, HAUTEUR_BARRE)
        
    def affichage_barre(self, stat_actuelle, stat_maximum, rect, couleur):
        """
        Affiche la barre d'un des elements demander (dans nos cas: la vie et l'enrgie)
        """
        # Affiche le fond de la barre 
        pygame.draw.rect(self.surface_ecran, COULEUR_BACKGROUND, rect)
        
        # conversion statistique du joueur en nombre de pixel et création du rect de la barre 
        ratio = stat_actuelle / stat_maximum
        taille_actuelle = rect.width * ratio 
        rect_barre = rect.copy()
        rect_barre.width = taille_actuelle 

        # Affiche la barre 
        pygame.draw.rect(self.surface_ecran, couleur, rect_barre)
        pygame.draw.rect(self.surface_ecran, COULEUR_BORDURE_BARRE, rect_barre, 3)

    def affichage_score(self, score):
        """
        Affiche le score du joueur. 
        """
        texte_surface = self.ecriture.render(str(int(score)), False, COULEUR_TEXTE)
        x = self.surface_ecran.get_size()[0] - 20
        y = self.surface_ecran.get_size()[1] - 20
        texte_rect = texte_surface.get_rect(bottomright = (x, y))

        pygame.draw.rect(self.surface_ecran, COULEUR_BACKGROUND, texte_rect.inflate(20, 20))
        self.surface_ecran.blit(texte_surface, texte_rect)
        pygame.draw.rect(self.surface_ecran, COULEUR_BACKGROUND, texte_rect.inflate(20,20), 3)

    def affichage(self, joueur): 
        """
        Affiche toute l'interface pour le joueur : La barre de vie mais aussi le score de celui-ci 
        """
        # Affiche la barre du joueur pour la vie 
        self.affichage_barre(joueur.vie, joueur.stats['vie'], self.barre_vie_rect, COULEUR_VIE)

        # Affiche le score du joueur 
        self.affichage_score(joueur.score)
