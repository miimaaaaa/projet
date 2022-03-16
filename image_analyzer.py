import cv2
import face_checker
import imutils

#Classe qui permet l'analyse de l'image, c'est plus pratique d'en faire
#une classe pour sauvegarder les choix de l'utilisateur vis a vis des
#options d'analyse
import shape_checker


class ImageAnalyzer:

    def __init__(self, face, body, shape, color, text):
        self.face = face
        self.body = body
        self.shape = shape
        self.color = color
        self.text = text

    def analyzeimage(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if self.face:
            print("face")
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
            ratio = image.shape[0] / float(image.shape[0])
            # On passe en gris pour alléger le calcul, et on floute pour éviter
            # de traiter le "bruit" présent sur l'image
            # puis on binarise pour révéler les formes
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
            # find contours in the thresholded image and initialize the
            # shape detector
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            # loop over the contours
            for c in cnts:
                # compute the center of the contour, then detect the name of the
                # shape using only the contour
                M = cv2.moments(c)
                cX = int((M["m10"] / M["m00"]) * ratio)
                cY = int((M["m01"] / M["m00"]) * ratio)
                shape = shape_checker.detect(c)
                # multiply the contour (x, y)-coordinates by the resize ratio,
                # then draw the contours and the name of the shape on the image
                c = c.astype("float")
                c *= ratio
                c = c.astype("int")
                cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 0), 2)

        return image
