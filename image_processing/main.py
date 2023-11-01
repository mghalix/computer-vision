from src.utils import ImageType, images
from src.image_enhancement import ImageEnhancement


def main():
    ie = ImageEnhancement(images[2], ImageType.GRAYSCALE)
    ie.image_negative()
    # ie.image_negative()

    # ie.image_negative()
    # ie.image_negative()
    # ie.image_negative()
    ie.save_img()
    # ie.show()


if __name__ == "__main__":
    main()
