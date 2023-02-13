# Toutes les variables pour parametrer le jeu... 
LARGEUR = 1280
HAUTEUR = 720
TAILLETUILE = 64 
FPS = 6000 # frames per second (fr: images par secondes)

# Arme du joueur : 
ARME = {'nom': 'épée', 'recharge': 100, 'degats': 15, 'images':'../graphics/arme/epee.png'} 

# Ennemis (infos)
INFO_ENNEMIS = {
    'baton': {'vie': 70, 
              'score': 120, 
              'degats': 8,
              'vitesse': 3, 
              'resistance': 3, 
              'attaque_distance_rayon': 80, 
              'notice_rayon': 360
    },
    'esprit': {'vie': 100, 
               'score': 110, 
               'degats': 5,
               'vitesse': 4, 
               'resistance': 3, 
               'attaque_distance_rayon': 60, 
               'notice_rayon': 350
    },
    'pikpik': {'vie': 110, 
               'score': 120, 
               'degats': 4,
               'vitesse': 3, 
               'resistance': 3, 
               'attaque_distance_rayon': 50, 
               'notice_rayon': 300
    }
}

# Interface 
HAUTEUR_BARRE = 20
LARGEUR_BARRE_VIE = 200

TAILLE_OBJET = 80

POLICE_ECRITURE = '../graphics/ecriture/style_ecriture.ttf' 
TAILLE_ECRITURE = 18

# Couleur interface 
COULEUR_EAU = '#71DDEE'
COULEUR_BACKGROUND = '#222222'
COULEUR_BORDURE_BARRE = '#111111'
COULEUR_TEXTE = '#EEEEEE'
COULEUR_VIE = 'red'
