import image_renderer
import image_analyzer
import upload
import video_analyzer
import PySimpleGUI as sg

# Partie upload de fichier
file_column = [
    [
        sg.T('Document à analyser')
    ],
    [
        sg.In(enable_events=True, key="FOLDER")
    ],
    [
        sg.FileBrowse(target=(-1, 0), key="IN"), sg.OK(key="OK"),
        sg.Text(key="WARNING")
    ]
]

# Partie sélection d'analyse
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
# Valeurs par défaut des analyses
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
        # Si le format n'est pas bon, on averti l'utilisateur et on clean tout
        if not upload.check_format(file):
            window['WARNING'].Update(value="Le format du fichier n'est pas supporté")
            window['OK'].Update(disabled=True)
        else:
            window['WARNING'].Update(value="")
            window['OK'].Update(disabled=False)
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
        if is_video:
            video_analyzer.analyzevideo(file, imageAnalyzer)
        # On est dans le cas d'une image ici
        else:
            image_renderer.renderimage(file, imageAnalyzer)
