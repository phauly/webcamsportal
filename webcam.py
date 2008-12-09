#!/usr/bin/env python
# Copyright 2008 Paolo Massa <paolo@gnuband.org>
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero Public License for more details.
#
#    You should have received a copy of the GNU Affero Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import socket
import urllib2
import webbrowser
import os
import time
import getopt, sys
import sys
import traceback

#the default prefix "webcams" where the images will be such as dir/webcams/name/year/month/day/ 
prefix="webcams"

def main():
  
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["help", "download-pictures=", "generate-slideshows="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    if opts==[]: 
        usage()
        sys.exit()	
    for o, a in opts:	
        if o in ("--help"):
            usage()
            sys.exit()
        elif o in ("--download-pictures"):
		directory = a
		download_pictures(directory)
        elif o in ("--generate-slideshows"):	
		directory = a
		generate_slideshows(directory)
        else:
            assert False, "unhandled option"
    # ...


# format is: "url, short_name, frequency of download in minutes (every x minutes we download this image)"
webcams = [
["http://camtef.negrellischool.it/webcam/webcam.jpg","feltre",5],
["http://www.opentopia.com/images/cams/bigpic/4574.jpg","Brasserie",5],
["http://www.vit.heidi.it/web/files/webcam/CAM32.jpg","trentino_traffico_CAM32",5],
["http://www.vit.heidi.it/web/files/webcam/CAM30.jpg","trentino_traffico_CAM30",5],
["http://www.vit.heidi.it/web/files/webcam/CAM1.jpg","trentino_traffico_CAM1",5],
["http://www.vit.heidi.it/web/files/webcam/CAM2.jpg","trentino_traffico_CAM2",5],
["http://www.vit.heidi.it/web/files/webcam/CAM18.jpg","trentino_traffico_CAM18",5],
["http://www.vit.heidi.it/web/files/webcam/CAM19.jpg","trentino_traffico_CAM19",5],
["http://www.vit.heidi.it/web/files/webcam/CAM28.jpg","trentino_traffico_CAM28",5],
["http://www.vit.heidi.it/web/files/webcam/CAM31.jpg","trentino_traffico_CAM31",5],
["http://www.vit.heidi.it/web/files/webcam/CAM26.jpg","trentino_traffico_CAM26",5],
["http://www.vit.heidi.it/web/files/webcam/CAM24.jpg","trentino_traffico_CAM24",5],
["http://www.vit.heidi.it/web/files/webcam/CAM10.jpg","trentino_traffico_CAM10",5],
["http://www.vit.heidi.it/web/files/webcam/CAM11.jpg","trentino_traffico_CAM11",5],
["http://www.vit.heidi.it/web/files/webcam/CAM20.jpg","trentino_traffico_CAM20",5],
["http://www.vit.heidi.it/web/files/webcam/CAM29.jpg","trentino_traffico_CAM29",5],
["http://www.vit.heidi.it/web/files/webcam/CAM21.jpg","trentino_traffico_CAM21",5],
["http://www.vit.heidi.it/web/files/webcam/CAM6.jpg","trentino_traffico_CAM6",5],
["http://www.vit.heidi.it/web/files/webcam/CAM23.jpg","trentino_traffico_CAM23",5],
["http://www.vit.heidi.it/web/files/webcam/CAM27.jpg","trentino_traffico_CAM27",5],
["http://www.vit.heidi.it/web/files/webcam/CAM22.jpg","trentino_traffico_CAM22",5],
["http://www.vit.heidi.it/web/files/webcam/CAM3.jpg","trentino_traffico_CAM3",5],
["http://www.vit.heidi.it/web/files/webcam/CAM7.jpg","trentino_traffico_CAM7",5],
["http://www.vit.heidi.it/web/files/webcam/CAM33.jpg","trentino_traffico_CAM33",5],
["http://www.vit.heidi.it/web/files/webcam/CAM8.jpg","trentino_traffico_CAM8",5],
["http://www.vit.heidi.it/web/files/webcam/CAM9.jpg","trentino_traffico_CAM9",5],
["http://www.vit.heidi.it/web/files/webcam/CAM4.jpg","trentino_traffico_CAM4",5],
["http://www.vit.heidi.it/web/files/webcam/CAM12.jpg","trentino_traffico_CAM12",5],
["http://www.vit.heidi.it/web/files/webcam/CAM5.jpg","trentino_traffico_CAM5",5],
["http://www.vit.heidi.it/web/files/webcam/CAM34.jpg","trentino_traffico_CAM34",5],
["http://www.vit.heidi.it/web/files/webcam/CAM35.jpg","trentino_traffico_CAM35",5],
["http://steinbock77.ch/webcam_4/bilder/livebild_vga.jpg","steinblock4",5],
["http://steinbock77.ch/webcam_8/bilder/livebild_vga.jpg","steinblock8",5],
["http://steinbock77.ch/webcam_7/bilder/livebild_vga.jpg","steinblock7",5],
["http://steinbock77.ch/webcam_5/bilder/am_5.jpg","steinblock5",5],
["http://steinbock77.ch/webcam_15/bilder/livebild_vga.jpg","steinblock15",5],
["http://steinbock77.ch/webcam_22/bilder/livebild_vga.jpg","steinblock22",5],
["http://steinbock77.ch/webcam_18/bilder/livebild_vga.jpg","steinblock18",5],
["http://www.gardasee-webcam.com/webcam/malcesine_webcam1.jpg","riva04",5],
["http://www.visitgardasee.de/webcam/tignale_webcam1.jpg","riva03",5],
["http://www.lagodigarda-webcam.com/webcam/garda_webcam2.jpg","riva02",5],
["http://www.lagodigardamagazine.com/pictures/conca_oro_windsurf_09.jpg","riva01",5],
["http://www.abbeyroad.com/webcam/crossing.jpg","abbey",5],
["http://www.alameteo.it/webcam/current/ala.jpg","ala",5],
["http://www.bbc.co.uk/england/webcams/live/bullring_internal.jpg","bullring",5],
["http://members.lycos.co.uk/trafficcameras/testcap69.jpg","indiatraffic",5],
["http://www.casasanblas.com/cuscopic1.jpg","cusco1",5],
["http://www.casasanblas.com/cuscopic2.jpg","cusco2",5],
["http://www2.comune.venezia.it/webCamSnf/imgsnf_00001.jpg","venezia1",5],
["http://www2.comune.venezia.it/webcamrialto/imgbridge2_00001.jpg","venezia2",5],
["http://www.hotelmontana.it/design/montana/images/webcam/palon.jpg","palon",5],
["http://www.altoadige24.info/upload/15/pw.jpg","bolzano1",5],
["http://www.bolzano-bozen.it/webcam/testimage.jpg","bolzano2",5],
["http://www.st24.tv/upload/15/walterplatz/webcam_bolzano_pos1.jpg","bolzano3",5],
["http://www.st24.tv/upload/15/walterplatz/webcam_bolzano_pos2.jpg","bolzano4",5],
["http://82.90.182.42/record/current.jpg","jesolo",5],
["http://www.beachview.com/pics/pc2288.jpg","panama",5],
["http://www.zeitcam.com/data/federationtower/latest.jpg","federationtowerconstruction",5],
["http://www.zeitcam.com/data/olive8/latest.jpg","construction01",5],
["http://images.webcams.travel/webcam/1193913990.jpg","graz01",5],
["http://gardolo.altervista.org/_altervista_ht/webcam.jpg","gardolo2",5],
["http://meteogardolo.altervista.org/_altervista_ht/webcam.php","gardolo_trento_nord",5],
["http://www.radiodolomiti.com/Telecamere/wcamtn.jpg","radio_dolomiti_trento",5],
["http://srv2.realcam.it/live/pub/6-6.jpg","bondone_skibar",5],
["http://home.rol3.com/myswitzerland/Livebild.jpg","train",5],
["http://www.panorama-hotel.de/webcam32.jpg","panorama_hotel",5],
["http://www.bucuticam.com/arubacam.jpg","aruba_zoom",5],
["http://www.sgisland.gs/webcam/cam/webcam.jpg","leonimairin01",5],
["http://www.sgisland.gs/webcam/cam/webcam2.jpg","leonimairin02",5],
["http://antarctica.martingrund.de/ohig-pingi-z.jpg","antartica_01",5],
["http://antarctica.martingrund.de/ohig-pingi.jpg","antartica_02",5],
["http://ivs.bkg.bund.de/vlbi/ohiggins/ohig-web.jpg","antartica_03",5],
["http://webcams.greenpeace.org/esperanza/latest.jpg","greenpeace_esperanza",5],
["http://webcams.greenpeace.org/rainbow-warrior/latest.jpg","greenpeace_rainbow_boat",5],
["http://webcams.greenpeace.org/arctic-sunrise/latest.jpg","greenpeace_artic_sunrise",5],
["http://barentsrent.no/nktv/nktv.jpg","nktv",5],
["http://gardenia-sanp.sevenc.co.za/webcams/nossob.jpg","nossob_park",5],
["http://gardenia-sanp.sevenc.co.za/webcams/orpen.jpg","orpen_park",5],
["http://gardenia-sanp.sevenc.co.za/webcams/satara.jpg","satara_park",5],
["http://www.antarctica.ac.uk/webcams/rothera/rothera_20081005_130229_rp.jpg","antarctica_rothera",5],
["http://www.antarctica.ac.uk/webcams/rrs_james_clark_ross/webcam.jpg","antarctica_rrs_james_clark_ross",5],
["http://www.breathebonaire.com/~bonairecam2/current.jpg","bonaire_under",5],
["http://www.blackrosebar.com/video.jpg","blackrose",5],
["http://www.portofinoevents.com/webcamfoto/portofino.jpg","portofino",5],
["http://209.227.206.176/M1/m1test.jpg","sorrento",5],
["http://www2.comune.venezia.it/webCamPsm/imgpsm_00001.jpg","venezia",5],
["http://www.vaticanstate.va/templates/..%5Cimages%5Cwebcam%5Cbracciocarlo.jpg","vatican01",5],
["http://www.vaticanstate.va/templates/..%5Cimages%5Cwebcam%5Cconciliazione.jpg","vatican02",5],
["http://www.vaticanstate.va/templates/..%5Cimages%5Cwebcam%5CsepolcroGP2.jpg","sepolcro",5],
["http://www.imb.it/fullsize.jpg","burgo",5],
["http://webcam.princess.com/webcam/caribbean_bridge.jpg","caribbeanbridge",5],
["http://85.128.90.130/axis-cgi/jpg/image.cgi?camera=&resolution=352x288","bench",5],
["http://camtef.negrellischool.it/Casere/webcam.jpg","casere",5],
["http://www.ploerr.com/dolomiten/webcam/dolomiten.jpg","dolomiten",5],
["http://www.dolomitiwebcam.com/cimadodici/vga.jpg","cimadodici",5],
["http://www.dolomitiwebcam.com/baitacuz/vga.jpg","baitacuz",5],
["http://www.dolomitiwebcam.com/sella/vga.jpg","sella",5],
["http://www.dolomitiwebcam.com/belvedere/vga.jpg","belvedere",5],
["http://www.dolomitiwebcam.com/marmolada/vga.jpg","marmolada",5],
["http://www.dolomitiwebcam.com/lago/vga.jpg","lago",5],
["http://www.dolomitiwebcam.com/catinaccio/vga.jpg","catinaccio",5],
["http://seis.it-wms.com/panorama1.jpg","siusipanorama",5],
["http://www.villa.ch/livecam/chillout.jpg","paraglidingchillout",5],
["http://www.ski.it/st16/images/webcam/big/6-9.jpg","bondone6-19",5],
["http://www.state.ak.us/dmv/Benson/benson.jpg","bensonboredom",5],
["http://www.parislive.net/eiffelwebcam1.jpg","eiffel1",5],
["http://www.parislive.net/eiffelcam3.jpg","eiffel3",5],
["http://www.csf4u.com/webcam/camimg/ElMedano.jpg","canarie",5],
["http://62.12.144.159/record/current.jpg","beachvolley",5],
["http://cai.provincia.bergamo.it/webcam/Coca-Valle.jpg","cocavalle",5],
["http://cai.provincia.bergamo.it/webcam/curolago.jpg","curolago",5]
]

def download_pictures(dir):
	print "Going to download images in "+dir

	# timeout in seconds
	timeout = 10
	socket.setdefaulttimeout(timeout)

	opener = urllib2.build_opener()

	#get current date and time
	loctime=time.localtime()
	print time.strftime("%Y-%m-%d", loctime)	
	year=time.strftime("%Y", loctime)
	month=time.strftime("%m", loctime)
	day=time.strftime("%d", loctime)
	hours_minutes_seconds=time.strftime("%H-%M-%S", loctime)

	#get current dir so that we can go back to this later on
	default_dir=os.getcwd()

	# cycle over the list and download the images, place them in dir/webcams/name/year/month/day/ save them as  name.year-month-day.hours-minutes-seconds.jpg
	for webcam in webcams:
		picture_url=webcam[0]
		short_name=webcam[1]
		
		target_dir=dir+"/"+prefix+"/"+short_name+"/"+year+"/"+month+"/"+day+"/"
		if not os.path.isdir(target_dir):
			os.makedirs(target_dir)

		os.chdir(target_dir)

		try:
			#filename is something like "caribbeanbridge.2008-12-04.01-20-01.jpg" and it is saved in caribbeanbridge/2008/12/04
			filename = short_name+"."+year+"-"+month+"-"+day+"."+hours_minutes_seconds+".jpg"	
			print 'Going to download from  %-40s' % (picture_url)
			page = opener.open(picture_url)
			my_picture = page.read()

			print '# %-16s  saved  %-29s  from  %-40s  in  %s' % (short_name,filename,picture_url,target_dir)
			fout = open(filename, "wb")
			fout.write(my_picture)
			fout.close()
			os.chdir(default_dir)
		except urllib2.URLError:
			print "WARNING!!! NOT POSSIBLE to download ("+short_name+") from "+picture_url+" PROBABLY a timeout error (timeout="+str(timeout)+")"
    		except urllib2.HTTPError:
			print "WARNING!!! NOT POSSIBLE to download ("+short_name+") from "+picture_url
    		except:
			print "WARNING!!! ANOTHER ERROR"
		        exInfo = formatExceptionInfo()
         		diag = getDiagnosisFromExcInfo(exInfo)
         		print "diag:", diag, "exc:", exInfo
			sys.exit(3)
		

def generate_slideshows(dir):
	#let us suppose the structure of the dirs is the following
	# /webcams/webcamname1/2008/12/08/
	# /webcams/webcamname1/2008/12/07/
	# /webcams/webcamname1/2008/12/06/
	# /webcams/webcamname2/2008/12/08/
	# ...
	#
	# we are going to create
	# /webcams/webcamname1/2008/12/08/index.html (containing just the links to the 3 html files in the same dir)
	# /webcams/webcamname1/2008/12/08/photos.html (containing the last x photos as thumbnails)
	# /webcams/webcamname1/2008/12/08/slideshow.html (containing the slideshow with the last x photos)
	# /webcams/webcamname1/2008/12/08.html
	# /webcams/webcamname1/2008/12/07.html
	# ....
	# /webcams/webcamname1/2008/12/index.html (links to 08.html, 07.html, ...)
	# /webcams/webcamname1/2008/12.html
	# /webcams/webcamname1/2008/11.html
	# ....
	# /webcams/webcamname1/2008/index.html (links to 12.html, 11.html, ...)
	#
	# /webcams/webcamname1/index.html (links to 12.html, 11.html, ...)
	# /webcams/webcamname1/last_slideshow.html (link to last slideshow such as ./2008/12/08/slideshow.html
	# /webcams/webcamname1/all_slideshows.html (containing a list of all slideshows)
	# /webcams/webcamname1/last_photos.html (link to last photos such as ./2008/12/08/photos.html
	# /webcams/webcamname1/all_photos.html (containing a list of all photos)
	# 
	# /webcams/index.html (list of all html pages such as webcamnam1/index.html, ...)
	# 
	print "NOTHING FOR NOW"
	print "Going to look for files in the directory '"+dir+"'"
                   

def formatExceptionInfo(maxTBlevel=5):
         cla, exc, trbk = sys.exc_info()
         excName = cla.__name__
         try:
             excArgs = exc.__dict__["args"]
         except KeyError:
             excArgs = "<no args>"
         excTb = traceback.format_tb(trbk, maxTBlevel)
         return (excName, excArgs, excTb)


def getDiagnosisFromExcInfo(excInfoTuple):
         try:
           excPattern = (excInfoTuple[0], excInfoTuple[1])
           return ExcDiagDict[ repr(excPattern) ]
         except KeyError:
           return None
         except:
           return None    # maybe was not tuple?


def usage():
	print "Choose between:"
	print "--help"
	print "--download-pictures"
	print "--generate-slideshows"

if __name__ == "__main__":
    main()
