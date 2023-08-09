import os.path as op
from io import BytesIO
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import time

font = ImageFont.truetype(
    op.join(op.dirname(__file__), "./JF-Dot-jiskan24h.ttf"), 100
)


def pil2cv(img):
    return cv2.cvtColor(np.array(img, dtype=np.uint8), cv2.COLOR_RGB2BGR)


def cv2pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def gen(text):
    img = Image.new("RGB", (0, 0), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    size = draw.textbbox((0, 0), text, font=font)[2:]
    img = Image.new("RGB", size, (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, (253, 126, 0), font=font)
    img = pil2cv(img)
    blank_x = np.zeros((img.shape[0], img.shape[0] * 10, 3), np.uint8)
    img = np.hstack((blank_x, img, blank_x))
    blank_y = np.zeros((10, img.shape[1], 3), np.uint8)
    img = np.vstack((blank_y, img, blank_y))
    xs = np.arange(0, size[0] + size[1] * 10, int(size[1] / 10))

    def make_frame(x):
        frame = cv2pil(img[:, x:x + img.shape[0] * 10, :])
        return frame

    frames = np.frompyfunc(make_frame, 1, 1)(xs)
    buff = BytesIO()
    frames[0].save(buff, format="GIF", save_all=True, append_images=frames[1:], loop=0)
    return buff


if __name__ == "__main__":
    start = time.perf_counter()
    data = gen("Hello, world").getvalue()
    print(f"{time.perf_counter() - start}s")
    with open("out.gif", "wb") as f:
        f.write(data)
