import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import htmllib
import formatter
import string 
import sys,urllib
import time

from sourceparser import Stack 
from sourceparser import nodenames, specialnodes, wildnodes
from styletree import trim
import wordsplit 

class DatatagExtractor(htmllib.HTMLParser):
    '''
    pass in a node
    and get the text of first tag
    and some special nodes like p b img and so on
    split text to words and treate special node as a word
    '''
    def __init__(self, verbose=0):
        f = formatter.NullFormatter()
        htmllib.HTMLParser.__init__(self, f, verbose)     
        self._stack = Stack()
        self.tagdataflag = False
        self.tagskipflag = False
        self._splitf = '||#'
        
    def init(self):
        self.datas = []
        self.data = ""
        
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
        if self.tagskipflag: return
        if self.tagdataflag:
            self.data += trim(data)

    def handle_starttag(self,tag, method, attrs):
        '''
        push in a node  and return it's direct children's text data
        '''
        # only care data from body
        print '>> handle tag:', tag
        print 'stack size: %d' % self._stack.size()
        '''
        if self._stack.empty():
            if tag == 'body':
                self._stack.push(tag)
            else: return
        '''
        if tag in wildnodes: 
            self.tagskipflag = True
            return
        if self._stack.size() == 1 and tag in nodenames:
            #direct child
            #tag data
            self.tagdataflag = True
            #<img/> hello world
            if tag in specialnodes:
                self.tagdataflag = False
            starttag = self._splitf + '<' + tag
            for a in attrs:
                starttag += str(a)
            starttag += '>'
            self.data += starttag
        self._stack.push(tag)
        
    def handle_endtag(self,tag, method):
        #print '>> handle_endtag', tag
        #self._stack.show()
        if self._stack.empty(): return
        if tag in wildnodes:
            self.tagskipflag = False
            return
        self._stack.pop()
        if tag in nodenames:
            self.tagdataflag = False
           
    def getData(self):
        return self.data.split( self._splitf)

    def getFeatures(self):
        for data in self.getData():
            '''
            tag text
            if text: split word
            '''
            if data:
                if data[0] == '<':
                    '''
                    a tag
                    '''
                    #dn.registerData(data)
                    yield data
                else:
                    words = wordsplit.split(data)
                    for word in words:
                        yield word




class FeatureExtrator(DatatagExtractor):
    '''
    extractor all features from a html file
    '''
    def __init__(self):
        DatatagExtractor.__init__(self)

    def fromfile(self, filename):
        c = open(filename).read()
        self.init()
        self.feed(c)

    def setSource(self, source):
        self.init()
        self.feed(source)

    def handle_starttag(self,tag, method, attrs):
        print '>> handle tag:', tag
        if tag in wildnodes: 
            self.tagskipflag = True
            return
        if self._stack.empty():
            if tag == 'body':
                self._stack.push(tag)
            else: return
        if tag in nodenames:
            #tag data
            self.tagdataflag = True
            if tag == 'img':
                self.tagdataflag = False
            starttag = self._splitf + '<' + tag
            for a in attrs:
                starttag += str(a)
            starttag += '>'
            self.data += starttag
        self._stack.push(tag)

    def handle_endtag(self,tag, method):
        if self._stack.empty(): return
        if tag in wildnodes:
            self.tagskipflag = False
            return
        self._stack.pop()
        if tag in nodenames:
            self.tagdataflag = False

    def handle_data(self,data):
        if self.tagskipflag or self._stack.empty(): return
        if self.tagdataflag:
            self.data += trim(data)
        else:
            self.data += self._splitf + trim(data)

if __name__ == '__main__':
    strr = '''
        <div id="nav">
            plain text 
            <a href=#>hello world</a>
            <a href=#>hello world</a>
            <a href=#>hello world</a>
            <p> tex in p </p>
            <img src='hello'/>after img
            <script src="hello">alert('ehllo'); </script>
        </div>

    '''
    print strr
    d = DatatagExtractor()
    d.init()
    #strr = open('./test/2').read()
    d.feed(strr)
    data = d.getFeatures()
    for da in data:
        print da

    print '-'*50
    print '-'*50
    print '-'*50

    strr = '''
    <title>hello</title>
    <body>
        <div id="nav">
            plain text 
            <a href=#>hello world</a>
            <a href=#>hello world</a>
            <a href=#>hello world</a>
            <p> hello world</p>
            <img src='hello'/>after img
            <script src="hello">alert('ehllo'); </script>
        </div>
    </body>

    '''
    print strr

    featureextrator = FeatureExtrator()
    featureextrator.init()
    featureextrator.feed(strr)
    datas = featureextrator.getFeatures()
    for d in datas:
        print d

