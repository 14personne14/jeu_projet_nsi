# Importation des modules...
import pygame
from parametre import *
from level import Level


class Game:
    def __init__(self, nom_utilisateur):
        """
        Création des variables pour le bon fonctionnement du jeu...
        """
        pygame.init()
        self.ecran = pygame.display.set_mode((LARGEUR,HAUTEUR))
        pygame.display.set_caption('Laby Adventure | by Eloi & Quentin')
        self.horloge = pygame.time.Clock()
        self.jeu = True
        self.info_quit = "" 
        self.nom_utilisateur = nom_utilisateur
        self.temps_jeu = None # Pas encore de temps de jeu 

        # Appel de la classe 'Level' (dans un autre fichier...)
        self.level = Level()

        # Joue la musique ('.ogg' obligatoire)
        musique = pygame.mixer.Sound('../musique/musique.ogg')
        musique.set_volume(0.8)
        musique.play(loops = -1)

    def run(self):
        """
        Execution du jeu (boucle du jeu jusqu'a ce que le joueur quitte la fenetre)
        """
        while self.jeu:
            for event in pygame.event.get():
                # Si le joueur quitte le jeu :
                if event.type == pygame.QUIT:
                    self.jeu = False
                    self.info_quit = 'quit'
                    
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.level.inverse_pause()

            # Actualise le jeu...
            self.ecran.fill(COULEUR_EAU)
            self.level.run()
            pygame.display.update()
            self.horloge.tick(FPS) # Regle la vitesse du jeu (en fonction des FPS dans le fichier 'parametre')

            # Si le joueur n'a plus de vie 
            if self.level.joueur.vie <= 0: 
                self.jeu = False 
                self.info_quit = 'vie'
            
            if not self.jeu:
                # Calcule le temps de jeu 
                temps_actuel = pygame.time.get_ticks()
                self.temps_jeu = (int(temps_actuel)/1000)%60 # converti millisecondes en secondes 


if __name__ == '__main__': # Si c'est le fichier principal 
    # Affiche les règle du jeu 
    print("""

----------------------------------------------------------- 
Bienvenue dans le jeu 'Laby Adventure'. 
Le but du jeu est d'arrivée à la fin du labyrinthe en affrontant des ennemis mais attention car ils peuvents aussi vous tuez ! 
Tu as aussi un score qui augment quand tu tue un ennemi (ça sert presque à rien mais bon...)
Voici les touches importantes : 
    - Les flèches de direction pour bouger dans tous les sens (-> <- ->)
    - La touche espace pour attaquer un ennemi (bim-bam-boum)
    - La touche 'p' pour mettre le jeu en pause (le temps d'aller au toilette...)
Voila vous connaissez le principe du jeu et toutes les commandes pour arrivée à la fin de ce labyrinthe infernal !!! 
(Appuier sur 'entrée' pour lancer le jeu)")
""")
    input() 
    print('Bon avant je vais juste te demander un pseudo :')
    nom_utilisateur = input('--> ')
    print('Merci et bonne chance... ')
    print('-----------------------------------------------------------')

    # Appel de la classe "Game" (ci-dessus)
    game = Game(nom_utilisateur)
    game.run() # Lance le jeu !!!

    # Affiche la fin du jeu... 
    print('-----------------------------------------------------------')
    if game.info_quit == 'vie':
        print(f'Bien {nom_utilisateur} jouer mais tu es MORT \nTu as jouer {game.temps_jeu} secondes et ton score est de {game.level.joueur.score} ! ')
    else:
        print(f'Merci d\'avoir jouer et au revoir {nom_utilisateur} !\nTu as jouer {game.temps_jeu} secondes et ton score est de {game.level.joueur.score} ! ')
    
    # Quitte le jeu quand tout est fini... (bye bye 👋)
    pygame.quit()
