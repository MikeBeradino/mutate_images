import cv2 as cv
import numpy as np

def normalize(r, g, b):
    return (r/255., g/255., b/255.)

def rgb2cmyk(r_, g_, b_):
    r, g, b = normalize(r_, g_, b_)

    c = 1 - r
    m = 1 - g
    y = 1 - b

    k = min(c, m, y)
    c = (c - k)/(1-k)
    m = (m - k)/(1-k)
    y = (y - k)/(1-k)

    return (c, m, y, k)

def cmy_cannels():

    #img = cv.imread("images/color_black2.jpg")
    img = cv.imread("color_black2/color_black2-clean.jpg")
    cv.imshow('img', img)

    b, g, r = cv.split(img)
    height, width = b.shape

    ####################### RGB2CMYK #######################

    c = np.zeros((height, width))
    m = np.zeros((height, width))
    y = np.zeros((height, width))
    k = np.zeros((height, width))

    for i in range(height):
        for j in range(width):
            c[i][j], m[i][j], y[i][j], k[i][j] = rgb2cmyk(
                r[i][j], g[i][j], b[i][j])

    cv.imwrite('/home/rootbox/PycharmProjects/mutate_images/cyan_test----.png', 255*c)
    #cv.imwrite('color_black2/magenta_test-----.png', m)
    #cv.imwrite('color_black2/yellow_test----.png',  y)

    cmyk = cv.merge((c, m, y, k))
    cv.imshow('cmyk', cmyk)
    cv.imshow('c', c)
    cv.imshow('m', m)
    cv.imshow('y', y)
    cv.imshow('k', k)


    ##################################################

####################### ####################### #######################
    k = cv.waitKey(0) & 0xFF
    if k == 27 or k == ord('q'):
        cv.destroyAllWindows()

cmy_cannels()