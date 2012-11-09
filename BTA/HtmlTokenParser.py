#!/usr/bin/python

'''
Modified by Bill Bushey <wbushey@acm.org> and Brian Young <byoung061@gmail.com> on August 10th, 2009
'''

import htmllib
import formatter
import string 
import sys,urllib
import time

class HtmlTokenParser(htmllib.HTMLParser):
	# return a dictionary mapping anchor texts to lists
	# of associated hyperlinks     
	def __init__(self, verbose=0):
		self.tokens = []
		self.binary_tokens = []
		f = formatter.NullFormatter()
		htmllib.HTMLParser.__init__(self, f, verbose)     
	def unknown_tag(self):
		self.tokens.append("TAG")
		self.binary_tokens.append(1)
	def unknown_starttag(self,tag, attrs):
		self.tokens.append("<"+tag+">")
		self.binary_tokens.append(1)
	def unknown_endtag(self,tag):
		self.tokens.append("<\\"+tag+">")
		self.binary_tokens.append(1)
	def handle_data(self,data):
		for t in string.split(data):
			self.tokens.append(t)
			self.binary_tokens.append(-1)
	def handle_starttag(self,tag, method, attrs):
		self.binary_tokens.append(1)
		self.tokens.append("<"+tag+">")
	def handle_endtag(self,tag, method):
		self.tokens.append("<\\"+tag+">")
		self.binary_tokens.append(1)
		

if __name__ == '__main__':
    htmltokenparser = HtmlTokenParser()

