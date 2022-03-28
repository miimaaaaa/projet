import numpy as np
import pandas as pd
import cv2
img = cv2.imread("jsk.jpg")
# On nomme les colonnes du fichier csv
index = ["couleur", "nom_couleur", "hexa", "R", "G", "B"]
# Importation du fichier csv qui contient les couleurs
csv = pd.read_csv('couleurs.csv', names=index, header=None)
# On initialise l'action "cliquer" à faux ainsi que le taux de couleurs rouge,vert et bleu et aussi la position de la souris
clicked = False
r = g = b = xpos = ypos = 0

# Une fonction qui cherche les valeurs les plus proches pour R,G et B et renvoi le nom de la couleur
def reconnaissance_couleur(R,G,B):
    # On initialise une valeur minimale avec un nombre plus grand que la taille du fichier csv
    min = 9000
    # On va parcourir tout le fichier csv
    for i in range(len(csv)):
        # On recherche les valeurs les plus proches de R,G et B
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        # Si la position trouvée est inférieure à celle de min, on remplace cette dernière par la nouvelle valeur
        if(d<=min):
            min = d
            # On recupére ensuite le nom de la couleur
            nom_c = csv.loc[i,"nom_couleur"]
    return nom_c

# Une fonction qui affiche le nom de la couleur au clique
def clic(double_clic, x, y, flags, param):
    # Au clic on remplaces les valeurs globales par les valeurs trouvés et avec la position du clic
    if double_clic == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
# On nome la fenêtre où l'image sera affichée
cv2.namedWindow('Resultat')
# Appel à la fonction "clic"
cv2.setMouseCallback('Resultat', clic)
# Un boucle à l'infini pour l'affichage de la fenêtre
while (1):
    # Affichage de la fenêtre qui contient l'image
    cv2.imshow("Resultat", img)
    # Si l'utilisateur a cliqué
    if (clicked):
        # Entourage du texte par un bloc de la même couleur detectée
        # cv2.rectangle(image, Point du début, Point de fin, couleur, opacité)
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        # Detection de la couleur et affichage du nom de la couleur et les valeurs en RGB)
        texte = reconnaissance_couleur(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
        cv2.putText(img, texte, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        # Pour les couleurs trés claires, on affiche le texte en noir
        if (r + g + b >= 600):
            cv2.putText(img, texte, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        clicked = False

# Pour sortir de la boucle on clique sur le bouton échape du clavier
    if cv2.waitKey(20) & 0xFF ==27:
        break
# On ferme toutes les fenêtres ouvertes
cv2.destroyAllWindows()