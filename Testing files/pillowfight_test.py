import pillowfight # pylint: disable=import-error
import PIL  # pylint: disable=import-error
import pytesseract  # pylint: disable=import-error

img = PIL.Image.open("static/uploads/IMG-20190602-WA0119.jpg")
# out = img
out = img.resize(tuple(i * 2 for i in img.size), PIL.Image.LANCZOS)
process = True
if process:
    out = pillowfight.ace(img, slope=10,
        limit=1000,
        samples=100,
        seed=None
        )

    # Canny edge detection
    # out = pillowfight.canny(out)

    # Gaussian blur
    # out = pillowfight.gaussian(out, sigma=2.0, nb_stddev=5)

    # sobel
    # out = pillowfight.sobel(out)

    # Stroke Width Transform
    # SWT_OUTPUT_BW_TEXT = 0  # default
    # SWT_OUTPUT_GRAYSCALE_TEXT = 1
    # SWT_OUTPUT_ORIGINAL_BOXES = 2
    out = pillowfight.swt(out, output_type=2)

    #unpaper
    out = pillowfight.unpaper_blackfilter(out)
    out = pillowfight.unpaper_blurfilter(out)
    out = pillowfight.unpaper_border(out)
    # out = pillowfight.unpaper_grayfilter(out) #adds white rectangles?
    out = pillowfight.unpaper_masks(out)
    out = pillowfight.unpaper_noisefilter(out)


print(pytesseract.image_to_string(out))

out.save("out.png")