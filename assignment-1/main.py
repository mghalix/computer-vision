# Read an image and get its matrix
import cv2


def open_image(path: str, flag: int):
    return cv2.imread(path, flag)


def show_image(img):
    cv2.imshow("image", img)
    cv2.waitKey(0)


def get_image_matrix(img) -> str:
    return str(img)


def free_memory() -> None:
    cv2.destroyAllWindows()


#  1 [cv2.IMREAD_COLOR] -> COLOR (default flag)
#  0 [cv2._IMREAD_GRAYSCALE] -> Grayscale
# -1 [cv2_IMREAD_UNCHANGED] -> Reads alpha channels
img = open_image("./img/grayscale-dog.jpg", 0)

print(get_image_matrix(img))

show_image(img)
free_memory()

# Press 0 to terminate the program
