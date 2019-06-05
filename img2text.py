import cv2
from numpy import ones, uint8
from pytesseract import image_to_string

# Path of working folder on Disk

def ocr_core(img_path):
    #Read image with opencv
    img = cv2.imread(img_path)
    height, width = img.shape[:2]
    if height<1000 or width<1000:
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = ones((1, 1), uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write the image after apply opencv
    cv2.imwrite("outs.png", img)

    # Recognize text with tesseract for python
    result = image_to_string(img)

    return result