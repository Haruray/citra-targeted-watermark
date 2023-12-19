from PIL import Image
import numpy as np

def encode_lsb_image(
    image: Image, secret: Image, output_path: str, lsb_bit_length: int = 1
):
    secret = secret.resize(image.size)
    output = Image.new("RGB", image.size)

    # rgb
    image = image.convert("RGB")
    secret = secret.convert("RGB")

    image_data = image.getdata()
    secret_data = secret.getdata()

    # encode lsb
    for i in range(len(image_data)):
        image_pixel = image_data[i]
        watermark_pixel = secret_data[i]

        r, g, b = watermark_pixel

        # modify lsb of image pixel
        bits_retained = (0xFF << lsb_bit_length) & 0xFF
        info_bits_length = 8 - lsb_bit_length
        new_r = (image_pixel[0] & bits_retained) | (r >> info_bits_length)
        new_g = (image_pixel[1] & bits_retained) | (g >> info_bits_length)
        new_b = (image_pixel[2] & bits_retained) | (b >> info_bits_length)

        # new pixel
        new_pixel = (new_r, new_g, new_b)
        output.putpixel((i % image.width, i // image.width), new_pixel)

    # output.save(output_path)
    return output


def decode_lsb_image(encoded_image: Image, output_path: str):
    # extract watermark from watermarked image
    encoded_image_data = encoded_image.getdata()
    secret_data = []
    for i in range(len(encoded_image_data)):
        encoded_pixel = encoded_image_data[i]
        watermark_pixel = (encoded_pixel[0] & 0x01) << 7
        secret_data.append(watermark_pixel)
    secret = Image.new("L", encoded_image.size)
    secret.putdata(secret_data)
    secret.save(output_path)
    print(f"Watermark saved to: {output_path}")


# Example usage of the watermark_image function:

# Watermark an image using a watermark image
# image_path = "1.png"
# watermark_path = "kagurabachi.jpg"
# output_path = "watermarked_image.png"
# image = Image.open(image_path)
# watermark = Image.open(watermark_path)
# encode_lsb_image(image, watermark, output_path)
# decode_lsb_image(Image.open(output_path), "watermark.png")
# print(f"Watermarked image saved to: {output_path}")
