import cv2
import numpy as np
from utils import ImageType, images, Utils as uti


class ImageEnhancement:
    def __init__(
        self, img_path: str, open_type: ImageType = ImageType.GRAYSCALE
    ) -> None:
        self.img_path = img_path
        self.open_type = open_type
        self.image = cv2.imread(img_path, open_type.value)
        self.matrix = np.array(self.image)
        self.filters = []

    def get_levels(self) -> int:
        return self.image.max() + 1  # from 0 to 255 so 256 levels

    def filters_applied(self) -> int:
        """filters amount

        Keyword arguments:
        Return: the amount of filters applied on the image
        """

        return len(self.filters)

    # A great use for this is the airport's baggage check-in conveyor which sees
    # inside of the bag is dark so it's better if we invert those to focus on the items
    def image_negative(self) -> None:
        L = self.get_levels()
        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[row])):
                self.matrix[row][col] = (L - 1) - self.matrix[row][col]

        flag = "negative"
        if self.filters_applied() == 0:
            self.filters.append(flag)
            return

        # if the previous filter was the same filter as this
        # then they're just going to cancel each other
        if self.filters[-1] == flag:
            self.filters.pop()

    def show(self) -> None:
        name = f"{uti.extract_file_name(self.img_path).capitalize()} Image Negative"
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        window = cv2.getWindowImageRect(name)
        cv2.moveWindow(name, *uti.get_center_screen(window))  # bug
        cv2.imshow(name, self.matrix)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def stretch_contrast(self):
        # r1 > s1 & r2 < s2
        r1 = 50
        r2 = 200
        s1 = 30
        s2 = 240

        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[0])):
                curr = self.matrix[row][col]
                if curr <= r1:
                    self.matrix[row][col] = curr * s1 / r1

                elif curr <= r2:
                    m = (s2 - s1) / (r2 - r1)
                    self.matrix[row][col] = curr * m + s1 - r1 * m

                else:
                    L = np.max(self.matrix) + 1  # 256
                    m = ((L - 1) - s2) / ((L - 1) - r2)
                    self.matrix[row][col] = (
                        curr * m + (L - 1) - (L - 1) * (L - s2) / (L - r2)
                    )

        self.filters.append("contrast_stretched")

    def contract_contrast(self):
        # r1 < s1 & r2 > s2
        r1 = 30
        r2 = 240
        s1 = 50
        s2 = 200

        for row in range(len(self.matrix)):
            for col in range(len(self.matrix[0])):
                curr = self.matrix[row][col]
                if curr <= r1:
                    self.matrix[row][col] = curr * s1 / r1

                elif curr <= r2:
                    m = (s2 - s1) / (r2 - r1)
                    self.matrix[row][col] = curr * m + s1 - r1 * m

                else:
                    L = np.max(self.matrix) + 1  # 256
                    m = ((L - 1) - s2) / ((L - 1) - r2)
                    self.matrix[row][col] = (
                        curr * m + (L - 1) - (L - 1) * (L - s2) / (L - r2)
                    )

        self.filters.append("contrast_contracted")

    def save_img(self) -> None:
        out = f"./filtered/{uti.extract_file_name(self.img_path)}"

        for i in range(self.filters_applied()):
            out += "_" + self.filters[i]

        cv2.imwrite(f"{out}.png", self.matrix)

    def reset(self) -> None:
        """Resets the image back to the original

        Keyword arguments:
        Return: None
        """
        self.matrix = np.array(self.image)


def main():
    ie = ImageEnhancement(images[2], ImageType.GRAYSCALE)
    # ie.image_negative()
    # ie.image_negative()
    # ie.stretch_contrast()
    # ie.contract_contrast()
    # ie.save_img()
    # ie.show()


if __name__ == "__main__":
    main()
