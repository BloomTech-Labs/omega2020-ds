from preprocessing import *
from model import *
import cv2
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("path_image", help="path to input image to be displayed")
args = parser.parse_args()
img = cv2.imread(args.path_image)

def pipeline(img):
#    img = cv2.imread('./data/img1.jpg', cv2.IMREAD_GRAYSCALE)
    processed = Preprocess.pre_process_image(img)
    corners = Preprocess.find_corners_of_largest_polygon(processed)
    cropped = Preprocess.crop_and_warp(img, corners)
    resized = Preprocess.resize(cropped)
    inverted = Preprocess.resize(invert)
    cv2.imshow('Inverted', invert)

    # Press q on keyboard to  exit
    cv2.waitKey(25) & 0xFF == ord('q')
    
    
    boxed = boxes(inverted)
    
    return boxed

if __name__ == '__main__':
    pipeline(img)