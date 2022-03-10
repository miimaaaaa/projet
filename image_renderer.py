import cv2

import image_analyzer


def renderimage(file, imageAnalyzer):
    image = cv2.imread(file)
    image = imageAnalyzer.analyzeimage(image)
    # Affichage de l'image
    cv2.imshow('Result', image)
    # Sauvegarde de l'image
    cv2.imwrite(file + '_output.jpg', image)
    key = cv2.waitKey(0)
    if key == 27:  # if ESC is pressed
        cv2.destroyAllWindows()