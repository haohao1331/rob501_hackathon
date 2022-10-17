import numpy as np
from numpy.linalg import inv

def bilinear_interp(I : np.ndarray, pt : np.ndarray):
    """
    Performs bilinear interpolation for a given image point.

    Given the (x, y) location of a point in an input image, use the surrounding
    four pixels to conmpute the bilinearly-interpolated output pixel intensity.

    Note that images are (usually) integer-valued functions (in 2D), therefore
    the intensity value you return must be an integer (use round()).

    This function is for a *single* image band only - for RGB images, you will 
    need to call the function once for each colour channel.

    Parameters:
    -----------
    I   - Single-band (greyscale) intensity image, 8-bit np.array (i.e., uint8).
    pt  - 2x1 np.array of point in input image (x, y), with subpixel precision.

    Returns:
    --------
    b  - Interpolated brightness or intensity value (whole number >= 0).
    """

    # Note: using formula from wikipedia: https://en.wikipedia.org/wiki/Bilinear_interpolation

    if pt.shape != (2, 1):
        print(pt.shape)
        raise ValueError('Point size is incorrect.')

    # get needed values
    x, y = pt
    x1, x2, y1, y2 = int(np.floor(x)), int(np.ceil(x)), int(np.floor(y)), int(np.ceil(y))
    # print(x1, x2, y1, y2)
    # print(I.shape)
    
    # construct matrix
    try:
        A = I[np.array([y1, y2, y1, y2]), np.array([x1, x1, x2, x2])].reshape(2, 2)
    except:
        return 0
    # get result
    b = np.array([x2-x, x-x1]).T @ A @ np.array([y2-y, y-y1])

    return round(b[0,0])