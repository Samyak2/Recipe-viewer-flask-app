import cv2
import numpy as np
import pytesseract
from PIL import Image

# Path of working folder on Disk

def ocr_core(img_path):
    #Read image with opencv
    img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write image after removed noise
    # cv2.imwrite("removed_noise.png", img)

    # Apply threshold to get image with only black and white
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    # cv2.imwrite("thres.png", img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open("thres.png"))

    # Remove template file
    #os.remove(temp)

    return result

# print("--- Start recognize text from image ---")
# print(get_string(r"static/uploads/test4.jpeg"))

# print("------ Done -------")