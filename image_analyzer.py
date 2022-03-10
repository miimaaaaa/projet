import cv2
import face_checker

#Classe qui permet l'analyse de l'image, c'est plus pratique d'en faire
#une classe pour sauvegarder les choix de l'utilisateur vis a vis des
#options d'analyse
class ImageAnalyzer:

    def __init__(self, face, body, shape, color, text):
        self.face = face
        self.body = body
        self.shape = shape
        self.color = color
        self.text = text

    def analyzeimage(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces_tab = face_checker.cycle_face(gray)
        if self.face:
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
        return image
