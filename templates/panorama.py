# Add other imports from available listing as your see fit.
import sys
import numpy as np
from cv2 import imread, imwrite, resize, imshow, waitKey, destroyAllWindows

def create_panorama(image_files):
    # Load images.
   
    # Mosaic all images.

    # Undo vignetting if desired.

    # Write out the result as a PNG.
    imwrite(Ipano)

if __name__ == "__main__":
    # Make sure the right number of input args are provided.
    if len(sys.argv) != 8:
        sys.exit(-1, "Too few command line argmuments.")

    create_panorama(sys.argv[1:])