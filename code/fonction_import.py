# Importation des modules... 
from os import walk 
import pygame

def extraction_csv(chemin_fichier): 
    """
    Renvoie une liste de liste contenant toute les informations contenu dans le fichier au format csv 
    """
    liste = []
    fichier = open(chemin_fichier)
    for ligne in fichier: 
            champs = ligne.split(',')
            liste.append(champs)

    return liste 

def import_dossier(nom_dossier): 
    """
    Renvoie une liste d'images contenant toutes les images contenu dans le dossier 
    """
    liste_images = []
    for _,__,liste_noms_images in walk(nom_dossier): # La fonction 'walk(path)' renvoie la liste des fichiers qu'il y a dans le dossier 'path' 
        for nom_image in liste_noms_images:
            chemin_image = nom_dossier + '/' + nom_image
            image_surface = pygame.image.load(chemin_image).convert_alpha()
            liste_images.append(image_surface)

    return liste_images
