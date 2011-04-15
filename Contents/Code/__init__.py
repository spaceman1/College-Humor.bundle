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
	playlist_xml = XML.ElementFromURL(CH_ROOT + CH_PLAYLIST + '/'.join(url.split('/')[:-1]))
	#playlist_xml = XML.ElementFromURL(url, True)
	flv_url = playlist_xml.xpath("//video/file")[0].text
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
	MediaContainer.httpCookies = HTTP.GetCookiesForURL(CH_ROOT)
	dir.Append(Function(DirectoryItem(OriginalsMenu, "CH Originals", thumb=R("icon-default.png"))))
	dir.Append(Function(DirectoryItem(ShowMenu, "Recently Added", thumb=R("icon-default.png")), url = CH_ROOT + CH_RECENT))
	dir.Append(Function(DirectoryItem(ShowMenu, "Most Viewed", thumb=R("icon-default.png")), url = CH_ROOT + CH_VIEWED))
	dir.Append(Function(DirectoryItem(VideoPlaylistsMenu, "Video Playlists"), url = CH_ROOT + CH_VIDEO_PLAYLIST))
	dir.Append(Function(DirectoryItem(SketchMenu, "Sketch Comedy"), url = CH_ROOT + CH_SKETCH))
	return dir

def getNext(url, menu):
	next = HTML.ElementFromURL(url).xpath('//a[@class="next"]')
	if len(next) != 0:
		return Function(DirectoryItem(menu, title='Next', thumb=R('Next.png')), url=urljoin(CH_ROOT, next[0].get('href')))

			
def OriginalsMenu(sender):
	dir = MediaContainer(title2=sender.itemTitle)
	thumbs = {
		'All Originals': [R('icon-default.png'), 'CollegeHumor Originals are original comedy videos written, directed and produced by the CollegeHumor staff. From our acclaimed pop culture-skewering shorts to our in-office sketch series, our 10 new videos per week will make you laugh until milk comes out your nose. Whether or not you have been drinking milk.'],
		'Sketch': ['http://6.media.collegehumor.cvcdn.com/62/39/collegehumor.efc39e574428dfaac412e2a689b68e61.jpg', 'The bread and butter of CH Originals, these live-action comedy videos take satirical aim at everything under the sun. So for instance, not the moon.'],
		'Star of the Week' : ['http://5.media.collegehumor.cvcdn.com/18/15/collegehumor.ce4c67d997c2bf6ccf149bba7d94fd82.jpg', 'CollegeHumor partners with Hollywood to bring you star-studded internet videos.'],
		'Animation' : ['http://7.media.collegehumor.cvcdn.com/69/68/collegehumor.d2041765f55a58f8d819fb29189b830c.jpg', "Cartoons aren't just for Saturday morning anymore. For instance, you could watch them on Tuesday afternoon. Or Thursday at dusk! The point is, these sketches are animated."],
		'Music Videos': ['http://9.media.collegehumor.cvcdn.com/56/15/collegehumor.4574f62ecd331496bee8f126a2920873.jpg', 'As Wolfgang Amadeus Mozart once said, "Funny songs are better than normal songs."'],
		'Troopers': ['http://8.media.collegehumor.cvcdn.com/15/7/collegehumor.006244cdd376d17aa8ebb0fbc755fdf1.jpg', 'In intergalactic war, there are heroes, there are villains, and then there are these guys.'],
		'Nerd Alert': ['http://4.media.collegehumor.cvcdn.com/50/39/collegehumor.c816b3d7a5928fc19662cb8a59968c39.jpg', 'Every week, three experts discuss the latest in videogames, comic books, cartoons and the other stuff that used to get them beat up.'],
		'Jake and Amir': ['http://3.media.collegehumor.cvcdn.com/8/69/collegehumor.30baaedd706f5adb55f50eb197c41f53.jpg', 'Jake and Amir are two co-workers. And best friends. Just co-workers.'],
		'Hardly Working': ['http://3.media.collegehumor.cvcdn.com/23/56/collegehumor.eb447318daa1d7f39622db3b8faa36e2.jpg', 'A workplace comedy about a comedy workplace.'],
		'Bad Dads': ['http://4.media.collegehumor.cvcdn.com/9/0/collegehumor.200bce938759ef954d5312650dcb3912.jpg', 'Before today, Cory had never met his father. Maybe it was better that way. Starring Michael Cera.'],
		'Very Mary-Kate': ['http://1.media.collegehumor.cvcdn.com/51/28/collegehumor.93260d2a5d79917a4c1f65a9d7f94f3a.jpg', "The unofficial biography of everyone's favorite Olsen twin."],
		'Full Benefits': ['http://0.media.collegehumor.cvcdn.com/4/45/collegehumor.2a16f1566f8397988ac2d5a73def19bb.jpg', 'Sarah and David complicate their work relationship.'],
		'Hello, My Name Is': ['http://3.media.collegehumor.cvcdn.com/19/74/collegehumor.0d97717c01ece1107ba674b07fc4be97.jpg', 'Wigs first, questions later. Spontaneous character-creation with Josh Ruben and Pat Cassels.'],
		'Prank War': ["http://2.media.collegehumor.cvcdn.com/8/12/collegehumor.f8483a22133b84482f6bd1c4caf9221e.jpg", 'Since 2006, CollegeHumor employees Amir Blumenfeld and Streeter Seidell have been embarrassing each other with increasingly elaborate pranks. Enjoy their humiliation here!'],
		
	}
	for show in HTML.ElementFromURL(CH_ROOT + '/videos').xpath('//div[@class="sidebar_nav"]/ul[2]/li/a')[:-1]:
		url = urljoin(CH_ROOT, show.get('href'))
		title = show.text
		thumb, summary = thumbs.get(title, ['', ''])
		dir.Append(Function(DirectoryItem(ShowMenu, title=title, thumb=thumb, summary=summary), url=url))
	return dir
	
def VideoPlaylistsMenu(sender, url):
	# FIXME: get FLV url from webpage
	dir = MediaContainer(title2=sender.itemTitle)
	for item in HTML.ElementFromURL(url).xpath("//div[@class='media video playlist horizontal']"):
		title = item.xpath('./a')[0].get('title')
		summary = item.xpath('./div/p')[0].text
		thumb = item.xpath("a/img")[0].get('src')
		videoURL = urljoin(CH_ROOT + CH_VIDEO_PLAYLIST, item.xpath('a')[0].get('href'))
		dir.Append(Function(DirectoryItem(ShowMenu, title=title, thumb=thumb, summary=summary), url=videoURL))
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
