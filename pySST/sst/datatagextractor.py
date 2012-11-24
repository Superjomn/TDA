import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from pyquery import PyQuery as pq
from sourceparser import nodenames, specialnodes, wildnodes
from styletree import trim, getTagName
import wordsplit 

class DatatagExtractor:
    '''
    pass in a node and return it's direct children features
    '''
    def __ini__(self):
        self.source = ""

    def setNode(self, node):
        self.source = str(node)
        if trim(self.source):
            tag = getTagName(self.source)
            if not tag: return
            self.root = pq(self.source)(tag)
            #clean source
            self.root.remove('script')
            self.root.remove('style')
            return True
        return False

    def getFeatures(self):  
        def searchAdd(list, data):
            if data in list:
                return
            list.append(data)
            
        children = self.root.children()
        
        containtags = []
        for i in range(len(children)):
            child = children.eq(i)
            _tag = getTagName(child)
            #print '_tag: ', _tag
            if _tag: searchAdd(containtags, _tag)
            if _tag in nodenames:
                #add special tag nodes as feature
                data = str(child)
                #fix pq bug: mistakenly treat "<img>hello" as a node
                #split tag and text data
                _end = data.rfind('>')
                yield trim(data[:_end+1])
                _res = trim(data[_end+1:])
                if _res: yield _res
        #print 'containtags: ', containtags

        #remove all tags
        #print 'containtags', containtags
        for t in containtags: self.root.remove(t)
        #words as features
        text = self.root.text()
        for word in [trim(w) for w in wordsplit.split(text)]:
            if word: yield word

class FeatureExtrator:
    '''
    pass in a html file and return all it's features
    '''
    def __init__(self):
        self.source = ""

    def setSource(self, source):
        self.source = source
        if trim(self.source):
            self.root = pq(self.source)('body')
            #clean source
            self.root.remove('script')
            self.root.remove('style')
            return True
        return False
        
    def getFeatures(self):  
        def searchAdd(self, list, data):
            if data in list:
                return
            list.append(data)
        #some tag nodes
        for tag in nodenames:
            tags = self.root(tag)
            for i in range(len(tags)):
                #fix pq bug: mistakenly treat "<img>hello" as a node
                #split tag and text data
                data = str(tags.eq(i))
                _end = data.rfind('>')
                #tag
                yield trim(data[:_end+1])
                #remaining text
                _res = trim(data[_end+1:])
                if _res:
                    for w in [trim(word) for word in wordsplit.split(_res)]:
                        if w: yield w
            #remove tags
            self.root.remove(tag)
        #words as features
        text = self.root.text()
        for word in [trim(w)  for w in wordsplit.split(text)]:
            if word: yield word



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
    print '-' * 50
    print 'tagname: %s' % getTagName(strr)
    d = DatatagExtractor()
    #strr = open('./test/2').read()
    d.setNode(strr)
    data = d.getFeatures()
    print 'get features:'
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
    featureextrator.setSource(strr)
    datas = featureextrator.getFeatures()
    for d in datas:
        print d

