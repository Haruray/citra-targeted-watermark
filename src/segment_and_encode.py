import cv2
import numpy as np
from PIL import Image
from stego_lsb import encode_lsb_image, decode_lsb_image


def segment_and_encode(image, size, secret, lsb_bit_length=1):
    # secret to pil
    # secret = cv2.cvtColor(secret, cv2.COLOR_BGR2RGB)
    secret = Image.fromarray(secret)
    # resize image
    image = cv2.resize(image, (size, size))
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray_img, (5, 5), 0)
    blurred = cv2.GaussianBlur(blurred, (5, 5), 0)

    edges = cv2.Canny(blurred, 50, 150)

    dilated = cv2.dilate(edges, None, iterations=1)

    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_contour_area = 2000  # subject to change
    filtered_contours = [
        cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area
    ]
    # Create a mask for each object and extract it
    for i, cnt in enumerate(filtered_contours):
        # object_mask = np.zeros_like(gray_img)
        # cv2.drawContours(object_mask, [cnt], -1, 255, thickness=cv2.FILLED)
        x, y, w, h = cv2.boundingRect(cnt)

        # crop the image based on coordinates
        object_image = image[y : y + h, x : x + w]

        # object_image_pil = cv2.cvtColor(object_image, cv2.COLOR_BGR2RGB)
        object_image_pil = Image.fromarray(object_image)
        # encode image with secret
        object_image_encoded = encode_lsb_image(
            object_image_pil, secret, f"watermarked_image{i}.png", lsb_bit_length
        )
        # object_image_encoded to cv2
        # object_image_encoded = cv2.cvtColor(
        #     np.array(object_image_encoded), cv2.COLOR_RGB2BGR
        # )
        object_image_encoded = np.array(object_image_encoded)
        object_image_encoded = cv2.cvtColor(object_image_encoded, cv2.COLOR_BGR2RGB)
        # in the original image, the extracted object_image shall be replaced with object_image_encoded
        # replace object_image with object_image_encoded

        image[y : y + h, x : x + w] = object_image_encoded

        # bounding box and text
    return image


# img = cv2.imread("2.png")
# watermark = cv2.imread("kagurabachi.jpg")
# watermark = cv2.resize(watermark, (500, 500))
# output = segment_and_encode(img, 500, watermark)
# cv2.imwrite("output.png", output)
