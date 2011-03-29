from urlparse import urljoin

CH_ROOT = "http://www.collegehumor.com"
CH_PLUGIN_PREFIX = "/video/college_humor"
CH_RECENT = "/videos"
CH_VIEWED = "/videos/most-viewed"

CH_VIDEO_PLAYLIST = '/videos/playlists'
CH_WEB_CELEB = '/web-celeb-hall-of-fame'
CH_SKETCH = '/sketch-comedy'
CH_PLAYLIST        = "/moogaloop"

####################################################################################################

def Start():
	Plugin.AddPrefixHandler(CH_PLUGIN_PREFIX, MainMenu, "College Humor", "icon-default.png", "art-default.jpg")
	Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
	MediaContainer.title1 = L('College Humor')
	MediaContainer.viewGroup = 'Details'
	MediaContainer.art = R('art-default.jpg')
	DirectoryItem.thumb = R('icon-default.png')
	HTTP.SetCacheTime(CACHE_1HOUR)
	
####################################################################################################

def GetFlvUrl(url, sender=None):
	playlist_xml = HTML.ElementFromURL(CH_ROOT + CH_PLAYLIST + '/' + url)
	#playlist_xml = XML.ElementFromURL(url, True)
	try: flv_url = playlist_xml.xpath("video/file")[0].text_content()
	except: flv_url = ''
	Log(flv_url)
	return Redirect(flv_url)

def GetFlvFromPage(url, sender=None):
	video = HTML.ElementFromURL(url).xpath('//div[@id="flash_player"]/object')[0].get('data')
	video = urljoin(url, video)
	Log(video)
	return Redirect(video)

####################################################################################################

def MainMenu():
	dir = MediaContainer()
	dir.Append(Function(DirectoryItem(OriginalsMenu, "CH Originals", thumb=R("icon-default.png"))))
	dir.Append(Function(DirectoryItem(ShowMenu, "Recently Added", thumb=R("icon-default.png")), url = CH_ROOT + CH_RECENT))
	dir.Append(Function(DirectoryItem(ShowMenu, "Most Viewed", thumb=R("icon-default.png")), url = CH_ROOT + CH_VIEWED))
	dir.Append(Function(DirectoryItem(VideoPlaylistsMenu, "Video Playlists"), url = CH_ROOT + CH_VIDEO_PLAYLIST))
#	dir.Append(Function(DirectoryItem(WebCelebMenu, "Web Celeb Archive")))
	dir.Append(Function(DirectoryItem(SketchMenu, "Sketch Comedy"), url = CH_ROOT + CH_SKETCH))
	return dir

def getNext(url, menu):
	next = HTML.ElementFromURL(url).xpath('//a[@class="next"]')
	if len(next) != 0:
		return Function(DirectoryItem(menu, title='Next', thumb=R('Next.png')), url=urljoin(CH_ROOT, next[0].get('href')))

			
def OriginalsMenu(sender):
	dir = MediaContainer(title2=sender.itemTitle)
	thumbs = {
		"All Originals": ["icon-default.png", 'CollegeHumor Originals are original comedy videos written, directed and produced by the CollegeHumor staff. From our acclaimed pop culture-skewering shorts to our in-office sketch series, our 10 new videos per week will make you laugh until milk comes out your nose. Whether or not you have been drinking milk.'],
		"CH Music": ["icon-CHMusic.png", 'Check out our collection of original and parody music videos, because as Wolfgang Amadeus Mozart once said, "Funny songs are better than normal songs."'],
		"Animations": ["icon-animations.png", "Cartoons aren't just for Saturday morning anymore. For instance, you could watch them on Tuesday afternoon. Or Thursday at dusk! The point is, these sketches are animated."],
		"Streeter Theeter": ["icon-streeter.png", "CollegeHumor editor Streeter Seidell is a man of many faces, if not talents. Here is where those faces gather."],
		"CH Live": ["icon-chlive.png", "Every month CollegeHumor escapes the Internet to put on a live comedy show at the Upright Citizens Brigade Theatre in New York City, featuring the CH staff and the best stand-up comedians and sketch groups."],
		"Prank War": ["icon-prank-wars.png", 'Since 2006, CollegeHumor employees Amir Blumenfeld and Streeter Seidell have been embarrassing each other with increasingly elaborate pranks. Enjoy their humiliation here!'],
		"Sketches": ["icon-sketches.png", 'The bread and butter of CH Originals, these live-action comedy videos take satirical aim at everything under the sun. So for instance, not the moon.'],
		"Hardly Working": ["icon-hardly-working.png", 'The CollegeHumor staff writers are the stars of these absurdist sketches, filmed right here in our New York City office.'],
		"Jake & Amir": ["icon-jake-amir.png", "BFF's. No were not."],
		"Bleep Bloop": ["icon-bleep-bloop.png", 'The videogames talk show hosted by Jeff Rubin. Where two thumbs down is a good thing!'],
	}
	for show in HTML.ElementFromURL(CH_ROOT).xpath('//div[@class="dropdown"]/ul/li[text()="CH Originals"]/following-sibling::li/a')[:-2]:
		url = urljoin(CH_ROOT, show.get('href'))
		title = show.text
		thumb, summary = thumbs.get(title, ['', ''])
		dir.Append(Function(DirectoryItem(ShowMenu, title=title, thumb=R(thumb), summary=summary), url=url))
	return dir
	
def VideoPlaylistsMenu(sender, url):
	# FIXME: get FLV url from webpage
	dir = MediaContainer(title2=sender.itemTitle)
	for item in HTML.ElementFromURL(url).xpath("//div[@class='media video playlist horizontal']"):
		title = item.xpath('./a')[0].get('title')
		summary = item.xpath('./div/p')[0].text
		thumb = item.xpath("a/img")[0].get('src')
		videoURL = urljoin(CH_ROOT + CH_VIDEO_PLAYLIST, item.xpath('a')[0].get('href'))
		dir.Append(Function(VideoItem(GetFlvFromPage, title=title, thumb=thumb, summary=summary), url=videoURL))
	next = getNext(url, VideoPlaylistsMenu)
	if next != None: dir.Append(next)
	return dir
	
def SketchMenu(sender, url):
	dir = MediaContainer(title2=sender.itemTitle)
	for item in HTML.ElementFromURL(url).xpath("//div[@class='media horizontal sketch_group']"):
		title = item.xpath('./a')[0].get('title')
		videoURL = urljoin(url, item.xpath('./a')[0].get('href'))
		summary = item.xpath('./div[@class="details"]/p')[0].text.strip()
		thumb = item.xpath('./a/img')[0].get('src')
		dir.Append(Function(DirectoryItem(ShowMenu, title=title, summary=summary, thumb=thumb), url=videoURL))
	next = getNext(url, SketchMenu)
	if next != None: dir.Append(next)
	return dir

def ShowMenu(sender, url):
	dir = MediaContainer(title2=sender.itemTitle)	
	for item in HTML.ElementFromURL(url).xpath('//div[@class="media video horizontal"]'):
		title = item.xpath('./a')[0].get('title')
		itemURL = item.xpath('./a')[0].get('href')
		summary = item.xpath('./div[@class="details"]/p')[0].text.strip()
		thumb = item.xpath('./a/img')[0].get('src')
		dir.Append(Function(VideoItem(GetFlvUrl, title=title, summary=summary, thumb=thumb), url=itemURL))
	next = getNext(url, ShowMenu)
	if next != None: dir.Append(next)
	return dir
