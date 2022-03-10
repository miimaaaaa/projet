import cv2
import image_transformer
import face_checker

img_trs = image_transformer.ImageTransformer()

def analyzevideo(video_file):
    video = cv2.VideoCapture(video_file)
    #Initialisation de l'outil d'export de la vidéo
    writer = cv2.VideoWriter(video_file+'_output.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20,
                             (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    if not video.isOpened():
        print("Erreur lors de l'ouverture du fichier vidéo.")
        exit()
    # On lit la vidéo jusqu'a la fin
    while video.isOpened():
        # On va lire frame par frame
        ret, frame = video.read()
        if ret:
            gray = img_trs.toGray(frame)
            # On va récupérer tous les pattern de visage dont on dispose
            faces_tab = face_checker.cycle_face(gray)
            for faces_pattern in faces_tab:
                for (x, y, w, h) in faces_pattern:
                    cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
                    #roi_gray = gray[y:y + h, x:x + w]
                    #roi_color = frame[y:y + h, x:x + w]
                    # On ecrit ce qui est détecté
                    cv2.putText(frame, "Visage", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
            # De même avec les corps
            body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
            bodies = body_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in bodies:
                cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 255, 0), 2)
                #roi_gray = gray[y:y + h, x:x + w]
                #roi_color = frame[y:y + h, x:x + w]
                # On ecrit ce qui est détecté
                cv2.putText(frame, "Corps", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1,
                            cv2.LINE_AA)
            #Affiche la frame
            cv2.imshow('Frame', frame)
            #et ecrit la frame
            writer.write(frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    video.release()
    writer.release()
    cv2.destroyAllWindows()
