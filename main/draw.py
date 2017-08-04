from PIL import Image
from PIL import ImageDraw
import math
import random


def draw_dizzy_circle(img, centerXY, radius, value=None):
    if value is None:
        value = [0, 0, 0]

    R, G, B = 0, 0, 0
    R_step, G_step, B_step = 5, 6, 7

    thickness = 60
    turn = 700
    step = 1.0 / 3 + 0.01
    angle = 0.0

    while angle < 360 * turn:
        # r = radius + random.randint(-thickness, thickness)
        r = radius + math.sin(angle / 100) * thickness
        x = int(math.cos(math.radians(angle)) * r) + centerXY[0]
        y = int(math.sin(math.radians(angle)) * r) + centerXY[1]

        print(r)
        value[0] = (value[0] + R_step) % 255
        value[1] = (value[1] + G_step) % 255
        value[2] = (value[2] + B_step) % 255

        img.putpixel((x, y), value=(value[0], value[1], value[2]))
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
