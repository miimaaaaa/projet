import cv2
import image_transformer
import face_checker

img_trs = image_transformer.ImageTransformer()

def analyzeimage(file, save):
    image = cv2.imread(file)
    gray = img_trs.toGray(image)
    faces_tab = face_checker.cycle_face(gray)
    for faces_pattern in faces_tab:
        for (x, y, w, h) in faces_pattern:
            cv2.rectangle(image, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
            #roi_gray = gray[y:y + h, x:x + w]
            #roi_color = image[y:y + h, x:x + w]
            # On ecrit ce qui est détecté
            cv2.putText(image, "Visage", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
    # De même avec les corps
    body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
    bodies = body_cascade.detectMultiScale(gray, 1.01, 6)
    print(bodies)
    for (x, y, w, h) in bodies:
        cv2.rectangle(image, (x, y), ((x + w), (y + h)), (0, 255, 0), 2)
        #roi_gray = gray[y:y + h, x:x + w]
        #roi_color = image[y:y + h, x:x + w]
        # On ecrit ce qui est détecté
        cv2.putText(image, "Corps", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
    #Affichage de l'image
    cv2.imshow('Frame', image)
    #Sauvegarde de l'image
    cv2.imwrite(file+'_output.jpg', image)
    key = cv2.waitKey(0)
    if key == 27:  # if ESC is pressed
        cv2.destroyAllWindows()