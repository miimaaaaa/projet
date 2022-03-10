import cv2

import image_analyzer


def analyzevideo(video_file, imageAnalyzer):
    video = cv2.VideoCapture(video_file)
    # Initialisation de l'outil d'export de la vidéo
    writer = cv2.VideoWriter(video_file + '_output.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20,
                             (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    if not video.isOpened():
        print("Erreur lors de l'ouverture du fichier vidéo.")
        exit()
    # On lit la vidéo jusqu'a la fin
    while video.isOpened():
        # On va lire frame par frame
        ret, frame = video.read()
        if ret:
            frame = imageAnalyzer.analyzeimage(frame)
            # Affiche la frame
            cv2.imshow('Frame', frame)
            # et ecrit la frame
            writer.write(frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    video.release()
    writer.release()
    cv2.destroyAllWindows()
