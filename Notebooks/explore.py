# Import the required packages
import argparse
import cv2

# We first create the ArgumentParser object 
# The created object 'parser' will have the necessary information
# to parse the command-line arguments into data types.
parser = argparse.ArgumentParser()

# Add 'path_image_input' argument using add_argument() including a help. The type is string (by default):
parser.add_argument("path_image_input", help="path to input image to be displayed")

# Add 'path_image_output' argument using add_argument() including a help. The type is string (by default):
#parser.add_argument("path_image_output", help="path of the processed image to be saved")

# Parse the argument and store it in a dictionary:
args = vars(parser.parse_args())

# We can load the input image from disk:
#src.create(rows, cols, CV_8UC1);
#src = imread(your-file, CV_8UC1);
src.create(rows, cols, CV_8UC1);
src = cv2.imread(args["path_image_input"], CV_8UC1);

# Show the loaded image:
#cv2.imshow("loaded image", image_input)

# Process the input image (convert it to grayscale):
def pre_process_image(img, skip_dilate=False):
    """Uses a blurring function, adaptive thresholding and dilation to expose the main features of an image."""
    # Gaussian blur with a kernal size (height, width) of 9.
    # Note that kernal sizes must be positive and odd and the kernel must be square.
    proc = cv2.GaussianBlur(img.copy(), (9, 9), 0).astype('uint8')
    # Adaptive threshold using 11 nearest neighbour pixels
    proc = cv2.adaptiveThreshold(src, proc, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    # Invert colours, so gridlines have non-zero pixel values.
    # Necessary to dilate the image, otherwise will look like erosion instead.
    proc = cv2.bitwise_not(proc, proc)
    #if not skip_dilate:
    #    # Dilate the image to increase the size of the grid lines.
    #    kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]])
    #    proc = cv2.dilate(proc, kernel)
    return proc

#gray_image = cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY)

# Show the processed image:
cv2.imshow("gray image", pre_process_image(image_input))


# Save the processed image to disk:
#cv2.imwrite(args["path_image_output"], gray_image)

# Wait until a key is pressed:
cv2.waitKey(0)

# Destroy all windows:
cv2.destroyAllWindows()