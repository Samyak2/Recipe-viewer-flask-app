import cv2
from numpy import ones, uint8
from pytesseract import image_to_string
from PIL import Image
import tempfile

# Path of working folder on Disk

IMAGE_SIZE = 1800
BINARY_THREHOLD = 180

size = None


def get_size_of_scaled_image(im):
    global size
    if size is None:
        length_x, width_y = im.size
        factor = max(1, int(IMAGE_SIZE / length_x))
        size = factor * length_x, factor * width_y
    return size


def process_image_for_ocr(file_path):
    temp_filename = set_image_dpi(file_path)
    im_new = remove_noise_and_smooth(temp_filename)
    return im_new


def set_image_dpi(file_path):
    im = Image.open(file_path)
    # size = (1800, 1800)
    size = get_size_of_scaled_image(im)
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    im_resized = im_resized.convert("RGB")
    im_resized.save(temp_filename, dpi=(300, 300))  # best for OCR
    return temp_filename


def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3


def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name, 0)
    _,filtered = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)#cv2.adaptiveThreshold(img.astype(uint8), 255, cv2.THRESH_OTSU, cv2.THRESH_BINARY, 41, 3)
    kernel = ones((1, 1), uint8)
    opening = cv2.morphologyEx(filtered.astype(uint8), cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image


def ocr_core(img_path):
    #Read image with opencv
    img = cv2.imread(set_image_dpi(img_path))
    # height, width = img.shape[:2]
    # if height<1000 or width<1000:
    #     img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = ones((1, 1), uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # img = remove_noise_and_smooth(img_path)
    # Write the image after apply opencv
    cv2.imwrite("outs.png", img)

    # Recognize text with tesseract for python
    result = image_to_string(img, lang="eng", config='--psm 3')
    whitelist = "/ %-\"'',.\n()"
    # result = str(i for i in result if i.isalpha() or i.isdigit() or i in whitelist)
    result = "".join(i for i in result if i.isalpha() or i.isdigit() or i in whitelist)

    return result

if __name__ == "__main__":
    print(ocr_core(r"static\uploads\WhatsApp Image 2019-08-03 at 7.02.47 PM.jpeg"))