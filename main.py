import cv2
import sys

import face_checker
import image_analyzer
import upload
import image_transformer
import numpy as np
#import matplotlib.pyplot as plt
import video_analyzer
import PySimpleGUI as sg

sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()

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
    video_analyzer.analyzevideo(video_file)
#On est dans le cas d'une image ici
else:
    image = cv2.imread(sys.argv[1])
    image_analyzer.analyzeimage(image)