import os
from PIL import Image

HOME = os.environ['HOME']
IMAGES_PATH = HOME + '/Desktop/images'  # 图片集地址
IMAGE_SAVE_PATH = HOME + '/Desktop/merged'  # 图片转换后的地址


def main():
    resize("1.png", 0.5)


def resize(file_name, multiple):
    im = Image.open(os.path.join(IMAGES_PATH, file_name))
    w, h = im.size
    new_w, new_h = w * multiple, h * multiple
    print(w, h)
    print(new_w, new_h)
    im.resize((int(new_w), int(new_h)), Image.ANTIALIAS)
    im.save(IMAGE_SAVE_PATH, "PNG")


if __name__ == '__main__':
    main()
