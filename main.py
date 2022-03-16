import image_renderer
import image_analyzer
import upload
import video_analyzer
import PySimpleGUI as sg

#Partie upload de fichier
file_column = [
    [
        sg.Text("Document à analyser"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FileBrowse(key="IN"),
        sg.Button("OK"),
    ]
]
#Partie sélection d'analyse
analyse_column = [
    [
        sg.Checkbox('Analyser visages', default=False, key="FACE"),
        sg.Checkbox('Analyser corps', default=False, key="BODY"),
        sg.Checkbox('Analyser formes', default=False, key="SHAPE"),
        sg.Checkbox('Analyser couleurs', default=False, key="COLOR"),
        sg.Checkbox('Analyser textes', default=False, key="TEXT"),
    ]
]

layout = [
    [
        sg.Column(file_column),
        sg.VSeperator(),
        sg.Column(analyse_column),
    ]
]
#Valeurs par défaut des analyses
face = False
body = False
shape = False
color = False
text = False

window = sg.Window("Image Viewer", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "OK":
        #On récupère le path dans file
        file = (values["IN"])
        #On créer les outils
        upload_checker = upload.UploadChecker()
        imageAnalyzer = image_analyzer.ImageAnalyzer(values["FACE"], values["BODY"], values["SHAPE"], values["COLOR"], values["TEXT"])
        #On vérifie d'abord que le format du fichier est exploitable
        if not upload_checker.check_format(file):
            print("Le fichier n'est pas dans un format reconnu.")
            exit()
        #Puis on détermine si on a une image ou une video
        is_video = upload_checker.assert_type(file)
        if is_video:
            video_analyzer.analyzevideo(file, imageAnalyzer)
        #On est dans le cas d'une image ici
        else:
            image_renderer.renderimage(file, imageAnalyzer)
