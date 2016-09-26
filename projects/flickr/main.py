# basic code from >>
# http://tkinter.unpythonic.net/wiki/PhotoImage
# sudo apt-get install python3-imaging-tk
# sudo apt-get install python3-pil
# sudo apt-get install python3-tk


# extra code -------------------------------------------------------------------------
from __future__ import print_function

import tkinter as tk
from PIL import ImageTk, Image
import sys, time
import platform
import hashlib
import json
import random
import urllib.request
import urllib.parse
import sys
from random import randint
import settings
import flickr


########################################## go #####################################

# basic code -------------------------------------------------------------------------
class FullScreenApp(object):
	def __init__(self, master, **kwargs):
		self.master = master
		
		pad=0
		self._geom='200x200+0+0'
		master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
		master.configure(background='black')
		master.bind('<Escape>',self.leave) 
		master.attributes('-fullscreen', True)

		button = tk.Button(master, justify=tk.CENTER, highlightthickness=0, bd=0, borderwidth=0, command=self.update_img)
		button.pack() 
		self.button = button   
		
		self.update_total_img()
		self.update_img()

	def update_total_img(self):
		self.max_photo = flickr.get_photo_count()
		self.master.after(6*60*60*1000, self.update_total_img)

	def update_img(self):
		now = time.strftime("%H:%M:%S")
		print(now)
		
#		if(randint(0,9)>5):
#			btn_img = resize_img('/home/kolja/Desktop/1.jpg')
#		else:
#			btn_img = resize_img('/home/kolja/Desktop/2514d628d165cec85d3f4b3907655195a05a5bc0.jpg')
		btn_img = resize_img(flickr.get_random_photo(self.max_photo))

		self.button.configure(image = btn_img)	
		self.button.image = btn_img
		self.master.after(5*60*1000, self.update_img)
	def leave(self,event):
		exit()


def resize_img(path):
	img = Image.open(path)
	scale_x = root.winfo_screenwidth()/img.size[0]
	scale_y = root.winfo_screenheight()/img.size[1]
	if(scale_x<scale_y):
		scale = scale_x
	else:
		scale = scale_y
	img = img.resize((int(img.size[0]*scale), int(img.size[1]*scale)), Image.ANTIALIAS) 
	return ImageTk.PhotoImage(img)
	
root=tk.Tk()
app = FullScreenApp(root)
root.mainloop()



