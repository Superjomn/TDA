import htmllib
import formatter
import string 
import sys,urllib
import time

from sourceparser import Stack, nodenames
from styletree import trim

class DatatagExtractor(htmllib.HTMLParser):
    '''
    pass in a node
    and get the text of first tag
    '''
    def __init__(self, verbose=0):
        f = formatter.NullFormatter()
        htmllib.HTMLParser.__init__(self, f, verbose)     
        self._stack = Stack()
        self.tagdataflag = False
        
    def init(self):
        self.data = ''
        
    def unknown_tag(self):
        pass
        
    def unknown_starttag(self,tag, attrs):
        #print '>> unknown_starttag !!!', tag
        self.handle_starttag(tag, None, attrs)
        
    def unknown_endtag(self,tag):
        self.handle_endtag(tag, None)

    def handle_data(self,data):
        #print '>> handle_data', data
        #self._stack.show()
        if (self._stack.size() == 2 and self.tagdataflag) \
            or self._stack.size() == 1:
            self.data += trim(data)

    def handle_starttag(self,tag, method, attrs):
        #print '>> handle_starttag', tag
        #self._stack.show()
        if self._stack.size() == 1 and tag in nodenames:
            #direct child
            #tag data
            self.tagdataflag = True
            starttag = '<' + tag
            for a in attrs:
                starttag += str(a)
            starttag += '>'
            self.data += starttag
        self._stack.push(tag)
        
    def handle_endtag(self,tag, method):
        #print '>> handle_endtag', tag
        #self._stack.show()
        self._stack.pop()
        if tag in nodenames:
            self.tagdataflag = False
            
    def getData(self):
        return self.data

if __name__ == '__main__':
    d = DatatagExtractor()
    d.init()
    strr = open('./test/2').read()
    d.feed(strr)
    print d.getData()

