# Billboard hack script file.
import numpy as np
from matplotlib.path import Path
from imageio import imread, imwrite

from dlt_homography import dlt_homography
from bilinear_interp import bilinear_interp
from histogram_eq import histogram_eq

# import matplotlib.pyplot as plt

def billboard_hack(Iyd, Ist):
    """
    Hack and replace the billboard!

    Parameters:
    ----------- 

    Returns:
    --------
    Ihack  - Hacked RGB intensity image, 8-bit np.array (i.e., uint8).
    """
    # Bounding box in Y & D Square image - use if you find useful.
    bbox = np.array([[404, 490, 404, 490], [38,  38, 354, 354]])

    # Point correspondences.
    Iyd_pts = np.array([[416, 485, 488, 410], [40,  61, 353, 349]])
    Ist_pts = np.array([[2, 218, 218, 2], [2, 2, 409, 409]])

    Iyd = imread('../images/yonge_dundas_square.jpg')
    Ist = imread('../images/uoft_soldiers_tower_light.png')
    
    # Iyd = imread('assignment1/images/yonge_dundas_square.jpg')
    # Ist = imread('assignment1/images/uoft_soldiers_tower_light.png')

    Ihack = np.asarray(Iyd)
    Ist = np.asarray(Ist)

    # Let's do the histogram equalization first.
    Ist_eq = histogram_eq(Ist)

    # Compute the perspective homography we need...
    H, A = dlt_homography(Iyd_pts, Ist_pts)
    
    # extracting all points that fall within the border
    area = Path(Iyd_pts.T)
    xr, yr = np.arange(Iyd.shape[0]), np.arange(Iyd.shape[1])
    Iyd_coord = np.zeros((Iyd.shape[0], Iyd.shape[1], 2), dtype=int)
    Iyd_coord[:, :, 0] = xr[:, None]
    Iyd_coord[:, :, 1] = yr[:]
    Iyd_coord = Iyd_coord.reshape(-1, 2)    # Iyd_coord contains the matrix with all the coordinates of Iyd
    area_to_hack = area.contains_points(Iyd_coord)
    
    # loop over all pixels that needs to be swaped out
    for point in Iyd_coord[area_to_hack]:
        # inverse warping
        p = H @ np.concatenate((point.reshape(2, 1), [[1]]), axis=0)

        # get and set the intensity
        st_intensity = bilinear_interp(Ist_eq, p[0:2, :] / p[-1, 0])    # normalize p and then bi interpolate
        Ihack[point[1], point[0], :] = st_intensity
    
    #------------------
    
    # print(Ihack)

    # Visualize the result, if desired...
    # plt.imshow(Ihack)
    # plt.show()
    # imwrite('billboard_hacked.png', Ihack)

    return Ihack

if __name__ == '__main__':
    billboard_hack()