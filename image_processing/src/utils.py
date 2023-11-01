import os, sys
from enum import Enum
from screeninfo import get_monitors
import logging

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    # format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    format="%(name)s::%(message)s",
)

log = logging.getLogger(__name__)

images = [
    "res/img/parrot.png",
    "res/img/dog.jpg",
    "res/img/monalisa.jpg",
    "res/img/eagle.jpg",
]


def path_exist(path: str) -> bool:
    return os.path.exists(path)


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
        return os.path.join(os.getcwd(), path)

    @classmethod
    def check_path_exists(cls, path: str) -> bool:
        return os.path.exists(path)

    @classmethod
    def get_basename_extension(cls, path: str) -> tuple:
        return os.path.splitext(path)

    @classmethod
    def create_folder(cls, path: str) -> None:
        if not cls.check_path_exists(path):
            log.info("Creating directory: " + path + " ...")
            os.mkdir(path)
        else:
            log.info(f"Directory {path} already exists.")

    # bug
    @classmethod
    def get_center_screen(cls, window):
        monitor = get_monitors()[0]
        x_center = (monitor.width - window[2]) // 2
        y_center = (monitor.height - window[2]) // 2
        return x_center, y_center
