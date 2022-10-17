# Add other imports from available listing as your see fit.
import sys
import numpy as np
from cv2 import imread, imwrite, resize, imshow, waitKey, destroyAllWindows

def mosaic_images(I1_name, I2_name, show_me = True):
    # Load images.
    I1 = imread(I1_name)
    I2 = imread(I2_name)

    # Feature matching - remember I1 is the anchor.

    # Return mosaicked images (of correct, full size).
    return Imosaic

if __name__ == "__main__":
    # Add test code here if you desire.
    pass