from pyquery import PyQuery as pq
import  chardet as cd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Cleaner:
	def init(self, source):
		self.pq = pq(source)
		self.clean_tags = [
			'style',
			'script',
			'STYLE',
			'SCRIPT',
		]
	
	def fromFile(self, filename):
		f = open(filename)
		c = f.read()
		f.close()
	
	def clean(self):
		for tag in self.clean_tags:
			self.pq(tag).remove()
	
	def toString(self):
		return self.pq.html()
	
	def toFile(self, filename='clean.test'):
		f = open(filename, 'w')
		f.write(ss)
		f.close()
