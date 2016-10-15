import flickr
import json
import random
import settings,sys,os

####################################################### api key #######################################################
print("######################## 1/5 ########################")
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

####################################################### mode? #######################################################
print("######################## 2/5 ########################")
print("Which mode would you like to run:")
print("1) Show all of photos from your flickr account")
print("2) Show only pictures from one album of your account")
print("3) Show random public photos from a given searchstring")
print("Please select ",end="")

i=0
while(int(settings.mode)>0 and int(settings.mode)<=3 and i==0):
	i=1
	if(settings.mode != ""):
		print("["+str(settings.mode)+"]:")
	else:
		print(":")
	input=sys.stdin.readline().rstrip()
	if(settings.mode != "" and input==""):
		input=settings.mode
	settings.mode=int(input)
####################################################### searchtag #######################################################
if(settings.mode==3):
	c=0
	while(c<1):
		print("Enter search term ",end="")
		if(settings.searchtag != ""):
			print("["+str(settings.searchtag)+"]:")
		else:
			print(":")
		input=sys.stdin.readline().rstrip()
		if(settings.searchtag != "" and input==""):
			input=settings.searchtag
		settings.searchtag=input
		c=flickr.get_public_photo_count_for_tag(settings.searchtag)
		if(c==0):
			print("Flickr couldn't find pictures for '"+str(settings.searchtag)+"', please choose another term")
		else:
			print("Found "+str(c)+" pictures for the search term")
####################################################### token #######################################################
if(settings.mode==1 or settings.mode==2):
	print("######################## 3/5 ########################")
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
if(settings.mode==2):
	print("######################## 3/5 ########################")
	print("loading all albums from your account")
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
####################################################### convert to b/w #######################################################
print("######################## 4/5 ########################")
input=-1
while(not(input in [0,1])):
	print("Do you want to convert to grayscale (n/y)",end="")
	if(str(settings.convert_color) == "1"):
		print("[Y]:")
	elif(str(settings.convert_color) == "0"):
		print("[N]:")
	else:
		print(":")
	input=sys.stdin.readline().rstrip()
	if(input==""):
		input=settings.convert_color
	elif(input.lower()=="y"):
		input=1
	elif(input.lower()=="n"):
		input=0
	settings.convert_color=input
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
	out.write("searchtag=\""+settings.searchtag+"\"\n")
	out.write("time_regular_update = 5*60*1000\n")
	out.write("time_splash = 1000\n")
	out.write("time_total_refresh = 6*60*60*1000\n")
	out.write("mode="+str(settings.mode)+"\n")
	out.write("convert_color="+str(settings.convert_color)+"\n")

print("######################## 4/5 ########################")
print("written settings file")
print("run './start.sh' or 'python3 "+os.path.dirname(os.path.realpath(__file__))+"/main.py'")
