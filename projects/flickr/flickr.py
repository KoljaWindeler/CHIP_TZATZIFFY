import sys, time
import platform
import hashlib
import json
import random
import urllib.request
import urllib.parse
import sys
import settings
import threading
import os
import math

# list of the photos (required for album mode)
photo_list=[]

# total number of photos for the search result
photo_total=0

########################################################################################
def init():
	refresh(p=1)
########################################################################################
def refresh(p=0):
	global photo_total, photo_list
	print("debug: running refresh")
	if(p):
		print("[flickr init] Start")

	# 1 = all private photos from given account 
	# 2 = private photos album from given account 
	# 3 = search for photos from all public photos

	if(settings.mode==1):
		if(p):
			print("[flickr init] running in privat all photos mode")
		photo_total=get_photo_count()
	elif(settings.mode==2):
		if(p):
			print("[flickr init] running in private album mode")
		photo_list=get_photos_for_album()
		#print(photo_list)
	else:
		if(p):
			print("[flickr init] running in public tag search mode, search for "+str(settings.searchtag))
		photo_total=get_public_photo_count_for_tag(settings.searchtag)
		if(photo_total==0):
			print("No photos found for searchtag '"+settings.searchtag+"', please run setup.py")
			exit()
	if(p):
		print("[flickr init] done")

	# schedule a recall for us to update the pictures total / list
	threading.Timer(settings.time_total_refresh,refresh)
########################################################################################
def get_photo(p=0,splash=0):
	global photo_total, photo_list
	#print("get photo, total "+str(photo_total))

	if(splash):
		if(p):
			print("[flickr] loading Splash ...")
		url = "file://"+os.path.dirname(os.path.realpath(__file__))+"/splash.png"
	elif(settings.mode==1):
		if(p):
			print("[flickr] downloading a random private photo")
		url=get_random_photo_url(photo_total)
	elif(settings.mode==2):
		if(p):
			print("[flickr] downloading a private album photo")
		r = random.randrange(0,len(photo_list))
		if(p):
			print("selected photo "+str(r)+"/"+str(len(photo_list)))
		url=photo_list[r]
	else:
		if(p):
			print("[flickr] downloading a public photo for "+str(settings.searchtag))
		url=get_random_public_photo_for_tag(settings.searchtag,photo_total)

	# download photo and return file name
	return download_photo(url)
########################################################################################
def get_api_sig_link(link):
	link=link.replace(" ","")
	arg=link.split("?")
	arg=arg[1].split("&")
	arg.sort()
	signature=settings.secret
	for i in range(0,len(arg)):
		sin_arg=arg[i].split("=")
		signature+=sin_arg[0]
		signature+=sin_arg[1]
	#print(signature)
	url=link+"&api_sig="+hashlib.md5(signature.encode()).hexdigest()
	#print(url)
	return url
########################################################################################
def get_page(url):
	req = urllib.request.urlopen(url)
	data = req.read().decode('utf-8')
	#print(data)
	return data
########################################################################################
def get_photo_count():
	if(settings.api_key == ""):
		print("no api key, please run setup.py")
		return -1
	else:
		url="https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key="+settings.api_key+"&user_id="+settings.user_id+"&per_page=1&page=1&format=json&nojsoncallback=1&auth_token="+settings.token
		page = get_page(get_api_sig_link(url))
		dec=json.loads(page)
		total=int(dec['photos']['total'])
	return total
########################################################################################
def get_public_photo_count_for_tag(tag):
	if(settings.api_key == ""):
		print("no api key, please run setup.py")
		return -1
	else:
		url="https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key="+settings.api_key+"&text="+str(tag)+"&format=json&nojsoncallback=1"
		#print(url)
		page = get_page(get_api_sig_link(url))
		#print(page)
		dec=json.loads(page)
		total=int(dec['photos']['total'])
		#print(total)
	return total
########################################################################################
def get_photos_for_album():
	if(not(settings.photoset_id!="")):
		return -1

	link="https://api.flickr.com/services/rest/?method=flickr.photosets.getPhotos&photoset_id="+settings.photoset_id+"&api_key="+settings.api_key+"&user_id="+settings.user_id+"&format=json&nojsoncallback=1&auth_token="+settings.token

	page = get_page(get_api_sig_link(link))
	dec=json.loads(page)
	
	p_list = []
	for i in range(0,len(dec['photoset']['photo'])):
		p_id=dec['photoset']['photo'][i]['id']
		p_secret=dec['photoset']['photo'][i]['secret']
		p_server=dec['photoset']['photo'][i]['server']
		p_farm=dec['photoset']['photo'][i]['farm']
		p_url = "http://farm"+str(p_farm)+".static.flickr.com/"+str(p_server)+"/"+str(p_id)+"_"+str(p_secret)+"_b.jpg";
		p_list.append(p_url)
	return p_list
########################################################################################
def get_random_photo_url(max_photo_count):
	if(settings.api_key == ""):
		print("no api key, please run setup.py")
		return -1
	else:
		photo_rand=random.randrange(1,max_photo_count)
		print("[flickr] Downloading randomly chosen photo Nr:"+str(photo_rand))
		url="https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key="+settings.api_key+"&user_id="+settings.user_id+"&per_page=1&page="+str(photo_rand)+"&format=json&nojsoncallback=1&auth_token="+settings.token
		page = get_page(get_api_sig_link(url))
		dec=json.loads(page)
		url="https://farm"+str(dec['photos']['photo'][0]['farm'])+".staticflickr.com/"+str(dec['photos']['photo'][0]['server'])+"/"+str(dec['photos']['photo'][0]['id'])+"_"+str(dec['photos']['photo'][0]['secret'])+"_b.jpg"
		return url
########################################################################################
def get_random_public_photo_for_tag(tag,max_photo_count):
	#print("get_random_public_photo_for_tag("+str(tag)+","+str(max_photo_count)+")")
	if(settings.api_key == ""):
		print("no api key, please run setup.py")
		return -1
	else:
		# ideally we'd just submit a random page, but flickr tends to return the same photo, even for different pages, strange!
		# lets select a random nr of photos for our first page (limited by 100 (reduce traffic) and by the number of available photos for the tag
		base_count=min(4000*500,max_photo_count) 
		per_page=min(500,max_photo_count)				# max 500 pictures per page. So technically we can get max 4000*500=2.000.000 pics
		if(max_photo_count<500):
			page=1
		else:
			page=random.randrange(1,math.floor(base_count/per_page))	# we can call MAX 4000 pages thats a flickr given max! (where did I find that?)
		
		print("[flickr] total "+str(max_photo_count)+" photos for the searchtag '"+str(tag)+"', select page "+str(page)+" and request "+str(per_page)+" photos on that page")
		
		url="https://api.flickr.com/services/rest/?method=flickr.photos.search&sort=relevance&api_key="+settings.api_key
		url+="&per_page="+str(per_page)+"&page="+str(page)+"&format=json&nojsoncallback=1&text="+tag
		#print(url)
		d_page = get_page(get_api_sig_link(url))
		dec=json.loads(d_page)

		# now select a random photo from this result, or choose the first if its only one
		if(len(dec['photos']['photo'])>1):
			photo_rand=random.randrange(0,len(dec['photos']['photo'])-1)
			print("[flickr] Request returned "+str(len(dec['photos']['photo']))+" photos, randomly select Nr "+str(photo_rand))
		else:
			photo_rand=0
		
		#debug: why did this photo show up?
		#print_photo_info(dec['photos']['photo'][photo_rand]['id'],dec['photos']['photo'][photo_rand]['secret'])


		url="https://farm"+str(dec['photos']['photo'][photo_rand]['farm'])+".staticflickr.com/"+str(dec['photos']['photo'][photo_rand]['server'])+"/"+str(dec['photos']['photo'][photo_rand]['id'])+"_"+str(dec['photos']['photo'][photo_rand]['secret'])+"_b.jpg"
		#print(url)
		return (url)
########################################################################################
def print_photo_info(id,secret):
	print("[flickr] ====== FILE INFO ==========")
	url="https://api.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key="+settings.api_key
	url+="&photo_id="+str(id)+"&secret="+str(secret)+"&format=json&nojsoncallback=1"
	e_page=get_page(get_api_sig_link(url))
	e_dec=json.loads(e_page)
	print("[flickr] Tags: ",end="")
	for tag in e_dec['photo']['tags']['tag']:
		print(tag['raw'],end=", ")
	print("")
	print("[flickr] Title:"+str(e_dec['photo']['title']['_content']))
	print("[flickr] ====== FILE INFO ==========")
########################################################################################
def get_albums():
	link="https://api.flickr.com/services/rest/?method=flickr.photosets.getList&api_key="+settings.api_key+"&user_id="+settings.user_id+"&format=json&nojsoncallback=1&auth_token="+settings.token
	page = get_page(get_api_sig_link(link))
	dec=json.loads(page)

	for i in range(0,int(dec['photosets']['total'])):
		print("%02d"%i+", id="+dec['photosets']['photoset'][i]['id']+", %04d Phtotos, "%dec['photosets']['photoset'][i]['photos']+dec['photosets']['photoset'][i]['title']['_content'])
	return dec
########################################################################################
def download_photo(url):
		print("[flickr] Downloading .. ",end="")
		urllib.request.urlretrieve (url, settings.temp_path)
		print("Done")
		return settings.temp_path

