import cv2
import numpy as np
import pytest

from src.image_enhancement.filters import Filter
from src.image_enhancement.ie import ImageEnhancement
from src.image_props.image import Image
from src.utils.image_utils import ImageUtils as uti


@pytest.mark.parametrize("img_path", uti.sample_images.values())
def test_image_negative(img_path):
    ie = ImageEnhancement(Image(img_path))
    expected = cv2.bitwise_not(ie.img.matrix)
    ie.image_negative()
    assert np.array_equal(ie.img.matrix, expected)


@pytest.mark.parametrize("img_path", uti.sample_images.values())
def test_stretch_contrast(img_path):
    ie = ImageEnhancement(Image(img_path))
    expected = ie.img.matrix
    ie.stretch_contrast(0)
    assert np.array_equal(ie.img.matrix, expected)


@pytest.mark.parametrize("img_path", uti.sample_images.values())
def test_histogram_equalization_in_range_vs_full_range(img_path):
    ie = ImageEnhancement(Image(img_path))
    full_range_matrix = ie.histogram_equalization().img.matrix

    in_range_of_full_range_matrix = ie.histogram_equalization(
        range=(np.uint8(0), np.uint8(255))
    ).img.matrix

    assert np.array_equal(full_range_matrix, in_range_of_full_range_matrix)


def test_image_subtraction():
    img1 = Image(uti.sample_images["eagle"])
    img2 = Image(uti.sample_images["eagle2"])
    subtract = cv2.subtract(img1.cv, img2.cv)
    ie = ImageEnhancement(img1)
    ie.image_subtracting(img2)
    assert np.array_equal(subtract, ie.img.matrix)
