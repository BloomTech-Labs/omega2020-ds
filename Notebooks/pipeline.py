from preprocessing import *
from model import *

def pipeline(self):
    img = cv2.imread('./data/img1.jpg', cv2.IMREAD_GRAYSCALE)
    processed = pre_process_image(img)
    corners = find_corners_of_largest_polygon(processed)
    cropped = crop_and_warp(img, corners)
    resized = resize(cropped)
    inverted = resize(invert)
    boxed = boxes(inverted)
    
    return boxed
