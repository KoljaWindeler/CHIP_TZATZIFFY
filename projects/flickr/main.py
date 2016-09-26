# basic code from >>
# http://tkinter.unpythonic.net/wiki/PhotoImage
# sudo apt-get install python3-pil.imagetk python3-pil python3-tk


# extra code -------------------------------------------------------------------------
from __future__ import print_function

import tkinter as tk
from tkinter import font


from PIL import ImageTk, Image, ImageEnhance


import sys, time
import platform
import sys
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


		helv36 = font.Font(family='Helvetica',size=36, weight='bold')  # you don't have to use Helvetica or bold, this is just an example
		button = tk.Button(master, justify=tk.CENTER, highlightthickness=0, bd=0, borderwidth=0, command=lambda: self.update_img(silent = 0), compound=tk.CENTER, font=helv36)
		button.pack() 

		self.button = button
		self.button_image = ""
		self.update_total_img()
		self.update_img(silent = 1)

	def update_total_img(self):
		self.max_photo = flickr.get_photo_count()
		self.master.after(6*60*60*1000, self.update_total_img)

	def update_img(self,silent = 1):
		# call it with silent == 0, on button push; else silent == 1 
		print(time.strftime("%H:%M:%S"))
		if(silent != 1):
			print("non silent update, add 'Loading' label")
			self.button.configure(text = "Loading ...")

			# if there was an old image, show it as grayscale
			if(self.button_image!=""):
				self.button_image_photo = ImageTk.PhotoImage(self.button_image.convert('LA'))
				self.button.configure(image = self.button_image_photo)	
				self.button.image = self.button_image_photo
				self.master.update()

		# download new image
		self.button_image = resize_img(flickr.get_random_photo(self.max_photo))
		self.button_image_photo = ImageTk.PhotoImage(self.button_image)
		# set it
		self.button.configure(image = self.button_image_photo, text = "")	
		self.button.image = self.button_image_photo
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
	return img
	
root=tk.Tk()
app = FullScreenApp(root)
root.mainloop()



