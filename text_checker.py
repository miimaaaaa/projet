import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
img = cv2.imread('mima.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# print(pytesseract.image_to_string(img))
# hauteur et largeur de l'image, le troisiéme argument "_" ne nous concerne pas c'est pour la couleur de l'image
hImg, wImg, _ = img.shape
# On stocke dans boxes des colonnes avec des informations sur le texte detecté (voir rapport)
boxes = pytesseract.image_to_data(img)
# on divise l'image en colonnes (boxes)
# On boucle sur le nombre de colonnes existantes
for x, b in enumerate(boxes.splitlines()):
    if x != 0:
        # transformer les informations dans boxes à des listes
        b = b.split()
        # On doit avoir des informations avec 12 colonnes si ce n'est pas le cas c'est que la colonne contient pas de texte
        if len(b) == 12:
            # Le numero 6 correspond au numero du mot
            # le 7 pour l'espace à gauche
            # le 8 pour la largeur
            # et le 9 pour la hauteur
            x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
            # On entoure les mots detéctés avec des rectangles
            cv2.rectangle(img, (x, y), (w + x, h + y), (0, 0, 255), 1)
            # Extraire chaque mot detecté au dessous des rectangles
            # Le numéro 11 correspond au texte
            cv2.putText(img, b[11], (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.4, (50, 50, 255), 1)

cv2.imshow('Resulat', img)
cv2.waitKey(0)