# -*- coding: utf-8 -*-
import threading  
import chardet
import urllib2  
import StringIO  
import gzip  
import string  


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pyquery import PyQuery as pq
import xml.dom.minidom as dom
import socket
import Queue as Q
from urlist import Urlist

class _Reptile:
    '''
    single tutorial
    '''
    def __init__(self, pageNum=200):
        self._urlist = Urlist()
        self._queue = Queue()
        self.pageNum = pageNum
        self._downloadedPageNum = 0

    def matchUrl(self, url):
        '''
        @in absolute path
        return true/false
        '''
        pass
    def inQueue(self, url):
        if not self._outPageRange():
            if self.matchUrl(url):
                if not self._urlist.find(url):
                    self._queue.put(url)

    def outPageRange(self):
        '''
        num of downloaded page is outof range?
        return true/false
        '''
        return self._pageNum > self._downloadedPageNum

    def requestSource(self, url):
        self.pageNum += 1
        self.opener = urllib2.build_opener()     
        request = urllib2.Request(url) 
        request.add_header('Accept-encoding', 'gzip')
        request.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
        try:            
            page = self.opener.open(request, timeout=2) #设置超时为2s

            if page.code == 200:      
                predata = page.read()
                pdata = StringIO.StringIO(predata)
                gzipper = gzip.GzipFile(fileobj = pdata)  
                
                try:  
                    data = gzipper.read()  
                except(IOError):  
                    data = predata

                length = len(data)    

                if length<300 or length > 3000000:
                    return False
                #begain to parse the page
                return data

            page.close()  
        except:  
            print 'time out'  


from sourseparser import SourceParser
from config import Config

class Reptile(_Reptile):
    '''
    main reptile
    '''
    def __init__(self):
        _config = Config()
        _Reptile.__init__(_config.getInt('reptile', 'page_num'))
        self.netloc = 'www.sina.com.cn'
        self.curPageUrl = ''
        self._sourceparser = SourceParser()
        self.inQueue.put( _config.get('reptile', 'startpage') )

    def matchUrl(self, url):
        return self._sourceparser.matchUrl(url)

    def run(self):
        while not self._queue.empty():
            if not self.outPageRange():
                url = self.inQueue.get()
                print 'post: ', url
                _source = self.requestSource(url)
                print 'get: source length ', len(_source)
                self._sourceparser.setSource(_source)
                self._sourceparser.saveSource(self.pageNum)
                _absurls = self._sourceparser.getAbsUrls()
                for url in _absurls:
                    self.inQueue(url)


        
        
        
        
        
        
        
        
        



if __name__ == '__main__':
    reptile = _Reptile()
    print reptile.requestSource('http://www.sina.com.cn/')
