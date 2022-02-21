import cv2
import sys
import upload
import image_transformer
import numpy as np
#import matplotlib.pyplot as plt

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')

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
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = frame[y:y + h, x:x + w]
            cv2.imshow('Frame',frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    video.release()
    cv2.destroyAllWindows()
