
#* Labyrinthe                                                                   

#* Modules                                                                   
import pygame as p
import random 
import copy
import csv
import time



#* Toutes les fonctions                                                                 




#- Fonction de conversion de la matrice tiled

def conversionMatrice(file):
    with open(file,'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    for j in range (len(data)):
        for i in range(len(data[j])):
            if data[j][i]=='4999':
                data[j][i]=1
            if data[j][i]=='-1':
                data[j][i]=0
            if data[j][i]=='4954':
                data[j][i]=4
            if data[j][i]=='4904':
                data[j][i]=3
    return data












#- Fonction principale du test de labyrinthe

def labyPoss (L):
    global posSor
    global posDep
    d=0
    #print(L)
    for j in {0,len(L[0])-1}:
        for i in range (len(L)) :
            if L[i][j]==4:
                posSor=(i,j)
            if L[i][j]==3:
                posDep=(i,j)
    x,y=posDep[0],posDep[1]+1
    #print(x,y)
    R=[[(x,y)]]
    while len(R[0])>=1 :
        """ d+=1
        if d<10:
            print(R) """
        for C in R :
            x,y = C[len(C)-1]
            if x>=len(L)-1 or y>len(L[0])-1 or x<0 or y<0:
                return('no')
            if L[x][y]==4:
                return('yes',C)
            
            for i in range(4):
                if deplacement(L,x,y)[i]:
                    if i==0 and not((x-1,y) in C):
                        R=R+[C+[(x-1,y)]]
                    if i==1 and not((x,y+1) in C):
                        R=R+[C+[(x,y+1)]]
                    if i==2 and not((x+1,y) in C):
                        R=R+[C+[(x+1,y)]]
                    if i==3 and not((x,y-1) in C):
                        R=R+[C+[(x,y-1)]]
                    
                if len(R)==0:
                    return('no')
                    img1 = font1.render('IMPOSSIBLE', True, 'red')
                    fenetre.blit(img1, (100, 100)) 
                for K in range(len(R)):
                    if R[K]==C:
                        del(R[K])
                        break
    return('no')
    img1 = font1.render('IMPOSSIBLE', True, 'red')
    fenetre.blit(img1, (100, 100)) 

def labyPoss_ralenti(L, fenetre, font1):
    start_time = time.time()
    global posSor
    global posDep
    d = 0
    G = set()
    visited = set()
    for j in {0, len(L[0]) - 1}:
        for i in range(len(L)):
            if L[i][j] == 4:
                posSor = (i, j)
            if L[i][j] == 3:
                posDep = (i, j)
    x, y = posDep[0], posDep[1] + 1
    R = [[(x, y)]]
    while len(R[0]) >= 1:
        d += 1
        new_R = []
        for C in R:
            x, y = C[-1]
            G.add((x, y))
            if L[x][y] == 4:
                end_time = time.time()
                elapsed_time = end_time - start_time
                img1 = font1.render(str(elapsed_time)[0:4], True, 'black')
                fenetre.blit(img1, (200, 10))
                p.display.flip()
                return "yes", C
            for i in range(4):
                if deplacement(L, x, y)[i]:
                    if i == 0:
                        new_pos = (x - 1, y)
                    elif i == 1:
                        new_pos = (x, y + 1)
                    elif i == 2:
                        new_pos = (x + 1, y)
                    elif i == 3:
                        new_pos = (x, y - 1)
                    else:
                        continue
                    if new_pos in visited:
                        continue
                    new_C = C + [new_pos]
                    new_R.append(new_C)
                    visited.add(new_pos)
        R = new_R
        p.draw.rect(fenetre, 'white', (0, 0, 200, 50))
        img1 = font1.render(str(len(R)), True, 'black')
        fenetre.blit(img1, (10, 10))
        affichageChemin(list(G))
        G = set()
    return "no"

def labyPoss_optimized(L, fenetre, font1):
    start_time = time.time()
    global posSor
    global posDep
    visited = set()
    for j in {0, len(L[0]) - 1}:
        for i in range(len(L)):
            if L[i][j] == 4:
                posSor = (i, j)
            if L[i][j] == 3:
                posDep = (i, j)
    x, y = posDep[0], posDep[1] + 1
    R = [[(x, y)]]
    while len(R[0]) >= 1:
        new_R = []
        for C in R:
            x, y = C[-1]
            if L[x][y] == 4:
                end_time = time.time()
                elapsed_time = end_time - start_time
                img1 = font1.render(str(elapsed_time)[0:4], True, 'black')
                fenetre.blit(img1, (200, 10))
                p.display.flip()
                return "yes", C
            for i in range(4):
                if deplacement(L, x, y)[i]:
                    if i == 0:
                        new_pos = (x - 1, y)
                    elif i == 1:
                        new_pos = (x, y + 1)
                    elif i == 2:
                        new_pos = (x + 1, y)
                    elif i == 3:
                        new_pos = (x, y - 1)
                    else:
                        continue
                    if new_pos in visited:
                        continue
                    new_C = C + [new_pos]
                    new_R.append(new_C)
                    visited.add(new_pos)
        R = new_R

    return "no"






def create_background_gradient(fenetre, color1, color2, taille_fenetre):
    """
    Creates a linear gradient background between two colors.
    
    Args:
        fenetre: The pygame surface to draw on
        color1: The starting color (RGB tuple)
        color2: The ending color (RGB tuple)
        taille_fenetre: The dimensions of the window (width, height)
    """
    width, height = taille_fenetre
    gradient_surface = p.Surface((width, height))
    
    for y in range(height):
        # Calculate the ratio based on y position
        ratio = y / height
        
        # Linear interpolation between colors
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        
        # Draw a horizontal line with the calculated color
        p.draw.line(gradient_surface, (r, g, b), (0, y), (width, y))
    
    fenetre.blit(gradient_surface, (0, 0))
    return gradient_surface

















#- Check des directions de déplacements possibles

def deplacement(L,x,y):
    N,E,S,W = 1,1,1,1
    if L[x+1][y] in (1,3):
        S=0
    if L[x-1][y] in (1,3):
        N=0
    if L[x][y+1] in (1,3):
        E=0
    if L[x][y-1] in (1,3):
        W=0
    return(N,E,S,W)

#- Fonction de déplacement pour la création de labyrinthe

def deplacement_créa(L,x,y):
    N,E,S,W = 1,1,1,1
    #on vérifie si les cases sont dans le labyrinthe
    if x+1>=len(L) or L[x+1][y] ==1:
        S=0
    if x-1<0 or L[x-1][y] ==1:
        N=0
    if y+1>=len(L[0]) or L[x][y+1] ==1:
        E=0
    if y-1<0 or L[x][y-1] ==1:
        W=0
    return(N,E,S,W)




















#- Affichage



def affichage(labyrinthe, fenetre, taille_case, couleur_mur, couleur_fond, joueur, decalage, historique_positions):
    decalage_x, decalage_y = decalage
    
    # Create gradient background instead of solid color
    if isinstance(couleur_fond, tuple) and len(couleur_fond) == 2:
        # If couleur_fond is a tuple of two colors, use them for gradient
        color1, color2 = couleur_fond
        create_background_gradient(fenetre, color1, color2, fenetre.get_size())
    else:
        # Fall back to solid color if not a tuple of two colors
        fenetre.fill(couleur_fond)

    for i, ligne in enumerate(labyrinthe):
        for j, case in enumerate(ligne):
            if case == 1:
                p.draw.rect(fenetre, couleur_mur, p.Rect(j * taille_case - decalage_x, i * taille_case - decalage_y, taille_case, taille_case))
            if case == 3:
                p.draw.rect(fenetre, 'red', p.Rect(j * taille_case - decalage_x, i * taille_case - decalage_y, taille_case, taille_case))
            if case == 4:
                p.draw.rect(fenetre, 'green', p.Rect(j * taille_case - decalage_x, i * taille_case - decalage_y, taille_case, taille_case))

    for index, (x, y) in enumerate(historique_positions):
        alpha = int(255 * (1 - index / len(historique_positions)))
        couleur_trainee = (100, 100, 100, alpha)
        trainee = p.Surface((taille_case, taille_case), p.SRCALPHA)
        trainee.fill(couleur_trainee)
        fenetre.blit(trainee, (x * taille_case - decalage_x, y * taille_case - decalage_y))
    
    # Dessiner le joueur
    p.draw.rect(fenetre, (0, 0, 0), p.Rect(joueur.x * taille_case - decalage_x, joueur.y * taille_case - decalage_y, taille_case, taille_case))

def affichageScore(score, fenetre, font1, couleur_texte, decalage,taille_fenetre):
    decalage_x, decalage_y = decalage
    score_texte = font1.render("Score: " + str(score), True, couleur_texte)
    fenetre.blit(score_texte, (taille_fenetre[0]//2-100+decalage_x*10, 20+decalage_y*10))
    p.display.flip()


#- Affichage en cours de création

def affichage_en_création(L, fenetre, caseSize, colorMur, backGroundColor, offset):
    # Create gradient background if backGroundColor is a tuple of two colors
    if isinstance(backGroundColor, tuple) and len(backGroundColor) == 2:
        color1, color2 = backGroundColor
        create_background_gradient(fenetre, color1, color2, fenetre.get_size())
    else:
        fenetre.fill(backGroundColor)
        
    for i in range(len(L)):
        for j in range(len(L[0])):
            if L[i][j] == 1:
                p.draw.rect(fenetre, colorMur, (offset[0] + caseSize * j, offset[1] + caseSize * i, caseSize, caseSize))
            if L[i][j] == 3:
                p.draw.rect(fenetre, 'red', (offset[0] + caseSize * j, offset[1] + caseSize * i, caseSize, caseSize))
            if L[i][j] == 4:
                p.draw.rect(fenetre, 'green', (offset[0] + caseSize * j, offset[1] + caseSize * i, caseSize, caseSize))
                
    p.display.flip()

#- Affichage du tracé de la solution

def affichageSolution (S, fenetre, caseSize, offset):
    
    
    gradient = create_gradient(len(S)+2)
    #print(gradient)
    for i in range (len(S)):
        P=S[i]
        if P==posSor :
            break
        
        p.draw.rect(fenetre, gradient[i], (offset[0]+caseSize*P[1], offset[1]+caseSize*P[0], caseSize, caseSize))
        # time.sleep(0.02)
        p.display.flip()

#- Affichage d'un chemin

def affichageChemin (S, fenetre, caseSize, colorMur, backGroundColor,offset):
    for i in range (len(S)):
        P=S[i]
        p.draw.rect(fenetre, "yellow", (offset[0]+caseSize*P[1], offset[1]+caseSize*P[0], caseSize, caseSize))
        p.display.flip()







def calculer_decalage_camera(joueur, taille_fenetre, taille_case,decalage,smooth_factor=0.1):
    nouveau_decalage_x = joueur.x * taille_case - taille_fenetre[0] // 2
    nouveau_decalage_y = joueur.y * taille_case - taille_fenetre[1] // 2
    decalage_x, decalage_y = decalage
    decalage_x = decalage_x * (1 - smooth_factor) + nouveau_decalage_x * smooth_factor
    decalage_y = decalage_y * (1 - smooth_factor) + nouveau_decalage_y * smooth_factor
    decalage = (decalage_x, decalage_y)
    return decalage


















#- Création d'un labyrinthe aléatoire






def labyAlea (n,m):
    #L est le labyrinthe
    #C est la liste des chemins
    #M est la liste des murs
    #n et m sont les dimensions du labyrinthe
    #c est le numéro sur la case en commençant par 5
    #x et y sont les coordonnées de la case actuelle
    #N,E,S,W sont les directions de déplacement possibles
    #R est la liste des chemins possibles

    

    n=2*n//2+1
    m=2*m//2+1
    c=4
    L = [[1 for j in range(m)] for i in range(n)]
    #mettre des 1 sur les bords
    for j in range(m):  
        L[0][j]=1
        L[n-1][j]=1
    for i in range(n):
        L[i][0]=1
        L[i][m-1]=1
    #on affiche 
    for i in range(n):
        for j in range(m):
            if i%2!=0 and j%2!=0:
                c+=1
                L[i][j]=c
    
   
    C=labyChemins(L)
    Cobj=copy.deepcopy(C[:])
    
    for i in Cobj:
        i[1]=5

    while C!=Cobj :
        M=labyMurs(L)
        P=random.choice(M)
        
        x,y=P[0],P[1]

        if deplacement_créa(L,x,y)[0] and deplacement_créa(L,x,y)[2]:
        
            if L[x-1][y] != L[x+1][y]:
                if L[x-1][y] < L[x+1][y]:
                    update_values(L, L[x+1][y], L[x-1][y])
                else:
                    update_values(L, L[x-1][y], L[x+1][y])
                L[x][y] = 5
        

        elif deplacement_créa(L,x,y)[1] and deplacement_créa(L,x,y)[3]:
            
            
            
            if L[x][y-1] != L[x][y+1]:
                if L[x][y-1] < L[x][y+1]:
                    update_values(L, L[x][y+1], L[x][y-1])
                else:
                    update_values(L, L[x][y-1], L[x][y+1])
                L[x][y] = 5
      

        C=labyChemins(L)
        
     
    for i in L:
        for j in i:
            if j ==5 :
                j=0

   
       
    #mettre la sortie en haut à droite et l'entrée en bas à gauche
    
    

    y,z=random.randint(2,n-4),random.randint(2,n-4)
    y,z=3,n-5
    y=y//2*2+1
    z=z//2*2+1
    L[y][0]=3
    L[y+1][1]=0
    L[y][1]=0
    L[y-1][1]=0
    L[y+1][2]=0
    L[y][2]=0
    L[y-1][2]=0
    L[z][m-1]=4
    L[z-1][m-2]=0
    L[z+1][m-2]=0
    L[z][m-2]=0
    L[z-1][m-3]=0
    L[z+1][m-3]=0
    L[z][m-3]=0


    
    return(L)


#- Création d'un labyrinthe aléatoire au ralenti




def labyAlea_ralenti (n,m):
    #L est le labyrinthe
    #C est la liste des chemins
    #M est la liste des murs
    #n et m sont les dimensions du labyrinthe
    #c est le numéro sur la case en commençant par 5
    #x et y sont les coordonnées de la case actuelle
    #N,E,S,W sont les directions de déplacement possibles
    #R est la liste des chemins possibles

    

    n=2*n//2+1
    m=2*m//2+1
    c=4
    L = [[1 for j in range(m)] for i in range(n)]
    #mettre des 1 sur les bords
    for j in range(m):  
        L[0][j]=1
        L[n-1][j]=1
    for i in range(n):
        L[i][0]=1
        L[i][m-1]=1
    #on affiche 
    for i in range(n):
        for j in range(m):
            if i%2!=0 and j%2!=0:
                c+=1
                L[i][j]=c

    #print(L)
    affichage_en_création(L)
    C=labyChemins(L)
    Cobj=copy.deepcopy(C[:])
    
    for i in Cobj:
        i[1]=5
    #print(Cobj)
    while C!=Cobj :
        M=labyMurs(L)
        print(len(M))
        P=random.choice(M)
        
        x,y=P[0],P[1]
        #print(x,y)
        #print(L[x][y])
        if deplacement_créa(L,x,y)[0] and deplacement_créa(L,x,y)[2]:
            

            if L[x-1][y] != L[x+1][y]:
                
                p.display.flip()
                #print(L[x-1][y], L[x+1][y])
                #time.sleep(1)
                if L[x-1][y] < L[x+1][y]:
                    update_values(L, L[x+1][y], L[x-1][y])
                else:
                    update_values(L, L[x-1][y], L[x+1][y])
                L[x][y] = 5
        

        elif deplacement_créa(L,x,y)[1] and deplacement_créa(L,x,y)[3]:
            
            if L[x][y-1] != L[x][y+1]:
                 
                p.display.flip()
                #print(L[x][y-1], L[x][y+1])
                #time.sleep(1)
                if L[x][y-1] < L[x][y+1]:
                    update_values(L, L[x][y+1], L[x][y-1])
                else:
                    update_values(L, L[x][y-1], L[x][y+1])
                L[x][y] = 5
        #print(L)
        affichage_en_création(L)

        C=labyChemins(L)
        
        #time.sleep(1)

    for i in L:
        for j in i:
            if j ==5 :
                j=0

   
       
    #mettre la sortie en haut à droite et l'entrée en bas à gauche
    
    y,z=random.randint(2,n-4),random.randint(2,n-4)
    y,z=3,n-5
    y=y//2*2+1
    z=z//2*2+1
    L[y][0]=3
    L[y+1][1]=0
    L[y][1]=0
    L[y-1][1]=0
    L[y+1][2]=0
    L[y][2]=0
    L[y-1][2]=0
    L[z][m-1]=4
    L[z-1][m-2]=0
    L[z+1][m-2]=0
    L[z][m-2]=0
    L[z-1][m-3]=0
    L[z+1][m-3]=0
    L[z][m-3]=0
    


    return(L)

import random

def labyAlea_optimise(n, m):
    n = 2 * (n // 2) + 1
    m = 2 * (m // 2) + 1
    labyrinthe = [[1 for _ in range(m)] for _ in range(n)]

    def voisins_possibles(x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        voisins = []

        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy
            if 1 <= nx < n - 1 and 1 <= ny < m - 1:
                if labyrinthe[nx][ny] == 1:
                    voisins.append((nx, ny))

        return voisins

    pile = [(1, 1)]
    labyrinthe[1][1] = 5

    while pile:
        x, y = pile[-1]
        voisins = voisins_possibles(x, y)
        #affichage_en_création(labyrinthe)
        if voisins:
            vx, vy = random.choice(voisins)
            labyrinthe[vx][vy] = 5
            labyrinthe[x + (vx - x) // 2][y + (vy - y) // 2] = 5
            pile.append((vx, vy))
        else:
            pile.pop()

    # Entrée et sortie du labyrinthe
    y,z=3,n-5
    y=y//2*2+1
    z=z//2*2+1
    labyrinthe[y][0]=3

    labyrinthe[z][m-1]=4

    return labyrinthe













#- Changer les grandes valeurs en petites
def update_values(L, old_val, new_val):
    """
    Updates all occurrences of old_val in the labyrinth L with new_val.
    """
    for i in range(len(L)):
        for j in range(len(L[0])):
            if L[i][j] == old_val:
                L[i][j] = new_val


#- Création de la liste avec que les murs

def labyMurs (L):
    L2=[]
    for i in range (1,len(L)-1):
        for j in range (1,len(L[0])-1) :
            if (i+j)%2!=0 and L[i][j]==1:
                L2.append((i,j))
    return(L2)

#- Création de la liste avec que les chemins

def labyChemins (L):
    L2=[]
    for i in range (1,len(L)-1):
        for j in range (1,len(L[0])-1) :
            if i%2!=0 and j%2!=0:
                L2.append([(i,j),L[i][j]])
    return(L2)    































#- Création du dégradé de couleur



def create_gradient(steps):
    """Crée un dégradé de couleurs qui change complètement mais graduellement toutes les 20 couleurs."""

    # Définition d'un nombre aléatoire de couleurs principales
    num_main_colors = 4
    
    # Génération de couleurs principales aléatoires
    main_colors = []
    for i in range(num_main_colors):
        r = random.randint(50, 200)
        g = random.randint(50, 200)
        b = random.randint(50, 200)
        main_color = (r, g, b)
        main_colors.append(main_color)
        
    # Ajout de la première couleur principale au début de la liste de couleurs
    colors = [main_colors[0]]
    
    # Parcours de la liste de couleurs principales et génération de couleurs intermédiaires
    for i in range(num_main_colors):
        # Sélection de la couleur principale actuelle et de la prochaine couleur principale
        prev_main_color = main_colors[i]
        next_main_color = main_colors[(i+1) % num_main_colors]
        
        # Parcours des 20 étapes entre chaque paire de couleurs principales
        for j in range(1, 21):
            # Calcul de la couleur intermédiaire pour cette étape
            frac = j / 20
            r = int((1-frac)*prev_main_color[0] + frac*next_main_color[0])
            g = int((1-frac)*prev_main_color[1] + frac*next_main_color[1])
            b = int((1-frac)*prev_main_color[2] + frac*next_main_color[2])
            color = (r, g, b)
            
            # Ajout de la couleur intermédiaire à la liste de couleurs
            colors.append(color)
    
    # Si le nombre de couleurs est inférieur à steps, on ajoute des couleurs intermédiaires
    while len(colors) < steps:
        prev_color = colors[-1]
        next_main_color = main_colors[len(colors) // 20 % num_main_colors]
        frac = len(colors) % 20 / 20
        r = int((1-frac)*prev_color[0] + frac*next_main_color[0])
        g = int((1-frac)*prev_color[1] + frac*next_main_color[1])
        b = int((1-frac)*prev_color[2] + frac*next_main_color[2])
        color = (r, g, b)
        colors.append(color)
    
    # Suppression des couleurs en trop
    colors = colors[:steps]
    
    return colors


#* Fin Du Code                    