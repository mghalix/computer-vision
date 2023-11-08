import pytest

from src.image_props.image import Image
from src.utils.files.file_utils import FileUtils as uti


@pytest.mark.parametrize("img_path", uti.sample_images.values())
def test_initiating_image(img_path):
    assert Image(img_path)


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        Image("not_found.png")


@pytest.mark.parametrize("img_path", uti.sample_images.values())
def test_image_levels(img_path):
    assert Image(img_path, uti.ImageType.GRAYSCALE).levels == 256
    assert Image(img_path, uti.ImageType.COLOR).levels == 16777216


@pytest.mark.parametrize("img_path", uti.sample_images.values())
def test_levels_wrong_open_type(img_path):
    with pytest.raises(ValueError):
        assert Image(img_path, uti.ImageType.UNCHANGED).levels == 16777216
