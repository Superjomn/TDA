#encoding=utf-8
'''
import sys
sys.path.append("../")
'''
import jieba

import re
default_encoding='utf-8'
def split(data):
    if not data: return []
    return jieba.cut(data)
'''
def split(text):
    #text = ''.join(open('somefile.txt').readlines())
    sentences = re.split(r' *[\.\?!][\'"\)\]]* *', text)
    return sentences.findall()


def split(paragraph):
    import re
    # to split by multile characters

    #   regular expressions are easiest (and fastest)
    sentenceEnders = re.compile('[\<\>\-\s,.!?]')
    sentenceList = sentenceEnders.split(paragraph)
    return sentenceList

'''

if __name__ == '__main__':
    path = '../reptile/source/2'
    c = open(path).read()
    from pyquery import PyQuery as pq
    t = pq(c)
    t.remove('script')
    t.remove('style')
    words = split(t.text())
    for word in words:
        print 'word: ', word
