
#* Labyrinthe                                                                   

#* Modules                                                                   


from functions import laby_fonctions as l
from functions import joueur as j

import pygame as p
import time
from pygame.time import Clock
#* Execution                                                                    


#-Labyrinthe à étudierz
p.init()
p.key.set_repeat(300, 100)
taille_fenetre = (1600, 950)
fenetre = p.display.set_mode(taille_fenetre)
backGroundColor=((79, 124, 172), (192, 224, 222))
colorMur = p.Color('#444444')
font1 = p.font.SysFont('script', 100)
font2 = p.font.SysFont('sysfont', 1)
caseSize=20
clock = Clock()

tailleLaby = (10,10)

Laby = l.labyAlea_optimise(tailleLaby[0], tailleLaby[1])

position_depart = (1, 3)  # Adaptez cette position en fonction de votre labyrinthe
position_arrivee = (tailleLaby[1]-1, tailleLaby[0]-3)
joueur = j.Joueur(*position_depart)

#-Execution des fonctions





""" poss = l.labyPoss_optimized(Laby,fenetre,font1)
l.affichageSolution(poss[1],fenetre,caseSize,(50,50)) """


    





score=0

historique_positions = []
max_longueur_historique = 40  # Ajustez cette valeur en fonction de la longueur de la trainée souhaitée


decalage_camera = (0,0)

textOr=(0,0)
colorText=(0,0,0)

deplacement_compteur = 0
seuil_de_deplacement = 4  # Changez cette valeur pour ajuster la vitesse du joueur.

continuer=1
while continuer:
    decalage_camera = l.calculer_decalage_camera(joueur, taille_fenetre, caseSize,decalage_camera, smooth_factor=0.1)
    if (joueur.x, joueur.y) in [position_arrivee,  (position_arrivee[0]+1, position_arrivee[1]),(position_arrivee[0]-1, position_arrivee[1])]:
        # Mettre à jour le score, générer un nouveau labyrinthe, et réinitialiser les positions du joueur et de l'arrivée
        score+=1
        caseSize=20-score//2
        caseSize = max(10, caseSize)
        print("caseSize",caseSize)
        tailleLaby = (tailleLaby[0]+score*2, tailleLaby[1]+score*3)
        Laby = l.labyAlea_optimise(tailleLaby[0], tailleLaby[1])
        position_arrivee = (tailleLaby[1]-1, tailleLaby[0]-3)
        print("position_arrivee",position_arrivee)
        joueur.x, joueur.y = position_depart

    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            continuer = 0
    if continuer == 0:
        break
    deplacement_compteur += 1
    historique_positions.append((joueur.x, joueur.y))

    historique_positions = historique_positions[-max_longueur_historique:]
    if deplacement_compteur >= seuil_de_deplacement:
        # Gérer les entrées du joueur
        keys = p.key.get_pressed()
        if keys[p.K_UP] or keys[p.K_z]:
            joueur.deplacer(0,-1,Laby)
            textOr=(0,1)
        if keys[p.K_DOWN] or keys[p.K_s]:
            joueur.deplacer(0,1,Laby)
            textOr=(0,-1)
        if keys[p.K_LEFT] or keys[p.K_q]:
            joueur.deplacer(-1,0,Laby)
            textOr=(1,0)
        if keys[p.K_RIGHT] or keys[p.K_d]:
            joueur.deplacer(1,0,Laby)
            textOr=(-1,0)
        deplacement_compteur = 0
    # Redessiner le labyrinthe et le joueur
    
    l.affichage(Laby, fenetre, caseSize, colorMur, backGroundColor, joueur, decalage_camera,historique_positions)
    l.affichageScore(score, fenetre, font1, colorText, textOr,taille_fenetre)
    clock.tick(160)



#* Fin Du Code                    


