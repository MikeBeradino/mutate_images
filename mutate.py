import center_tk_window
from tkinter import filedialog
from tkinter import *
import tkinter.ttk as ttk
import tkinter.scrolledtext as st
from tkcolorpicker import askcolor
from random import random, randint , shuffle
from PIL import Image
from PIL import ImageTk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import drawSvg as draw
import svgutils.transform as sg
import re
from math import sin, cos, radians
import sys
sys.setrecursionlimit(10**6) # needed for some opencv--> gcode conversions
import numpy as np
import matplotlib.pyplot as plt
# External Imports
import os
import sys
import re
from array import *
import xml.etree.ElementTree as ET

###########################################################
#used to generate Gcode
###########################################################
# Local Imports
sys.path.insert(0, './lib') # (Import from lib folder)
import shapes as shapes_pkg
from shapes import point_generator
DEBUGGING = True
SVG = set(['rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'])
#############################################################
###########################################################
#used in blacklines
###########################################################
from blackstripes import crossed
from blackstripes import sketchy
from blackstripes import spiral
###########################################################
###########################################################
###########################################################
#PenKIT stuff
###########################################################
from penkit.fractal import hilbert_curve
from penkit.textures.util import fit_texture
from penkit.textures import make_grid_texture
from penkit.textures.util import rotate_texture
from penkit.surfaces import make_noise_surface
#from penkit.write import write_plot
from penkit.projection import project_and_occlude_texture
import xml.etree.ElementTree as ET
import numpy as np
###########################################################
###########################################################
###########################################################
#line_drawing_stuff
###########################################################

import math
import argparse
from PIL import Image, ImageDraw, ImageOps
from filters import *
from strokesort import *
import perlin
from util import *
no_cv = False
try:
    import numpy as np
    import cv2
except:
    print("Cannot import numpy/openCV. Switching to NO_CV mode.")
    no_cv = True
###########################################################
###########################################################
#import image editor

###########################################################
###########################################################
###########################################################
###########################################################
#import eggbot
#import egg_main
###########################################################
###########################################################
color_pick="#000000"

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

def test_custom():
    if root.SVGfile == "":
        # *** open file ***
        root.SVGfile = filedialog.askopenfilename(initialdir="svgs4images", title="Select file", filetypes=(("SVG files", "*.svg"), ("all files", "*.*")))
        print ("opening file at  " +str(root.SVGfile))
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # get nib size
    # get pix size
    # caculate svgs per pixel

    # make temp " pixels
    # +++++++++++++++++++++++++++++++++++++++++++++++
    svgfile = (str(root.SVGfile))
    image = Image.open("working/pixelated_image.tif").convert('LA').rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
    pix_size = (e5.get())
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
            if (rows_out <= cols_out):
                y_orent = (cols_out - (j * int_pix_size))
            else:
                y_orent = (cols_out - (j * int_pix_size))

            svg_name.append([str(number)])
            svg_to_append.append([str(number)])
            svg_name[number] = sg.fromfile(svgfile)
            svg_to_append[number] = svg_name[number].getroot()

            svg_to_append[number].moveto(l * int_pix_size, (y_orent), scale=1)
            fig.append([svg_to_append[number]])
            number = number+1
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++

    # +++++++++++++++++++++++++++++++++++++++++++++++
    setleng = len(set_button_list)
    for i in range(setleng):
        layer_name = root.set_button_name_var[i].get()
        if layer_name == "1":
            fig.save('Layers/layer_' + str(i) +'_.svg')
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++

    layer_sample()

def custom():

    if root.SVGfile == "":
        # *** open file ***
        root.SVGfile = filedialog.askopenfilename(initialdir="svgs4images", title="Select file", filetypes=(("SVG files", "*.svg"), ("all files", "*.*")))
        print ("opening file at  " +str(root.SVGfile))

    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    svgfile = (str(root.SVGfile))
    image = Image.open("working/pixelated_image.tif").convert('LA').rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
    pix_size = (e5.get())
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
            if (rows_out <= cols_out):
                y_orent = (cols_out - (j * int_pix_size))
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

    # +++++++++++++++++++++++++++++++++++++++++++++++
    setleng = len(set_button_list)
    for i in range(setleng):
        layer_name = root.set_button_name_var[i].get()
        if layer_name == "1":
            fig.save('Layers/layer_' + str(i) +'_.svg')
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++

    layer_sample()

def ASCII():

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

    shortASCII =" .:-=+*#%@"
    longASCII = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,^'. "
    for l in range(rows):
        for j in range(cols):
            color_index = ((px[l, j]))
            gray, alpa = color_index
            #color_flip = 256 - gray # color invert correction <-- that was wrong
            color_flip =  gray
            if (root.ascii_small.get() == '1'):
                index = color_flip /25.5
                int_index = int(index)
                char = shortASCII[int_index]
            if (root.ascii_large.get() == '1'):
                index = color_flip /3.75
                int_index = int(index)
                char = longASCII[int_index]

            numb_of_squares = color_flip / gray_scale_values
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
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    setleng = len(set_button_list)
    for i in range(setleng):
        layer_name = root.set_button_name_var[i].get()
        if layer_name == "1":
            fig.save('Layers/layer_' + str(i) +'_.svg')
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++

    layer_sample()

def layers():
    x_offset = x_offest_box.get()
    y_offset = y_offset_box.get()
    scale = scale_box.get()
    x_offset_float= float(x_offset)
    y_offset_float=float(y_offset)
    scale_float=float(scale)
    vewleng = len(view_button_list)
    for i in range(vewleng):
        set_checked = root.set_button_name_var[i].get()
        if set_checked == "1":
            transform_data[i]=[x_offset_float,y_offset_float,scale_float]

def Set_layers():
    count = 60
    root.set_button_name_var= []
    root.view_button_name_var = []
    Button(root, text='View_Layer', command=layer_sample, bg="gray20",anchor="w", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=1325, y=40, height=20, width=100)
    Button(root, text='SET_Layer', command=layers, bg="gray20", anchor="w",fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=1425, y=40, height=20, width=100)

    layer_boxes = layers_box.get()
    int_layer_boxes = int(layer_boxes)
    
    # remove previous Checkboxes
    for cb in set_button_list and view_button_list:
        cb.destroy()
        cb.forget()

    for cb in set_button_list:
        cb.destroy()
        cb.forget()
    view_button_list.clear()
    set_button_list.clear()
    transform_data.clear()
    root.set_button_name_var.clear()
    root.view_button_name_var.clear()

    for i in range (int_layer_boxes):

        root.set_button_name_var.append(StringVar())
        root.view_button_name_var.append(StringVar())
        set_button_name = Checkbutton(root, text=str(i) + " set", anchor="e", variable=root.set_button_name_var[i], bg="gray20",
                                       fg="lime green", highlightbackground="gray20", activebackground="deep sky blue")
        set_button_name.select()
        set_button_name.place(x=1425, y=count)
        set_button_list.append(set_button_name)

        # create Checkbutton for filename and keep on list
        view_button_name = Checkbutton(root,text =str(i)+" view", anchor="e",variable=root.view_button_name_var[i], bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
        view_button_name.select()
        view_button_name.place(x=1335, y=count)
        count = count + 20
        view_button_list.append(view_button_name)
        transform_data.append([0, 0, 1.0])
# to keep all Checkbuttons
view_button_list = []
set_button_list = []
transform_data = [[0,0,1.0],[0,0,1.0]]

def make_layer_stack():
    print("makelayers")
    # add offset val box
    # link to normal layers
    # get folder
def dots():
    print("dots")
    dot_size = e3.get()
    pixel_size = e5.get()
    dpi = int(pixel_size)/float(dot_size)
    int_dpi = int(dpi)
    int_pix_size = int(pixel_size)
    int_dpi_box = int_dpi*int_dpi
    image = Image.open("working/pixelated_image.tif").convert('LA').transpose(Image.FLIP_TOP_BOTTOM)
    px = image.load()
    rows = image.size[0]
    cols = image.size[1]
    rows_out = image.size[0] * int_pix_size
    cols_out = image.size[1] * int_pix_size
    d = draw.Drawing(rows_out, cols_out, origin=(0, 0), displayInline=False)
    gray_scale_values = 256 / int_dpi_box # if dpi=25  grayscalevalues = 10ish --- every shift by 10vla makes more or less dots
    ### make a 2d arary to hold all points in a given pixle of the output
    no_repeat = [[""] * (2) for _ in range(int(int_dpi_box))]

    for l in range(cols):
        print (l ,"_cols")
        #foward
        #if l%2 == 0:
        for j in range(rows):
            print(j,"_rows")
            color_index = ((px[j, l]))
            x_min = j*int_dpi
            x_max = j*int_dpi+int_dpi
            y_min = l*int_dpi
            y_max = l*dpi+dpi
            gray, alpa = color_index
            num_of_dots = (255-gray) / gray_scale_values
            int_num_of_dots = int(num_of_dots)
            print(gray_scale_values, " gray_scae")
            print(gray , " gray")
            print(int_num_of_dots,  " num_of_dots")

            index = 0
            for i in range(int_dpi):
                for j in range(int_dpi):
                    no_repeat[index][0] = [i+x_min]
                    no_repeat[index][1] = [j+y_min]
                    index += 1
            ### shuffle up the array
            shuffle(no_repeat)
            for ii, sublist in enumerate(no_repeat):
                shuffle(no_repeat[ii])
            print(no_repeat)
            #need to trim leng of no_repeat to int_num_of_dots
            cut_dots_pos = no_repeat[:int_num_of_dots]
            print(cut_dots_pos)


            for dots in range(len(cut_dots_pos)):
                ran_x = cut_dots_pos[dots][0]
                ran_y = cut_dots_pos[dots][1]
                str_ran_x = str(ran_x).strip('[]')
                str_ran_y = str(ran_y).strip('[]')
                int_ran_x = int(str_ran_x )
                int_ran_y = int(str_ran_y )
                print(ran_x, sep='')
                print (ran_x , " ranx")
                print("making dots")
                d.append(draw.Lines(int_ran_x, int_ran_y, int_ran_x+.8, int_ran_y, close=False, fill="none", stroke=color_pick, stroke_width=dot_size))
        '''
        else:
            for j in range(rows):
                print(j,"_rows")
                color_index = ((px[j, l]))
                x_min = j*int_dpi
                x_max = j*int_dpi+int_dpi
                y_min = l*int_dpi
                y_max = l*dpi+dpi
                gray, alpa = color_index
                num_of_dots = (255-gray) / gray_scale_values
                int_num_of_dots = int(num_of_dots)
                print(gray_scale_values, " gray_scae")
                print(gray , " gray")
                print(int_num_of_dots,  " num_of_dots")

                index = 0
                for i in range(int_dpi):
                    for j in range(int_dpi):
                        no_repeat[index][0] = [i+x_min]
                        no_repeat[index][1] = [j+y_min]
                        index += 1
                ### shuffle up the array
                shuffle(no_repeat)
                for ii, sublist in enumerate(no_repeat):
                    shuffle(no_repeat[ii])
                print(no_repeat)
                #need to trim leng of no_repeat to int_num_of_dots
                cut_dots_pos = no_repeat[:int_num_of_dots]
                print(cut_dots_pos)

                for dots in range(len(cut_dots_pos)):
                    ran_x = cut_dots_pos[dots][0]
                    ran_y = cut_dots_pos[dots][1]
                    str_ran_x = str(ran_x).strip('[]')
                    str_ran_y = str(ran_y).strip('[]')
                    int_ran_x = int(str_ran_x )
                    int_ran_y = int(str_ran_y )
                    print(ran_x, sep='')
                    print (ran_x , " ranx")
                    print("making dots")
                    d.append(draw.Lines(int_ran_x, int_ran_y, int_ran_x + .01, int_ran_y, close=False, fill="none",
                                        stroke=color_pick, stroke_width=dot_size))


        '''

            


    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    setleng = len(set_button_list)
    for i in range(setleng):
        layer_name = root.set_button_name_var[i].get()
        if layer_name == "1":
            d.saveSvg('Layers/layer_' + str(i) +'_.svg')
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++

    layer_sample()





def gray_Lines():
    mode5 = (line_type.get())
    ("Horizontal", "Horizontal"),
    ("Spin", "Spin"),
    ("Rotate", "Rotate"),
    image = Image.open("working/pixelated_image.tif").convert('LA').transpose(Image.FLIP_TOP_BOTTOM)
    pix_size = (e5.get())
    nib_size = (e3.get())
    max_lines = float(pix_size) / float(nib_size)
    int_pix_size = int(pix_size)
    degrees = root.rotation_slider.get()
    rows = image.size[0]  # 11
    cols = image.size[1]  # 6
    rows_out = image.size[0] * int_pix_size  # 14*11=154
    cols_out = image.size[1] * int_pix_size  # 14*6=84
    px = image.load()
    d = draw.Drawing(rows_out, cols_out, origin=(0, -cols_out), displayInline=False)
    gray_scale_values = 256 / int(max_lines)


    for l in range(rows):
        for j in range(cols):
            color_index = ((px[l, j]))
            gray, alpa = color_index
            color_flip = gray
            print(color_flip  , "  flip")
            numb_of_squares = color_flip / gray_scale_values
            int_number_of_squares = int(numb_of_squares)
            print(int_number_of_squares , "nub_squares")
            if (rows_out <= cols_out):
                y_orent = (cols_out - (j * int_pix_size))  #
            else:
                y_orent = (cols_out - (j * int_pix_size))
            if (root.white_val.get() == '1'):
                if (int_number_of_squares != 1):
                    for numb in range(int_number_of_squares-1):
                        if (mode5 == "Horizontal"):
                            x2 = ((l * int_pix_size) + int_pix_size/2)
                            y2 = (y_orent+ numb)-int_pix_size
                            x1 = ((l * int_pix_size) + int_pix_size/2) # int_pix_size
                            y1 = (((y_orent) + int_pix_size)+ numb)-int_pix_size
                            point1 = rotate_point((x1, y1), 90, ((x1 + x2) / 2, (y1 + y2) / 2))
                            point2 = rotate_point((x2, y2), 90, ((x1 + x2) / 2, (y1 + y2) / 2))
                            x1, y1pos = point1
                            x2, y2pos = point2
                            y1 = -y1pos
                            y2 = -y2pos

                        elif (mode5 == "Spin"):
                            x2 = (l * int_pix_size + numb)
                            y2 = (y_orent)
                            x1 = (l * int_pix_size + numb)  # int_pix_size
                            y1 = (((y_orent) - int_pix_size))
                            point1 = rotate_point((x1, y1), gray, ((x1 + x2) / 2, (y1 + y2) / 2))
                            point2 = rotate_point((x2, y2), gray, ((x1 + x2) / 2, (y1 + y2) / 2))
                            x1, y1pos = point1
                            x2, y2pos = point2
                            y1 = -y1pos
                            y2 = -y2pos

                        elif (mode5 == "Rotate"):  # not working with white

                            x2 = (l * int_pix_size + numb)
                            y2 = (y_orent)
                            x1 = (l * int_pix_size + numb)  # int_pix_size
                            y1 = (((y_orent) - int_pix_size))
                            point1 = rotate_point((x1, y1), 45, ((x1 + x2) / 2, (y1 + y2) / 2))
                            point2 = rotate_point((x2, y2), 45, ((x1 + x2) / 2, (y1 + y2) / 2))
                            x1, y1pos = point1
                            x2, y2pos = point2
                            y1 = -y1pos
                            y2 = -y2pos
                        else:
                            x1 = (l * int_pix_size + numb)
                            y1 = (y_orent)
                            x2 = (l * int_pix_size + numb)  # int_pix_size
                            y2 = (y_orent) + int_pix_size
                        d.append(draw.Lines((x1), (y1),
                                            (x2), (y2),
                                            stroke_width=1,
                                            stroke=color_pick,
                                            fill='none',
                                            close=False))

            else:
                for numb in range(int_number_of_squares):
                    if (mode5 == "Horizontal"):
                        x2 = ((l * int_pix_size) + int_pix_size / 2)
                        y2 = (y_orent + numb) - int_pix_size
                        x1 = ((l * int_pix_size) + int_pix_size / 2)  # int_pix_size
                        y1 = (((y_orent) + int_pix_size) + numb) - int_pix_size
                        point1 = rotate_point((x1, y1), 90, ((x1 + x2) / 2, (y1 + y2) / 2))
                        point2 = rotate_point((x2, y2), 90, ((x1 + x2) / 2, (y1 + y2) / 2))
                        x1, y1 = point1
                        x2, y2 = point2
                    elif (mode5 == "Rotate"):
                        x2 = (l * int_pix_size + numb)
                        y2 = (y_orent)
                        x1 = (l * int_pix_size + numb)  # int_pix_size
                        y1 = (((y_orent) - int_pix_size))
                        int_degrees = int(degrees)
                        point1 = rotate_point((x1, y1), int_degrees, ((x1 + x2) / 2, (y1 + y2) / 2))
                        point2 = rotate_point((x2, y2), int_degrees, ((x1 + x2) / 2, (y1 + y2) / 2))
                        x1, y1 = point1
                        x2, y2 = point2
                    elif (mode5 == "Spin"):
                        x2 = (l * int_pix_size + numb)
                        y2 = (y_orent)
                        x1 = (l * int_pix_size + numb)  # int_pix_size
                        y1 = (((y_orent) - int_pix_size))
                        point1 = rotate_point((x1, y1), gray, ((x1 + x2) / 2, (y1 + y2) / 2))
                        point2 = rotate_point((x2, y2), gray, ((x1 + x2) / 2, (y1 + y2) / 2))
                        x1, y1 = point1
                        x2, y2 = point2
                    else:
                        x1 = (l * int_pix_size + numb)
                        y1 = (y_orent)
                        x2 = (l * int_pix_size + numb) # int_pix_size
                        y2 = (y_orent) - int_pix_size
                    d.append(draw.Lines((x1), (-y1), #########wtf !!!!!!
                                        (x2), (-y2),
                                        stroke_width=1,
                                        stroke=color_pick,
                                        fill='none',
                                        close=False))
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    setleng = len(set_button_list)
    for i in range(setleng):
        layer_name = root.set_button_name_var[i].get()
        if layer_name == "1":
            d.saveSvg('Layers/layer_' + str(i) +'_.svg')
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++

    layer_sample()

def layer_sample():
    canvas_w = (e1.get())
    canvas_h = (e2.get())
    nib_size = (e3.get())
    fig = sg.SVGFigure(canvas_w, canvas_h)
    viewleng = len(view_button_list)
    for i in range(viewleng):
        layer_name = root.view_button_name_var[i].get()
        if layer_name == "1":
            str_i = sg.fromfile('Layers/layer_'+str(i)+'_.svg')
            plot_i = str_i.getroot()
            x_offset,y_offset,scale_new = transform_data[i]
            print(x_offset,y_offset,scale_new)
            plot_i.moveto(x_offset,y_offset, scale=scale_new)
            fig.append([plot_i])
    fig.save("working/example_draw.svg")

    svgsample()

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

def gray_scale():
    use_canvase_scale = root.SCALE_TO_CANVASE_SIZE.get()
    mode2 = (shapes.get())
    marker_size = float(e3.get())
    inout = root.in_to_out.get()
    pix_size = (e5.get())
    int_pix_size = int(pix_size)
    offset = (float(marker_size) * 2)


    if (use_canvase_scale == "1"):
        canvas_width = int(e1.get())
        canvas_height = int(e2.get())
        marker_size = float(e3.get())
        # add overlap for markersize?
        ##use pil to scale the image to canvas frame
        # so 200x200 ---> 400x400
        ## bypass the manual pixelation
        img = Image.open(str(root.filename))
        width, height = img.size[:2]
        pixel_width_to_mm = int(canvas_width) / int(pix_size)
        pixel_height_to_mm = int(canvas_height) / int(pix_size)

        if height > width:
            baseheight = pixel_width_to_mm
            hpercent = (baseheight / float(img.size[1]))
            wsize = int((float(img.size[0]) * float(hpercent)))
            img = img.resize((int(wsize), int(baseheight), Image.ANTIALIAS))
            img.save('working/pixelated-cs_image.tif')
        else:
            basewidth = pixel_height_to_mm
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((int(basewidth), hsize), Image.ANTIALIAS)
            img.save('working/pixelated-cs_image.tif')
        # +++++++++++++++++++++++++++++++++++++++++++++++
        # +++++++++++++++++++++++++++++++++++++++++++++++
        image = Image.open("working/pixelated-cs_image.tif").convert('LA').transpose(Image.FLIP_TOP_BOTTOM)
        # pixel sizes should be about 10mm
        numb_of_boxes = (float(pix_size) / float(offset))
        int_numb_of_boxes = int(numb_of_boxes)
        rows = image.size[0]  # 11
        cols = image.size[1]  # 6
        rows_out = image.size[0] * int_pix_size  # 14*11=154
        cols_out = image.size[1] * int_pix_size  # 14*6=84
    else:
        image = Image.open("working/pixelated_image.tif").convert('LA').transpose(Image.FLIP_TOP_BOTTOM)
        rows = image.size[0]  # 11
        cols = image.size[1]  # 6
        rows_out = image.size[0] * int_pix_size  # 14*11=154
        cols_out = image.size[1] * int_pix_size  # 14*6=84

    px = image.load()
    print(rows_out, cols_out)
    d = draw.Drawing(rows_out, cols_out, origin=(0, -cols_out), displayInline=False)  # more wtf !!!

    if (mode2 == "CIRCLES" or mode2 == "SQUARE_"):
        if (use_canvase_scale == "1"):
            gray_scale_values = 256 / int_numb_of_boxes # 51
        else:
            gray_scale_values = 256 / int_pix_size

        for l in range(rows):
            for j in range(cols):
                color_index = ((px[l, j]))
                gray, alpa = color_index
                color_flip = 256 - gray
                numb_of_squares = color_flip / gray_scale_values
                int_number_of_squares = int(numb_of_squares)
                y_orent = (cols_out - (j * int_pix_size))

                if (use_canvase_scale != "1"):
                    if (root.white_val.get() == '1'):
                        if (int_number_of_squares != 1):

                            if (mode2 == "CIRCLES"):
                                for numb in range(int_number_of_squares):
                                    d.append(draw.Circle((l * int_pix_size)+int_pix_size/2, (-y_orent)+int_pix_size/2, numb-1 , stroke_width=marker_size, stroke=color_pick,
                                                         fill='none'))

                            if (mode2 == "SQUARE_"):
                                for numb in range(int_number_of_squares):
                                    d.append(
                                        draw.Rectangle((l * int_pix_size + (numb * offset) / 2), (-y_orent + (numb * offset) / 2), (int_pix_size - (numb * offset)),
                                                       (int_pix_size - (numb * offset)), stroke_width=marker_size, stroke=color_pick, fill='none', ))
                            if ((mode2 == "SQUARE_") and (inout == "1")):
                                print("finish this")
                    else:
                        if (mode2 == "CIRCLES"):
                            for numb in range(int_number_of_squares):
                                d.append(draw.Circle((l * int_pix_size) + int_pix_size / 2, (-y_orent) + int_pix_size / 2, numb - 1, stroke_width=marker_size, stroke=color_pick,
                                                     fill='none'))

                        if (mode2 == "SQUARE_"):
                            for numb in range(int_number_of_squares):
                                d.append(
                                    draw.Rectangle((l * int_pix_size + (numb * offset) / 2), (-y_orent + (numb * offset) / 2), (int_pix_size - (numb * offset)),
                                                   (int_pix_size - (numb * offset)), stroke_width=marker_size, stroke=color_pick, fill='none', ))
                        if ((mode2 == "SQUARE_") and (inout == "1")):
                            print("finish this")
                else:
                    if (root.white_val.get() == '1'):
                        if (int_number_of_squares > 0  ):
                            if ((mode2 == "CIRCLES") ):
                                for numb in range(0,int_number_of_squares,1):
                                    d.append(draw.Circle((l * int_pix_size) + int_pix_size / 2, (-y_orent) + int_pix_size / 2, numb*offset/2, stroke_width=marker_size, stroke=color_pick,
                                                    fill='none'))

                            if ((mode2 == "SQUARE_")): #inside out
                                print("works2")
                                print(int_number_of_squares)
                                for numb in range(0,int_number_of_squares,1):
                                    print(numb)
                                    d.append(
                                        draw.Rectangle(((l * int_pix_size) + int_pix_size )-( numb*offset/2)-(int_pix_size/2) , (-y_orent)-(( numb*offset/2)-(int_pix_size)/2) , ( ((numb) * (offset))),
                                                       (((numb)*offset)), stroke_width=marker_size, stroke=color_pick, fill='none', ))
                            if ((mode2 == "SQUARE_") and (inout != "1")):
                                for numb in range(int_number_of_squares):
                                    d.append(
                                        draw.Rectangle((l * int_pix_size + (numb * offset) / 2), (-y_orent + (numb * offset) / 2), (int_pix_size - (numb * offset)),
                                                       (int_pix_size - (numb * offset)), stroke_width=marker_size, stroke=color_pick, fill='none', ))



                    else:
                        if ((mode2 == "CIRCLES")):
                            for numb in range(0, int_number_of_squares + 1, 1):
                                d.append(draw.Circle((l * int_pix_size) + int_pix_size / 2, (-y_orent) + int_pix_size / 2, numb * offset / 2, stroke_width=marker_size, stroke=color_pick,
                                                     fill='none'))

                        if ((mode2 == "SQUARE_") and (inout == "1")):  # inside out
                            print("works2")
                            print(int_number_of_squares)
                            for numb in range(0, int_number_of_squares + 1, 1):
                                print(numb)
                                d.append(
                                    draw.Rectangle(((l * int_pix_size) + int_pix_size) - (numb * offset / 2) - (int_pix_size / 2), (-y_orent) - ((numb * offset / 2) - (int_pix_size) / 2), (((numb) * (offset))),
                                                   (((numb) * offset)), stroke_width=marker_size, stroke=color_pick, fill='none', ))


                        if ((mode2 == "SQUARE_") and (inout != "1") ):
                            for numb in range(int_number_of_squares):
                                d.append(
                                    draw.Rectangle((l * int_pix_size + (numb * offset) / 2), (-y_orent + (numb * offset) / 2), (int_pix_size - (numb * offset)),
                                                   (int_pix_size - (numb * offset)), stroke_width=marker_size, stroke=color_pick, fill='none', ))
                    '''
                    if (mode2 == "SQUARE_"):
                        for numb in range(int_number_of_squares):
                            d.append(
                                draw.Rectangle((l * int_pix_size + (numb*offset)/ 2) , (-y_orent + (numb*offset)/ 2), (int_pix_size - (numb* offset)),
                                               (int_pix_size - (numb*offset)), stroke_width=marker_size, stroke=color_pick, fill='none', ))

                    
                    if (mode2 == "SQUARE_"):
                        for numb in range(int_number_of_squares):
                            d.append(
                                draw.Rectangle((l * int_pix_size + (numb*offset)/ 2) , (-y_orent + (numb*offset)/ 2), ( (numb* offset)),
                                               ((numb*offset)), stroke_width=marker_size, stroke=color_pick, fill='none', ))
                    '''


    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    setleng = len(set_button_list)
    for i in range(setleng):
        layer_name = root.set_button_name_var[i].get()
        if layer_name == "1":
            d.saveSvg('Layers/layer_' + str(i) +'_.svg')
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++

    layer_sample()

def build_pixels():
    print(e5.get())
    mode2 = (shapes.get())
    print(mode2)

    if (root.sim.get() == '1'):
        stroke_val = 0.3
    else:
        stroke_val = 1

    redval  = 1
    blueval = 1
    greenval=1
    toneval = 128
    redval_max  = 255
    blueval_max = 255
    greenval_max=255

    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++

    image = Image.open("working/pixelated_image.tif").transpose(Image.FLIP_TOP_BOTTOM)
    px = image.load()
    pix_size = (e5.get())
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
            if (r > redval_max):
                r = redval_max
            if (r < redval):
                r = redval

            if (g > greenval_max):
                g = greenval_max
            if (g < greenval):
                g = greenval

            if (b > blueval_max):
                b = blueval_max
            if (b < blueval):
                b = blueval

            if (rows_out <= cols_out):
                y_orent = (cols_out - (j * int_pix_size))  #
            else:
                y_orent = (cols_out - (j * int_pix_size))

            if(r < toneval and g < toneval and b < toneval):
                r = 0
                g = 0
                b = 0

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

            numb_of_squares_magenta = Ma * int_pix_size
            int_number_of_squares_magenta = int(numb_of_squares_magenta)

            numb_of_squares_cyan = Cy * int_pix_size
            int_number_of_squares_cyan = int(numb_of_squares_cyan)

            numb_of_squares_yellow = Ye * int_pix_size
            int_number_of_squares_yellow = int(numb_of_squares_yellow)


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
    setleng = len(set_button_list)
    for i in range(setleng):
        layer_name = root.set_button_name_var[i].get()
        if layer_name == "1":
            d.saveSvg('Layers/layer_' + str(i) +'_.svg')
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    fix_svg_pixels_cirlces()

def build_circles():
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++

    image = Image.open("working/pixelated_image.tif").transpose(Image.FLIP_TOP_BOTTOM)
    px = image.load()
    circle_size = (e5.get())

    int_circle_size = int(circle_size)
    rows = image.size[0]#11
    cols = image.size[1]#6
    rows_out = image.size[0] * int_circle_size#14*11=154
    cols_out = image.size[1] * int_circle_size#14*6=84
    d = draw.Drawing(rows_out,cols_out, origin=(-int_circle_size/2,int_circle_size/2), displayInline=False)
    redval  = 1
    blueval = 1
    greenval=1
    toneval = 128

    for l in range(rows):
        for j in range(cols):
            color_index = ((px[l, j]))
            r, g, b = color_index
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
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    setleng = len(set_button_list)
    for i in range(setleng):
        layer_name = root.set_button_name_var[i].get()
        if layer_name == "1":
            d.saveSvg('Layers/layer_' + str(i) +'_.svg')
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    fix_svg_pixels_cirlces()

def fix_svg_pixels_cirlces():
    print("fixing")
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    path= ""
    temp_file_path = ""
    setleng = len(set_button_list)
    for i in range(setleng):
        layer_name = root.set_button_name_var[i].get()
        if layer_name == "1":
            path = ('Layers/layer_' + str(i)+'_.svg')
            temp_file_path = ('Layers/layer_' + str(i)+'temp_.svg')
    # +++++++++++++++++++++++++++++++++++++++++++++++
    svg_to_fix = open(path, 'r')
    outfile = open(temp_file_path, 'w')
    number_of_lines = 0
    with open(path, 'r') as f:
        for line in f:
            number_of_lines += 1

    count = 0
    index = 0
    w_h =[0,0,0,0,0]
    for text in svg_to_fix:
        if count <= 2 :
            width_raw = re.findall('width=".+?" ',text)
            width_temp = re.findall(r'\d+', str(width_raw))
            width = ''.join(width_temp)
            height_raw = re.findall('width=".+?" ',text)
            height_temp = re.findall(r'\d+', str(height_raw))
            height = ''.join(height_temp)

            #res = list(map(int, width_temp))

        '''
        for x in range (len(res)):
            if res[x] >= 0:
                w_h[index]= (res[x])
                index +=1
        '''
        if count == 3 :
            #width = str(w_h[2])
            #height =str(w_h[3])
            outfile.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n')
            outfile.write('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="'+width+' height='+height+'"  viewBox="0 0 '+width+' '+height+'">'+ '\n')
        if count > 2 and count < number_of_lines:
            allpos = text.replace('-', '')
            outfile.write(allpos)
        count +=1
    outfile.close()
    os.rename(temp_file_path,path)
    layer_sample()

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

def imagestuff():
    # pick an image file you have .bmp  .jpg  .gif.  .png
    # (if not in the working directory, give full path)
    pil_image = Image.open(str(root.filename))
    # common modes are
    # "L" (luminance) for greyscale images,
    # "RGB" for true color images,
    # "CMYK" for pre-press images
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

def set_px_by_box():
    box_scale =e6.get()
    int_box_scale = int(box_scale)
    root.pixelate_sliderVal.set(int_box_scale)

def pixelate():
    # Open Paddington
    img = Image.open(str(root.filename))
    size = (root.pixelate_sliderVal.get())
    mode = (v.get())
    # Scale back up using NEAREST to original
    if v.get() != NONE:
        if img.size[1] < img.size[0]:
            maxsize =img.size[1]
        else:
            maxsize=img.size[0]
        wpercent = (size / float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))

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
        result.save('working/result.png')
        # Save
        imgSmall.save('working/pixelated_image.tif')
        imgSmall.save('working/pixelated_image.png')

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
    max_val= root.CV_sliderVal_max.get()
    min_val= root.CV_sliderVal.get()
    float_min_val = float(min_val)
    float_max_val = float(max_val)
    stroke_color = color_pick
    stroke_width = e3.get()

    img = cv2.imread(str(root.filename))

    (h, w) = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    edged = cv2.Canny(hsv, float_min_val, float_max_val)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    idx = 0

    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    path=""
    setleng = len(set_button_list)
    for i in range(setleng):
        layer_name = root.set_button_name_var[i].get()
        if layer_name == "1":
            path =('Layers/layer_' + str(i) +'_.svg')
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++


    with open(path, "w+") as f:
        f.write('<?xml version = "1.0" encoding = "UTF-8"?>\n')
        f.write(f'<svg xmlns = "http://www.w3.org/2000/svg" xmlns:xlink = "http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}"> ')
        #f.write(f'<svg width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">')

        for c in contours:
            print(len(c), "line number = ", i)
            if (len(c)) > 1:
                f.write('\n<path d="M')
                for i in range(len(c)):
                    x, y = c[i][0]
                    f.write(f'{x} {y} ')
                f.write(f'" stroke-width="{stroke_width}" stroke="{stroke_color}" fill="none" />')
        f.write("</svg>")



    layer_sample()

    #svgsample()

def EGG_BOT_fill():
    import egg_main
    egg_main



def Image_edit():
    os.system('python3 image_edit.py &')

def Vector_fill():
    os.system('python3 egg_main.py &')

##################################################
### gcode generater

# name-files-according to origional name
# auto drop multi file
# auot offset
##################################################
def generate_gcode(filename):
    start,pre,post,end,pen_up,pen_down,pen_motor,XY_feed_rate,Pen_feed_rate,Homing = gcode_menu()

    '''G-code emitted at the start of processing the SVG file'''
    preamble = start

    '''G-code emitted at the end of processing the SVG file'''
    postamble = end

    '''G-code emitted before processing a SVG shape G4 is the command for dwell P is the time in ms'''
    shape_preamble = "G0 "+ pen_motor + pen_down+ " "+ Pen_feed_rate+"\n"

    '''G-code emitted after processing a SVG shape'''
    shape_postamble =  "G0 " + pen_motor + pen_up+ " "+ Pen_feed_rate+"\n"


    # A4 area:               210mm x 297mm
    # Printer Cutting Area: ~178mm x ~344mm
    # Testing Area:          150mm x 150mm  (for now)
    canvas_width = int(e1.get())
    canvas_height = int(e2.get())

    '''Print bed width in mm'''
    bed_max_x = canvas_width

    '''Print bed height in mm'''
    bed_max_y = canvas_height

    ''' Used to control the smoothness/sharpness of the curves.
        Smaller the value greater the sharpness. Make sure the
        value is greater than 0.1'''
    smoothness = 0.2


    ''' The main method that converts svg files into gcode files.
        Still incomplete. See tests/start.svg'''
    # *** open file ***


    # Check File Validity

    if not os.path.isfile(filename):
        raise ValueError("File \"" + filename + "\" not found.")

    if not filename.endswith('.svg'):
        raise ValueError("File \"" + filename + "\" is not an SVG file.")

    # Define the Output
    # ASSUMING LINUX / OSX FOLDER NAMING STYLE
    log = ""
    log += debug_log("Input File: " + filename)

    file = filename.split('/')[-1]
    dirlist = filename.split('/')[:-1]
    dir_string = ""
    for folder in dirlist:
        dir_string += folder + '/'

    # Make Output File
    outdir = dir_string + "gcode_output/"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    outfile = outdir + file.split(".svg")[0] + '.gcode'
    log += debug_log("Output File: " + outfile)

    # Make Debug File
    debugdir = dir_string + "log/"
    if not os.path.exists(debugdir):
        os.makedirs(debugdir)
    debug_file = debugdir + file.split(".svg")[0] + '.log'
    log += debug_log("Log File: " + debug_file + "\n")

    # Get the SVG Input File
    file = open(filename, 'r')
    tree = ET.parse(file)
    root = tree.getroot()
    file.close()

    # Get the Height and Width from the parent svg tag
    width = root.get('width')
    height = root.get('height')
    if width == None or height == None:
        viewbox = root.get('viewBox')
        if viewbox:
            _, _, width, height = viewbox.split()

    if width == None or height == None:
        # raise ValueError("Unable to get width or height for the svg")
        print("Unable to get width and height for the svg")
        sys.exit(1)

    # Scale the file appropriately
    # (Will never distort image - always scales evenly)
    # ASSUMES: Y ASIX IS LONG AXIS
    #          X AXIS IS SHORT AXIS
    # i.e. laser cutter is in "portrait"
    scale_x = bed_max_x / float(width)
    scale_y = bed_max_y / float(height)
    scale = min(scale_x, scale_y)
    if scale > 1:
        scale = 1

    log += debug_log("wdth: " + str(width))
    log += debug_log("hght: " + str(height))
    log += debug_log("scale: " + str(scale))
    log += debug_log("x%: " + str(scale_x))
    log += debug_log("y%: " + str(scale_y))

    # CREATE OUTPUT VARIABLE
    gcode = ""

    # Write Initial G-Codes
    gcode += preamble + "\n"

    # Iterate through svg elements
    for elem in root.iter():
        log += debug_log("--Found Elem: " + str(elem))
        new_shape = True
        try:
            tag_suffix = elem.tag.split("}")[-1]
        except:
            print("Error reading tag value:", tag_suffix)
            continue

        # Checks element is valid SVG shape
        if tag_suffix in SVG:

            log += debug_log("  --Name: " + str(tag_suffix))

            # Get corresponding class object from 'shapes.py'
            shape_class = getattr(shapes_pkg, tag_suffix)
            shape_obj = shape_class(elem)

            log += debug_log("\tClass : " + str(shape_class))
            log += debug_log("\tObject: " + str(shape_obj))
            log += debug_log("\tAttrs : " + str(list(elem.items())))
            log += debug_log("\tTransform: " + str(elem.get('transform')))

            ############ HERE'S THE MEAT!!! #############
            # Gets the Object path info in one of 2 ways:
            # 1. Reads the <tag>'s 'd' attribute.
            # 2. Reads the SVG and generates the path itself.
            d = shape_obj.d_path()
            log += debug_log("\td: " + str(d))

            # The *Transformation Matrix* #
            # Specifies something about how curves are approximated
            # Non-essential - a default is used if the method below
            #   returns None.
            m = shape_obj.transformation_matrix()
            log += debug_log("\tm: " + str(m))

            if d:
                log += debug_log("\td is GOOD!")


                points = point_generator(d, m, smoothness)
                #gcode += shape_preamble + "\n"

                log += debug_log("\tPoints: " + str(points))

                for x, y in points:
                    # log += debug_log("\t  pt: "+str((x,y)))

                    x = scale * x
                    y = bed_max_y - scale * y

                    log += debug_log("\t  pt: " + str((x, y)))

                    if x >= -10000000 and x <= bed_max_x + 10000000000 and y >= -1000000000 and y <= bed_max_y + 100000000000:
                        if new_shape:
                            gcode += ("G0 X%0.1f Y%0.1f\n" % (x, y))
                            #make sure to move with the pen up
                            gcode += shape_preamble + "\n"
                            gcode += ("G0 X%0.1f Y%0.1f\n" % (x, y))
                            #gcode += "M03\n" spindel on
                            new_shape = False
                        else:
                            gcode += ("G0 X%0.1f Y%0.1f\n" % (x, y))
                        log += debug_log("\t    --Point printed")
                    else:
                        log += debug_log("\t    --POINT NOT PRINTED (" + str(bed_max_x) + "," + str(bed_max_y) + ")")
                gcode += shape_postamble + "\n"
            else:
                log += debug_log("\tNO PATH INSTRUCTIONS FOUND!!")
        else:
            log += debug_log("  --No Name: " + tag_suffix)

    gcode += postamble + "\n"



    sample_gcode(gcode)
    # Write the Result
    ofile = open(outfile, 'w+')
    ofile.write(gcode)
    ofile.close()

    # Write Debugging
    if DEBUGGING:
        dfile = open(debug_file, 'w+')
        dfile.write(log)
        dfile.close()
#opens svg file selector

def svg_for_gcode():
    root.SVGfile = filedialog.askopenfilename(initialdir="Layers/", title="Select file", filetypes=(
    ("SVG files", "*.svg"), ("all files", "*.*")))
    file = str(root.SVGfile)
    generate_gcode(file)
#log for gcode generator
def debug_log(message):
    ''' Simple debugging function. If you don't understand
        something then chuck this frickin everywhere. '''
    if (DEBUGGING):
        print(message)
    return message + '\n'
#used in generate gcode
##################################################
#blackstripes
##################################################
def levels_by_preview_name(name):
	return (100, 150, 200, 230)

def crop_by_preview_name(name):
	return name

def blackstripes_filters():
    mode3 = (blackstripes_filter.get())
    image_path = ("working/pixelated_image.png")


    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    path= ""
    setleng = len(set_button_list)
    for i in range(setleng):
        layer_name = root.set_button_name_var[i].get()
        if layer_name == "1":
            path = ('Layers/layer_' + str(i) +'_.svg')
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++

    str_path = str(path)
    color = color_pick
    scale = float(root.scale_factor_sliderVal.get())
    space = int(root.space_factor_sliderVal.get())
    nib_size = float(e3.get())
    l1, l2, l3, l4 = levels_by_preview_name(image_path)

    if (mode3 == "SPIRAL_"):

        spiral.draw(image_path,            # input
                str_path,                      # output
                nib_size,                  # nibsize (line size in output svg)
                color,                     # line color
                scale,                     # scaling factor
                l1, l2, l3, l4,            # levels
                space,                     # line spacing
                1,1,1                      # signature transform
                )

    if (mode3 =="CROSSED" ):

        crossed.draw(image_path,            # input
                    str_path,                   # output
                    nib_size,               # nibsize (line size in output svg)
                    color,                  # line color
                    scale,                  # scaling factor
                    l1, l2, l3, l4,         # levels
                    1,                      # type
                    1,1,1                   # signature transform
                 )
    #svgsample()
    #layer_sample()
    fix_svg_blackstripes()
    #layer_sample()

def fix_svg_blackstripes():
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    path= ""
    temp_file_path = ""
    setleng = len(set_button_list)
    for i in range(setleng):
        layer_name = root.set_button_name_var[i].get()
        if layer_name == "1":
            path = ('Layers/layer_' + str(i)+'_.svg')
            temp_file_path = ('Layers/layer_' + str(i)+'temp_.svg')
    # +++++++++++++++++++++++++++++++++++++++++++++++
    svg_to_fix = open(path, 'r')
    outfile = open(temp_file_path, 'w')
    number_of_lines = 0
    with open(path, 'r') as f:
        for line in f:
            number_of_lines += 1

    count = 0
    index = 0
    w_h =[0,0]
    for text in svg_to_fix:
        viewbox = re.findall('viewBox=.+?enable-background',text)
        temp = re.findall(r'\d+', str(viewbox))
        res = list(map(float, temp))
        for x in range (len(res)):
            if res[x] > 0:
                w_h[index]= (res[x])
                index +=1
        if count == 1 :
            width = str(w_h[0])
            height =str(w_h[1])
            outfile.write('<?xml version="1.0" encoding="UTF-8"?>'+'\n')
            outfile.write('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="'+width+' height='+height+'"  viewBox="0 0 '+width+' '+height+'">'+ '\n')
        if count > 1 and count < number_of_lines:
            outfile.write(text)
        if count == number_of_lines-1:
            outfile.write("</svg>")
        count +=1
    outfile.close()

    os.rename(temp_file_path,path)
    layer_sample()
##################################################
##################################################
import xml.etree.ElementTree as ET
import numpy as np

# Landscape Letter
DEFAULT_PAGE_WIDTH = 11
DEFAULT_PAGE_HEIGHT = 8.5
DEFAULT_PAGE_UNIT = 'mm'

# Plot-related defaults
DEFAULT_VIEW_BOX_MARGIN = 0.1
STROKE_THICKNESS = 0.003  # Fraction of width of image
PLOT_COLORS = ['black', 'red', 'green', 'blue', 'cyan', 'orange']

def calculate_view_box(layers, aspect_ratio, margin=DEFAULT_VIEW_BOX_MARGIN):
    """Calculates the size of the SVG viewBox to use.

    Args:
        layers (list): the layers in the image
        aspect_ratio (float): the height of the output divided by the width
        margin (float): minimum amount of buffer to add around the image, relative
            to the total dimensions

    Returns:
        tuple: a 4-tuple of floats representing the viewBox according to SVG
            specifications ``(x, y, width, height)``.
    """
    min_x = min(np.nanmin(x) for x, y in layers)
    max_x = max(np.nanmax(x) for x, y in layers)
    min_y = min(np.nanmin(y) for x, y in layers)
    max_y = max(np.nanmax(y) for x, y in layers)
    height = max_y - min_y
    width = max_x - min_x

    if height > width * aspect_ratio:
        adj_height = height * (1. + margin)
        adj_width = adj_height / aspect_ratio
    else:
        adj_width = width * (1. + margin)
        adj_height = adj_width * aspect_ratio

    width_buffer = (adj_width - width) / 2.
    height_buffer = (adj_height - height) / 2.

    return (
        min_x - width_buffer,
        min_y - height_buffer,
        adj_width,
        adj_height
    )

def _layer_to_path_gen(layer):
    """Generates an SVG path from a given layer.

    Args:
        layer (layer): the layer to convert

    Yields:
        str: the next component of the path
    """
    draw = False
    for x, y in zip(*layer):
        if np.isnan(x) or np.isnan(y):
            draw = False
        elif not draw:
            yield 'M {} {}'.format(x, y)
            draw = True
        else:
            yield 'L {} {}'.format(x, y)

def layer_to_path(layer):
    """Generates an SVG path from a given layer.

    Args:
        layer (layer): the layer to convert

    Returns:
        str: an SVG path
    """
    return ' '.join(_layer_to_path_gen(layer))

def plot_to_svg(plot, width, height):
    stroke = e3.get()
    float_stroke = float(stroke)
    """Converts a plot (list of layers) into an SVG document.

    Args:
        plot (list): list of layers that make up the plot
        width (float): the width of the resulting image
        height (float): the height of the resulting image
        unit (str): the units of the resulting image if not pixels

    Returns:
        str: A stringified XML document representing the image
    """
    flipped_plot = [(x, -y) for x, y in plot]
    aspect_ratio = height / width
    view_box = calculate_view_box(flipped_plot, aspect_ratio=aspect_ratio)
    view_box_str = '{} {} {} {}'.format(*view_box)
    stroke_thickness = float_stroke * (view_box[2])

    svg = ET.Element('svg', attrib={
        'xmlns': 'http://www.w3.org/2000/svg',
        'xmlns:inkscape': 'http://www.inkscape.org/namespaces/inkscape',
        'width': '{}{}'.format(width,""),
        'height': '{}{}'.format(height,""),
        'viewBox': view_box_str})

    for i, layer in enumerate(flipped_plot):
        group = ET.SubElement(svg, 'g', attrib={
            'inkscape:label': '{}-layer'.format(i),
            'inkscape:groupmode': 'layer',
        })

        color = PLOT_COLORS[i % len(PLOT_COLORS)]
        ET.SubElement(group, 'path', attrib={
            'style': 'stroke-width: {}; stroke: {};'.format(stroke_thickness , color),
            'fill': 'none',
            'd': layer_to_path(layer)
        })

    try:
        return ET.tostring(svg, encoding='unicode')
    except LookupError:
        # Python 2.x
        return ET.tostring(svg)

def layer_to_svg(layer, **kwargs):
    """Converts a layer into an SVG image.

    Wrapper around ``plot_to_svg``.

    Args:
        layer (layer): the layer to plot
        width (float): the width of the resulting image
        height (float): the height of the resulting image
        unit (str): the units of the resulting image if not pixels

    Returns:
        str: A stringified XML document representing the image
    """
    return plot_to_svg([layer], **kwargs)

def write_plot(plot, filename, width=DEFAULT_PAGE_WIDTH, height=DEFAULT_PAGE_HEIGHT):
    """Writes a plot SVG to a file.

    Args:
        plot (list): a list of layers to plot
        filename (str): the name of the file to write
        width (float): the width of the output SVG
        height (float): the height of the output SVG
        unit (str): the unit of the height and width
    """
    svg = plot_to_svg(plot, width, height)
    with open(filename, 'w') as outfile:
        outfile.write(svg)

##################################################
#pen kit
##################################################
def pen_kit_gen():
    mode4 = (grid_type.get())
    A = float(root.scale_factor_A_sliderVal.get())
    B = float(root.scale_factor_B_sliderVal.get())
    E = int(root.scale_factor_E_sliderVal.get())

    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    path= ""
    setleng = len(set_button_list)
    for i in range(setleng):
        layer_name = root.set_button_name_var[i].get()
        if layer_name == "1":
            path = ('Layers/layer_' + str(i) +'_.svg')
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++


    if (mode4 == "Grid___"):
        #Grid Surface Projection
        # create a texture
        grid_density = 100
        texture = make_grid_texture(grid_density, grid_density, E)
        # rotate the texture
        texture = rotate_texture(texture, rotation=A)
        # create the surface
        surface = make_noise_surface(blur=B, seed=12345) * 10
        # project the texture onto the surface
        proj = project_and_occlude_texture(texture, surface, angle=B)
        # plot the result
        write_plot([proj], path )

    if (mode4 =="Hilbert"):
        #Hilbert Curve Surface Projection
        # create a texture
        texture = hilbert_curve(7)
        # rotate the texture
        texture = rotate_texture(texture, E)
        texture = fit_texture(texture)
        # create the surface
        surface = make_noise_surface(blur=B) * 5
        # project the texture onto the surface
        proj = project_and_occlude_texture(texture, surface, B)
        # plot the result
        write_plot([proj], path )

    layer_sample()
    #svgsample()
##################################################
##################################################

##################################################
#line_drawing
##################################################
def find_edges(IM):
    print("finding edges...")
    if no_cv:
        #appmask(IM,[F_Blur])
        appmask(IM,[F_SobelX,F_SobelY])
    else:
        im = np.array(IM)
        im = cv2.GaussianBlur(im,(3,3),0)
        im = cv2.Canny(im,100,200)
        IM = Image.fromarray(im)
    return IM.point(lambda p: p > 128 and 255)

def getdots(IM):
    print("getting contour points...")
    PX = IM.load()
    dots = []
    w, h = IM.size
    for y in range(h - 1):
        row = []
        for x in range(1, w):
            if PX[x, y] == 255:
                if len(row) > 0:
                    if x - row[-1][0] == row[-1][-1] + 1:
                        row[-1] = (row[-1][0], row[-1][-1] + 1)
                    else:
                        row.append((x, 0))
                else:
                    row.append((x, 0))
        dots.append(row)
    return dots

def connectdots(dots):
    print("connecting contour points...")
    contours = []
    for y in range(len(dots)):
        for x, v in dots[y]:
            if v > -1:
                if y == 0:
                    contours.append([(x, y)])
                else:
                    closest = -1
                    cdist = 100
                    for x0, v0 in dots[y - 1]:
                        if abs(x0 - x) < cdist:
                            cdist = abs(x0 - x)
                            closest = x0

                    if cdist > 3:
                        contours.append([(x, y)])
                    else:
                        found = 0
                        for i in range(len(contours)):
                            if contours[i][-1] == (closest, y - 1):
                                contours[i].append((x, y,))
                                found = 1
                                break
                        if found == 0:
                            contours.append([(x, y)])
        for c in contours:
            if c[-1][1] < y - 1 and len(c) < 4:
                contours.remove(c)
    return contours

def getcontours(IM, sc=2):
    print("generating contours...")
    IM = find_edges(IM)
    IM1 = IM.copy()
    IM2 = IM.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
    dots1 = getdots(IM1)
    contours1 = connectdots(dots1)
    dots2 = getdots(IM2)
    contours2 = connectdots(dots2)

    for i in range(len(contours2)):
        contours2[i] = [(c[1], c[0]) for c in contours2[i]]
    contours = contours1 + contours2

    for i in range(len(contours)):
        for j in range(len(contours)):
            if len(contours[i]) > 0 and len(contours[j]) > 0:
                if distsum(contours[j][0], contours[i][-1]) < 8:
                    contours[i] = contours[i] + contours[j]
                    contours[j] = []

    for i in range(len(contours)):
        contours[i] = [contours[i][j] for j in range(0, len(contours[i]), 8)]

    contours = [c for c in contours if len(c) > 1]

    for i in range(0, len(contours)):
        contours[i] = [(v[0] * sc, v[1] * sc) for v in contours[i]]

    for i in range(0, len(contours)):
        for j in range(0, len(contours[i])):
            contours[i][j] = int(contours[i][j][0] + 10 * perlin.noise(i * 0.5, j * 0.1, 1)), int(
                contours[i][j][1] + 10 * perlin.noise(i * 0.5, j * 0.1, 2))

    return contours

def hatch(IM, sc=16):
    PX = IM.load()
    w, h = IM.size
    lg1 = []
    lg2 = []
    for x0 in range(w):
        for y0 in range(h):
            x = x0 * sc
            y = y0 * sc
            if PX[x0, y0] > 144:
                pass

            elif PX[x0, y0] > 64:
                lg1.append([(x, y + sc / 4), (x + sc, y + sc / 4)])
            elif PX[x0, y0] > 16:
                lg1.append([(x, y + sc / 4), (x + sc, y + sc / 4)])
                lg2.append([(x + sc, y), (x, y + sc)])

            else:
                lg1.append([(x, y + sc / 4), (x + sc, y + sc / 4)])
                lg1.append([(x, y + sc / 2 + sc / 4), (x + sc, y + sc / 2 + sc / 4)])
                lg2.append([(x + sc, y), (x, y + sc)])

    lines = [lg1, lg2]
    for k in range(0, len(lines)):
        for i in range(0, len(lines[k])):
            for j in range(0, len(lines[k])):
                if lines[k][i] != [] and lines[k][j] != []:
                    if lines[k][i][-1] == lines[k][j][0]:
                        lines[k][i] = lines[k][i] + lines[k][j][1:]
                        lines[k][j] = []
        lines[k] = [l for l in lines[k] if len(l) > 0]
    lines = lines[0] + lines[1]

    for i in range(0, len(lines)):
        for j in range(0, len(lines[i])):
            lines[i][j] = int(lines[i][j][0] + sc * perlin.noise(i * 0.5, j * 0.1, 1)), int(
                lines[i][j][1] + sc * perlin.noise(i * 0.5, j * 0.1, 2)) - j
    return lines

def sketch(path):
    IM = None
    possible = [path, "images/" + path, "images/" + path + ".jpg", "images/" + path + ".png", "images/" + path + ".tif"]
    for p in possible:
        try:
            IM = Image.open(p)
            break
        except FileNotFoundError:
            print("The Input File wasn't found. Check Path")
            exit(0)
            pass
    w, h = IM.size
    print(w,h)

    IM = IM.convert("L")
    IM = ImageOps.autocontrast(IM, 10)
    contour_simplify = (root.contour_sliderVal.get())
    hatch_size = (root.hatch_sliderVal.get())
    resolution = (root.scale_sliderVal.get())

    contour_simplify_str = str(contour_simplify)
    hatch_size_str = str(hatch_size)

    lines = []
    if (contour_simplify_str != "1"):
        lines += getcontours(IM.resize((resolution // contour_simplify, resolution // contour_simplify * h // w)),
                                 contour_simplify)
    if (hatch_size_str != "1"):
        lines += hatch(IM.resize((resolution // hatch_size, resolution // hatch_size * h // w)), hatch_size)

    lines = sortlines(lines)
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++
    path= ""
    setleng = len(set_button_list)
    for i in range(setleng):
        layer_name = root.set_button_name_var[i].get()
        if layer_name == "1":
            path = ('Layers/layer_' + str(i) +'_.svg')
    # +++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++

    f = open(path, 'w')
    f.write(makesvg(lines))
    f.close()
    layer_sample()
    #svgsample()
    return lines

def makesvg(lines):
    canvas_w = (e1.get())
    canvas_h = (e2.get())
    nib_size = (e3.get())
    color = color_pick
    out = '<svg xmlns="http://www.w3.org/2000/svg" width="'+canvas_w+'" height="'+canvas_h+'" viewBox="0 0 '+canvas_w+' '+canvas_h+'" version="1.1">'
    for l in lines:
        l = ",".join([str(p[0] * 0.5) + "," + str(p[1] * 0.5) for p in l])
        out += '<polyline points="' + l + '" stroke="'+color+'" stroke-width="'+nib_size+'" fill="none" />\n'
    out += '</svg>'
    return out

def line_drawing():
    input_path = ("working/pixelated_image.tif")
    sketch(input_path)

##################################################
##################################################
root = Tk()

root.geometry("1520x700")  # Width x Height

# Center a window on the screen
center_tk_window.center_on_screen(root)

root.title("MUTATE_IMAGES")
def submenu_and_checkboxes():
    # ***main menue***
    menu =Menu(root)
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
    c1.place(x=622, y=0)

    #*** check button***
    root.sim = StringVar()
    c2 = Checkbutton(root, text ="simulate", variable=root.sim, bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    c2.deselect()
    c2.place(x=522, y=0)


    #*** check button***
    root.white_val = StringVar()
    c3 = Checkbutton(root, text ="white_value", variable=root.white_val, font=('Helvetica', '12'), bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    c3.deselect()
    c3.place(x=35,y= 593)

    #*** check button***
    root.set_colors = StringVar()
    c8 = Checkbutton(root, text ="set_color", variable=root.set_colors, bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    c8.select()
    c8.place(x=0,y= 385)

    #*** check button***
    root.ascii_small = StringVar()
    c9 = Checkbutton(root, text ="10chr", variable=root.ascii_small, bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    c9.deselect()
    c9.place(x=200, y=491)

    #*** check button***
    root.ascii_large = StringVar()
    c11 = Checkbutton(root, text ="75chr", variable=root.ascii_large, bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    c11.deselect()
    c11.place(x=260, y=491)


    #*** check button***
    root.SCALE_TO_CANVASE_SIZE = StringVar()
    c12 = Checkbutton(root, text ="SCALE_TO_CANVASE_SIZE", anchor="e",variable=root.SCALE_TO_CANVASE_SIZE, bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    c12.deselect()
    c12.place(x=30, y=0)

    #*** check button***
    root.in_to_out = StringVar()
    c13 = Checkbutton(root, text ="in->out", anchor="e",variable=root.in_to_out, bg="gray20", fg="lime green",highlightbackground="gray20",activebackground="deep sky blue")
    c13.deselect()
    c13.place(x=0, y=680)

submenu_and_checkboxes()

def show_entry_fields():
    print("OUTPUT X: %s\nOUTPUT Y: %s" % (e1.get(), e2.get()))
    print("machine code: %s\nnumb of colors: %s" % (e3.get(), e5.get()))
    print(  e5.get())

def reset():
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    #e4.delete(0, END)
    e5.delete(0, END)

def getColor():
    style = ttk.Style(root)
    style.theme_use('clam')
    hex_code, RGB_code = askcolor((255, 255, 0), root)
    print(hex_code, RGB_code)
    return RGB_code

def buttons_and_Labels():
    Label(root, text="scale",anchor="w",bg="gray20", fg="lime green", font=('Helvetica', '10')).place(x=730, y=610, height=20, width=50)
    Label(root, text="space",anchor="w",bg="gray20", fg="lime green", font=('Helvetica', '10')).place(x=730, y=640, height=20, width=50)
    Label(root, text="Hatch",anchor="w",bg="gray20", fg="lime green", font=('Helvetica', '10')).place(x=520, y=553, height=20, width=40)
    Label(root, text="Edge",anchor="w",bg="gray20", fg="lime green", font=('Helvetica', '10')).place(x=560, y=553, height=20, width=40)
    Label(root, text="Scale", anchor="w", bg="gray20", fg="lime green", font=('Helvetica', '10')).place(x=595, y=553, height=20, width=40)
    Label(root, text="OUT width in mm",anchor="e",bg="gray20", fg="lime green").place(x=5, y=25, height=20, width=125)
    Label(root, text="OUT height in mm",anchor="e",bg="gray20", fg="lime green").place(x=5, y=45, height=20, width=125)
    Label(root, text="Marker Size in mm",anchor="e",bg="gray20", fg="lime green").place(x=5, y=65, height=20, width=125)
    #Label(root, text="# of colors",anchor="e",bg="gray20", fg="lime green").place(x=5, y=85, height=20, width=125)
    Label(root, text="OUTPUT pixel size",anchor="e",bg="gray20", fg="lime green").place(x=5, y=85, height=20, width=125)
    Label(root, text="Number of Pixels", anchor="e", bg="gray20", fg="lime green").place(x=5, y=105, height=20,width=125)
    Label(root, text="Pix",anchor="e",bg="gray20", fg="lime green").place(x=5, y=145, height=20, width=123)
    Label(root, text="X_shift",anchor="e",bg="gray20", fg="lime green").place(x=1365, y=0, height=20, width=50)
    Label(root, text="Y_shift",anchor="e",bg="gray20", fg="lime green").place(x=1465, y=0, height=20, width=50)
    Label(root, text="Scale", anchor="e", bg="gray20", fg="lime green").place(x=1465, y=20, height=20, width=50)
    Button(root, text='SET', command=set_px_by_box, bg="gray20", fg="lime green", highlightbackground="gray20",activebackground="deep sky blue").place(x=175, y=105, height=20, width=35)
    Button(root, text='layers', command=Set_layers, bg="gray20", fg="lime green", highlightbackground="gray20", activebackground="deep sky blue").place(x=1365, y=20, height=25, width=50)
    Button(root,text='',  command=setcolorred, bg="red", fg="red",highlightbackground="lime green",activebackground="red").place(x=5,y=145,height= 40, width=40)
    Button(root,text='',  command=setcolorgreen, bg="green", fg="green",highlightbackground="lime green",activebackground="green").place(x=45,y=145,height= 40, width=40)
    Button(root,text='',  command=setcolorblue, bg="blue", fg="blue",highlightbackground="lime green",activebackground="blue").place(x=5,y=185,height= 40, width=40)
    Button(root,text='',  command=setcolorwhite, bg="white", fg="white",highlightbackground="lime green",activebackground="white").place(x=45,y=185,height= 40, width=40)
    Button(root,text='',  command=setcolorblack, bg="black", fg="black",highlightbackground="lime green",activebackground="black").place(x=5,y=225,height= 40, width=40)
    Button(root,text='',  command=setcoloryellow, bg="yellow", fg="yellow",highlightbackground="lime green",activebackground="yellow").place(x=45,y=225,height= 40, width=40)
    Button(root,text='',  command=setcolormagenta, bg="magenta", fg="magenta",highlightbackground="lime green",activebackground="magenta").place(x=5,y=265,height= 40, width=40)
    Button(root,text='',  command=setcolorcyan, bg="cyan", fg="cyan",highlightbackground="lime green",activebackground="cyan").place(x=45,y=265,height= 40, width=40)

    Button(root, text='Line_drawing', command=line_drawing, bg="gray20", fg="lime green",
           highlightbackground="gray20", activebackground="deep sky blue").place(x=523, y=527, height=25, width=110)

    Button(root, text='Grid_gen', command=pen_kit_gen, bg="gray20", fg="lime green",
           highlightbackground="gray20", activebackground="deep sky blue").place(x=370, y=527, height=25, width=150)
    Button(root, text='Blackstripes', command=blackstripes_filters, bg="gray20", fg="lime green",
           highlightbackground="gray20", activebackground="deep sky blue").place(x=640, y=527, height=25, width=130)
    Button(root, text='Gcode', command=svg_for_gcode, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=770, y=527, height=25, width=100)

    Button(root, text='edit_image', command=Image_edit, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=110, y=280, height=30, width=100)
    Button(root, text='Vector_fill', command=Vector_fill, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=110, y=310, height=30, width=100)
    Button(root, text='Make_layers', command=make_layer_stack, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=110, y=340, height=30, width=100)

    Button(root, text='Dots', command=dots, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=110, y=370, height=30, width=100)

#    Button(root, text='graph_fill', command=Fill, bg="gray20", fg="lime green", highlightbackground="gray20",
           #activebackground="deep sky blue").place(x=0, y=465, height=25, width=100)
    Button(root, text='OUTLINE', command=OUTLINE, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=0, y=515, height=25, width=100)
    Button(root, text='ASCII', command=ASCII, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=0, y=490, height=25, width=100)
    Button(root, text='img info', command=infopanel, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=322, y=0, height=25, width=100)
    Button(root, text='Custom', command=custom, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=0, y=440, height=25, width=100)
    Button(root, text='RGB split', command=RGB, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=422, y=0, height=25, width=100)
    Button(root, text='color circles', command=build_circles, bg="gray20", fg="lime green",
           highlightbackground="gray20", activebackground="deep sky blue").place(x=0, y=540, height=25, width=100)
    Button(root, text='color pixels', command=build_pixels, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=0, y=565, height=25, width=100)
    Button(root, text='Gray_shapes', command=gray_scale, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=0, y=615, height=25, width=100)
    Button(root, text='Gray_Lines', command=gray_Lines, bg="gray20", fg="lime green", highlightbackground="gray20",
           activebackground="deep sky blue").place(x=101, y=615, height=25, width=100)

def sample_gcode(gcode_preview):
    Label(root, text="Gcode", anchor="w", bg="gray20", fg="lime green", font=('Helvetica', '12')).place(x=1290, y=560,
                                                                                                      height=20,width=100)
    Gcode_Text = st.ScrolledText(root,
                            bg='white',
                            relief=GROOVE,
                            font='TkFixedFont', )
    Gcode_Text.insert(INSERT, gcode_preview)
    Gcode_Text.place(x=1290, y=580, height=120, width=200)

def gcode_menu():
    with open("gcode_default.ini", "r") as gcode_defaults:
            commands = gcode_defaults.read()
    str_XY_FEED_Rate_mm_dirty = re.search(r'XY_FEED_Rate_mm.*?Pen_Down_FEED_Rate_mm', commands, re.DOTALL).group()
    str_XY_FEED_Rate_mm = str_XY_FEED_Rate_mm_dirty.replace("XY_FEED_Rate_mm\n", "").replace("Pen_Down_FEED_Rate_mm", "").replace("\n","")

    str_Pen_Down_FEED_Rate_mm_dirty = re.search(r'Pen_Down_FEED_Rate_mm.*?PEN_UP_HIGHT_mm', commands, re.DOTALL).group()
    str_Pen_Down_FEED_Rate_mm = str_Pen_Down_FEED_Rate_mm_dirty.replace("Pen_Down_FEED_Rate_mm\n", "").replace("PEN_UP_HIGHT_mm", "").replace("\n","")

    str_PEN_UP_HIGHT_mm_dirty = re.search(r'PEN_UP_HIGHT_mm.*?PEN_DOWN_HIGHT_mm', commands, re.DOTALL).group()
    str_PEN_UP_HIGHT_mm = str_PEN_UP_HIGHT_mm_dirty.replace("PEN_UP_HIGHT_mm\n", "").replace("PEN_DOWN_HIGHT_mm", "").replace("\n","")

    str_PEN_DOWN_HIGHT_mm_dirty = re.search(r'PEN_DOWN_HIGHT_mm.*?Pen_Motor', commands, re.DOTALL).group()
    str_PEN_DOWN_HIGHT_mm = str_PEN_DOWN_HIGHT_mm_dirty.replace("PEN_DOWN_HIGHT_mm\n", "").replace("Pen_Motor", "").replace("\n","")

    str_Pen_dirty = re.search(r'Pen_Motor.*?Homing', commands, re.DOTALL).group()
    str_Pen = str_Pen_dirty.replace("Pen_Motor\n", "").replace("Homing", "").replace("\n","")

    str_Homing_dirty = re.search(r'Homing.*?Start', commands, re.DOTALL).group()
    str_Homing = str_Homing_dirty.replace("Homing\n", "").replace("Start", "").replace("\n","")

    str_start_dirty = re.search(r'Start.*?Pre_move', commands, re.DOTALL).group()
    str_start = str_start_dirty.replace("Start\n", "").replace("Pre_move", "")

    str_pre_dirty = re.search(r'Pre_move.*?Post_move', commands, re.DOTALL).group()
    str_pre = str_pre_dirty.replace("Pre_move\n", "").replace("Post_move", "")

    str_post_dirty = re.search(r'Post_move.*?End', commands, re.DOTALL).group()
    str_post =  str_post_dirty .replace("Post_move\n", "").replace("End", "")

    str_end_diry = re.search(r'End.*?Finish', commands, re.DOTALL).group()
    str_end = str_end_diry.replace("End\n", "").replace("Finish", "")



    Label(root, text="Pen Motor", anchor="w", bg="gray20", fg="lime green", font=('Helvetica', '8')).place(x=1090, y=560,height=20, width=100)
    default_Pen_Text = StringVar(root, value= str_Pen)
    default_Pen_Text = Entry(root, textvariable=default_Pen_Text)
    default_Pen_Text.place(x=1090, y=580, height=20, width=80)

    Label(root, text="XY_F_rate", anchor="w", bg="gray20", fg="lime green", font=('Helvetica', '9')).place(x=1090, y=600,height=20, width=100)
    default_XY_feed_Text = StringVar(root, value= str_XY_FEED_Rate_mm)
    default_XY_feed_Text = Entry(root, textvariable= default_XY_feed_Text)
    default_XY_feed_Text.place(x=1090, y=620, height=20, width=80)

    Label(root, text="PEN_F_rate", anchor="w", bg="gray20", fg="lime green", font=('Helvetica', '9')).place(x=1090, y=640,height=20, width=100)
    PEN_FEED_RATE_Text = StringVar(root, value= str_Pen_Down_FEED_Rate_mm)
    PEN_FEED_RATE_Text = Entry(root, textvariable=PEN_FEED_RATE_Text)
    PEN_FEED_RATE_Text.place(x=1090, y=660, height=20, width=80)

    Label(root, text="PEN_Up_pos", anchor="w", bg="gray20", fg="lime green", font=('Helvetica', '9')).place(x=1175, y=560,height=20, width=100)
    PEN_UP_HIGHT_mm_Text = StringVar(root, value= str_PEN_UP_HIGHT_mm)
    PEN_UP_HIGHT_mm_Text = Entry(root, textvariable=PEN_UP_HIGHT_mm_Text )
    PEN_UP_HIGHT_mm_Text.place(x=1175, y=580, height=20, width=80)

    Label(root, text="PEN_Down_pos", anchor="w", bg="gray20", fg="lime green", font=('Helvetica', '9')).place(x=1175, y=600,height=20, width=100)
    PEN_DOWN_HIGHT_mm_Text = StringVar(root, value= str_PEN_DOWN_HIGHT_mm)
    PEN_DOWN_HIGHT_mm_Text = Entry(root, textvariable=PEN_DOWN_HIGHT_mm_Text )
    PEN_DOWN_HIGHT_mm_Text.place(x=1175, y=620, height=20, width=80)

    Label(root, text="HOMING", anchor="w", bg="gray20", fg="lime green", font=('Helvetica', '9')).place(x=1175, y=640,height=20, width=100)
    str_Homing_Text = StringVar(root, value= str_Homing)
    str_Homing_Text = Entry(root, textvariable=str_Homing_Text)
    str_Homing_Text.place(x=1175, y=660, height=20, width=80)

    Label(root, text="Start", anchor="w", bg="gray20", fg="lime green", font=('Helvetica', '12')).place(x=780, y=560,
                                                                                                        height=20,
                                                                                                        width=100)
    Start_Text = st.ScrolledText(root,
                              bg='white',
                              relief=GROOVE,
                              font='TkFixedFont')

    Start_Text.insert(INSERT,str_start)
    Start_Text.place(x=780, y=580, height=50, width=150)

    Label(root, text="Pre_move", anchor="w", bg="gray20", fg="lime green", font=('Helvetica', '12')).place(x=780, y=630,
                                                                                                           height=20,
                                                                                                           width=100)
    Pre_move_Text = st.ScrolledText(root,
                                 bg='white',
                                 relief=GROOVE,
                                 font='TkFixedFont' )
    Pre_move_Text.insert(INSERT,str_pre)
    Pre_move_Text.place(x=780, y=650, height=50, width=150)

    Label(root, text="Post_move", anchor="w", bg="gray20", fg="lime green", font=('Helvetica', '12')).place(x=935,
                                                                                                            y=630,
                                                                                                            height=20,
                                                                                                            width=100)
    Post_move_Text = st.ScrolledText(root,
                                  bg='white',
                                  relief=GROOVE,
                                  font='TkFixedFont', )
    Post_move_Text.insert(INSERT,str_post)
    Post_move_Text.place(x=935, y=650, height=50, width=150)

    Label(root, text="End", anchor="w", bg="gray20", fg="lime green", font=('Helvetica', '12')).place(x=935, y=560,
                                                                                                      height=20,
                                                                                                      width=100)
    End_Text = st.ScrolledText(root,
                            bg='white',
                            relief=GROOVE,
                            font='TkFixedFont', )
    End_Text.insert(INSERT,str_end)
    End_Text.place(x=935, y=580, height=50, width=150)


    return(str_start,str_pre,str_post,str_end,str_PEN_UP_HIGHT_mm,str_PEN_DOWN_HIGHT_mm,str_Pen,str_XY_FEED_Rate_mm,str_Pen_Down_FEED_Rate_mm,str_Homing)

default_x_mm_output = StringVar(root, value='1000')
e1 = Entry(root, textvariable=default_x_mm_output)
default_y_mm_output = StringVar(root, value='420')
e2 = Entry(root, textvariable=default_y_mm_output)
default_markertip_mm_output = StringVar(root, value='1.6')
e3 = Entry(root, textvariable=default_markertip_mm_output)
deault = StringVar(root, value='8')
e5 = Entry(root, textvariable=deault)
deault_pixels = StringVar(root, value='2')
e6 = Entry(root, textvariable=deault_pixels)

e1.place(x=135, y=25, height=20, width=75)
e2.place(x=135, y=45, height=20, width=75)
e3.place(x=135, y=65, height=20, width=75)
e5.place(x=135, y=85, height=20, width=75)
e6.place(x=135, y=105, height=20, width=40)

root.scale_factor_A_sliderVal= Scale(root, from_=1, to=500, resolution=1,length=75,width=7,font=('Helvetica', '8'), orient=HORIZONTAL, bg="gray20",
                           fg="lime green",
                           highlightbackground="gray20", activebackground="deep sky blue", troughcolor="spring green")
root.scale_factor_A_sliderVal.place(x=365, y=600)
root.scale_factor_B_sliderVal= Scale(root, from_=1, to=25, resolution=1,length=75,width=7,font=('Helvetica', '8'), orient=HORIZONTAL, bg="gray20",
                           fg="lime green",
                           highlightbackground="gray20", activebackground="deep sky blue", troughcolor="spring green")
root.scale_factor_B_sliderVal.place(x=365, y=625)
root.scale_factor_C_sliderVal= Scale(root, from_=.1, to=10, resolution=.1,length=75,width=7,font=('Helvetica', '8'), orient=HORIZONTAL, bg="gray20",
                           fg="lime green",
                           highlightbackground="gray20", activebackground="deep sky blue", troughcolor="spring green")
root.scale_factor_C_sliderVal.place(x=365, y=650)
root.scale_factor_D_sliderVal= Scale(root, from_=.01, to=2, resolution=.01,length=75,width=7,font=('Helvetica', '8'), orient=HORIZONTAL, bg="gray20",
                           fg="lime green",
                           highlightbackground="gray20", activebackground="deep sky blue", troughcolor="spring green")
root.scale_factor_D_sliderVal.place(x=440, y=600)
root.scale_factor_E_sliderVal= Scale(root, from_=1, to=250, resolution=.01,length=75,width=7,font=('Helvetica', '8'), orient=HORIZONTAL, bg="gray20",
                           fg="lime green",
                           highlightbackground="gray20", activebackground="deep sky blue", troughcolor="spring green")
root.scale_factor_E_sliderVal.place(x=440, y=625)

root.scale_factor_sliderVal= Scale(root, from_=1, to=50, resolution=.1,length=90,width=7,font=('Helvetica', '8'), orient=HORIZONTAL, bg="gray20",
                           fg="lime green",
                           highlightbackground="gray20", activebackground="deep sky blue", troughcolor="spring green")
root.scale_factor_sliderVal.place(x=640, y=600)

root.space_factor_sliderVal= Scale(root, from_=1, to=10,resolution=.1, length=90,width=7,font=('Helvetica', '8'), orient=HORIZONTAL, bg="gray20",
                           fg="lime green",
                           highlightbackground="gray20", activebackground="deep sky blue", troughcolor="spring green")
root.space_factor_sliderVal.place(x=640, y=625)

root.scale_sliderVal= Scale(root, from_=1, to=2500, length=100,width=7,font=('Helvetica', '8'), orient=VERTICAL, bg="gray20",
                           fg="lime green",
                           highlightbackground="gray20", activebackground="deep sky blue", troughcolor="spring green")
root.scale_sliderVal.place(x=587, y=575)

root.hatch_sliderVal = Scale(root, from_=1, to=50, length=100,width=7,font=('Helvetica', '8'), orient=VERTICAL, bg="gray20",
                           fg="lime green",
                           highlightbackground="gray20", activebackground="deep sky blue", troughcolor="spring green")
root.hatch_sliderVal.place(x=513, y=575)

root.contour_sliderVal = Scale(root, from_=1, to=50, length=100,width=7, font=('Helvetica', '8'), orient=VERTICAL, bg="gray20",
                           fg="lime green",
                           highlightbackground="gray20", activebackground="deep sky blue", troughcolor="spring green")
root.contour_sliderVal.place(x=557, y=575)

root.ASCII_sliderVal = Scale(root, from_=1, to=100, length=100,width=7, orient=HORIZONTAL, bg="gray20",
                           fg="lime green",
                           highlightbackground="gray20", activebackground="deep sky blue", troughcolor="spring green")
root.ASCII_sliderVal.place(x=100, y=476)

root.CV_sliderVal = Scale(root, from_=0, to=128, length=75, width=7,font=('Helvetica', '8'), orient=HORIZONTAL, bg="gray20",
                             fg="lime green",
                             highlightbackground="gray20", activebackground="deep sky blue", troughcolor="black")
root.CV_sliderVal.place(x=100, y=510)
root.CV_sliderVal_max = Scale(root, from_=129, to=255, length=75, width=7,font=('Helvetica', '8'),orient=HORIZONTAL, bg="gray20",
                             fg="lime green",
                             highlightbackground="gray20", activebackground="deep sky blue", troughcolor="white")
root.CV_sliderVal_max.place(x=175, y=510)
root.rotation_slider = Scale(root, from_=0, to=360, length=75, width=7,font=('Helvetica', '8'),orient=HORIZONTAL, bg="gray20",
                             fg="lime green",
                             highlightbackground="gray20", activebackground="deep sky blue", troughcolor="white")
root.rotation_slider.place(x=180, y=670)

root.pixelate_sliderVal = Scale(root, from_=2, to=0, length=75, orient=HORIZONTAL, bg="gray20",
                                fg="lime green",
                                highlightbackground="gray20", activebackground="deep sky blue", troughcolor="lavender")
root.pixelate_sliderVal.place(x=135, y=125)

root.ASCII_sliderVal.set(12)  # Set the initial value to 125
root.CV_sliderVal.set(0)  # Set the initial value to 125
root.CV_sliderVal_max.set(255)  # Set the initial value to 125

# Create a spinbox
set_val_xoffset = DoubleVar(value=0.0)  # initial value
x_offest_box = Spinbox(root, from_=-99, to=99,width = 3, increment=.1,textvariable=set_val_xoffset)
x_offest_box.place(x=1325, y=0)
set_val_yoffset = DoubleVar(value=0.0)  # initial value
y_offset_box = Spinbox(root, from_=-99, to=99,width = 3, increment=.1,textvariable=set_val_yoffset)
y_offset_box.place(x=1425, y=0)
layers_box = Spinbox(root, from_=1, to=256,width = 3)
layers_box.place(x=1325, y=20 )
set_val = DoubleVar(value=1.0)  # initial value
scale_box = Spinbox(root, increment=.1,from_=-10.0, to=10.0,width = 3, textvariable=set_val)
scale_box.place(x=1425, y=20 )

Label(root, text="Sample_Mode", anchor="w", bg="gray20", fg="lime green").place(x=105, y=165, height=20, width=100)
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
                    highlightbackground="gray20", activebackground="deep sky blue").place(x=105, y=185 + count)
    count = count + 20
v.set("LANCZOS ")

MODES2 = [
    ("CIRCLES", "CIRCLES"),
    ("SQUARE_", "SQUARE_"),

]
shapes = StringVar()
shapes.set("L")  # initialize
menue_count = 0
for text2, mode2 in MODES2:
    b2 = Radiobutton(root, text=text2, variable=shapes, value=mode2, bg="gray20",
                     fg="lime green", highlightbackground="gray20", activebackground="deep sky blue").place(x=0,
                                                                                                            y=640 + menue_count)
    menue_count = menue_count + 20
shapes.set("SQUARE_")

Label(root, anchor="w", bg="gray20", fg="lime green").place(x=625, y=555, height=20, width=100)
MODES3 = [
    ("SPIRAL_", "SPIRAL_"),
    ("CROSSED", "CROSSED"),
]

blackstripes_filter = StringVar()
blackstripes_filter.set("L")  # initialize
menu2_count = 0
for text3, mode3 in MODES3:
    b = Radiobutton(root, text=text3, variable=blackstripes_filter, value=mode3, bg="gray20", fg="lime green",
                    highlightbackground="gray20", activebackground="deep sky blue").place(x=640, y=555 + menu2_count)
    menu2_count = menu2_count + 20
blackstripes_filter.set("CROSSED")

Label(root, anchor="w", bg="gray20", fg="lime green").place(x=390, y=550, height=20, width=100)

MODES4 = [
    ("Grid___", "Grid___"),
    ("Hilbert", "Hilbert")
]

grid_type = StringVar()
grid_type.set("L")  # initialize
menu4_count = 0
for text4, mode4 in MODES4:
    b = Radiobutton(root, text=text4, variable=grid_type, value=mode4, bg="gray20", fg="lime green",
                    highlightbackground="gray20", activebackground="deep sky blue").place(x=370, y=554 + menu4_count)
    menu4_count = menu4_count + 20
grid_type.set("Hilbert")


MODES5 = [
    ("Horizontal", "Horizontal"),
    ("Spin", "Spin"),
    ("Rotate", "Rotate"),
]
line_type = StringVar()
line_type.set("L")  # initialize
menue5_count = 0
for text5, mode5 in MODES5:
    b5 = Radiobutton(root, text=text5, variable=line_type, value=mode5, bg="gray20",
                     fg="lime green", highlightbackground="gray20", activebackground="deep sky blue").place(x=101,
                                                                                                            y=600 + menue_count)
    menue_count = menue_count + 20
line_type.set("Horizontal")

root.configure(background='gray20')
buttons_and_Labels()
gcode_menu()
Set_layers()
root.SVGfile = ""

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
    set_size = e6.get()
    root.pixelate_sliderVal = Scale(root, from_=2, to=size, length=75, orient=HORIZONTAL,command=cmd, bg="gray20",
                               fg="lime green",
                               highlightbackground="gray20", activebackground="deep sky blue",troughcolor="lavender")
    root.pixelate_sliderVal.place(x=135, y=125)
    root.pixelate_sliderVal.set(set_size)  # Set the initial value to 125

root.mainloop()