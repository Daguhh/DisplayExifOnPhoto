#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os
import datetime
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS

############## Parameters ###############
path = "/home/david/Programmation/SmallScripts/text_on_photo/"
font_type = 'Comic_Sans_MS.ttf' # arial.ttf Comic_Sans_MS.ttf    Times_New_Roman.ttf  Verdana.ttf

file_name = "DSC00968.JPG"
logo_name = "debian_logo.jpeg"
logo_name_2 = "openlogo-nd-100.png"

text_yr = 5/100 # relative y position
text_xr = 50/100 # relative x position
text_size_r = 5/100 # relative image/text fontsize

logo_xr = 0/100
logo_yr = 100/100
logo_size_r = 15/100

border_size_r = 2/100
border_color = (255,255,255) # white

DateTimeOriginal = 36867 # DateTimeOriginal exif decimal code

########### functions ################
def get_date_from_metadata(im) :
    exif_datas = im.getexif()
    #print(TAGS[DateTimeOriginal])
    date = exif_datas[DateTimeOriginal]
    date = datetime.datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
    day = date.strftime('%d/%m/%Y')
    hour = date.strftime('%HH%M')
    return day, hour

########### Start #################
#file_list = os.listdir(path)
#os.makedirs(path + "processed")

if 1 : #for file_name in file_list :

    im = Image.open(path + file_name)
    draw = ImageDraw.Draw(im)

    im_w, im_h = im.size

    ############## Text ##############
    day, hour = get_date_from_metadata(im)
    text_displayed = "BlaBla!!!, réalisée le {} à {}".format(day,hour)
    print(text_displayed)

    font_size = round(im_h * text_size_r)
    font = ImageFont.truetype(font_type, font_size)

    text_w, text_h = font.getsize(text_displayed)

    x = im_w*(text_xr) - text_w/2
    y = im_h*(1-text_yr) - text_h/2

    draw.rectangle([(x, y), (x + text_w, y + text_h)], fill=(0,0,0,128))
    draw.text((x, y), text_displayed, font=font)

    ############## Logo ##############
    logo_im = Image.open(path + logo_name_2)

    logo_w, logo_h = logo_im.size

    hw_ratio = logo_h/logo_w
    new_w = round(im_w*logo_size_r)
    new_h = round(hw_ratio*new_w)

    logo_im = logo_im.resize((new_w, new_h))
    x = round(im_w*logo_xr)
    y = round(im_h*(1-logo_yr))

    im.paste(logo_im,(x,y))

    ########## Border ############
    size = round(border_size_r * im_h)
    border = Image.new("RGB", (im_w+2*size, im_h+2*size), border_color)
    border.paste(im,(size,size))

    ############### Save  ###############
    border.save(path + "processed/" + file_name)



