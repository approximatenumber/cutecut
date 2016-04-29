#!/usr/bin/env python

import os
import sys
import _imghdr as imghdr
from wand.image import Image

supported = ['jpeg', 'png', 'tiff']
exported = 'exported'


def _exit(message):
    print(message)
    raise SystemExit


def find_images(path):
    try:
        images = []
        for file in os.listdir(path):
            if (os.path.isfile(os.path.join(path, file)) and
               (imghdr.what(os.path.join(path, file)) in supported)):
                    images.append(file)
        return sorted(images)
    except FileNotFoundError:
        _exit('"%s" doesn`t exist!' % path)
    except PermissionError as e:
        print(e)
        pass


def crop(path, images):
    for image in images:
        with Image(filename=os.path.join(path, image)) as orig:
            if orig.width/orig.height < 1:
                print('It looks like image %s needs to be rotated...' % image)
                orig.rotate(90)
            # rotate and crop left part of image
            with orig.convert('jpeg') as img:
                img.crop(0, 0, int(img.width/2), img.height)
                img.save(filename=os.path.join(path, exported, os.path.splitext(image)[0]) + '_l.jpg')
            # rotate and crop right part of image
            with orig.convert('jpeg') as img:
                img.crop(int(img.width/2), 0, img.width, img.height)
                img.save(filename=os.path.join(path, exported, os.path.splitext(image)[0]) + '_r.jpg')
    return images


def convert2pdf(path, images):
    img = Image()
    for image in images:
        img.read(filename=os.path.join(path, image))
    img.compression_quality = 75
    img.save(filename=os.path.join(path, 'exported.pdf'))
    return path


def ask(question):
    print(question)
    answer = str(input())
    return answer


def main():
    if len(sys.argv) < 2 or '--help' in sys.argv[1]:
        _exit("Usage:\n%s <path-to-directory>" % sys.argv[0])
    else:
        path = sys.argv[1]

    if not find_images(path):
        _exit('No images in %s.' % path)

    if not os.path.exists(os.path.join(path, exported)):
        os.makedirs(os.path.join(path, exported))

    exp_path = os.path.join(path, exported)
    images = find_images(path)
    print('Founded images in %s: \n%s' % (path, '\n'.join(images)))
    crop(path, images=images)

    a = ask('\nConvert cropped images to PDF? y/n')

    if a == 'y':
        convert2pdf(path=exp_path, images=find_images(exp_path))
        _exit('Done.')
    elif a == 'n':
        _exit('Skipped converting.')
    else:
        _exit('Skipped converting.')

if __name__ == '__main__':
    main()