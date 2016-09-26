import sys, time
import platform
import hashlib
import json
import random
import urllib.request
import urllib.parse
import sys
import settings

########################################## flickr #####################################	
def get_api_sig_link(link):
	arg=link.split("?")
	arg=arg[1].split("&")
	arg.sort()
	signature=settings.secret
	for i in range(0,len(arg)):
		sin_arg=arg[i].split("=")
		signature+=sin_arg[0]
		signature+=sin_arg[1]
	url=link+"&api_sig="+hashlib.md5(signature.encode()).hexdigest()
	req = urllib.request.urlopen(url)
	data = req.read().decode('utf-8')
	#print(data)
	return data

def get_photo_count():
	print("Requesting total nr of photos on your account")
	if(settings.api_key == "" or settings.user_id == "" or settings.token == ""):
		setup()
		return -1
	else:
		url="https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key="+settings.api_key+"&user_id="+settings.user_id+"&per_page=1&page=1&format=json&nojsoncallback=1&auth_token="+settings.token
		page = get_api_sig_link(url)
		dec=json.loads(page)
		total=int(dec['photos']['total'])
		print("%d photos found"%total)
	return total
	
	
def get_random_photo(max_photo_count):
	if(settings.api_key == "" or settings.user_id == "" or settings.token == ""):
		setup()
		return -1
	else:
		photo_rand=random.randrange(1,max_photo_count)
		print("Downloading randomly chosen photo Nr:"+str(photo_rand))
		url="https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key="+settings.api_key+"&user_id="+settings.user_id+"&per_page=1&page="+str(photo_rand)+"&format=json&nojsoncallback=1&auth_token="+settings.token
		page = get_api_sig_link(url)
		dec=json.loads(page)
		url="https://farm"+str(dec['photos']['photo'][0]['farm'])+".staticflickr.com/"+str(dec['photos']['photo'][0]['server'])+"/"+str(dec['photos']['photo'][0]['id'])+"_"+str(dec['photos']['photo'][0]['secret'])+"_b.jpg"
		urllib.request.urlretrieve (url, settings.temp_path)
		print("Done")
		return settings.temp_path

def setup():
	if(settings.api_key == "" ):
		print("you have to get an api key at: https://www.flickr.com/services/apps/create/noncommercial/?")
		print("add the key and secret values in the setting.py and rerun")
		exit()
		return -1
	elif(settings.frob == "" ):
		url="https://flickr.com/services/rest/?method=flickr.auth.getFrob&api_key="+settings.api_key+"&format=json"
		page = get_api_sig_link(url)
		page=page.replace("jsonFlickrApi(","")[:-1]
		dec=json.loads(page)
		settings.frob=dec['frob']['_content']
		#save_parameter(settings.api_key,settings.secret,settings.frob,settings.token,settings.user_id,settings.temp_path)
		print("frob generated, please edit your settings.py and set the frob to: "+settings.frob)
		print("now please open: "+get_api_sig_link("http://flickr.com/services/auth/?api_key="+settings.api_key+"&perms=read&frob="+settings.frob))
		return -1
	elif(settings.token == "" or settings.user_id == "" ):
		url="https://flickr.com/services/rest/?method=flickr.auth.getToken&format=json&api_key="+settings.api_key+"&frob="+settings.frob
		page = get_api_sig_link(url)
		page=page.replace("jsonFlickrApi(","")[:-1]
		dec=json.loads(page)
		print(dec)
		settings.token=dec['auth']['token']['_content']
		settings.user_id=dec['auth']['user']['nsid']
		print("user_id generated, please edit your settings.py and set the user_id to: "+settings.user_id)
		print("token generated, please edit your settings.py and set the token to: "+settings.token)
		return -1
		#save_parameter(settings.api_key,settings.secret,settings.frob,settings.token,settings.user_id,settings.temp_path)
	else:
		print("setup completed, please edit your settings.py and rerun")
