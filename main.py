import image_renderer
import image_analyzer
import upload
import video_analyzer
import PySimpleGUI as sg

#Partie upload de fichier
file_column = [
    [
        sg.Text("Document à analyser"),
        sg.In(size=(25, 1), enable_events=True, key="FOLDER"),
        sg.FileBrowse(key="IN"),
        sg.Button("OK"),
    ]
]
#Partie sélection d'analyse
analyse_column = [
    [
        sg.Checkbox('Analyser visage', default=False, key="FACE"),
        sg.Checkbox('Analyser corps', default=False, key="BODY"),
        sg.Checkbox('Analyser forme', default=False, key="SHAPE"),
        sg.Checkbox('Analyser couleur', default=False, enable_events=True, key="COLOR"),
        sg.Checkbox('Analyser texte', default=False, key="TEXT"),
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
    elif event == "FOLDER":
        # On récupère le path dans file
        file = (values["IN"])
        # On détermine si on a une image ou une video
        is_video = upload.assert_type(file)
        # On autorise pas l'analyse de couleur sur un fichier vidéo
        if is_video:
            window['COLOR'].Update(disabled=True)
        else:
            window['COLOR'].Update(disabled=False)

    # Comme le fonctionnement de l'analyse de couleur est différent, on autorise
    # pas de faire les autres analyses en même temps
    elif event == "COLOR":
        if values["COLOR"]:
            window['FACE'].Update(value=False, disabled=True)
            window['BODY'].Update(value=False, disabled=True)
            window['SHAPE'].Update(value=False, disabled=True)
            window['TEXT'].Update(value=False, disabled=True)
        else:
            window['FACE'].Update(disabled=False)
            window['BODY'].Update(disabled=False)
            window['SHAPE'].Update(disabled=False)
            window['TEXT'].Update(disabled=False)
    elif event == "OK":
        # On créer les outils
        imageAnalyzer = image_analyzer.ImageAnalyzer(values["FACE"], values["BODY"], values["SHAPE"], values["COLOR"], values["TEXT"], file)
        # On vérifie d'abord que le format du fichier est exploitable
        if not upload.check_format(file):
            print("Le fichier n'est pas dans un format reconnu.")
            exit()
        if is_video:
            video_analyzer.analyzevideo(file, imageAnalyzer)
        # On est dans le cas d'une image ici
        else:
            image_renderer.renderimage(file, imageAnalyzer)
