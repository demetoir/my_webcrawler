from PIL import Image
from PIL import ImageDraw
import math


def draw_dizzy_circle(img, center, r):
    X = 0
    Y = 1
    value = (0, 0, 0)
    step = 1.0/3 + 0.01

    angle = 0.0
    while angle < 360:
        x = int(math.cos(math.radians(angle)) * r) + center[X]
        y = int(math.sin(math.radians(angle)) * r) + center[Y]
        print(angle,math.radians(angle), x, y)
        img.putpixel((x, y), value)

        angle += step
    return img


def img_set_background(img, value):
    for i in range(IMG_SIZE):
        for j in range(IMG_SIZE):
            img.putpixel((i, j), value)
    return img


IMG_SIZE = 512
if __name__ == '__main__':
    img = Image.new('RGB', size=(IMG_SIZE, IMG_SIZE))
    img = img_set_background(img, (256, 256, 256))
    img = draw_dizzy_circle(img, (256, 256), 100)
    img.show()
    pass
