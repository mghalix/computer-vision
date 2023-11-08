import logging
import sys

import cv2
import numpy as np

from src.image_enhancement.filters.filters import Filter
from src.image_enhancement.ie import Contrast, ImageEnhancement

# from src.connectivity import Connectivity
from src.image_props.image import Image
from src.image_props.image_stats import ImageStatistics
from src.utils.files.file_utils import FileUtils as uti
from src.utils.image_enhancement.filters.linear.kernels import KERNEL_DICT, KernelName

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(name)s - %(message)s",
)

# to prevent getting DEBUG messages from the following libraries
logging.getLogger("PIL").setLevel(logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)


def main():
    # img = Image(uti.sample_images["eagle"], uti.ImageType.GRAYSCALE)
    # ie = ImageEnhancement(img)
    # ie.show()
    # ie.save_img()

    print(KERNEL_DICT[KernelName.GAUSSIAN])
    print(KERNEL_DICT[KernelName.GAUSSIAN]["3x3"])
    print(KERNEL_DICT[KernelName.GAUSSIAN]["5x5"])


if __name__ == "__main__":
    main()
