import cv2
import numpy as np
import sys

def undo_vignetting(img, sigma, brightness):

    """
    Parameters
    -----------
    img: str
        image path
    sigma: float
        standard deviation for gaussian kernel as a funtion of dimension
        both dimensions use the same sigma
        default is half the the dimension
    brightness: float
        increased brightness after vignette correction
        (brightness * 100)% image brightness
        default is 1.3
    """

    sigma = sigma or 0.5
    brightness = brightness or 1.3

    img = cv2.imread(img)
    h, w = img.shape[:2]
    og_img = img.copy()

    # get gaussian mask
    sigma_w = w * sigma
    sigma_h = h * sigma
    kernel_x = cv2.getGaussianKernel(w, sigma_w)
    kernel_y = cv2.getGaussianKernel(h, sigma_h)
    kernel = kernel_y * kernel_x.T
    mask = 255 * kernel / np.linalg.norm(kernel)

    # apply mask to 3 colour channels
    for i in range(3):
        img[:,:,i] = normalize(img[:,:,i] / mask, 255)

    # increase brightness
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img = np.array(img, dtype = np.float64)
    for i in range(1, 3):
        img[:,:,i] = img[:,:,i] * brightness
        img[:,:,i][img[:,:,i] > 255]  = 255
    img = np.array(img, dtype = np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)

    cv2.imshow("og", og_img)
    cv2.imshow("fixed", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return img


# normalize values between 0 and 255 for 8bit images
def normalize(img, maxval):

    return ((img - img.min()) * (1 / (img.max() - img.min()) * maxval)).astype("uint8")

if __name__ == "__main__":

    img_file = sys.argv[1]
    sigma = None
    brightness = None
    if len(sys.argv) > 2:
        sigma = float(sys.argv[2])
        if len(sys.argv) > 3:
            brightness = float(sys.argv[3])

    undo_vignetting(img_file, sigma, brightness)
