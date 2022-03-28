import cv2


def cycle_face(frame):
    faces_tab = []
    # On ajoute si on détecte un visage de face du pattern "default"
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces_tab.append(face_cascade.detectMultiScale(frame, 1.20, 5))
    # On ajoute si on détecte un visage de face du pattern "alt", et ainsi de suite avec tous les patterns de visage
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
    faces_tab.append(face_cascade.detectMultiScale(frame, 1.20, 5))
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
    faces_tab.append(face_cascade.detectMultiScale(frame, 1.20, 5))
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt_tree.xml')
    faces_tab.append(face_cascade.detectMultiScale(frame, 1.20, 5))
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_profileface.xml')
    faces_tab.append(face_cascade.detectMultiScale(frame, 1.20, 5))
    return faces_tab
