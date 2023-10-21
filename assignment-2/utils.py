import os
from enum import Enum


images = [
    "./images/parrot.png",
    "./images/dog.jpg",
    "./images/monalisa.jpg",
    "./images/eagle.jpg",
]


class ImageType(Enum):
    GRAYSCALE = 0
    UNCHANGED = -1
    COLOR = 1


class Utils:
    @classmethod
    def extract_file_name(cls, path: str) -> str:
        return path.split("/")[-1].split(".")[0]

    @classmethod
    def get_absolute_path(cls, path: str) -> str:
        return os.path.abspath(path)

    @classmethod
    def check_path_exists(cls, path: str) -> bool:
        return os.path.exists(path)
