import cv2
import color_analyzer


def renderimage(file, imageAnalyzer):
    image = cv2.imread(file)
    # La détection de couleur utilise un fonctionnement différent du reste
    # et nécessite un traitement spécial
    if imageAnalyzer.color:
        color_analyzer.analyze(image)
    else:
        image = imageAnalyzer.analyzeimage(image)
        # Affichage de l'image
        cv2.imshow('Result', image)
        # Sauvegarde de l'image
        cv2.imwrite(file + '_output.jpg', image)
        key = cv2.waitKey(0)
        if key == 27:  # if ESC is pressed
            cv2.destroyAllWindows()