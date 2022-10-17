from gc import get_count
import cv2 as cv
import numpy as np
import sys
import matplotlib.pyplot as plt
from matplotlib.path import Path
np.set_printoptions(threshold=sys.maxsize)
from leo_lab1.bilinear_interp import bilinear_interp
from leo_lab1.dlt_homography import dlt_homography


def get_contour_points(path):
    img = cv.imread(path)
    imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    ret, thresh = cv.threshold(imgray, 1, 255, 0)


    contours, heirarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    output = None
    for i in range(len(contours)):
        # print(contours[i].shape)
        if cv.contourArea(contours[i]) > 10000:
            cnt = contours[i]
            epsilon = 0.1*cv.arcLength(cnt,True)
            approx = cv.approxPolyDP(cnt,epsilon,True)
            print(cv.contourArea(contours[i]))
            print(approx)
            cv.drawContours(img, (approx, ), -1, (0,255,0), 1)
            output = approx.reshape(4, -1)
            break
    
    #show the image
    # cv.namedWindow('Contours',cv.WINDOW_NORMAL)
    # # cv.namedWindow('Thresh',cv.WINDOW_NORMAL)
    # cv.imshow('Contours', img)
    # # cv.imshow('Thresh', thresh)

    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return output

def unwrap(path1):
    img = cv.imread(path1)
    Ihack = np.asarray(img)
    Iyd = Ihack
    print(Ihack.shape)
    x_max, y_max, _ = Ihack.shape

    img_corner = np.array([[0, x_max, 0, x_max], [0, 0, y_max, y_max]])
    content_corner = get_contour_points(path1).T
    print(content_corner)
    print(img_corner)
    # Iyd = imread('assignment1/images/yonge_dundas_square.jpg')
    # Ist = imread('assignment1/images/uoft_soldiers_tower_light.png')

    
    Ist = np.asarray(content_corner)

    # Compute the perspective homography we need...
    H, A = dlt_homography(img_corner, content_corner)
    
    # extracting all points that fall within the border
    area = Path(content_corner.T)
    xr, yr = np.arange(Iyd.shape[0]), np.arange(Iyd.shape[1])
    Iyd_coord = np.zeros((Iyd.shape[0], Iyd.shape[1], 2), dtype=int)
    Iyd_coord[:, :, 0] = xr[:, None]
    Iyd_coord[:, :, 1] = yr[:]
    Iyd_coord = Iyd_coord.reshape(-1, 2)    # Iyd_coord contains the matrix with all the coordinates of Iyd
    area_to_hack = area.contains_points(Iyd_coord)
    
    print(len(Iyd_coord[area_to_hack]))
    # quit(Iyd_coord[area_to_hack][0])
    i = 0
    # loop over all pixels that needs to be swaped out
    for point in Iyd_coord[area_to_hack]:
        print(i)
        # inverse warping
        p = H @ np.concatenate((point.reshape(2, 1), [[1]]), axis=0)

        # get and set the intensity
        st_intensity = bilinear_interp(cv.cvtColor(Iyd, cv.COLOR_BGR2GRAY), p[0:2, :] / p[-1, 0])    # normalize p and then bi interpolate
        Ihack[point[1], point[0], :] = st_intensity
        i += 1
    return Ihack

if __name__ == '__main__':
    path = 'images/sub_image_07_dark.png'
    print(get_contour_points(path))
    plt.imshow(unwrap(path))
    plt.show()

