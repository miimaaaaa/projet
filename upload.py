import os

accepted_video_formats = [".mp4"]
accepted_image_formats = [".jpg", ".jpeg", ".png"]


class UploadChecker:
    name = ""
    extension = ""

    def check_format(self, file):
        self.name, self.extension = os.path.splitext(file)
        return self.extension in accepted_video_formats or accepted_image_formats

    # On renvoie true si c'est un format video, on saura donc par extension si c'est une image car on renverra false
    def assert_type(self, file):
        return self.extension in accepted_video_formats
