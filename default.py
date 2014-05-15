#!/usr/bin/python2.7
#took addDir and addLink from the southpark plugin
import xbmcplugin,xbmcgui,xbmcaddon
import re,urllib,sys
import HTMLParser,blip
h = HTMLParser.HTMLParser()

#url="http://redlettermedia.com/half-in-the-bag/"
pluginhandle = int(sys.argv[1])
#addon=xbmcaddon.Addon(id='plugin.redlettermedia')

def index():
    addDir('Mr. Plinkett', 'http://redlettermedia.com/plinkett/','get_menus','')
    addDir('Half in the Bag','http://redlettermedia.com/half-in-the-bag/','get_menus','')
    addDir('Best of the Worst','http://redlettermedia.com/best-of-the-worst/','get_menus','')
    addDir('Reviews Archive','http://redlettermedia.com/reviews-archive/','get_menus','')
    addDir('Films','http://redlettermedia.com/films/','get_menus','')
    addDir('Shorts','http://redlettermedia.com/shorts/','get_menus','')
    xbmcplugin.endOfDirectory(pluginhandle)

def get_menus(url):
#    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_LABEL)
    site=urllib.urlopen('http://redlettermedia.com/').read()
    fooR=re.compile(url+'([^"]+)/">([^<]+)')
    foo=fooR.findall(site)
    if foo==[]:
        get_videos(url)
    for menu in foo:
        name=menu[1]
        link=menu[0]
        if not(re.match('^http',link)):
            link=url+link
        addDir(name,link,'get_videos','')
    xbmcplugin.endOfDirectory(pluginhandle)

def get_videos(url):
    site=urllib.urlopen(url).read()
    fooR=re.compile('<a href="([^"]+)"><img src="([^"]+)">')
    videolist=fooR.findall(site)
    for videos in videolist:
        link=videos[0]
        if not(re.match('^http',link)):
            link=url+'/'+link
        nameR=re.compile('.+/([^/]+)/?')
        name=nameR.findall(link)
        name=name[0]
        addLink(re.sub('-',' ',name),link,'playVideo',videos[1],'')
#        addLink(link,link,'playVideo',videos[1],'')
    if videolist==[]:
        listR=re.compile('<a href="([^"]+)">([^<]+)</a> ')
        videolist=listR.findall(site)
        for video in videolist:
            addLink(h.unescape(video[1]),video[0],'','','')
    if videolist==[]:
        videolist=blip.get_blip(url)
        for video in videolist:
            addLink('url',video,'playVideo','','')
    if videolist==[]:
        foo2R=re.compile('src="http://www.youtube.com/embed/([^"]+)"')
        videolist=foo2R.findall(site)
        for video in videolist:
            addLink(video,'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid='+video,'playVideo','','')
    xbmcplugin.endOfDirectory(pluginhandle)

def addLink(name,url,mode,iconimage,desc):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name , "Plot": desc } )
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def playVideo(url):
    urlFull="stack://"
    if re.match('^plugin:',url):
        urlFull+=url + ' , '
    linkliste=[]
    linkliste=blip.get_blip(url)
    if linkliste==[]:
        linkliste=blip.get_blip(url+'/')
    for link in linkliste:
        urlFull+=link + ' , '
    urlFull=urlFull[:-3]
    listitem = xbmcgui.ListItem(path=urlFull)
#    listitem.setInfo(type="Video")
    return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

def parameters_string_to_dict(parameters):
        ''' Convert parameters encoded in a URL to a dict. '''
        paramDict = {}
        if parameters:
            paramPairs = parameters[1:].split("&")
            for paramsPair in paramPairs:
                paramSplits = paramsPair.split('=')
                if (len(paramSplits)) == 2:
                    paramDict[paramSplits[0]] = paramSplits[1]
        return paramDict


#print get_thingies(url)
#print get_videos("http://redlettermedia.com/plinkett/star-trek/")

params=parameters_string_to_dict(sys.argv[2])
mode=params.get('mode')
url=params.get('url')
if type(url)==type(str()):
  url=urllib.unquote_plus(url)

if mode == 'get_menus':
    get_menus(url)
elif mode == 'get_videos':
    get_videos(url)
elif mode == 'playVideo':
    playVideo(url)
elif mode == 'search':
    search()
else:
    index()

