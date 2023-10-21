import pytest
import numpy as np
import cv2
from image_enhancement import ImageEnhancement
from utils import images


@pytest.mark.parametrize("img_path", images)
def test_image_negative(img_path):
    ie = ImageEnhancement(img_path)
    expected = cv2.bitwise_not(ie.matrix)
    ie.image_negative()
    assert np.array_equal(ie.matrix, expected)
