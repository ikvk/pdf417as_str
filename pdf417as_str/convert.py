from PIL import Image, ImageFont, ImageDraw, ImageChops, ImageOps


def to_png(string, border=10):
    """
    Create png by pdf417 text code
    * I'm sure there are more efficient solutions for create barcode png
    * I don't recommend use this function in production
    
    :param string: bar code text for pdf417 font
    :param border: white border
    :return: PIL.Image with barcode png
    """

    def trim(im):
        bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)

    image = Image.new("RGBA", (700, 500), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("pdf417.ttf", 20)  # work with 20, 21

    row_height = 6
    for i, row in enumerate(string.split('\r\n')):
        draw.text((10, 10 + row_height * i), row, (0, 0, 0), font=font)

    image = trim(image)

    # add border
    return ImageOps.expand(image, border, (255, 255, 255))
