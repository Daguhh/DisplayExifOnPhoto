#!/usr/bin/python3
#-*- coding: utf-8 -*-
""" A non destructive python script to add 
        1) text from metadata, 
        2) images/logo,
        3) a border
    to images of a whole folder
    Please refer and edit "Parameters" section """
    
############# Import ###############
import os
import datetime # date parser 
from PIL import Image, ImageDraw, ImageFont # image processing library
from PIL.ExifTags import TAGS # list of exif tags and their refs
from cli_progress_bar import printProgressBar # cli progress bar script

############## Parameters ###############
# Position value are in percentage to adjust new object size to the picture dimensions
# See parameters comments for more details

#### Images to process ####
path = "/home/david/Médias/Images/"
file_format = ((".JPG", ".jpg", ".png")) # filter image to modify by their format
MODE = "RGB" # image loading color mode : L, RGB, RGBA / please match the original image color mode

#### Text Properties ####
text_font = 'Comic_Sans_MS.ttf' # arial.ttf Comic_Sans_MS.ttf    Times_New_Roman.ttf  Verdana.ttf
text_yr = 5/100 # text relative y position
text_xr = 50/100 # text relative x position
text_size_r = 5/100 # text relative fontsize
text_static = "BlaBla!!!, réalisée le {} à {}" # date and hour to insert from metadata
DateTimeOriginal = 36867 # DateTimeOriginal exif decimal code

#### Logo Properties ####
logo_name = "openlogo-nd-100.png"
logo_path = "/home/david/Programmation/SmallScripts/text_on_photo/"
logo_xr = 0/100 # logo relative position
logo_yr = 100/100
logo_size_r = 15/100 # logo relative size (to image height)

#### Border Properties ####
border_size_r = 2/100 # border relative size (to image height)
border_color = (255,255,255) # white

########### functions ################
def get_date_from_metadata(im) :
    """ return a formated date et hour from the DateTimeOriginal value 
        obtained in the picture exif metadata.
        return an "empty value" if no metadata 
        Parameters :
            a pillow image
        Return :
            two string : day, hour """
    try :
        exif_datas = im.getexif()
        #print(TAGS[DateTimeOriginal])
        date = exif_datas[DateTimeOriginal]
        date = datetime.datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
        day = date.strftime('%d/%m/%Y')
        hour = date.strftime('%HH%M')
    except :
        day = "0/0/0"
        hour = "0H0"
    return day, hour

########### Start #################
# list files in path
file_list = os.listdir(path)
nb_files = len(file_list) 

# create folder for processed image
if not os.path.isdir(path + "processed") :
    os.makedirs(path + "processed") # create folder is doesn't exist

# few display before loop    
print("starting job on", path, " ...")
print("{} file to process".format(nb_files))
print("this is a non-destructive script")
print("created files are placed in 'processed/' subfolder")

# progress bar initialization
printProgressBar(0, nb_files, prefix = 'Progress:', suffix = 'Complete', length = 50)

# loop over pictures
for i, file_name in enumerate(file_list) :
    
    # keep only file with wanted format
    if not file_name.endswith(file_format) : # process only file with file_format extension
        continue

    # print progress
    printProgressBar(i + 1, nb_files, prefix = 'Progress:', suffix = 'Complete', length = 50)

    ############# Load Image ##############
    im = Image.open(path + file_name).convert("RGBA")
    draw = ImageDraw.Draw(im)

    im_w, im_h = im.size

    ############## 1) Text ##############
    # add date from metadata into text to display
    day, hour = get_date_from_metadata(im)
    text_displayed = text_static.format(day,hour) 

    # adapt and set fontsize in function of image height
    font_size = round(im_h * text_size_r)
    font = ImageFont.truetype(text_font, font_size) 

    # get size of the text area
    text_w, text_h = font.getsize(text_displayed)

    # get absolute position of the text
    x = im_w*(text_xr) - text_w/2 # position from text area center
    y = im_h*(1-text_yr) - text_h/2

    # draw text on a black background
    draw.rectangle([(x, y), (x + text_w, y + text_h)], fill=(0,0,0,128))
    draw.text((x, y), text_displayed, font=font)

    ############## 2) Logo ##############
    # load logo with alpha values
    logo_im = Image.open(logo_path + logo_name).convert("RGBA")
    
    # get logo size
    logo_w, logo_h = logo_im.size

    # resize logo
    hw_ratio = logo_h/logo_w
    new_w = round(im_w*logo_size_r)
    new_h = round(hw_ratio*new_w)
    logo_im = logo_im.resize((new_w, new_h))
    
    # get absolute position
    x = round(im_w*logo_xr) # position from logo upper left corner
    y = round(im_h*(1-logo_yr))

    # draw it on the picture
    im.paste(logo_im, (x,y), mask=logo_im)

    ########## 3) Border ############
    # get border size
    size = round(border_size_r * im_h)
    # make an image that is larger than the picture (+ 2 time the border size)
    background = Image.new(MODE, (im_w+2*size, im_h+2*size), border_color)
    # and put it under the picture to make border
    background.paste(im,(size,size))

    ############### Save  ###############
    background.save(path + "processed/" + file_name)



