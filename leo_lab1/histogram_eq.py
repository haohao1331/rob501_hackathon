from itertools import count
import numpy as np

def histogram_eq(I : np.ndarray):
    """
    Histogram equalization for greyscale image.

    Perform histogram equalization on the 8-bit greyscale intensity image I
    to produce a contrast-enhanced image J. Full details of the algorithm are
    provided in the Szeliski text.

    Parameters:
    -----------
    I  - Single-band (greyscale) intensity image, 8-bit np.array (i.e., uint8).

    Returns:
    --------
    J  - Contrast-enhanced greyscale intensity image, 8-bit np.array (i.e., uint8).
    """

    # Verify I is grayscale.
    if I.dtype != np.uint8:
        raise ValueError('Incorrect image format!')

    # get probability density function
    c = np.zeros(256)
    counts = np.unique(I, return_counts=True)
    print(type(counts[1]))
    c[counts[0]] = counts[1][:]
    
    # get commulative density function
    cdf = np.cumsum(c) / (I.shape[0] * I.shape[1])
    
    # remap value to 0 to 255
    J = cdf[I] * 255
    
    return J