import os
from PIL import Image
import random

templates = os.listdir("stress/")

for i in range(1000):
    img = Image.new('RGB', (640, 480), color='black')
    obj = templates[random.randint(0, len(templates) - 1)]
    temp = Image.open("stress/" + obj)
    mxposx = img.width - temp.width - 1
    mxposy = img.height - temp.height - 1
    x = random.randint(0, mxposx)
    y = random.randint(0, mxposy)
    area = (x, y, x + temp.width, y + temp.height)
    img.paste(temp, area)
    img.save("stress_images/" + str(i) + ".png")
