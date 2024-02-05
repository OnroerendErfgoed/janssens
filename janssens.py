#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Janssens. Find duplicate images in a folder
'''
import os
import glob

from wand.image import Image
from wand.exceptions import CorruptImageError
from wand.exceptions import CoderError
import dhash

import datetime
import logging

FILENAME_LOG = f"janssens_{datetime.datetime.now()}.log"
logging.basicConfig(
    filename=FILENAME_LOG,
    filemode='w',
    level=logging.INFO
)

FOLDER = './fixtures'

THRESHOLD = 75

DHASHES = []

def main():
    for filename in glob.iglob(FOLDER + '**/**', recursive=True):
        if not os.path.isfile(filename):
            continue
        dhash, height, width = get_hash_height_width(filename)
        if dhash:
            DHASHES.append({
            'filename': filename,
            'dhash': dhash,
            'height': height,
            'width': width
            })
    for image in DHASHES:
        title = f'{image["filename"]} ({image["height"]}*{image["width"]})'
        print(title)
        print('='*len(title))
        match_score, match_image = get_best_match(image)
        if match_score:
            print(f'{match_score} match: {match_image["filename"]} ({match_image["height"]}*{match_image["width"]})')
        else:
            print(f'No match found')
        print()

def get_hash_height_width(image_path):
    if not os.path.exists(image_path):
        logging.error(f'Image {image_path} does not exist')
        return None, None, None
    try:
        with Image(filename=image_path) as f:
            image_binary = f.make_blob()
    except (CorruptImageError, CoderError) as e:
        logging.error(f"{e} for {image_path}")
        return None, None, None
    with Image(blob=image_binary) as img:
        try:
            image_hash = dhash.dhash_int(img)
        except IndexError as e:
            logging.error(f"{e} for {image_path}")
            return None, None, None
        return image_hash, img.height, img.width

def calculate_dhash_match(query_hash, image_hash):
    '''
    Calculate the similarity between two hashes
    '''
    return (128 - dhash.get_num_bits_different(
        query_hash, image_hash)) / 128 * 100

def get_best_match(image):
    '''
    Find best match for this image
    '''
    query_hash = image['dhash']
    best_match_score = 0
    best_match_image = None
    for dhash_row in DHASHES:
        # Skip the image itself
        if image['filename'] == dhash_row['filename']:
            continue
        image_hash = dhash_row['dhash']
        match = calculate_dhash_match(int(query_hash), int(image_hash))
        if match == 100:
            logging.warning(f'Found exact match for {query_hash}')
        if match > best_match_score:
            best_match_score = match
            best_match_image = dhash_row
    if best_match_score < THRESHOLD:
        best_match_score = 0
        best_match_image = None
    return (best_match_score, best_match_image)

if __name__ == "__main__":
    main()
