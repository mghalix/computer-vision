from __future__ import annotations

import cv2
import numpy as np

from src.utils.image_utils import ImageUtils as iuti


class Image:
    def __init__(self, path: str, open_type=iuti.ImageType.GRAYSCALE) -> None:
        """Initializes an ImageEnhancement object.

        Args:
            path (str): The path to the image file.
            open_type (ImageType): The type of the image, either grayscale or color.
        """
        self.path = iuti.get_absolute_path(path)
        if not iuti.path_exist(path):
            raise FileNotFoundError(f"File {path} does not exist")
        self.open_type = open_type
        self.cv = cv2.imread(path, open_type.value)
        self.matrix = np.array(self.cv).astype(np.uint8)
        self.name = iuti.extract_file_name(path)

    @property
    def levels(self) -> int:
        """returns the maximum of levels in an image, e.g. range 0 -> 255 of grayscale is 256 levels

        Return: 256
        """
        # return self.cv.max() + 1  # from 0 to 255 so 256 levels
        if self.open_type == iuti.ImageType.GRAYSCALE:
            return 256
        elif self.open_type == iuti.ImageType.COLOR:
            return 256**3
        else:
            raise ValueError(f"Unknown open_type: {self.open_type}")

    def __eq__(self, o: object) -> bool:
        """Checks if two images are equal.

        Args:
            o (object): The other image to compare with.

        Returns:
            bool: True if equal, False otherwise.
        """
        if not isinstance(o, Image) or self.matrix.shape != o.matrix.shape:
            return False

        return np.array_equal(self.matrix, o.matrix)

    def update(self) -> None:
        """Responsible for updating the image cv attribute from a modified matrix"""

        self.cv = self.matrix.copy()

    def copy(self) -> Image:
        """
        Returns a new Image object that is a copy of the current image.
        """
        new = Image(self.path, self.open_type)
        new.matrix = self.matrix
        new.cv = self.cv
        new.name = self.name
        return new

    def __len__(self) -> int:
        return len(self.matrix)

    @property
    def resolution(self) -> tuple[int, int]:
        """Returns the resolution of the image.

        Returns:
            tuple: The resolution of the image.
        """
        m, n = self.matrix.shape
        return (m, n)
