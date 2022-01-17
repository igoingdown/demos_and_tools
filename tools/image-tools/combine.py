import os
from PIL import Image


def combine(config):
    file_names = image_file_names_in_dir(config)
    file_names.sort()
    new_sizes, total_hight = unify_image_width(config, file_names)
    resize_and_combine(config, file_names, new_sizes, total_hight)


def image_file_names_in_dir(config):
    return [name for name in os.listdir(config["image_path"]["source"]) for item in config["image_formats"] if os.path.splitext(name)[1] == item]


def unify_image_width(config, file_names):
    new_sizes = []
    h_sum = 0
    for name in file_names:
        im = Image.open(os.path.join(config["image_path"]["source"], name))
        w, h = im.size
        print(name, w, h)
        w_percent = (config["image_size"]["width"]/float(w))
        new_h = int(h * w_percent)
        h_sum += new_h
        new_sizes.append((config["image_size"]["width"], new_h))
    return new_sizes, h_sum


def resize_and_combine(config, file_names, new_sizes, total_hight):
    new_im = Image.new('RGB', (config["image_size"]["width"], total_hight))
    copy_pos_down = 0
    assert len(file_names) == len(new_sizes)
    for i in range(len(file_names)):
        im = Image.open(os.path.join(config['image_path']['source'], file_names[i])).resize((new_sizes[i][0], new_sizes[i][1]), Image.ANTIALIAS)
        new_im.paste(im, (0, copy_pos_down))
        copy_pos_down += new_sizes[i][1]
    new_im.save(config["image_path"]["dest"], "JPEG")
