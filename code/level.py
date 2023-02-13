# Importation des modules...
import pygame
from parametre import *
from tuile import Tuile
from ennemi import Ennemi
from joueur import Joueur
from fonction_import import *
from arme import Arme
from interface import Interface 


class Level:
    def __init__(self):
        """
        Initialisation de tous les variables important pour le jeu
        """

        self.surface_ecran = pygame.display.get_surface()
        self.jeu_pause = False

        # Création de groupe (avec 'sprite') où sera enregistré les elements visibles pour le jeu et les obstacles.
        self.objets_visible = GroupeCameraMouvement() # **Groupe spécial pour pouvoir gérer la caméra (voir plus bas)
        self.objets_obstacle = pygame.sprite.Group()

        self.objets_pour_attaque = pygame.sprite.Group()
        self.objets_attaquable = pygame.sprite.Group()

        # Création du groupe des attaques (les attaques se supprimeront les unes à la suite des autres avec une autre fonction)
        self.attaque_en_cour = None

        # Création de la map
        self.create_map()

        # création de l'interface pour le joueur
        self.interface = Interface() 

    def create_map(self):
        """
        Importation et création des elements graphiques du jeu
        """

        # Création d'un dictionaire contenant la liste des positions pour les élements graphiques
        positions_elements = {
            'collision': extraction_csv('../map/map_limites.csv'),
            'entites': extraction_csv('../map/map_entites.csv')
        }

        # Trie tous les elements
        for nom, positions in positions_elements.items():
            for ligne_index, ligne in enumerate(positions):
                for colonne_index, colonne in enumerate(ligne):
                    if colonne != '-1':
                        x = colonne_index * TAILLETUILE
                        y = ligne_index * TAILLETUILE
                        if nom == 'collision':
                            Tuile((x,y), [self.objets_obstacle], 'invisible')
                        
                        if nom == 'entites': 
                            if colonne == '394': # Si l'id correspond à celui du joueur dans le fichier csv (ici 394)
                                self.joueur = Joueur(
                                    (x, y),
                                    [self.objets_visible],
                                    self.objets_obstacle, 
                                    self.creer_attaque, 
                                    self.supprimer_attaque 
                                )
                            else: # Si l'id correspond à celui d'un ennemi dans le fichier csv 
                                if colonne == '390': 
                                    nom_ennemi = 'baton'
                                elif colonne == '393': 
                                    nom_ennemi = 'pikpik'
                                else: # (colonne == '391')  
                                    nom_ennemi = 'esprit'
                                Ennemi(
                                    nom_ennemi, 
                                    (x, y), 
                                    [self.objets_visible, self.objets_attaquable], 
                                    self.objets_obstacle, 
                                    self.ennemi_attaque,
                                    self.ajouter_score
                                )

    def creer_attaque(self):
        """
        Création d'une attaque
        """
        self.attaque_en_cour = Arme(self.joueur, [self.objets_visible, self.objets_pour_attaque])

    def supprimer_attaque(self):
        """
        Suppression d'une attaque
        """
        if self.attaque_en_cour:
            self.attaque_en_cour.kill()
        self.attaque_en_cour = None

    def joueur_attaque(self):
        """
        Fait une attaque seulement si un ennemi est à proximité 
        """
        if self.objets_pour_attaque: 
            for objet_attaque in self.objets_pour_attaque:
                ennemi_en_collision = pygame.sprite.spritecollide(objet_attaque, self.objets_attaquable, False)
                if ennemi_en_collision:
                    for ennemi in ennemi_en_collision:
                        ennemi.infige_degat(self.joueur)

    def inverse_pause(self):
        """
        Met le jeu en pause si le joueur appuie sur 'p' (voi fichier 'main.py')
        """
        self.jeu_pause = not self.jeu_pause

    def ennemi_attaque(self, degat): 
        """
        Enlève des points de vie au joueur (en fonction des degat de l'ennemi)
        """
        if self.joueur.vulnerable:
            self.joueur.vie -= degat
            self.joueur.vulnerable = False
            self.joueur.temps_blesser = pygame.time.get_ticks()
        
    def ajouter_score(self, points):
        """
        Ajoute des points au score du joueur
        """
        self.joueur.score += points

    def run(self):
        """
        Création et actualisation des elements visibles sur la fenetre (= affichage)
        """
        self.objets_visible.custom_draw(self.joueur)
        self.interface.affichage(self.joueur)
        if self.jeu_pause:
            pass
        else: 
            self.objets_visible.update()
            self.objets_visible.actualise_ennemi(self.joueur)
            self.joueur_attaque() 


class GroupeCameraMouvement(pygame.sprite.Group): # **
    def __init__(self):
        """
        Initialise les elements pour le mouvement de la camera
        """

        super().__init__()

        self.surface_ecran = pygame.display.get_surface()
        self.largeur_moitier_ecran = self.surface_ecran.get_size()[0] // 2
        self.hauteur_moitier_ecran = self.surface_ecran.get_size()[1] // 2
        self.decalage = pygame.math.Vector2() # Vecteur pour le décalage de la position du joueur par rapport à (0,0)

        # Création de l'image du sol
        self.sol_image = pygame.image.load('../graphics/carte/carte.png')
        self.sol_rect = self.sol_image.get_rect(topleft = (0,0))

    def custom_draw(self, joueur):
        """
        Dessine tous les elements de la carte en fonction des deplacements du joueur.
        """

        # Calcule le décalage entre le joueur et le millieu de l'écran
        self.decalage.x = joueur.rect.centerx - self.largeur_moitier_ecran
        self.decalage.y = joueur.rect.centery - self.hauteur_moitier_ecran

        # Dessine le sol en fonction du decalage
        decalage_sol = self.sol_rect.topleft - self.decalage
        self.surface_ecran.blit(self.sol_image, decalage_sol)

        # Dessine toutes les images en fonction du decalage :
        for tuile in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): # trie les sprites pour que le joueur soit bien en dessous ou au dessus des elements
            decalage_tuile = tuile.rect.topleft - self.decalage
            self.surface_ecran.blit(tuile.image, decalage_tuile)
    
    def actualise_ennemi(self, joueur):
        """
        Appel la fonction d'actualisation de l'ennemi pour tous les ennemis 
        """
        objets_ennemi = [objet for objet in self.sprites() if hasattr(objet, 'type_objet') and objet.type_objet == 'ennemi'] # Récupère tous les 'objets' ennemi (qui sont dans les groupes) / La fonction 'hasattr(objet, "nom")' recherche si l'objet a une propriété 'nom' 
        for ennemi in objets_ennemi: 
            ennemi.actualise_ennemi(joueur)
