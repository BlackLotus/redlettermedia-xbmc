#!/usr/bin/python2
#blip downloader beta 0.2
import re,urllib,sys,urllib2
import xml.dom.minidom

playR=re.compile('(http:\/\/blip.tv\/play\/[^"^ ^?]+)')
rssR=re.compile('(/rss/flash/[^"^?^ ^&]+)')

#link=sys.argv[1]


def get_rss(link):
    site=urllib.urlopen(link)
    content=site.read()
    if site.url != link:
        content=urllib.urlopen(site.url).read()
    rssurl=[]
    if site.url != link and re.match('http://blip.tv',link):
        rssurl.append('http://blip.tv'+rssR.findall(urllib.unquote(site.url))[0])
        return rssurl
    elif rssR.findall(content):
        rssurl.append('http://blip.tv'+rssR.findall(site.read())[0])
        return rssurl
    elif playR.findall(content):
        for link in playR.findall(content):
            for rss in get_rss(link):
                rssurl.append(rss)
        return rssurl
    else:
        print 'Nothing to do.Sure there is any blip video?'
        print site.read()

def get_links(rss):
    links={}
    xmlc = xml.dom.minidom.parse(urllib.urlopen(rss))
    for media_item in xmlc.getElementsByTagName('item'):
        item_media_group = media_item.getElementsByTagName('media:group')[0]
        item_media_content = item_media_group.getElementsByTagName('media:content')
        for element in item_media_content:
            links.update({element.getAttribute('type') : element.getAttribute('url')})
        return links

def get_blip(link,ftype="video/x-m4v"):
    rssa=get_rss(link)
    links=[]
    for rss in rssa:
        print rss
        links.append(get_links(rss)[ftype])
    return links
