import cv2


class ImageTransformer:

    def toGray(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
