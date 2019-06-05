from PIL import Image
import pytesseract
import cv2
import numpy as np

def ocr_core(filename):
    print(filename)
    img = cv2.imread(filename)
    img = cv2.resize(img, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=3)
    img = cv2.erode(img, kernel, iterations=3)
    # Apply blur to smooth out the edges
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.medianBlur(img, 3)
    img = cv2.bilateralFilter(img,9,75,75)
    
    # Apply threshold to get image with only b&w (binarization)
    # img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # img = cv2.threshold(img,100,255,cv2.THRESH_BINARY)[1]
    # img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 4)
    # img = cv2.GaussianBlur(img, (5, 5), 0)

    cv2.imwrite("output.png", img)

    result = pytesseract.image_to_string(img, lang="eng")
    return result

    # text = pytesseract.image_to_string(Image.open(filename))
    # return text

# print(ocr_core("ocr-1.png"))