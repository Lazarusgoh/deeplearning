import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cv2
from PIL import Image


def list_directory(path):
    if path[-1] != '/':
        path = path + '/'
    return [path + p + '/' for p in os.listdir(path)]

def get_image_onemask_paths(path, onemask=True):
    image_paths = [p + 'images/' + p.split('/')[-2] + '.png' for p in list_directory(path)]
    if onemask:
        mask_paths =  [p + 'one_mask.png' for p in list_directory(path)]
        return list(zip(image_paths, mask_paths))
    else:
        return image_paths

def get_img_mask_paths(MAIN_PATH, i):
    """
    return image file path and masks file path for i th image from sorted image folders list
    as well as the id of that img
    """
    IMG_FOLDER_PATHS = [MAIN_PATH + p for p in os.listdir(MAIN_PATH)]
    IMG_PATH = IMG_FOLDER_PATHS[i] + '/images/'
    MASK_PATHS = IMG_FOLDER_PATHS[i] + '/masks/'
    IMG_FILE_PATH = IMG_PATH + os.listdir(IMG_PATH)[0]
    MASK_FILES_PATH = [MASK_PATHS + p for p in os.listdir(MASK_PATHS)]

    return IMG_FILE_PATH, MASK_FILES_PATH, IMG_FOLDER_PATHS[i]


def create_one_mask_file(MASK_FILES_PATH, IMG_FOLDER_PATH):
    """
    This function will combine mask files into a single array
    Inputs:
        path: path of the masks directory
        target: where to save the new one mask
    """
    mask_arrays = [cv2.imread(p, cv2.IMREAD_GRAYSCALE) for p in MASK_FILES_PATH]
    zeros = np.zeros((mask_arrays[0].shape[0], mask_arrays[0].shape[1]))
    for arr in mask_arrays:
        zeros = zeros + arr
    zeros = np.dstack([zeros]*3).astype('uint8')
    im = Image.fromarray(zeros)
    im.save(IMG_FOLDER_PATH + '/one_mask.png')


def create_one_mask_arr(MASK_FILES_PATH):
    """
    This function will combine mask files into a single array
    Inputs:
        path: path of the masks directory
        target: where to save the new one mask
    """
    mask_arrays = [cv2.imread(p, cv2.IMREAD_GRAYSCALE) for p in MASK_FILES_PATH]
    zeros = np.zeros((mask_arrays[0].shape[0], mask_arrays[0].shape[1]))
    for arr in mask_arrays:
        zeros = zeros + arr

    return zeros


def show_image(image_path, one_mask_path=None, alpha=0.35, figsize=(20, 20)):

    """
    Show original image and masked image next to each other
    Input:
        image_path: path of the original image
        image_mask_arr:
    """
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    plt.figure(figsize=figsize)
    if one_mask_path is not None:
        image_mask = cv2.imread(one_mask_path, cv2.IMREAD_GRAYSCALE)
        masked_image = np.ma.masked_where(image_mask == 0, image_mask)
        plt.subplot(1, 2, 1)
        plt.imshow(image)
        plt.imshow(masked_image, cmap='cool', alpha=alpha)
        plt.subplot(1, 2, 2)
        plt.imshow(image)
        print(image_path.split('/')[-1])
        plt.show()
    else:
        plt.imshow(image)
        print(image_path.split('/')[-1])
        plt.show()

def show_image2(image_arr, mask_arr, alpha=0.35, figsize=(20, 20)):

    """
    Show original image and masked image next to each other
    Input:
        image_path: path of the original image
        image_mask_arr:
    """

    mask_arr = np.ma.masked_where(mask_arr == 0, mask_arr)
    plt.figure(figsize=figsize)
    plt.subplot(1, 2, 1)
    plt.imshow(image_arr)
    plt.imshow(mask_arr, cmap='cool', alpha=alpha)
    plt.subplot(1, 2, 2)
    plt.imshow(image_arr)
    plt.show()

