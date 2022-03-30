import cv2
import face_checker
import pytesseract
import os.path

# Classe qui permet l'analyse de l'image, c'est plus pratique d'en faire
# une classe pour sauvegarder les choix de l'utilisateur vis a vis des
# options d'analyse

class ImageAnalyzer:

    def __init__(self, face, body, shape, color, text, file):
        self.face = face
        self.body = body
        self.shape = shape
        self.color = color
        self.text = text
        self.file = file

    # En fonction des choix utilisateur on va analyser chaque élément a la suite par frame
    def analyzeimage(self, image):
        # On passe en nuance de gris pour gérer moins de données
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if self.face:
            # On va chercher les différents patterns de visage dont on dispose
            faces_tab = face_checker.cycle_face(gray)
            for faces_pattern in faces_tab:
                for (x, y, w, h) in faces_pattern:
                    # Création d'un rectangle
                    cv2.rectangle(image, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
                    # On ecrit ce qui est détecté
                    cv2.putText(image, "Visage", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        if self.body:
            # De même avec les corps
            body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
            bodies = body_cascade.detectMultiScale(gray, 1.15, 5)
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
        if self.text:
            pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
            # On doit convertir de BGR(utilisé par cv2) à RGB(utilisé par tesseract)
            img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # On essai de lire le fichier ou on append ce qu'on lit,
            # si on ne parvient pas à le lire on le crée
            if not os.path.isfile(self.file + '_output.txt'):
                with open(self.file + '_output.txt', 'x') as f:
                    f.write(pytesseract.image_to_string(img))
            else:
                with open(self.file + '_output.txt', 'w') as f:
                    f.write(pytesseract.image_to_string(img))
        return image
