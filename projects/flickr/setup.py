import flickr
import json
import random
import settings,sys,os

####################################################### api key #######################################################
print("######################## 1/4 ########################")
print("First you need a api key, get one at: https://www.flickr.com/services/apps/create/noncommercial/?")
print("Please enter the displayed api key from the website ",end="")
if(settings.api_key != ""):
	print("["+settings.api_key+"]:")
else:
	print(":")
input=sys.stdin.readline().rstrip()
if(settings.api_key != "" and input==""):
	input=settings.api_key
settings.api_key = input

print("Please enter the secret values ",end="")
if(settings.secret != ""):
	print("["+settings.secret+"]:")
else:
	print(":")
input=sys.stdin.readline().rstrip()
if(settings.secret != "" and input==""):
	input=settings.secret
settings.secret=input

####################################################### token #######################################################
print("######################## 2/4 ########################")
if(settings.token != "" and settings.user_id != "" ):
	print("You already have a flickr security token, do you want to keep it? [y]/n:")
	mode=sys.stdin.readline().rstrip()
	if(mode == "n" or mode == "no" or mode == "N"):
		settings.token = ""
		settings.user_id = "" 
else:
	print("lets get a flickr security token")

if(settings.token == "" or settings.user_id == "" ):
	print("we have to get a one time key (frob) to allow this app to access you flickr account")
	url="https://flickr.com/services/rest/?method=flickr.auth.getFrob&api_key="+settings.api_key+"&format=json"
	page = flickr.get_page(flickr.get_api_sig_link(url))
	page=page.replace("jsonFlickrApi(","")[:-1]
	dec=json.loads(page)
	settings.frob=dec['frob']['_content']
	res=flickr.get_api_sig_link("http://flickr.com/services/auth/?api_key="+settings.api_key+"&perms=read&frob="+settings.frob)
	print("frob generated, now please open: \n"+res)
	print("hit [enter] once you've opened the website and granted access")
	null=sys.stdin.readline()

	url="https://flickr.com/services/rest/?method=flickr.auth.getToken&format=json&api_key="+settings.api_key+"&frob="+settings.frob
	page = flickr.get_page(flickr.get_api_sig_link(url))
	page=page.replace("jsonFlickrApi(","")[:-1]
	dec=json.loads(page)
	settings.token=dec['auth']['token']['_content']
	settings.user_id=dec['auth']['user']['nsid']
	print("user_id generated")
	print("token generated")

####################################################### photoset #######################################################
print("######################## 3/4 ########################")
print("Do you want to run this on all photos from you account or just one photoset/album",end="")
if(settings.photoset_id != ""):
	print(" [currently running on album mode]:")
else:
	print(":")

print("All photos mode? ([y]/n)")
mode=sys.stdin.readline().rstrip()
if(mode == "n" or mode == "no" or mode == "N"):
	print("ok, I'll list all sets ... loading")
	album=flickr.get_albums()
	photo_id=-1
	while(photo_id<0 or photo_id>int(album['photosets']['total'])-1):
		print("please enter the nr 0-"+str(int(album['photosets']['total'])-1)+":")
		try:
			photo_id = int(sys.stdin.readline().rstrip())
		except:
			photo_id=-1
	settings.photoset_id=album['photosets']['photoset'][photo_id]['id']
	print("choose album ",end="")
	print(album['photosets']['photoset'][photo_id]['title']['_content'])
else:
	settings.photoset_id=""

####################################################### write settings #######################################################
filename=os.path.dirname(os.path.realpath(__file__))+"/settings.py"
with open(filename, 'w') as out:
	out.write("import tempfile\n")
	out.write("api_key=\""+settings.api_key+"\"\n")
	out.write("secret=\""+settings.secret+"\"\n")
	out.write("token=\""+settings.token+"\"\n")
	out.write("user_id=\""+settings.user_id+"\"\n")
	out.write("photoset_id=\""+settings.photoset_id+"\"\n")
	out.write("temp_path=tempfile.mktemp()\n")

print("######################## 4/4 ########################")
print("written settings file")
print("run './start.sh' or 'python3 "+os.path.dirname(os.path.realpath(__file__))+"/main.py'")
