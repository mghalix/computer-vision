import cv2
import numpy as np
from utils import ImageType, images, Utils as uti


class ImageEnhancement:
    def __init__(self, img_path: str, open_type=ImageType.GRAYSCALE) -> None:
        """Initializes an ImageEnhancement object.

        Args:
            img_path (str): The path to the image file.
            img_type (ImageType): The type of the image, either grayscale or color.
        """
        self.img_path = img_path
        self.open_type = open_type
        self.image = cv2.imread(img_path, open_type.value)
        self.matrix = np.array(self.image)
        self.filters = []

    def get_levels(self) -> int:
        """returns the range of levels in an image, e.g. 0 -> 255

        Return:
            int: The range of levels in an image.
        """

        return self.image.max() + 1  # from 0 to 255 so 256 levels

    def filters_applied(self) -> int:
        """Returns the amount of filters applied on the image.

        Returns:
            int: The amount of filters applied on the image.
        """

        return len(self.filters)

    def show(self) -> None:
        """Displays the image on a named window.

        Returns:
            None
        """

        name = f"{uti.extract_file_name(self.img_path).capitalize()} - {self.filters_applied()} filters applied"
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        window = cv2.getWindowImageRect(name)
        cv2.moveWindow(name, *uti.get_center_screen(window))  # bug
        cv2.imshow(name, self.matrix)
        cv2.waitKey(0)

        cv2.destroyAllWindows()

    def save_img(self) -> None:
        """Saves the filtered image to a file.

        Returns:
            None
        """
        out = f"./filtered/{uti.extract_file_name(self.img_path)}"

        for i in range(self.filters_applied()):
            out += "_" + self.filters[i]

        cv2.imwrite(f"{out}.png", self.matrix)

    def reset(self) -> None:
        """Resets the image back to the original

        Return: None
        """
        self.matrix = np.array(self.image)

    def _inside_range(self, number: int, range: tuple) -> bool:
        """Checks if a number is inside a given range.

        Args:
            number (int): The number to check.
            range (tuple): A tuple representing the range to check.

        Returns:
            bool: True if the number is inside the range, False otherwise.
        """
        return number > range[0] and number < range[1]

    def gray_level_slicing(
        self, range: tuple[int, int], type: str = "highlight"
    ) -> None:
        """Gray level slicing is used to highlight a certain color in an image
        by setting all other colors to black

        Keyword arguments:
        range -- the range of colors to highlight
        type -- the type of highlighting, either "highlight" or "darken"
        """
        color = 0 if type == "darken" else self.get_levels() - 1
        # for row in range(len(self.matrix)):
        #     for col in in range(len(self.matrix[1])):
        for (row, col), pixel in np.ndenumerate(self.matrix):
            if not self._inside_range(pixel, range):
                continue
            self.matrix[row][col] = color

        self.filters.append("gray_level_slicing")

    def _plane(self, number: int) -> int:
        """Returns the plane of a number.

        Args:
            number (int): The number to get the plane of.

        Returns:
            int: The plane of the number.
        """

        # return np.bitwise_not(1 << number)
        return ~(1 << number)

    def apply_plane(self, pixel: int, planes: list[int]) -> None:
        """Applies a mask to a pixel.

        Args:
            pixel (int): The pixel to apply the mask to.
            planes (list): A list of planes to apply to the pixel.

        Returns:
            None
        """

        for plane in planes:
            pixel &= self._plane(plane)

        return pixel

    def bit_plane_slicing(self, plane: int) -> None:
        """Bit plane slicing is used to highlight a certain bit in an image
        by setting all other bits to black

        Keyword arguments:
        bit -- the bit to highlight
        """
        planes = list(range(plane, 8))
        print(planes)
        for (row, col), pixel in np.ndenumerate(self.matrix):
            self.matrix[row][col] = self.apply_plane(pixel, planes)

        self.filters.append("bit_plane_slicing")


def main():
    ie = ImageEnhancement(images[4], ImageType.GRAYSCALE)
    ie.image_negative()
    # ie.stretch_contrast(20)
    # ie.contract_contrast(20)
    # ie.save_img()
    # ie.gray_level_slicing((100, 115), "darken")
    ie.bit_plane_slicing(4)
    ie.show()


if __name__ == "__main__":
    main()
