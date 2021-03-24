import tkinter as tk

"""
* Fabriquer des zones de couleurs si la balle touche la zone elle prend la couleur de la zone et au bout de 30 rebonds la balle s'arrête.
* La balle ne doit rebondir que sur les parois du côté et lorsque'elle tape le haut elle répparaît en bas et vice versa et y'a aussi un compteur de rebond à faire.
* Au bout de 5 rebonds la balle alterne entre carré et puis cercle.
"""

##################
# Constantes

LARGEUR = 600
HAUTEUR = 400
compteur = 0
couleur = "blue"
zone_de_couleur = []


###################
# Fonctions

def creer_balle():
    """Dessine un rond bleu et retourne son identifiant
     et les valeurs de déplacements dans une liste"""
    x, y = LARGEUR // 2, HAUTEUR // 2
    dx, dy = 3, 5
    rayon = 20
    cercle = canvas.create_oval((x-rayon, y-rayon),
                                (x+rayon, y+rayon),
                                fill=couleur)
    return [cercle, dx, dy]

def creer_zone(x0, y0, x1, y1, couleur_du_carre):
    """Créer une zone et l'ajouter dans la liste zone_de_couleur"""
    global zone_de_couleur
    canvas.create_oval((x0, y0), (x1, y1), fill=couleur_du_carre, outline=couleur_du_carre)
    zone_de_couleur.append((x0, y0, x1, y1, couleur_du_carre))

def collision(rectA, rectB):
    """Détection de la collision entre 2 éléments"""
    if rectB[2] < rectA[0]:
        # rectB est à gauche
        return False
    if rectB[3] < rectA[1]:
        # rectB est au-dessus
        return False
    if rectB[0] > rectA[2]:
        # rectB est à droite
        return False
    if rectB[1] > rectA[3]:
        # rectB est en-dessous
        return False
    # Dans tous les autres cas il y a collision
    return True

def mouvement():
    """
    1. Déplace la balle et ré-appelle la fonction avec un compte-à-rebours.
    2. Détecte si une collision a lieu entre la balle et les zones de couleurs. 
    3. Change la forme au bout de 5 rebonds.
    """
    global couleur
    rebond()
    canvas.move(balle[0], balle[1], balle[2])
    for zone in zone_de_couleur:
        if collision(canvas.coords(balle[0]), zone[:-1]):
            couleur = zone[-1]
            canvas.itemconfig(balle[0], fill=couleur)
    repeat = canvas.after(20, mouvement)
    if compteur % 5 == 0 and compteur != 0:
        x0, y0, x1, y1 = canvas.coords(balle[0])
        canvas.delete(balle[0])
        balle[0] = canvas.create_rectangle(x0, y0, x1, y1, fill=couleur)
    if compteur % 10 == 0:
        x0, y0, x1, y1 = canvas.coords(balle[0])
        canvas.delete(balle[0])
        balle[0] = canvas.create_oval(x0, y0, x1, y1, fill=couleur)
    if compteur == 30:
        canvas.after_cancel(repeat)


def rebond():
    """Fait rebondir la balle sur les bords du canevas"""
    global balle, compteur
    x0, y0, x1, y1 = canvas.coords(balle[0])
    if x0 <= 0 or x1 >= 600:
        balle[1] = -balle[1]
        compteur += 1
        print(compteur)
    if y1 <= 0:
        canvas.coords(balle[0], (x0, 360, x1, 400))
    if y0 >= 400:
        canvas.coords(balle[0], (x0, -40, x1, 0))

######################
# programme principal

racine = tk.Tk()
canvas = tk.Canvas(racine, bg="black", width=600, height=400)
canvas.grid()
balle = creer_balle()
creer_zone(20, 20, 100, 100, "yellow")
creer_zone(200, 200, 280, 280, "pink")
mouvement()
racine.mainloop()
