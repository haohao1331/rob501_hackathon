import numpy as np
from numpy.linalg import inv, norm
from scipy.linalg import null_space

def dlt_homography(I1pts : np.ndarray, I2pts : np.ndarray):
    """
    Find perspective Homography between two images.

    Given 4 points from 2 separate images, compute the perspective homography
    (warp) between these points using the DLT algorithm.

    Parameters:
    ----------- 
    I1pts  - 2x4 np.array of points from Image 1 (each column is x, y).
    I2pts  - 2x4 np.array of points from Image 2 (in 1-to-1 correspondence).

    Returns:
    --------
    H  - 3x3 np.array of perspective homography (matrix map) between image coordinates.
    A  - 8x9 np.array of DLT matrix used to determine homography.
    """
    I1pts_cat = np.concatenate((I1pts, np.ones((1, I1pts.shape[1]), dtype=I1pts.dtype)), axis=0).T
    
    # getting right 3 section of the A matrix
    I2pts_gen = np.repeat(I2pts.T.reshape(-1, 1), I1pts_cat.shape[1], axis=1)
    I1pts_gen = np.repeat(I1pts_cat, 2, axis=0)
    A_right = np.multiply(I1pts_gen, I2pts_gen) # the right three columns of A
    
    # the left and middle 3 columns of A
    A_left = np.concatenate((-1*I1pts_cat, np.zeros((I1pts_cat.shape[0], 3))), axis=1).reshape(-1, 3)
    A_middle = np.concatenate((np.zeros((I1pts_cat.shape[0], 3)), -1*I1pts_cat), axis=1).reshape(-1, 3)
    
    # putting columns together
    A = np.concatenate((A_left, A_middle, A_right), axis=1)
    H = null_space(A).reshape(3, 3)
    return H / H[-1, -1], A # normalize and return