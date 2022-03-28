import cv2
import face_checker
import pytesseract
import pandas as pd

# Classe qui permet l'analyse de l'image, c'est plus pratique d'en faire
# une classe pour sauvegarder les choix de l'utilisateur vis a vis des
# options d'analyse

class ImageAnalyzer:

    def __init__(self, face, body, shape, color, text):
        self.face = face
        self.body = body
        self.shape = shape
        self.color = color
        self.text = text

    def analyzeimage(self, file):
        image = cv2.imread(file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if self.face:
            # print("face")
            faces_tab = face_checker.cycle_face(gray)
            for faces_pattern in faces_tab:
                for (x, y, w, h) in faces_pattern:
                    cv2.rectangle(image, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
                    # On ecrit ce qui est détecté
                    cv2.putText(image, "Visage", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        if self.body:
            # De même avec les corps
            body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
            bodies = body_cascade.detectMultiScale(gray, 1.01, 6)
            for (x, y, w, h) in bodies:
                cv2.rectangle(image, (x, y), ((x + w), (y + h)), (0, 255, 0), 2)
                # On ecrit ce qui est détecté
                cv2.putText(image, "Corps", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        if self.shape:
            gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # On utilise la fonction canny pour détecter les "bords" de l'images
            edges = cv2.Canny(gray_img, 50, 200)
            contours, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            for cnt in contours:
                shape = "*"
                approx = cv2.approxPolyDP(cnt, 0.03 * cv2.arcLength(cnt, True), True)
                point_x = approx[0][0][0]
                point_y = approx[0][0][1]
                # On va assigner une forme en fonction de la sortie de approxPolyDP
                if len(approx) == 3:
                    shape = 'Triangle'
                elif len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(cnt)
                    if abs(w - h) < 5:
                        shape = 'Square'
                    else:
                        shape = 'Rectangle'
                elif len(approx) == 8:
                    shape = 'Circle'
                if not shape == "*":
                    cv2.putText(image, shape, (point_x, point_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 1)
        if self.color:
            # On nomme les colonnes du fichier csv
            index = ["couleur", "nom_couleur", "hexa", "R", "G", "B"]
            # Importation du fichier csv qui contient les couleurs
            csv = pd.read_csv('couleurs.csv', names=index, header=None)
            # On initialise le taux de couleurs rouge,vert et bleu
            r = g = b = 0

            # Une fonction qui cherche les valeurs les plus proches pour R,G et B et renvoi le nom de la couleur
            def reconnaissance_couleur(R, G, B):
                # On initialise une valeur minimale avec un nombre plus grand que la taille du fichier csv
                min = 9000
                # On va parcourir tout le fichier csv
                for i in range(len(csv)):
                    # On recherche les valeurs les plus proches de R,G et B
                    d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
                    # Si la position trouvée est inférieure à celle de min, on remplace cette dernière par la nouvelle valeur
                    if (d <= min):
                        min = d
                        # On recupére ensuite le nom de la couleur
                        nom_c = csv.loc[i, "nom_couleur"]
                return nom_c
            # Entourage du texte par un bloc de la même couleur detectée
            # cv2.rectangle(image, Point du début, Point de fin, couleur, opacité)
            cv2.rectangle(image, (20, 20), (750, 60), (b, g, r), -1)
            # Detection de la couleur et affichage du nom de la couleur et les valeurs en RGB)
            texte = reconnaissance_couleur(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
            cv2.putText(image, texte, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
            # Pour les couleurs trés claires, on affiche le texte en noir
            if (r + g + b >= 600):
                cv2.putText(image, texte, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        if self.text:
            pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
            img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # On essai de lire le fichier ou on append ce qu'on lit,
            # si on ne parvient pas à le lire on le crée
            try:
                with open(file + '_output.txt', 'x') as f:
                    f.write(pytesseract.image_to_string(img))
            except FileNotFoundError:
                with open(file + '_output.txt', 'w') as f:
                    f.write(pytesseract.image_to_string(img))
            print()
        return image
