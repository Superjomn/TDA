# -*- coding: utf-8 -*- 

'''
Modified by Bill Bushey <wbushey@acm.org> and Brian Young <byoung061@gmail.com> on August 10th, 2009
'''
import htmllib
import formatter
import string 
import sys,urllib
import time
import matplotlib.pyplot as plt
import jieba

def search(_list, c):
	try:
		i = _list.index(c)
		return True
	except:
		return False

class HtmlTokenParser(htmllib.HTMLParser):
    #重载了HTMLParser
	# return a dictionary mapping anchor texts to lists
	# of associated hyperlinks     
	def __init__(self, verbose=0):
		self.tokens = []
        #二元记录   
		self.binary_tokens = []
		f = formatter.NullFormatter()
		htmllib.HTMLParser.__init__(self, f, verbose)     
		self.ignore_tags = ['script', 'style', 'SCRIPT', 'STYLE']
		self.ignore_flag = False
	def unknown_tag(self):
		self.tokens.append("TAG")
		self.binary_tokens.append(1)
	def unknown_starttag(self,tag, attrs):
		self.tokens.append("<"+tag+">")
        #如果是 Token 则加入1
		self.binary_tokens.append(1)
	def unknown_endtag(self,tag):
        #tokens 记录标签
		self.tokens.append("<\\"+tag+">")
        #始终均有标签
		self.binary_tokens.append(1)
	def handle_data(self,data):
		'''
		#english
		for t in string.split(data):
		'''
		#for Chinese split string to characters
		if not self.ignore_flag:
			'''
			ignore style script
			'''
			for t in jieba.cut(data):
				self.tokens.append(t)
				#对每一个词 添加-1
				self.binary_tokens.append(-1)
	def handle_starttag(self,tag, method, attrs):
		if search(self.ignore_tags, tag):
			self.ignore_flag = True
			print '>> find <script>'
		else:
			self.binary_tokens.append(1)
			self.tokens.append("<"+tag+">")

	def handle_endtag(self,tag, method):
		if search(self.ignore_tags, tag):
			self.ignore_flag = False
		else:
			self.tokens.append("<\\"+tag+">")
			self.binary_tokens.append(1)
		
class HtmlBodyTextExtractor(HtmlTokenParser):
	''' Modified to include the initialization of total_tokens_before'''
	def __init__(self):
		HtmlTokenParser.__init__(self)
		self.encoded = [0]
		self.total_tokens_before = [0]
		self.lookup0N = [0]
		self.lookupN0 = [0]
		self.body_txt = ""
	
	def close(self):
		HtmlTokenParser.close(self)
		self._encode_binary_tokens()
		self._initialise_lookups()
		self.test()

	''' Modified to set values in total_tokens_before'''
	def _encode_binary_tokens(self):
		i = 0
		for x in self.binary_tokens:
			if(abs(x + self.encoded[i]) < abs(self.encoded[i])):
				self.encoded.append(0)
				self.total_tokens_before.append(self.total_tokens_before[-1])
				i = i + 1
			self.encoded[i] = self.encoded[i] + x
			self.total_tokens_before[i] = self.total_tokens_before[i] + 1


		# total_tokens_before works better in the rest of the class if we shift all values up one index
		self.total_tokens_before.insert(0,0) 
	
	def test(self):
		print ">> _encode_binary_tokens"
		print '>> binary tokens', '>> tokens'
		for i, d in enumerate(self.binary_tokens):
			print d, self.tokens[i]

		print '>> ... encoded', self.encoded
		print '>> ... total_tokens_before', self.total_tokens_before


		import numpy as np
		x = np.linspace(0, 10, len(self.binary_tokens))
		y = []
		tag_num = 0
		for i in self.binary_tokens:
			if i>0:
				tag_num += 1
			y.append(tag_num)
		#draw a liner image tokens-tagtokennum
		plt.figure(figsize=(8,4))
		plt.plot(x,y,label="$sin(x)$",color="red",linewidth=2)
		plt.xlabel("token num")
		plt.ylabel("tagtoken num")
		plt.title("PyPlot First Example")
		plt.legend()
		plt.show()


		
		'''
		print '>> _initialise_lookups'
		print '>> ... lookupON', self.lookupON
		print '>> ... lookupN0', self.lookupN0
		'''

	def _initialise_lookups(self):
		t = 0
		#正向tag 数目
		for x in self.encoded:
			if(x>0):
				t = t + x
			self.lookup0N.append(t)
		self.encoded.reverse()
		t = 0
		#反向tag 数目
		for x in self.encoded:
			if(x>0):
				t = t + x
			self.lookupN0.append(t)
		self.encoded.reverse()
		self.lookupN0.reverse()
		del(self.lookupN0[0]) #will never need these values
		del(self.lookup0N[-1])
		
	'''
	This method has been modified to be in O(1).
	This version of the method works with the assumption that all nodes are
	either text or tags. Since we can quickly find out the number of tags
	that have occured upto a given region, and the number of total tags up
	to that region, we can quickly calculate the number of text nodes that 
	have occured upto that region.

	The original method is available as _objective_fcn_old 
	So that, we can get the pos of tokens to maximize the number of text tokens, as well with maximizing the number of tag tokens between and after text tokens, 
	This algorithm just maximize the number of number of tokens of a tag-text-tag token-pair.
	'''
	def _objective_fcn(self,i,j):
		tags_to_i = self.lookup0N[i]
		tags_after_j = self.lookupN0[j]

		text_to_i = self.total_tokens_before[i] - tags_to_i
		text_to_j = self.total_tokens_before[j] - self.lookup0N[j]

		text_between_i_j = text_to_j - text_to_i
		return_val = tags_to_i + tags_after_j + text_between_i_j
		return return_val

	'''
	The original method, which is in O(n)
	'''
	def _objective_fcn_old(self,i,j):
		return_val = self.lookup0N[i] + self.lookupN0[j]
		for x in self.encoded[i:j]:
			if(x<0):
				return_val = return_val - x
		return return_val


	def _is_tag(self,s):
		if(s[0]=='<' and s[-1]=='>'):
			return(1)
		else:
			return(0)
	
	'''
	Method which uses the modified version of _objective_fcn, this function is in O(n^2)
	This method has also been modified to improve the finding of the 'start' and 'end' variables
	Finally, body_text now uses the join method for building the output string
	'''
	def body_text(self):
		self.body_txt = ""
		obj_max = 0
		i_max = 0
		j_max = len(self.encoded)-1
		for i in range(len(self.encoded)-1):
			#越过tag
			if self.encoded[i] > 0:	
				continue
			#i point to text tokens
			for j in range(i,len(self.encoded)):
				#search in remaining tag tokens
				if self.encoded[j] > 0:
					continue
				#j point to following text tokens 
				#between so i and j ,there are tag-text-tag tokens
				obj = self._objective_fcn(i,j)
				if(obj > obj_max):
					obj_max = obj
					i_max = i
					j_max = j
		start = self.total_tokens_before[i_max]
		end = self.total_tokens_before[j_max]

		self.body_txt = " ".join(x for x in self.tokens[start:end] if not self._is_tag(x))

		# This is added for testing purposes, so that the old and new versions produce the same string.
		self.body_txt = self.body_txt + " "

		return(self.body_txt)	

	'''
	Method which uses _objective_fcn_old, this function is in O(n^3)
	'''
	def body_text_old(self):
		self.body_txt = ""
		obj_max = 0
		i_max = 0
		j_max = len(self.encoded)-1
		for i in range(len(self.encoded)-1):
			for j in range(i,len(self.encoded)):
				obj = self._objective_fcn_old(i,j)
				if(obj > obj_max):
					obj_max = obj
					i_max = i
					j_max = j
		start = 0
		end = 0
		for x in self.encoded[:i_max]:
			start = start + abs(x)
		for x in self.encoded[j_max:]:
			end = end + abs(x)
		for x in self.tokens[start:-end]:
			if(not(self._is_tag(x))):
				self.body_txt = self.body_txt + x + " "
		return(self.body_txt)

	def summary(self, start=0, bytes=255):
		if(not(self.body_txt)):
			self.body_text()
		return(self.body_txt[start:(start+bytes)])

	'''
	Modified to use the more efficient join method for building the string
	'''
	def full_text(self):
		ft = ""
		ft = " ".join(x for x in self.tokens if not self._is_tag(x))
		return ft

if __name__ == '__main__':
	html = open(sys.argv[1]).read()
	t0 = time.clock()
	p = HtmlBodyTextExtractor()
	p.feed(html)
	p.close()
	r10 = range(10)
	t1 = time.clock()
	for r in r10:
		x = p.body_text()
	t2 = time.clock()
	for r in r10:
		z = p.body_text_old()
	t3 = time.clock()
	x = p.body_text()
	z = p.body_text_old()
	s = p.summary()
	t = p.full_text()
#	print "\nNew Bodytext:\n",x
#	print "\nOld Bodytext:\n",z
#	print "\nFull Text:\n",t
	if (x == z):
		print "The SAME!!!!!\n"
	print "Time to initialize: %f\nTime for new method: %f\nTime for old method: %f\n" % (t1-t0, t2-t1, t3-t2)

# (c) 2001 Aidan Finn
# Released under the terms of the GNU GPL





