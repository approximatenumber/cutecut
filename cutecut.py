#!/usr/bin/env python

import os
import shutil
import sys
import imghdr
from wand.image import Image
from wand.display import display

supported = ['jpeg', 'png', 'tiff']
exported = 'exported'


def crop(path, image):
    with Image(filename=image) as orig:
        # rotate and crop left part of image
        with orig.convert('jpeg') as img:
            img.rotate(90)  # rotate to 270 deg
            img.crop(0, 0, int(img.width/2), img.height)
            img.save(filename='%s/%s/%s_l.jpg' % (path, exported, os.path.splitext(image)[0]))
        # rotate and crop right part of image
        with orig.convert('jpeg') as img:
            img.rotate(90)  # rotate to 270 deg)
            img.crop(int(img.width/2), 0, img.width, img.height)
            img.save(filename='%s/%s/%s_r.jpg' % (path, exported, os.path.splitext(image)[0]))
    return image


def _exit(message):
    print(message)
    raise SystemExit


def get_images(path):
    try:
        images = []
        for file in os.listdir(path):
            if (os.path.isfile(os.path.join(path, file)) and
               (imghdr.what(os.path.join(path, file)) in supported)):
                    images.append(file)
        if not images:
            _exit('no images in %s' % path)
        return images
    except FileNotFoundError as e:
        _exit('"%s" doesn`t exist!' % path)


def main():
    try:
        path = sys.argv[1]
    except IndexError as e:
        _exit("Usage:\ncutecut.py <path-to-directory>")

    if not os.path.exists(path + "/" + exported):
        os.makedirs(path + "/" + exported)
    for image in get_images(path):
        crop(path, image)


if __name__ == '__main__':
    main()