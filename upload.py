import os

accepted_video_formats = [".mp4"]
accepted_image_formats = [".jpg", ".jpeg", ".png"]

# On vérifie simplement si le fichier a une extension acceptée
def check_format(file):
    name, extension = os.path.splitext(file)
    return extension in accepted_video_formats or extension in accepted_image_formats


# On renvoie true si c'est un format video, on saura donc par extension si c'est une image car on renverra false
def assert_type(file):
    name, extension = os.path.splitext(file)
    return extension in accepted_video_formats
