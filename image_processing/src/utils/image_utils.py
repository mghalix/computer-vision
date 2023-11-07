import logging
import os
from enum import Enum

from screeninfo import get_monitors

log = logging.getLogger(__name__)


class ImageUtils:
    class ImageType(Enum):
        GRAYSCALE = 0
        UNCHANGED = -1
        COLOR = 1

    sample_images = {
        "parrot": "res/img/parrot.png",
        "dog": "res/img/dog.jpg",
        "monalisa": "res/img/monalisa.jpg",
        "eagle": "res/img/eagle.jpg",
        "coins": "res/img/coins.webp",
        "white_noise_img": "res/img/white_noise_img.png",
        "eagle2": "res/img/eagle2.jpg",
    }

    @staticmethod
    def path_exist(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def extract_file_name(path: str) -> str:
        return path.split("/")[-1].split(".")[0]

    @staticmethod
    def get_absolute_path(path: str) -> str:
        return os.path.join(os.getcwd(), path)

    @staticmethod
    def check_path_exists(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def get_basename_extension(path: str) -> tuple[str, str]:
        basename, extension = os.path.splitext(path)
        basename = ImageUtils.extract_file_name(basename)
        return (basename, extension)

    @staticmethod
    def create_folder(path: str) -> str:
        if ImageUtils.check_path_exists(path):
            log.debug(f"Directory {path} already exists.")
            return path

        log.info("Creating directory: " + path + " ...")
        os.mkdir(path)
        return path

    # bug
    @staticmethod
    def get_center_screen(window):
        monitor = get_monitors()[0]
        x_center = (monitor.width - window[2]) // 2
        y_center = (monitor.height - window[2]) // 2
        return x_center, y_center

    @staticmethod
    def image_title(name) -> str:
        basename, _ = ImageUtils.get_basename_extension(name)
        return " ".join(basename.split("_")).title()
