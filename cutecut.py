#!/usr/bin/env python

import os
import sys
import imghdr
from wand.image import Image

supported = ['jpeg', 'png', 'tiff']
exported = 'exported'


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
        return images
    except FileNotFoundError:
        _exit('"%s" doesn`t exist!' % path)
    except PermissionError as e:
        print(e)
        pass


def crop(path, image):
    filepath = os.path.join(path, exported)
    with Image(filename=image) as orig:
        if orig.width/orig.height < 1:
            print('it looks like image %s needs to be rotated...' % image)
            orig.rotate(90)
        # rotate and crop left part of image
        with orig.convert('jpeg') as img:
            img.crop(0, 0, int(img.width/2), img.height)
            img.save(filename=os.path.join(filepath, os.path.splitext(image)[0]) + '_l.jpg')
        # rotate and crop right part of image
        with orig.convert('jpeg') as img:
            img.crop(int(img.width/2), 0, img.width, img.height)
            img.save(filename=os.path.join(filepath, os.path.splitext(image)[0]) + '_r.jpg')
    return image


def convert2pdf(images):
    pass


def main():
    if len(sys.argv) < 2 or '--help' in sys.argv[1]:
        _exit("Usage:\ncutecut.py <path-to-directory>")
    else:
        path = sys.argv[1]
    if not get_images(path):
        _exit('no images in %s' % path)
    if not os.path.exists(os.path.join(path, exported)):
        os.makedirs(os.path.join(path, exported))
    for image in get_images(path):
        crop(path, image)


if __name__ == '__main__':
    main()