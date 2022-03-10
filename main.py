import cv2
import os.path
import image_analyzer
import upload
import image_transformer
import video_analyzer
import PySimpleGUI as sg

#Partie upload de fichier
file_column = [
    [
        sg.Text("Document à analyser"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FileBrowse(key="-IN-"),
        sg.Button("OK"),
    ]
]

layout = [
    [
        sg.Column(file_column),
        sg.VSeperator(),
        sg.Checkbox('Sauvegarder la sortie', default=False, key="-SAVE-"),
        #sg.Column(viewer_column),
    ]
]

window = sg.Window("Image Viewer", layout)
file = window.read()
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "SAVE":
        save = values["-SAVE-"]
        print(save)
    if event == "OK":
        #On récupère le path dans file
        file = (values["-IN-"])
        upload_checker = upload.UploadChecker()
        img_trs = image_transformer.ImageTransformer()
        #On vérifie d'abord que le format du fichier est exploitable
        if not upload_checker.check_format(file):
            print("Le fichier n'est pas dans un format reconnu.")
            exit()
        #Puis on détermine si on a une image ou une video
        is_video = upload_checker.assert_type(file)
        if is_video:
            video_file = file
            video_analyzer.analyzevideo(video_file)
        #On est dans le cas d'une image ici
        else:
            image_analyzer.analyzeimage(file)
