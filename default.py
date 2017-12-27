# -*- coding: utf-8 -*-
#Библиотеки, които използват python и Kodi в тази приставка
import re
import sys
import os
import urllib
import urllib2
import xbmc, xbmcplugin,xbmcgui,xbmcaddon
import urlresolver
import unicodedata

__addon_id__= 'plugin.video.filmi2k'
__Addon = xbmcaddon.Addon(__addon_id__)
searchicon = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/search.png")

MUA = 'Mozilla/5.0 (Linux; Android 5.0.2; bg-bg; SAMSUNG GT-I9195 Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) Version/1.0 Chrome/18.0.1025.308 Mobile Safari/535.19' #За симулиране на заявка от мобилно устройство
UA = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0' #За симулиране на заявка от  компютърен браузър



def CATEGORIES():
        addDir('Търсене на филм','https://filmi2k.com/?s=',2,searchicon)
        #addDir('Сериали','https://filmi2k.com/seriali-onlayn/',2, 'https://filmi2k.com/wp-content/uploads/2017/08/movies.png')
        #addDir('Всички филми','https://filmi2k.com/?filter=date&cat=0',1,'DefaultVideo.png')
        baseurl = 'https://filmi2k.com/'
        req = urllib2.Request(baseurl)
        req.add_header('User-Agent', UA)
        response = urllib2.urlopen(req)
        data=response.read()
        response.close()
        cr = 0
        match = re.compile('li class="menu-item menu-item-type-taxonomy menu-item-object-category menu-item-.*"><a title=".+?" href="(.+?)">(.+?)</a>').findall(data)
        for link, title in match:
         thumbnail = 'https://filmi2k.com/wp-content/uploads/2017/08/movies.png'
         addDir(title,link,1,thumbnail)
         cr = cr + 1

def INDEXPAGES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', MUA)
        response = urllib2.urlopen(req)
        data=response.read()
        response.close()
        br = 0 
        match = re.compile('<a href="(.+?)" rel="bookmark" title="(.+?)">\n.*\n.*\n.*\n.*\n.*src="(.+?)"').findall(data)
        for vid,title,thumb in match:
         thumbnail = 'https://filmi2k.com/' + thumb
         addLink(title,vid,3,thumbnail)
         br = br + 1
        if br == 25:
         matchp = re.compile('<a class="current">(.+?)</a></li><li><a href=.(.+?)/page/').findall(data)
         for pagenumb,baseurl in matchp:
             print pagenumb
             print baseurl
             page = int(pagenumb)
             currentDisplayCounter = page + 1
             url = baseurl + '/page/' + str(currentDisplayCounter)
             print 'sledvasta stranica' + url
             thumbnail='DefaultFolder.png'
             addDir('следваща страница>>'+str(currentDisplayCounter),url,1,thumbnail)
         
#Търсачка
def SEARCH(url):
        keyb = xbmc.Keyboard('', 'Търсачка')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
         searchText = urllib.quote_plus(keyb.getText())
         searchText=searchText.replace(' ','+')
         searchurl = url + searchText
         searchurl = searchurl.encode('utf-8')
         INDEXPAGES(searchurl)
        else:
         addDir('Върнете се назад в главното меню за да продължите','','',"DefaultFolderBack.png")


def SHOW(url):
       req = urllib2.Request(url)
       req.add_header('User-Agent', UA)
       response = urllib2.urlopen(req)
       data=response.read()
       response.close()
       match = re.compile('var _.*"(.+?)"').findall(data)
       for link in match:
        enclink = link.decode('unicode_escape').encode('raw_unicode_escape').decode('utf8', 'ignore').encode('utf8', 'ignore')
        matchi = re.compile('thumbnailUrl" content="(.+?)" />').findall(data)
        for thumb in matchi:
         matchd = re.compile('</div><p>(.+?)</p>').findall(data)
         for desc in matchd:
        #print link
          thumbnail = 'https://filmi2k.com' + thumb
          match0 = re.compile('<iframe src="(.+?)"').findall(enclink)
          for enc in match0:
           addLink2(name,enc,4,desc,thumbnail)



def PLAY(url):
         li = xbmcgui.ListItem(iconImage=iconimage, thumbnailImage=iconimage, path=url)
         li.setInfo('video', { 'title': name })
         link = url
         try: stream_url = urlresolver.HostedMediaFile(url).resolve()
         except:
               deb('Link URL Was Not Resolved',link); deadNote("urlresolver.HostedMediaFile(link).resolve()","Failed to Resolve Playable URL."); return
        ##xbmc.Player().stop()
         play=xbmc.Player() ### xbmc.PLAYER_CORE_AUTO | xbmc.PLAYER_CORE_DVDPLAYER | xbmc.PLAYER_CORE_MPLAYER | xbmc.PLAYER_CORE_PAPLAYER
         try: _addon.resolve_url(url)
         except: t=''
         try: _addon.resolve_url(stream_url)
         except: t=''
         play.play(stream_url, li); xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=li)
         try: _addon.resolve_url(url)
         except: t=''
         try: _addon.resolve_url(stream_url)
         except: t=''

def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty("IsPlayable" , "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink2(name,url,mode,plot,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setArt({ 'thumb': iconimage,'poster': iconimage, 'banner' : iconimage, 'fanart': iconimage })
        liz.setInfo( type="Video", infoLabels={ "Title": name, "plot": plot } )
        liz.setProperty("IsPlayable" , "true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param







params=get_params()
url=None
name=None
iconimage=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        name=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass



if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
    
elif mode==1:
        print ""+url
        INDEXPAGES(url)

elif mode==2:
        print ""+url
        SEARCH(url)

elif mode==3:
        print ""+url
        SHOW(url)
        
elif mode==4:
        print ""+url
        PLAY(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
