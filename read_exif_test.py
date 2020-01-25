#!/usr/bin/python3
#-*- coding: utf-8 -*-

import os
import datetime
from PIL import Image, ImageDraw, ImageFont
from PIL.ExifTags import TAGS

# exif decimal code
DateTimeOriginal = 36867 # DateTimeOriginal

# paramètres ################################
path = "/home/david/Programmation/SmallScripts/"
font_type = 'Comic_Sans_MS.ttf' # arial.ttf Comic_Sans_MS.ttf    Times_New_Roman.ttf  Verdana.ttf

# position des éléments
def none(im) :
    return "test"

text1 = {"value" : "BlaBla!!!",
         "fontsize" : 5/100,
         "y_pos" : 5/100,
         "x_pos" : 50/100,
         "metadata" : none}

def get_date(im) :
    exif_datas = im.getexif()
    #print(TAGS[DateTimeOriginal])
    date = exif_datas[DateTimeOriginal]
    date = datetime.datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
    date = [date.strftime('%d/%m/%Y'), date.strftime('%HH%M')]
    return date

text2 = {"value" : "BlaBla!!!, réalisée le {} à {}",
         "fontsize" : 5/100,
         "y_pos" : 95/100,
         "x_pos" : 5/100,
         "metadata" : get_date}


texts = [text1, text2]

# program ###################################
#file_list = os.listdir(path)
#os.makedirs(path + "processed")

file_name = "DSC00968.JPG"
if 1 :
#for file_name in file_list :
    #### Image ####
    # on ouvre l'image
    im = Image.open(path + file_name)
    draw = ImageDraw.Draw(im)

    # dimension de l'image
    im_w, im_h = im.size


    for text in texts :

        # obtention des metadatas
        date = text['metadata'](im)


        #### Texte ####
        # texte à afficher
        text_displayed = text['value'].format(*date)

        # calcul taille de police
        font_size = round(im_h * text['fontsize'])
        font = ImageFont.truetype(font_type, font_size)

        # determination des dimensions du texte
        text_w, text_h = font.getsize(text_displayed)
        print(text_displayed)

        # et de sa position
        x = im_w*(text['x_pos']) - text_w/2 # in the middle (horizontally)
        y = im_h*(1-text['y_pos']) - text_h/2 # à 1/text1_relative_position_y % de la hauteur de l'image

        # on trace le texte sur (et) un fond noir
        draw.rectangle([(x, y), (x + text_w, y + text_h)], fill=(0,0,0,128))
        draw.text((x, y), text_displayed, font=font)

    # sauvegarde l'image

    im.save(path + "processed/" + file_name)



