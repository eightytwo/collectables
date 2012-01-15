import math
import os
import random
import re
import string
import time
from unicodedata import normalize

from flask import current_app
from flaskext.uploads import UploadSet, IMAGES
from PIL import Image

#from collection import app

PUNCT_RE = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
BASE_LIST = 'bcdfghjklmnpqrstvwxyz0123456789BCDFGHJKLMNPQRSTVWXYZ'
BASE_DICT = dict((c, i) for i, c in enumerate(BASE_LIST))

THUMB_SIZE = 80, 80
PREVIEW_SIZE = 300, 300

def debug():
    """Allows the Flask debugger to be triggered."""
    assert current_app.debug == False, "Don't panic! You're here by" \
                                       "request of debug() :)"

def get_photo_base_url():
    """Gets the base URL for the photo store."""
    photos = UploadSet('photos', IMAGES)
    return photos.url('')

def upload_photo(file_data, path, filename):
    """Uploads a photo to storage."""
    photo_set = UploadSet('photos', IMAGES)
    if photo_set:
        # Create the thumbnail and preview
        thumb = create_thumbnail(file_data.stream, THUMB_SIZE)
        preview = create_thumbnail(file_data.stream, PREVIEW_SIZE)

        # Save the full size picture and the thumbnail and preview
        try:
            photo_set.save(file_data, path, filename)
            save_image(thumb, path, 'thumb_' + filename)
            save_image(preview, path, 'preview_' + filename)
        except Exception, ex:
            raise ex

def create_thumbnail(stream, size):
    """Creates a thumbnail of an image at a specfied size."""
    # Get the width and height of the image
    img = Image.open(stream)
    width, height = img.size

    # Determine the bounds for cropping the image into a square
    if width > height:
       delta = width - height
       left = int(delta / 2)
       upper = 0
       right = height + left
       lower = height
    else:
       delta = height - width
       left = 0
       upper = int(delta / 2)
       right = width
       lower = width + upper

    # Crop the image
    img = img.crop((left, upper, right, lower))

    # Create the thumbnail
    img.thumbnail(size, Image.ANTIALIAS)

    # Rewind the position of the stream back to the beginning
    stream.seek(0)

    return img

def save_image(img, path, filename):
    """Saves an image to a specified location."""
    # Get the full path for this image
    imgdir = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], path)
    # Create the directory if it doesn't exist
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)

    # Save the image
    try:
        img.save(os.path.join(imgdir, filename), 'JPEG')
    except Exception, ex:
        raise ex

def remove_image(path, filename):
    """Removes an image and its thumbnails/preview from disk."""
    # Get the full path for this image
    imgdir = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], path)
    try:
        os.remove(os.path.join(imgdir, filename))
        os.remove(os.path.join(imgdir, 'thumb_' + filename))
        os.remove(os.path.join(imgdir, 'preview_' + filename))
    except Exception, ex:
        raise ex

def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in PUNCT_RE.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))

def uniqid(prefix='', more_entropy=False):
    """A function to generate a short uniqe id, copied from
    http://gurukhalsa.me/2011/uniqid-in-python/
    """
    m = time.time()
    uniqid = '%8x%05x' %(math.floor(m),(m-math.floor(m))*1000000)
    if more_entropy:
        valid_chars = list(set(string.hexdigits.lower()))
        entropy_string = ''
        for i in range(0,10,1):
            entropy_string += random.choice(valid_chars)
        uniqid = uniqid + entropy_string
    uniqid = prefix + uniqid
    return uniqid

def b62decode(string, reverse_base=BASE_DICT):
    """Decodes a base62 value to a bae10 integer.
    Source: http://stackoverflow.com/questions/1119722/base-62-conversion-in-python/2549514#2549514
    """
    length = len(reverse_base)
    ret = 0
    for i, c in enumerate(string[::-1]):
        try:
            ret += (length ** i) * reverse_base[c]
        except KeyError:
            pass

    return ret

def b62encode(integer, base=BASE_LIST):
    """Encodes a base10 integer to a base32 string.
    Source: http://stackoverflow.com/questions/1119722/base-62-conversion-in-python/2549514#2549514
    """
    length = len(base)
    ret = ''
    while integer != 0:
        ret = base[integer % length] + ret
        integer /= length

    return ret
