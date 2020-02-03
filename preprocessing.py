import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import Image
import cv2
import os
import pickle
from random import shuffle
import operator
from skimage import io


class Preprocess:
    """
    Class based preprocessing functions to transform, resize, and
    change images to be passed on for predictions to the model
    """

    def __init__(self, img):

        self.img = img

    def pre_process_image(img, skip_dilate=False):
        """Uses a blurring function, adaptive thresholding and dilation to expose the main features of an image."""
        # Gaussian blur with a kernal size (height, width) of 9.
        # Note that kernal sizes must be positive and odd and the kernel must
        # be square.
        proc = cv2.GaussianBlur(img.copy(), (9, 9), 0)
        # Adaptive threshold using 11 nearest neighbour pixels
        proc = cv2.adaptiveThreshold(
            proc,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            11,
            2)
        # Invert colours, so gridlines have non-zero pixel values.
        # Necessary to dilate the image, otherwise will look like erosion
        # instead.
        proc = cv2.bitwise_not(proc, proc)
        # if not skip_dilate:
        #    # Dilate the image to increase the size of the grid lines.
        #    kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]])
        #    proc = cv2.dilate(proc, kernel)
        return proc

    def find_corners_of_largest_polygon(img):
        """Finds the 4 extreme corners of the largest contour in the image."""
        contours, h = cv2.findContours(
            img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find contours
        contours = sorted(
            contours,
            key=cv2.contourArea,
            reverse=True)  # Sort by area, descending
        polygon = contours[0]  # Largest image
        # Use of `operator.itemgetter` with `max` and `min` allows us to get the index of the point
        # Each point is an array of 1 coordinate, hence the [0] getter, then [0] or [1] used to get x and y respectively.
        # Bottom-right point has the largest (x + y) value
        # Top-left has point smallest (x + y) value
        # Bottom-left point has smallest (x - y) value
        # Top-right point has largest (x - y) value
        bottom_right, _ = max(enumerate(
            [pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
        top_left, _ = min(enumerate([pt[0][0] + pt[0][1]
                                     for pt in polygon]), key=operator.itemgetter(1))
        bottom_left, _ = min(enumerate(
            [pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
        top_right, _ = max(enumerate([pt[0][0] - pt[0][1]
                                      for pt in polygon]), key=operator.itemgetter(1))
        # Return an array of all 4 points using the indices
        # Each point is in its own array of one coordinate
        return [
            polygon[top_left][0],
            polygon[top_right][0],
            polygon[bottom_right][0],
            polygon[bottom_left][0]]

    def display_points(in_img, points, radius=5, colour=(0, 0, 255)):
        """Draws circular points on an image."""
        img = in_img.copy()
        # Dynamically change to a colour image if necessary
        if len(colour) == 3:
            if len(img.shape) == 2:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            elif img.shape[2] == 1:
                img = find_corners_of_largest_polygon(img)
        """Finds the 4 extreme corners of the largest contour in the image."""
        contours, h = cv2.findContours(
            img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find contours
        contours = sorted(
            contours,
            key=cv2.contourArea,
            reverse=True)  # Sort by area, descending
        polygon = contours[0]  # Largest image
        # Use of `operator.itemgetter` with `max` and `min` allows us to get the index of the point
        # Each point is an array of 1 coordinate, hence the [0] getter, then [0] or [1] used to get x and y respectively.
        # Bottom-right point has the largest (x + y) value
        # Top-left has point smallest (x + y) value
        # Bottom-left point has smallest (x - y) value
        # Top-right point has largest (x - y) value
        bottom_right, _ = max(enumerate(
            [pt[0][0] + pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
        top_left, _ = min(enumerate([pt[0][0] + pt[0][1]
                                     for pt in polygon]), key=operator.itemgetter(1))
        bottom_left, _ = min(enumerate(
            [pt[0][0] - pt[0][1] for pt in polygon]), key=operator.itemgetter(1))
        top_right, _ = max(enumerate([pt[0][0] - pt[0][1]
                                      for pt in polygon]), key=operator.itemgetter(1))
        for point in points:
            img = cv2.circle(img, tuple(int(x)
                                        for x in point), radius, colour, -1)
        return img

    def show_image(img):
        """Shows an image until any key is pressed."""
        cv2.imshow('image', img)  # Display the image
        # Wait for any key to be pressed (with the image window active)
        cv2.waitKey(0)
        cv2.destroyAllWindows()  # Close all windows

    def distance_between(p1, p2):
        """Returns the scalar distance between two points"""
        a = p2[0] - p1[0]
        b = p2[1] - p1[1]
        return np.sqrt((a ** 2) + (b ** 2))

    def crop_and_warp(img, crop_rect):
        """Crops and warps a rectangular section from an image into a square of similar size."""
        # Rectangle described by top left, top right, bottom right and bottom
        # left points
        top_left, top_right, bottom_right, bottom_left = crop_rect[
            0], crop_rect[1], crop_rect[2], crop_rect[3]
        # Explicitly set the data type to float32 or `getPerspectiveTransform`
        # will throw an error
        src = np.array([top_left, top_right, bottom_right,
                        bottom_left], dtype='float32')
        # Get the longest side in the rectangle
        side = max([
            Preprocess.distance_between(bottom_right, top_right),
            Preprocess.distance_between(top_left, bottom_left),
            Preprocess.distance_between(bottom_right, bottom_left),
            Preprocess.distance_between(top_left, top_right)
        ])
        # Describe a square with side of the calculated length, this is the new
        # perspective we want to warp to
        dst = np.array(
            [[0, 0], [side - 1, 0], [side - 1, side - 1], [0, side - 1]], dtype='float32')
        # Gets the transformation matrix for skewing the image to fit a square
        # by comparing the 4 before and after points
        m = cv2.getPerspectiveTransform(src, dst)
        # Performs the transformation on the original image
        return cv2.warpPerspective(img, m, (int(side), int(side)))

    def resize(img):
        W = 1000
        if len(img.shape) == 3:
            height, width, depth = img.shape
        else:
            height, width = img.shape
        imgScale = W / width
        newX, newY = img.shape[1] * imgScale, img.shape[0] * imgScale
        new_img = cv2.resize(img, (int(newX), int(newY)))
        #cv2.imshow("Show by CV2", new_img)
        # cv2.waitKey(0)
        return new_img

    def invert(new_img):

        #        just_img, thresh1 = cv2.threshold(new_img, 200, 255, cv2.THRESH_BINARY)
        try:
            gray_img = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
        except cv2.error:
            print("Image already in Grayscale")
            gray_img = new_img
        # convert the BGR to gray to perform adaptive thresholding
        thresh_img = cv2.adaptiveThreshold(
            gray_img,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            15,
            5)
        # do a smoothing fitler to clear the noise
        smooth_img = cv2.bilateralFilter(thresh_img, 15, 25, 25)
        # invert the image again to black and white
        invert_img = cv2.bitwise_not(smooth_img)

        return invert_img

    def boxes(invert_img):
        #This sets the coordinates of the grid lines to to splice a processed image to a individual sudoku cells.
        rows = [(30, 110), (125, 205), (235, 315), (350, 430),
                (455, 535), (580, 660), (680, 760), (785, 865), (890, 970)]
        columns = [(30, 110), (130, 210), (240, 320), (355, 435),
                   (455, 535), (575, 655), (680, 760), (800, 880), (890, 970)]
        images_list = []
        for unit in rows:
            for units in columns:
                images_list.append(
                    invert_img[unit[0]:unit[1], units[0]:units[1]])
                pass

        final_images = []
        for i in range(len(images_list)):
            resize_img = cv2.resize(images_list[i], (28, 28))
            final_images.append(resize_img)

        return final_images

    def process_cells(img):
        rows = np.shape(img)[0]
        rowtop = None
        rowbottom = None
        colleft = None
        colright = None
        thresholdBottom = 50
        thresholdTop = 50
        thresholdLeft = 50
        thresholdRight = 50
        center = rows // 2
        for i in range(center, rows):
            if rowbottom is None:
                temp = img[i]
                if sum(temp) < thresholdBottom or i == rows - 1:
                    rowbottom = i
            if rowtop is None:
                temp = img[rows - i - 1]
                if sum(temp) < thresholdTop or i == rows - 1:
                    rowtop = rows - i - 1
            if colright is None:
                temp = img[:, i]
                if sum(temp) < thresholdRight or i == rows - 1:
                    colright = i
            if colleft is None:
                temp = img[:, rows - i - 1]
                if sum(temp) < thresholdLeft or i == rows - 1:
                    colleft = rows - i - 1

        # Centering the bounding box's contents
        newimg = np.zeros(np.shape(img))
        startatX = (rows + colleft - colright) // 2
        startatY = (rows - rowbottom + rowtop) // 2
        for y in range(startatY, (rows + rowbottom - rowtop) // 2):
            for x in range(startatX, (rows - colleft + colright) // 2):
                newimg[y, x] = img[rowtop + y -
                                   startatY, colleft + x - startatX]
        return newimg
