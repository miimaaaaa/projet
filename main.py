import cv2
import sys

import face_checker
import upload
import image_transformer
import numpy as np
#import matplotlib.pyplot as plt

upload_checker = upload.UploadChecker()
img_trs = image_transformer.ImageTransformer()
#On vérifie d'abord que le format du fichier est exploitable
if not upload_checker.check_format(sys.argv[1]):
    print("Le fichier n'est pas dans un format reconnu.")
    exit()
#Puis on détermine si on a une image ou une video
is_video = upload_checker.assert_type(sys.argv[1])

if is_video:
    video_file = sys.argv[1]
    video = cv2.VideoCapture(video_file)
    if not video.isOpened():
        print("Erreur lors de l'ouverture du fichier vidéo.")
        exit()
    #On lit la vidéo jusqu'a la fin
    while video.isOpened():
        #On va lire frame par frame
        ret, frame = video.read()
        if ret:
            gray = img_trs.toGray(frame)
            #On va récupérer tous les pattern de visage dont on dispose
            faces_tab = face_checker.cycle_face(gray)
            for faces_pattern in faces_tab:
                for (x, y, w, h) in faces_pattern:
                    cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_color = frame[y:y + h, x:x + w]
                    #On ecrit ce qui est détecté
                    cv2.putText(frame, "Visage", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
            #De même avec les corps
            body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')
            bodies = body_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in bodies:
                cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 255, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
                # On ecrit ce qui est détecté
                cv2.putText(frame, "Corps", (x+x, y+y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.imshow('Frame', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    video.release()
    cv2.destroyAllWindows()
