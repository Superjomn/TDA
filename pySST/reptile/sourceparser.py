# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pyquery import PyQuery as pq
import urlparse 
from config import Config

class _UrlParser:
    def __init__(self, netlocs=[]):
        self._netlocs = netlocs

    def matchUrl(self, url):
        netloc = urlparse.urlparse(url).netloc
        return netloc in self._netlocs

    def setFiletypes(self, typedic={}):
        '''
        dic structure:
        {
            'html': ['html', 'html'],
        }
        '''
        self._typedic = typedic

    def typeDetect(self, stdUrl):
        path = urlparse.urlparse(stdUrl).path
        ext = os.path.splitext(path)[1:]
        ext = ext[0][1:]
        for key in self._typedic:
            if ext in self._typedic[key]:
                return key
        return 'html'

    def toAbsUrl(self, curPageUrl, newUrl):
        #print '.. curPageUrl: ', curPageUrl
        #print '.. newUrl: ', newUrl
        if not newUrl:
            return curPageUrl
        if len(newUrl)>7 and newUrl[:7] == 'http://':
            return newUrl
        return urlparse.urljoin(curPageUrl, newUrl)
        

class _SourceParser(_UrlParser):
    '''
    parse html and url
    '''
    def __init__(self, netlocs=[]):
        _UrlParser.__init__(self, netlocs)

    def setSource(self, source):
        '''
        put in html source
        '''
        self.source = source
        self.pq = pq(self.source)

    def saveSource(self, key):
        pass

    def setCurPageUrl(self, url):
        self._curPageUrl = url

    def getAbsUrls(self):
        '''
        get abstract link address
        '''
        links = self._getLinks()
        absurls = []
        for link in links:
            #assert( self._curPageUrl != type([]))
            absurl = self.toAbsUrl(self._curPageUrl, link)
            #print '.. trans absurl', absurl
            absurls.append(absurl)
        return absurls

    def _getLinks(self):
        a = self.pq('a')
        aa = []
        for i in range(len(a)):
            aindex=a.eq(i)
            href = aindex.attr('href')
            #print '.. html link:', href
            #aa.append( [aindex.text(), href])
            aa.append(href)
        return aa

import os.path
class SourceParser(_SourceParser):
    def __init__(self):
        _config = Config()
        _netloc = _config.get('reptile', 'netloc')
        _SourceParser.__init__(self, [_netloc])
        self._sourcepath = _config.get('path', 'source')

    def saveSource(self, key):
        print '.. saving ', key
        f = open( self._sourcepath + str(key), 'w')
        f.write(self.source)
        f.close()

