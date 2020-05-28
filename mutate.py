from tkinter import filedialog
from tkinter import *
import tkinter.ttk as ttk
from tkcolorpicker import askcolor
from PIL import Image
from PIL import ImageTk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import drawSvg as draw
import svgutils.transform as sg
from math import sin, cos, radians


import cv2
import numpy as np
import matplotlib.pyplot as plt


def setcolorred():
    global color_pick
    color_pick ="#ff0000"
def setcolorgreen():
    global color_pick
    color_pick = "#00ff00"
    print(color_pick)
def setcolorblue():
    global color_pick
    color_pick = "#0000ff"
    print(color_pick)
def setcolorwhite():
    global color_pick
    color_pick = "#ffffff"
    print(color_pick)
def setcolorblack():
    global color_pick
    color_pick = "#000000"
    print(color_pick)
def setcoloryellow():
    global color_pick
    color_pick ="#ffff00"
    print(color_pick)
def setcolorcyan():
    global color_pick
    color_pick = "#00ffff"
    print(color_pick)
def setcolormagenta():
    global color_pick
    color_pick = "#ff00ff"
    print(color_pick)

def infopanel():
    root = Tk()
    S = Scrollbar(root)
    T = Text(root, height=4, width=50)
    S.pack(side=RIGHT, fill=Y)
    T.pack(side=LEFT, fill=Y)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    print(imagestuff())
    T.insert(END,imagestuff())

def rotate_point(point, angle, center_point=(0, 0)):
    """Rotates a point around center_point(origin by default)
    Angle is in degrees.
    Rotation is counter-clockwise
    """
    angle_rad = radians(angle % 360)
    # Shift the point so that center_point becomes the origin
    new_point = (point[0] - center_point[0], point[1] - center_point[1])
    new_point = (new_point[0] * cos(angle_rad) - new_point[1] * sin(angle_rad),
                 new_point[0] * sin(angle_rad) + new_point[1] * cos(angle_rad))
    # Reverse the shifting we have done
    new_point = (new_point[0] + center_point[0], new_point[1] + center_point[1])
    return new_point

def rotate_polygon(polygon, angle, center_point=(0, 0)):
    """Rotates the given polygon which consists of corners represented as (x,y)
    around center_point (origin by default)
    Rotation is counter-clockwise
    Angle is in degrees
    """
    rotated_polygon = []
    for corner in polygon:
        rotated_corner = rotate_point(corner, angle, center_point)
        rotated_polygon.append(rotated_corner)
    return rotated_polygon

def shape_select():
    mode2 = (shapes.get())
    if (mode2 == "CIRCLES" ):
        print("circles")

    if (mode2 == "SQUARE_"):
        print("SQUARE_")

    if (mode2 ==  "POLY___" ):
        print( "POLY___")

    if (mode2 == "TRY____"):
        print("try")

    if (mode2 == "CUSTOM_"):
        print("CUSTOM_")

def custom():
    print("custom")
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    svgfile = (str(root.SVGfile))
    image = Image.open("working/pixelated_image.tif").convert('LA').rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
    pix_size = (e4.get())
    int_pix_size = int(pix_size)
    rows = image.size[0]  # 11
    cols = image.size[1]  # 6
    rows_out = image.size[0] * int_pix_size  # 14*11=154
    cols_out = image.size[1] * int_pix_size  # 14*6=84
    px = image.load()
    gray_scale_values = 256 / int_pix_size
    fig = sg.SVGFigure(rows_out, cols_out)
    svg_name = []
    svg_to_append = []
    number=0
    for l in range(rows):
        for j in range(cols):
            color_index = ((px[l, j]))
            gray, alpa = color_index
            color_flip = 256 - gray
            numb_of_squares = color_flip / gray_scale_values
            print(numb_of_squares)
            if (rows_out <= cols_out):
                y_orent = (cols_out - (j * int_pix_size))  #
            else:
                y_orent = (cols_out - (j * int_pix_size))

            svg_name.append([str(number)])
            svg_to_append.append([str(number)])
            svg_name[number] = sg.fromfile(svgfile)
            svg_to_append[number] = svg_name[number].getroot()

            svg_to_append[number].moveto(l * int_pix_size, (y_orent), scale=numb_of_squares/10)
            fig.append([svg_to_append[number]])
            number = number+1
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # save generated SVG files
    fig.save('working/example_draw.svg')

    #d.saveSvg('working/example_draw.svg')
    svgsample()

def ASCII():
    print("ascii")
    image = Image.open("working/pixelated_image.tif").convert('LA').rotate(180).transpose(Image.FLIP_LEFT_RIGHT)

    txt_size = root.ASCII_sliderVal.get()
    int_pix_size = int(txt_size)
    rows = image.size[0]  # 11
    cols = image.size[1]  # 6
    rows_out = image.size[0] * int_pix_size  # 14*11=154
    cols_out = image.size[1] * int_pix_size  # 14*6=84
    px = image.load()
    gray_scale_values = 255 / int_pix_size
    fig = sg.SVGFigure(rows_out, cols_out)
    txt_name = []
    txt_to_append = []
    number = 0

    shortASCII =  " .:-=+*#%@"
    longASCII = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^'. "
    for l in range(rows):
        for j in range(cols):
            color_index = ((px[l, j]))
            gray, alpa = color_index
            color_flip = 256 - gray
            print (color_flip)
            if (root.ascii_small.get() == '1'):
                index = color_flip /25.5
                int_index = int(index)
                char = shortASCII[int_index]
            if (root.ascii_large.get() == '1'):
                index = color_flip /3.75
                int_index = int(index)
                char = longASCII[int_index]

            numb_of_squares = color_flip / gray_scale_values
            print(numb_of_squares)
            if (rows_out <= cols_out):
                y_orent = (cols_out - (j * int_pix_size))  #
            else:
                y_orent = (cols_out - (j * int_pix_size))
            txt_name.append([str(number)])
            txt_to_append.append([str(number)])
            txt_to_append[number] = sg.TextElement(0,0, char, size=int_pix_size, weight="bold", color=color_pick)
            txt_to_append[number].moveto(l * int_pix_size, (y_orent), scale=numb_of_squares / 10)
            fig.append([txt_to_append[number]])
            number = number + 1

    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # save generated SVG files
    fig.save('working/example_draw.svg')


    svgsample()

def gray_scale():

    print("gray_scale")
    mode2 = (shapes.get())

    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++

    image = Image.open("working/pixelated_image.tif").convert('LA')
    pix_size = (e4.get())
    int_pix_size = int(pix_size)
    rows = image.size[0]  # 11
    cols = image.size[1]  # 6
    rows_out = image.size[0] * int_pix_size  # 14*11=154
    cols_out = image.size[1] * int_pix_size  # 14*6=84
    px = image.load()


    d = draw.Drawing(rows_out, cols_out, origin=(0, 0), displayInline=False)



    if (mode2 == "CIRCLES" or mode2 == "SQUARE_"):
        gray_scale_values = 256 / int_pix_size

        for l in range(rows):
            for j in range(cols):
                color_index = ((px[l, j]))
                gray, alpa = color_index
                color_flip = 256 - gray
                numb_of_squares = color_flip / gray_scale_values
                int_number_of_squares = int(numb_of_squares)

                if (rows_out <= cols_out):
                    y_orent = (cols_out - (j * int_pix_size))  #
                else:
                    y_orent = (cols_out - (j * int_pix_size))

                if (root.white_val.get() == '1'):
                    if (int_number_of_squares != 1):

                        if (mode2 == "CIRCLES"):
                            for numb in range(int_number_of_squares):
                                d.append(draw.Circle(l * int_pix_size, (y_orent), numb - 1, stroke_width=1, stroke=color_pick,
                                                     fill='none'))

                        if (mode2 == "SQUARE_"):
                            for numb in range(int_number_of_squares):
                                d.append(
                                    draw.Rectangle((l * int_pix_size + numb / 2), (y_orent + numb / 2), int_pix_size - numb,
                                                   int_pix_size - numb, stroke_width=0.5, stroke=color_pick, fill='none', ))

                else:
                    if (mode2 == "CIRCLES"):
                        for numb in range(int_number_of_squares):
                            d.append(
                                draw.Circle(l * int_pix_size, (y_orent), numb - 1, stroke_width=1, stroke=color_pick,
                                            fill='none'))

                    if (mode2 == "SQUARE_"):
                        for numb in range(int_number_of_squares):
                            d.append(
                                draw.Rectangle((l * int_pix_size + numb / 2), (y_orent + numb / 2), int_pix_size - numb,
                                               int_pix_size - numb, stroke_width=0.5, stroke=color_pick, fill='none', ))

    if (mode2 == "LINE___"):
        gray_scale_values = 256 / int_pix_size

        for l in range(rows):
            for j in range(cols):
                color_index = ((px[l, j]))
                gray, alpa = color_index

                color_flip = 256 - gray
                numb_of_squares = color_flip / gray_scale_values

                int_number_of_squares = int(numb_of_squares)
                if (rows_out <= cols_out):
                    y_orent = (cols_out - (j * int_pix_size))  #
                else:
                    y_orent = (cols_out - (j * int_pix_size))

                if (root.white_val.get() == '1'):
                    if (int_number_of_squares != 1):
                        for numb in range(int_number_of_squares):
                            if (root.hor_line.get() == '1'):

                                x2 = (l * int_pix_size + numb)
                                y2 = (y_orent)
                                x1 = (l * int_pix_size + numb)  # int_pix_size
                                y1 = (((y_orent) + int_pix_size))

                                point1 = rotate_point((x1, y1), 90, ((x1 + x2) / 2, (y1 + y2) / 2))
                                point2 = rotate_point((x2, y2), 90, ((x1 + x2) / 2, (y1 + y2) / 2))
                                print(point1)
                                print(point2)
                                x1, y1 = point1
                                x2, y2 = point2


                            elif (root.spin_line.get() == '1'):
                                print("spin_line")
                                x2 = (l * int_pix_size + numb)
                                y2 = (y_orent)
                                x1 = (l * int_pix_size + numb)  # int_pix_size
                                y1 = (((y_orent) + int_pix_size))

                                point1 = rotate_point((x1, y1), gray, ((x1 + x2) / 2, (y1 + y2) / 2))
                                point2 = rotate_point((x2, y2), gray, ((x1 + x2) / 2, (y1 + y2) / 2))
                                print(point1)
                                print(point2)
                                x1, y1 = point1
                                x2, y2 = point2


                            elif (root.rotate_line.get() == '1'):  # not working with white
                                print("rot_line")
                                x2 = (l * int_pix_size + numb)
                                y2 = (y_orent)
                                x1 = (l * int_pix_size + numb)  # int_pix_size
                                y1 = (((y_orent) + int_pix_size))

                                point1 = rotate_point((x1, y1), 45, ((x1 + x2) / 2, (y1 + y2) / 2))
                                point2 = rotate_point((x2, y2), 45, ((x1 + x2) / 2, (y1 + y2) / 2))
                                print(point1)
                                print(point2)
                                x1, y1 = point1
                                x2, y2 = point2
                            else:
                                print("here 2")
                                x1 = (l * int_pix_size + numb)
                                y1 = (y_orent)
                                x2 = (l * int_pix_size + numb)  # int_pix_size
                                y2 = (y_orent) + int_pix_size

                            print(x1, y1, x2, y2)
                            d.append(draw.Lines((x1), (y1),
                                                (x2), (y2),
                                                stroke_width=1,
                                                stroke=color_pick,
                                                fill='none',
                                                close=False))

                else:
                    for numb in range(int_number_of_squares):
                        if (root.hor_line.get() == '1'):

                            x2 = (l * int_pix_size + numb)
                            y2 = (y_orent)
                            x1 = (l * int_pix_size + numb)  # int_pix_size
                            y1 = (((y_orent) + int_pix_size))

                            point1 = rotate_point((x1, y1), 90, ((x1 + x2) / 2, (y1 + y2) / 2))
                            point2 = rotate_point((x2, y2), 90, ((x1 + x2) / 2, (y1 + y2) / 2))
                            print(point1)
                            print(point2)
                            x1, y1 = point1
                            x2, y2 = point2

                        elif (root.rotate_line.get() == '1'):
                            x2 = (l * int_pix_size + numb)
                            y2 = (y_orent)
                            x1 = (l * int_pix_size + numb)  # int_pix_size
                            y1 = (((y_orent) + int_pix_size))
                            point1 = rotate_point((x1, y1), 45, ((x1 + x2) / 2, (y1 + y2) / 2))
                            point2 = rotate_point((x2, y2), 45, ((x1 + x2) / 2, (y1 + y2) / 2))
                            print(point1)
                            print(point2)
                            x1, y1 = point1
                            x2, y2 = point2

                        elif (root.spin_line.get() == '1'):
                            print("spin_line")
                            x2 = (l * int_pix_size + numb)
                            y2 = (y_orent)
                            x1 = (l * int_pix_size + numb)  # int_pix_size
                            y1 = (((y_orent) + int_pix_size))

                            point1 = rotate_point((x1, y1), gray, ((x1 + x2) / 2, (y1 + y2) / 2))
                            point2 = rotate_point((x2, y2), gray, ((x1 + x2) / 2, (y1 + y2) / 2))
                            print(point1)
                            print(point2)
                            x1, y1 = point1
                            x2, y2 = point2



                        else:
                            print("here 4")
                            x1 = (l * int_pix_size + numb)
                            y1 = (y_orent)
                            x2 = (l * int_pix_size + numb)  # int_pix_size
                            y2 = (y_orent) + int_pix_size

                        if (root.hor_line.get() == '1'):
                            int_number_of_squares = 1

                        print(x1, y1, x2, y2)
                        d.append(draw.Lines((x1), (y1),
                                            (x2), (y2),
                                            stroke_width=1,
                                            stroke=color_pick,
                                            fill='none',
                                            close=False))

    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++

    d.saveSvg('working/example_draw.svg')
    svgsample()
    #fix_viewport_grayscale()

def build_pixels():
    print("build_pixels")
    print(e4.get())
    mode2 = (shapes.get())
    print(mode2)

    if (root.sim.get() == '1'):
        print("toggled")
        stroke_val = 0.3
    else:
        stroke_val = 1


    redval  = root.red_sliderVal.get()
    blueval = root.blue_sliderVal.get()
    greenval=root.green_sliderVal.get()
    toneval = root.tone_sliderVal.get()
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++

    image = Image.open("working/pixelated_image.tif")
    px = image.load()
    pix_size = (e4.get())
    int_pix_size = int(pix_size)

    rows = image.size[0]  # 11
    cols = image.size[1]  # 6

    rows_out = image.size[0] * int_pix_size # 14*11=154
    cols_out = image.size[1] * int_pix_size  # 14*6=84

    d = draw.Drawing(rows_out, cols_out, origin=(0, int_pix_size), displayInline=False)

    for l in range(rows):
        for j in range(cols):
            color_index = ((px[l, j]))
            r,g,b = color_index

            if (rows_out <= cols_out):
                y_orent = (cols_out - (j * int_pix_size))  #
            else:
                y_orent = (cols_out - (j * int_pix_size))

            if(r < toneval and g < toneval and b < toneval):
                r = 0
                g = 0
                b = 0

            print(r)
            print(g)
            print(b)

            Cy = (1-(r/redval))
            Ma = (1-(g / greenval))
            Ye = (1-(b / blueval))

            var_K = 1
            if (Cy < var_K):
                var_K = Cy
            if (Ma < var_K):
                var_K = Ma
            if (Ye < var_K):
                var_K = Ye

            if (var_K == 1):
                Cy = 0
                Ma = 0
                Ye = 0


            else:
                Cy = (Cy - var_K) / (1 - var_K)
                Ma = (Ma - var_K) / (1 - var_K)
                Ye = (Ye - var_K) / (1 - var_K)
                print("color")
                print(Cy,Ma,Ye)


            numb_of_squares_magenta = Ma * int_pix_size
            int_number_of_squares_magenta = int(numb_of_squares_magenta)
            print("magenta")
            print(int_number_of_squares_magenta)

            numb_of_squares_cyan = Cy * int_pix_size
            int_number_of_squares_cyan = int(numb_of_squares_cyan)
            print("cyan")
            print(int_number_of_squares_cyan)

            numb_of_squares_yellow = Ye * int_pix_size
            int_number_of_squares_yellow = int(numb_of_squares_yellow)
            print("yellow")
            print(int_number_of_squares_yellow)

            if (r < toneval and g < toneval and b < toneval):
                color_flip_black = 1.0

            else:
                color_flip_black = 0



            numb_of_squares_black = color_flip_black * int_pix_size  # howmany rects to add 1.0/
            int_number_of_squares_black = int(numb_of_squares_black)




            for numb in range(int_number_of_squares_black):
                d.append(draw.Rectangle((l * int_pix_size + numb/2), (y_orent + numb/2), int_pix_size - numb, int_pix_size - numb, stroke_width=0.5,stroke='black', fill='none', ))

            for numb in range(int_number_of_squares_magenta):
                d.append(draw.Rectangle((l * int_pix_size + numb / 2), (y_orent + numb / 2), int_pix_size - numb, int_pix_size - numb, stroke_width=0.5, stroke='magenta',stroke_opacity=stroke_val, fill='none', ))

            for numb in range(int_number_of_squares_cyan):
                d.append(draw.Rectangle((l * int_pix_size + numb / 2), (y_orent + numb / 2), int_pix_size - numb, int_pix_size - numb, stroke_width=0.5, stroke='cyan',stroke_opacity=stroke_val,fill='none', ))

            for numb in range(int_number_of_squares_yellow):
                d.append(draw.Rectangle((l * int_pix_size + numb / 2), (y_orent + numb / 2), int_pix_size - numb, int_pix_size - numb, stroke_width=0.5, stroke='yellow',stroke_opacity=stroke_val, fill='none', ))

    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++


    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++

    d.saveSvg('working/example_draw.svg')

    svgsample()

def build_circles():
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++

    image = Image.open("working/pixelated_image.tif")
    px = image.load()
    print("image.size   = (%d, %d)" % image.size)
    circle_size = (e5.get())

    int_circle_size = int(circle_size)
    print (type(int_circle_size))
    rows = image.size[0]#11
    cols = image.size[1]#6

    rows_out = image.size[0] * int_circle_size#14*11=154
    cols_out = image.size[1] * int_circle_size#14*6=84


    d = draw.Drawing(rows_out,cols_out, origin=(-int_circle_size/2,int_circle_size/2), displayInline=False)

    redval  = root.red_sliderVal.get()
    blueval = root.blue_sliderVal.get()
    greenval=root.green_sliderVal.get()
    toneval = root.tone_sliderVal.get()

    for l in range(rows):
        for j in range(cols):
            color_index = ((px[l, j]))
            r, g, b = color_index
            print(color_index)
            if (rows_out <= cols_out):
                y_orent=(cols_out-(j*int_circle_size))#
            else:
                y_orent =(cols_out-(j*int_circle_size))

            if (root.v.get() == '1'):
                if (r > redval):
                    d.append(draw.Circle((l*int_circle_size), (y_orent), 7, stroke_width=1, stroke='#00ffff',fill="none"))

                if (g > greenval):
                    d.append(draw.Circle(l*int_circle_size, (y_orent), 5, stroke_width=1, stroke='#ff00ff',fill='none'))

                if (b > blueval):
                    d.append(draw.Circle(l*int_circle_size, (y_orent), 3, stroke_width=1, stroke='#ffff00',fill='none',))

                if ((r+b+g/3) > toneval):
                    d.append(draw.Circle(l*int_circle_size, (y_orent), 1, stroke_width=1, stroke='black',fill='none',))

            else:
                if (r >= redval):
                    d.append(draw.Circle(l*int_circle_size, (y_orent), 7, stroke_width=1, stroke='red',fill='none'))

                if (g >= greenval):
                    d.append(draw.Circle(l*int_circle_size, (y_orent), 5, stroke_width=1, stroke='green',fill='none',))

                if (b >= blueval):
                    d.append(draw.Circle(l*int_circle_size, (y_orent), 3, stroke_width=1, stroke='blue',fill='none'))

                if ((r + b + g / 3) <= toneval):
                    d.append(draw.Circle(l*int_circle_size, (y_orent), 1, stroke_width=1, stroke='black', fill='none', ))

    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++

    d.saveSvg('working/example_draw.svg')

    svgsample()

def fix_viewport_grayscale():
    # create new SVG figure
    #user size input
    x_in_mm = e2.get()
    y_in_mm = e1.get()
    float_x_in_px = float(x_in_mm) * 3.7795275591
    float_y_in_px = float(y_in_mm) * 3.7795275591

    string_loat_x_in_mm = str(x_in_mm) +"mm"
    string_loat_y_in_mm = str(y_in_mm ) +"mm"



    print(string_loat_x_in_mm)
    print(string_loat_y_in_mm)
    print(float_x_in_px," float_x_in_px", float_y_in_px," float_y_in_px")
    print()

    sized = sg.SVGFigure(string_loat_x_in_mm, string_loat_y_in_mm)

    second_svg = sg.fromfile('working/3.svg')

    input_size = second_svg.get_size()
    x_width , y_height = input_size
    float_x_width = float(x_width)
    float_y_height = float(y_height)
    print (float_x_width, " float_x_width-in mm", float_y_height," float_y_height inmm")
    print()


    px_x_width = float(x_width) * 3.7795275591
    px_y_height = float(y_height) * 3.7795275591


    print("----")
    print(px_x_width , " px_x_width- of newsvg inpx", px_y_height, " px_y_height - of nesvg in px")
    print("-----")
    second_svg_obj = second_svg.getroot()

    newscale_x = float_x_in_px / float_x_width
    newscale_y = float_y_in_px / float_y_height

    print(newscale_x," newscale_x", newscale_y," newscale_y")
            #  144 * 11.8 = 1700
    bigsvgy = float_y_height * newscale_x

    print(bigsvgy)
    print("======================")

    if newscale_x < newscale_y:
        # It must be fixed by width
        print("fixed by x")
        offset_y = float((float_y_in_px -72))
        print(offset_y, " offset_y")
        #less moves up?? 2100
        second_svg_obj.scale_xy(newscale_x, newscale_x)
        second_svg_obj.moveto(0.0, offset_y, scale=1)
    else:
        # Fixed by height

        print("fixed by y")
        #second_svg_obj.scale_xy(3034.0,1611.0)
        #second_svg_obj.moveto(0.0,0.0,scale=newscale_y)

    #txt1 = sg.TextElement(0.0, float_y_in_mm, "A", size=120, weight="bold")

    sized.append(second_svg_obj)
    #sized.append(txt1)
    second_svg_obj.save('working/both.svg')

    '''
    #get the finished svg
    example_draw = sg.fromfile("working/example_draw.svg")
    input_size = example_draw.get_size()
    #gets the input of finshied svg
    x_width,y_height = input_size
    print(x_width,y_height)
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # fix view port
    reading_file = open("working/example_draw.svg", "r")
    new_file_content = ""

    for i, line in enumerate(reading_file):
        stripped_line = line.strip()
        if i == 2 :
            new_line = stripped_line.replace(stripped_line, 'width="'+x_width+'" height="'+y_height+'" viewBox="0 0 '+x_width+' '+y_height+'">')
            new_file_content += new_line + "\n"

        else:
            new_line = stripped_line.replace("-", "")
            new_file_content += new_line  + "\n"

    reading_file.close()
    writing_file = open("working/example_draw.svg", 'w')
    writing_file.write(new_file_content)
    writing_file.close()

    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    '''

def svgsample():
    drawing = svg2rlg("working/example_draw.svg")
    renderPM.drawToFile(drawing, "working/temp.png", fmt="PNG")

    image_pil = Image.open(("working/temp.png"))

    '''
    Resize PIL image keeping ratio and using black background.
    '''

    width = 750
    height = 500
    ratio_w = width / image_pil.width
    ratio_h = height / image_pil.height
    if ratio_w < ratio_h:
        # It must be fixed by width
        resize_width = width
        resize_height = round(ratio_w * image_pil.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * image_pil.width)
        resize_height = height
    image_resize = image_pil.resize((resize_width, resize_height), Image.ANTIALIAS)
    background = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background.paste(image_resize, offset)

    sample = ImageTk.PhotoImage(background)
    label9 = Label(image=sample)
    label9.image = sample
    label9.place(x=575, y=25, anchor="nw")
    ###################################################
    ###################################################

def imagestuff():
    # pick an image file you have .bmp  .jpg  .gif.  .png
    # (if not in the working directory, give full path)
    pil_image = Image.open(str(root.filename))
    # retrieve some information
    print()
    print("image.size   = (%d, %d)" +str( pil_image.size[1:-1]))
    print()
    print("image.format = %s" % pil_image.format)  # 'JPEG'
    # common modes are
    # "L" (luminance) for greyscale images,
    # "RGB" for true color images,
    # "CMYK" for pre-press images
    print("image.mode   = %s" % pil_image.mode)    # 'RGB'
    filepath = str(root.filename)
    shortpath = filepath.rsplit("/",1)[1]
    imageInfoString = ("Opening file:  " +shortpath+"\n"+"image.size = (%d, %d)" % pil_image.size +"\n"+ "image.format = %s" % pil_image.format+"\n"+"image.mode   = %s" % pil_image.mode)


    return imageInfoString

def close_window():
    root.destroy()

def openfile():
    # *** open file ***
    root.filename = filedialog.askopenfilename(initialdir="images/", title="Select file", filetypes=(
    ("jpeg files", "*.jpg"),("png files", "*.png"), ("all files", "*.*")))

    print ("opening file at  " +str(root.filename))

    displayimageSample()

def openSVG():
    # *** open file ***
    root.SVGfile = filedialog.askopenfilename(initialdir="SVGS/", title="Select file", filetypes=(
    ("SVG files", "*.svg"), ("all files", "*.*")))

    print ("opening file at  " +str(root.SVGfile))

def savefile():
    # *** save_file ***
    root.filenamesave = filedialog.asksaveasfilename(initialdir="images/", title="Select file", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    print("saving file to "+ root.filenamesave)

# *** display images***
def displayimageSample():
    image = Image.open(str(root.filename))
    print("image.size   = (%d, %d)" % image.size)
    # 200x200 is good

    if image.size[1] > image.size[0]:
        (maxsize(image.size[1]))
    else:
        (maxsize(image.size[0]))

    '''
        Resize PIL image keeping ratio and using black background.
        '''

    width = 250
    height = 250
    ratio_w = width / image.width
    ratio_h = height / image.height
    if ratio_w < ratio_h:
        # It must be fixed by width
        resize_width = width
        resize_height = round(ratio_w * image.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * image.width)
        resize_height = height
    image_resize = image.resize((resize_width, resize_height), Image.ANTIALIAS)
    background = Image.new('RGB', (width, height), (0, 0, 0))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background.paste(image_resize, offset)

    photoblack = ImageTk.PhotoImage(background)
    label8 = Label(image=photoblack)
    label8.image = photoblack
    label8.place(x=325, y=25, anchor="nw")

def RGB():

    img = Image.open(str(root.filename))
    data = img.getdata()


    if (root.v.get() == '1'):
        print("inverting")

        r = [(d[0], 255, 255) for d in data]
        g = [(255, d[1], 255) for d in data]
        b = [(255, 255, d[2]) for d in data]
    else:
        print("normal")

        # Suppress specific bands (e.g. (255, 120, 65) -> (0, 120, 0) for g)
        r = [(d[0], 0, 0) for d in data]
        g = [(0, d[1], 0) for d in data]
        b = [(0, 0, d[2]) for d in data]

    img.putdata(r)
    img.save('working/r.png')
    img.putdata(g)
    img.save('working/g.png')
    img.putdata(b)
    img.save('working/b.png')
    #### image previews ###


    red = Image.open(('working/r.png'))

    green = Image.open(('working/g.png'))

    blue = Image.open(('working/b.png'))


    width = 250
    height = 250
    ratio_w = width / img.width
    ratio_h = height / img.height
    if ratio_w < ratio_h:
        # It must be fixed by width
        resize_width = width
        resize_height = round(ratio_w * img.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * img.width)
        resize_height = height

    image_resize_red = red.resize((resize_width, resize_height), Image.ANTIALIAS)
    image_resize_green = green.resize((resize_width, resize_height), Image.ANTIALIAS)
    image_resize_blue = blue.resize((resize_width, resize_height), Image.ANTIALIAS)


    background_red = Image.new('RGB', (width, height), (0, 0, 0))
    background_green = Image.new('RGB', (width, height), (0, 0, 0))
    background_blue = Image.new('RGB', (width, height), (0, 0, 0))

    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))


    background_red.paste(image_resize_red, offset)
    background_green.paste(image_resize_green, offset)
    background_blue.paste(image_resize_blue, offset)


    photored =ImageTk.PhotoImage(background_red)
    photogreen = ImageTk.PhotoImage(background_green)
    photoblue = ImageTk.PhotoImage(background_blue)

###################################################
###################################################

    label11 = Label(image=photored)
    label11.image = photored
    label11.place(x=575, y=25, anchor="nw")

###################################################
###################################################


    label11 = Label(image=photogreen)
    label11.image = photogreen
    label11.place(x=825, y=25, anchor="nw")
###################################################
###################################################
    label9 = Label(image=photoblue)
    label9.image = photoblue
    label9.place(x=1075, y=25, anchor="nw")


###################################################
###################################################
    photo_pixelate_small = Image.open(('working/result.tif'))
    data_pix = photo_pixelate_small.getdata()

    if (root.v.get() == '1'):
        print("inverting")
        # Suppress specific bands (e.g. (255, 120, 65) -> (0, 120, 0) for g)
        p_r = [(di[0], 255, 255) for di in data_pix]
        p_g = [(255, di[1], 255) for di in data_pix]
        p_b = [(255, 255, di[2]) for di in data_pix]
    else:
        print("normal")

        # Suppress specific bands (e.g. (255, 120, 65) -> (0, 120, 0) for g)
        p_r = [(di[0], 0, 0) for di in data_pix]
        p_g = [(0, di[1], 0) for di in data_pix]
        p_b = [(0, 0, di[2]) for di in data_pix]

    photo_pixelate_small.putdata(p_r)
    photo_pixelate_small.save('working/p_r.png')
    photo_pixelate_small.putdata(p_g)
    photo_pixelate_small.save('working/p_g.png')
    photo_pixelate_small.putdata(p_b)
    photo_pixelate_small.save('working/p_b.png')


    red_pix = Image.open(('working/p_r.png'))
    redthumb_pix =red_pix.resize((resize_width, resize_height), Image.ANTIALIAS)
    green_pix = Image.open(('working/p_g.png'))
    greenthumb_pix =green_pix.resize((resize_width, resize_height), Image.ANTIALIAS)
    blue_pix = Image.open(('working/p_b.png'))
    bluethumb_pix =blue_pix.resize((resize_width, resize_height), Image.ANTIALIAS)

    background_red_p = Image.new('RGB', (width, height), (0, 0, 0))
    background_green_p = Image.new('RGB', (width, height), (0, 0, 0))
    background_blue_p = Image.new('RGB', (width, height), (0, 0, 0))

    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))

    background_red_p.paste(redthumb_pix, offset)
    background_green_p.paste(greenthumb_pix, offset)
    background_blue_p.paste(bluethumb_pix, offset)

    photored_thumb = ImageTk.PhotoImage(background_red_p)
    photogreen_thumb = ImageTk.PhotoImage(background_green_p)
    photoblue_thumb = ImageTk.PhotoImage(background_blue_p)


###################################################
###################################################


    label9 = Label(image=photored_thumb)
    label9.image = photored_thumb
    label9.place(x=575, y=275, anchor="nw")
###################################################
###################################################


    label11 = Label(image=photogreen_thumb)
    label11.image = photogreen_thumb
    label11.place(x=825, y=275, anchor="nw")
###################################################
###################################################


    label11 = Label(image=photoblue_thumb)
    label11.image = photoblue_thumb
    label11.place(x=1075, y=275, anchor="nw")

def pixelate():
    print(v.get())
    # Open Paddington
    img = Image.open(str(root.filename))

    # Resize smoothly down to 16x16 pixels
    #size = 60
    size = (root.pixelate_sliderVal.get())
    mode = (v.get())

    print (mode)
    print (size)
    print(img.size[0])
    print (img.size[1])

    # Scale back up using NEAREST to original
    if v.get() != NONE:

        if img.size[1] < img.size[0]:
            maxsize =img.size[1]
        else:
            maxsize=img.size[0]

        print (maxsize)

        wpercent = (size / float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))

        ###
        # PIL.Image.NEAREST,
        # PIL.Image.BILINEAR,
        # PIL.Image.BICUBIC
        # PIL.Image.LANCZOS
        ###
        if mode == "BILINEAR":
            imgSmall = img.resize((int(size), int(hsize)), resample=Image.BILINEAR)
        if mode == "NEAREST ":
            imgSmall = img.resize((int(size), int(hsize)), resample=Image.NEAREST)
        if mode == "BICUBIC ":
            imgSmall = img.resize((int(size), int(hsize)), resample=Image.BICUBIC)
        if mode == "LANCZOS ":
            imgSmall = img.resize((int(size), int(hsize)), resample=Image.LANCZOS)

        result = imgSmall.resize((img.size[0], img.size[1]), resample=Image.NEAREST)

        # Save
        result.save('working/result.tif')
        # Save
        imgSmall.save('working/pixelated_image.tif')

    ###################################################
    ###################################################


    pixelateimg = Image.open(('working/result.tif'))

    width = 250
    height = 250
    ratio_w = width / pixelateimg.width
    ratio_h = height / pixelateimg.height
    if ratio_w < ratio_h:
        # It must be fixed by width
        resize_width = width
        resize_height = round(ratio_w * pixelateimg.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * pixelateimg.width)
        resize_height = height
    image_resize = pixelateimg.resize((resize_width, resize_height), Image.ANTIALIAS)
    background_pixelate = Image.new('RGB', (width, height), (0, 0, 0))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background_pixelate.paste(image_resize, offset)
    pixelsample = ImageTk.PhotoImage(background_pixelate)


###################################################
###################################################
    labelpixel = Label(image=pixelsample)
    labelpixel.image = pixelsample
    labelpixel.place(x=325, y=275, anchor="nw")

def OUTLINE():
    print("outline")
    img = cv2.imread(('working/pixelated_image.tif'))
    (h, w) = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    edged = cv2.Canny(hsv, 100, 200)
    image, contours, hierachy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    idx = 0
    for c in contours:
        plt.plot(c[:, 0, 0], h - c[:, 0, 1], linewidth=1)
    plt.axis('off')

    plt.savefig("working/test1.svg", format="svg")
    plt.show()
def Fill():
    print("fill")

def Image_edit():
    print("Image_edit")
    img = Image.open("working/pixelated_image.tif")

    redval  = root.red_sliderVal.get()
    blueval = root.blue_sliderVal.get()
    greenval=root.green_sliderVal.get()
    toneval = root.tone_sliderVal.get()


    img = img.convert("RGBA")

    pixdata = img.load()



    # Clean the background noise, if color != white, then set to black.

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y] <= (redval, blueval, greenval, toneval):
                pixdata[x, y] = (redval, blueval, greenval, toneval)
            else:
                pixdata[x, y] =

    img.save('working/result.tif')

    ###################################################
    ###################################################

    pixelateimg = Image.open(('working/result.tif'))

    width = 250
    height = 250
    ratio_w = width / pixelateimg.width
    ratio_h = height / pixelateimg.height
    if ratio_w < ratio_h:
        # It must be fixed by width
        resize_width = width
        resize_height = round(ratio_w * pixelateimg.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * pixelateimg.width)
        resize_height = height
    image_resize = pixelateimg.resize((resize_width, resize_height), Image.ANTIALIAS)
    background_pixelate = Image.new('RGB', (width, height), (0, 0, 0))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background_pixelate.paste(image_resize, offset)
    pixelsample = ImageTk.PhotoImage(background_pixelate)

    ###################################################
    ###################################################
    labelpixel = Label(image=pixelsample)
    labelpixel.image = pixelsample
    labelpixel.place(x=325, y=275, anchor="nw")


###################################################
root = Tk()
def submenu_and_checkboxes():

    # ***main menue***
    menu =Menu(root)
    root.geometry("1150x650") #Width x Height
    root.config(menu=menu)

    subMenu = Menu(menu)
    menu.add_cascade(label="File", menu=subMenu)
    subMenu.add_command(label = "open image", command= openfile)
    subMenu.add_command(label = "open SVG", command= openSVG)
    subMenu.add_separator()
    subMenu.add_command(label = "exit", command = close_window)

    #look at this menue not working
    editMenu = Menu(menu)
    menu.add_cascade(label = "Edit", command = openfile)
    editMenu.add_command(label = "Redo",command = openfile)

    #*** check button***
    root.v = StringVar()
    c1 = Checkbutton(root, text ="invert colors", variable=root.v,bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    c1.deselect()
    c1.grid(row=0, column=0)

    #*** check button***
    root.sim = StringVar()
    c2 = Checkbutton(root, text ="simulate", variable=root.sim, bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    c2.deselect()
    c2.grid(row=0, column=1)


    #*** check button***
    root.white_val = StringVar()
    c3 = Checkbutton(root, text ="white_val", variable=root.white_val, bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    c3.deselect()
    c3.place(x=100,y= 640)

    #*** check button***
    root.hor_line = StringVar()
    c4 = Checkbutton(root, text ="horizontal", variable=root.hor_line, bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    c4.deselect()
    c4.place(x=193,y= 640)

    #*** check button***
    root.rotate_line = StringVar()
    c5 = Checkbutton(root, text ="rotate_line", variable=root.rotate_line, bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    c5.deselect()
    c5.place(x=289,y= 640)

    #*** check button***
    root.spin_line = StringVar()
    c6 = Checkbutton(root, text ="spin_line", variable=root.spin_line, bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    c6.deselect()
    c6.place(x=389,y= 640)


    #*** check button***
    root.set_colors = StringVar()
    c8 = Checkbutton(root, text ="set_color", variable=root.set_colors, bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    c8.select()
    c8.place(x=0,y= 385)

    #*** check button***
    root.ascii_small = StringVar()
    c9 = Checkbutton(root, text ="10chr", variable=root.ascii_small, bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    c9.deselect()
    c9.place(x=200, y=473)

    #*** check button***
    root.ascii_large = StringVar()
    c11 = Checkbutton(root, text ="75chr", variable=root.ascii_large, bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    c11.deselect()
    c11.place(x=260, y=473)


submenu_and_checkboxes()

def show_entry_fields():
    print("OUTPUT X: %s\nOUTPUT Y: %s" % (e1.get(), e2.get()))
    print("machine code: %s\nnumb of colors: %s" % (e3.get(), e4.get()))
    print(  e5.get())

def reset():
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)

def getColor():
    style = ttk.Style(root)
    style.theme_use('clam')
    hex_code, RGB_code = askcolor((255, 255, 0), root)
    print(hex_code, RGB_code)
    return RGB_code

def buttons_and_Labels():
    #*** text boxes***
    Label(root, text="OUT height in mm",anchor="e",bg="gray20", fg="lime green").place(x=5, y=25, height=20, width=125)
    Label(root, text="OUT  width in mm",anchor="e",bg="gray20", fg="lime green").place(x=5, y=45, height=20, width=125)
    Label(root, text="Marker Size in mm",anchor="e",bg="gray20", fg="lime green").place(x=5, y=65, height=20, width=125)
    Label(root, text="# of colors",anchor="e",bg="gray20", fg="lime green").place(x=5, y=85, height=20, width=125)
    Label(root, text="OUTPUT pixel size",anchor="e",bg="gray20", fg="lime green").place(x=5, y=105, height=20, width=125)
    Label(root, text="Pix",anchor="e",bg="gray20", fg="lime green").place(x=5, y=145, height=20, width=123)
    Label(root, text="Red",anchor="e",bg="gray20", fg="lime green").place(x=5, y=185, height=20, width=125)
    Label(root, text="Blu",anchor="e",bg="gray20", fg="lime green").place(x=5, y=225, height=20, width=125)
    Label(root, text="Gre",anchor="e",bg="gray20", fg="lime green").place(x=5, y=265, height=20, width=125)
    Label(root, text="B/W",anchor="e",bg="gray20", fg="lime green").place(x=5, y=305, height=20, width=125)

    Button(root,text='',  command=setcolorred, bg="red", fg="red",highlightbackground="lime green",activebackground="red").place(x=5,y=145,height= 40, width=40)
    Button(root,text='',  command=setcolorgreen, bg="green", fg="green",highlightbackground="lime green",activebackground="green").place(x=45,y=145,height= 40, width=40)
    Button(root,text='',  command=setcolorblue, bg="blue", fg="blue",highlightbackground="lime green",activebackground="blue").place(x=5,y=185,height= 40, width=40)
    Button(root,text='',  command=setcolorwhite, bg="white", fg="white",highlightbackground="lime green",activebackground="white").place(x=45,y=185,height= 40, width=40)
    Button(root,text='',  command=setcolorblack, bg="black", fg="black",highlightbackground="lime green",activebackground="black").place(x=5,y=225,height= 40, width=40)
    Button(root,text='',  command=setcoloryellow, bg="yellow", fg="yellow",highlightbackground="lime green",activebackground="yellow").place(x=45,y=225,height= 40, width=40)
    Button(root,text='',  command=setcolormagenta, bg="magenta", fg="magenta",highlightbackground="lime green",activebackground="magenta").place(x=5,y=265,height= 40, width=40)
    Button(root,text='',  command=setcolorcyan, bg="cyan", fg="cyan",highlightbackground="lime green",activebackground="cyan").place(x=45,y=265,height= 40, width=40)

    Button(root, text='edit_image', command=Image_edit, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=105, y=423, height=25, width=100)
    Button(root, text='path_fill', command=Fill, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=0, y=423, height=25, width=100)
    Button(root, text='OUTLINE', command=OUTLINE, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=0, y=448, height=25, width=100)
    Button(root, text='ASCII', command=ASCII, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=0, y=473, height=25, width=100)
    Button(root, text='Color_Picker', command=getColor, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=285, y=0, height=25, width=100)
    Button(root, text='img info', command=infopanel, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=195, y=0, height=25, width=100)
    Button(root, text='Custom', command=custom, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=0, y=498, height=25, width=100)
    Button(root, text='RGB split', command=RGB, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=385, y=0, height=25, width=100)
    Button(root, text='color circles', command=build_circles, bg="gray20", fg="lime green",
           highlightbackground="gray20", activebackground="deep sky blue").place(x=0, y=523, height=25, width=100)
    Button(root, text='color pixels', command=build_pixels, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=0, y=548, height=25, width=100)
    Button(root, text='Gray_shapes', command=gray_scale, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=0, y=572, height=25, width=100)
deault = StringVar(root, value='8')
e5 = Entry(root, textvariable=deault)
deault2 = StringVar(root, value='8')
e4 = Entry(root, textvariable=deault2)

default_x_mm_output = StringVar(root, value='600')
e1 = Entry(root, textvariable=default_x_mm_output)
default_y_mm_output = StringVar(root, value='800')
e2 = Entry(root, textvariable=default_y_mm_output)
default_markertip_mm_output = StringVar(root, value='1.6')
e3 = Entry(root, textvariable=default_markertip_mm_output)

e1.place(x=135, y=25, height=20, width=75)
e2.place(x=135, y=45, height=20, width=75)
e3.place(x=135, y=65, height=20, width=75)
e4.place(x=135, y=85, height=20, width=75)
e5.place(x=135, y=105, height=20, width=75)



root.ASCII_sliderVal = Scale(root, from_=0, to=100, length=100, orient=HORIZONTAL, bg="gray20",
                           fg="lime green",
                           highlightbackground="gray20", activebackground="deep sky blue", troughcolor="spring green")
root.ASCII_sliderVal.place(x=100, y=453)
root.red_sliderVal = Scale(root, from_=0, to=255, length=150, orient=HORIZONTAL, bg="gray20",
                           fg="lime green",
                           highlightbackground="gray20", activebackground="deep sky blue", troughcolor="red")
root.red_sliderVal.place(x=135, y=165)

root.blue_sliderVal = Scale(root, from_=0, to=255, length=150, orient=HORIZONTAL, bg="gray20",
                            fg="lime green",
                            highlightbackground="gray20", activebackground="deep sky blue", troughcolor="blue")
root.blue_sliderVal.place(x=135, y=205)

root.green_sliderVal = Scale(root, from_=0, to=255, length=150, orient=HORIZONTAL, bg="gray20",
                             fg="lime green",
                             highlightbackground="gray20", activebackground="deep sky blue", troughcolor="green")
root.green_sliderVal.place(x=135, y=245)
root.tone_sliderVal = Scale(root, from_=0, to=255, length=150, orient=HORIZONTAL, bg="gray20",
                            fg="lime green",
                            highlightbackground="gray20", activebackground="deep sky blue", troughcolor="gray49")
root.tone_sliderVal.place(x=135, y=285)

root.tone_sliderVal.set(125)  # Set the initial value to 125
root.green_sliderVal.set(125)  # Set the initial value to 125
root.blue_sliderVal.set(125)  # Set the initial value to 125
root.red_sliderVal.set(125)  # Set the initial value to 125
root.ASCII_sliderVal.set(12)  # Set the initial value to 125

Label(root, text="Sample_Mode", anchor="w", bg="gray20", fg="lime green").place(x=210, y=25, height=20, width=100)
MODES = [
    ("NEAREST ", "NEAREST "),
    ("BILINEAR", "BILINEAR"),
    ("BICUBIC ", "BICUBIC "),
    ("LANCZOS ", "LANCZOS "),
]

v = StringVar()
v.set("L")  # initialize
count = 0
for text, mode in MODES:
    b = Radiobutton(root, text=text, variable=v, value=mode, command=pixelate, bg="gray20", fg="lime green",
                    highlightbackground="gray20", activebackground="deep sky blue").place(x=215, y=44 + count)
    count = count + 20
v.set("LANCZOS ")

MODES2 = [
    ("CIRCLES", "CIRCLES"),
    ("SQUARE_", "SQUARE_"),
    ("LINE___", "LINE___"),
]
shapes = StringVar()
shapes.set("L")  # initialize
menue_count = 0
for text2, mode2 in MODES2:
    b2 = Radiobutton(root, text=text2, variable=shapes, value=mode2, command=shape_select, bg="gray20",
                     fg="lime green", highlightbackground="gray20", activebackground="deep sky blue").place(x=0,
                                                                                                            y=600 + menue_count)
    menue_count = menue_count + 20
shapes.set("SQUARE_")
root.configure(background='gray20')
buttons_and_Labels()

def box1_color():
    button_color1 = box1color
    if (root.set_colors.get() == "0"):
        global color_pick
        color_pick = box1color
        print("uphere")

    else:
        Button(root, text='', command=setvar1, bg=button_color1, fg=button_color1, highlightbackground="lime green",
               activebackground=button_color1).place(x=5, y=305, height=40, width=40)

def setvar1():

    if (root.set_colors.get() == "1"):
        button_color1 = getColor()
        global color_pick
        color_pick = button_color1
        global box1color
        box1color = button_color1
        Button(root, text='', command=box1_color, bg=button_color1, fg=button_color1, highlightbackground="lime green",
               activebackground=button_color1).place(x=5, y=305, height=40, width=40)

def box2_color():
    button_color2 = box2color
    if (root.set_colors.get() == "0"):
        global color_pick
        color_pick = box2color

    else:
        Button(root, text='', command=setvar2, bg=button_color2, fg=button_color2, highlightbackground="lime green",
               activebackground=button_color2).place(x=45, y=305, height=40, width=40)

def setvar2():
    if (root.set_colors.get() == "1"):
        button_color2 = getColor()
        global color_pick
        color_pick = button_color2
        global box2color
        box2color = button_color2
        Button(root, text='', command=box2_color, bg=button_color2, fg=button_color2, highlightbackground="lime green",
               activebackground=button_color2).place(x=45, y=305, height=40, width=40)

def box3_color():
    button_color3 = box3color
    if (root.set_colors.get() == "0"):
        global color_pick
        color_pick = box3color
    else:
        Button(root, text='', command=setvar3, bg=button_color3, fg=button_color3, highlightbackground="lime green",
               activebackground=button_color3).place(x=5, y=345, height=40, width=40)

def setvar3():
    if (root.set_colors.get() == "1"):
        button_color3 = getColor()
        global color_pick
        color_pick = button_color3
        global box3color
        box3color = button_color3
        Button(root, text='', command=box3_color, bg=button_color3, fg=button_color3, highlightbackground="lime green",
               activebackground=button_color3).place(x=5, y=345, height=40, width=40)

def box4_color():
    button_color4 = box4color
    if (root.set_colors.get() == "0"):
        global color_pick
        color_pick = box4color
    else:
        Button(root, text='', command=setvar4, bg=button_color4, fg=button_color4, highlightbackground="lime green",
               activebackground=button_color4).place(x=45, y=345, height=40, width=40)

def setvar4():
    if (root.set_colors.get() == "1"):
        button_color4 = getColor()
        global color_pick
        color_pick = button_color4
        global box4color
        box4color = button_color4
        Button(root, text='', command=box4_color, bg=button_color4, fg=button_color4, highlightbackground="lime green",
               activebackground=button_color4).place(x=45, y=345, height=40, width=40)

def set_color_buttons():
    button_color1 = "azure2"
    Button(root,text='',  command=setvar1, bg=button_color1, fg=button_color1,highlightbackground="lime green",activebackground=button_color1).place(x=5,y=305,height= 40, width=40)
    button_color2 = "azure2"
    Button(root,text='',  command=setvar2, bg=button_color2, fg=button_color2,highlightbackground="lime green",activebackground=button_color2).place(x=45,y=305,height= 40, width=40)
    button_color3 = "azure2"
    Button(root,text='',  command=setvar3, bg=button_color3, fg=button_color3,highlightbackground="lime green",activebackground=button_color3).place(x=5,y=345,height= 40, width=40)
    button_color4 = "azure2"
    Button(root,text='',  command=setvar4, bg=button_color4, fg=button_color4,highlightbackground="lime green",activebackground=button_color4).place(x=45,y=345,height= 40, width=40)
set_color_buttons()

def cmd(speed):
    pixelate()

def maxsize(size):
    root.pixelate_sliderVal = Scale(root, from_=2, to=size, length=150, orient=HORIZONTAL,command=cmd, bg="gray20",
                               fg="lime green",
                               highlightbackground="gray20", activebackground="deep sky blue",troughcolor="lavender")
    root.pixelate_sliderVal.place(x=135, y=125)

root.mainloop()