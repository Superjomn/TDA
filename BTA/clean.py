# -*- coding: utf-8 -*- 
#from pyquery import PyQuery as pq
import re
import chardet
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def transcode(source):
	'''
	转码 自动转化为utf8
	'''
	try:
		res = chardet.detect(source)
	except:
		return False
	confidence = res['confidence']
	encoding = res['encoding']
	print encoding
	p = re.compile("&#(\S+);")
	source = p.sub("",source)
	if encoding == 'utf-8':
		return source
	if confidence < 0.6:
		return False
	else:
		print 'transcode...'
		return source.decode(encoding)
		#return unicode(source, encoding, 'ignore')

class HtmlCleaner:
    '''
    clean the html so that the template detection algorithm can work
    '''
    def __init__(self):
        pass

    def init(self, source):
		self.source = transcode(source)

    def initFromFile(self, filename):
        f = open(filename)
        c = f.read()
        f.close()
        self.init(c)

    def rmScript(self):
        #self.pq('script').remove()
		rule=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.M)
		rule=re.compile('<\s*SCRIPT[^>]*>[^<]*<\s*/\s*SCRIPT\s*>',re.I|re.S|re.M)
		self.source = rule.sub("", self.source)

    def rmStyle(self):
		rule=re.compile('<\s*STYLE[^>]*>[^<]*<\s*/\s*STYLE\s*>',re.I|re.S|re.M)
		rule=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I|re.S|re.M)
		self.source = rule.sub("", self.source)

    def toString(self):
		return self.source

    def toFile(self, filename='test.html'):
        print '> to file'
        f = open(filename, 'w')
        f.write(self.toString())
        f.close()
        

if __name__ == '__main__':
        htmlcleaner = HtmlCleaner()
        htmlcleaner.initFromFile('./sina.html')
        htmlcleaner.rmScript()
        htmlcleaner.rmStyle()
        htmlcleaner.toFile('sina.clean.html')
