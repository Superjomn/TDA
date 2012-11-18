# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pyquery import PyQuery as pq
from styletree import StyleTree, ElementNode, StyleNode, DataNode
from styletree import getTagName, datanodenames

class Stack:
    def __init__(self):
        self.datas = []

    def init(self):
        self.datas = []

    def push(self, data):
        print '.. push', data
        self.datas.append(data)

    def pop(self):
        #print '.. pop'
        return self.datas.pop()

    def size(self):
        return len(self.datas)

    def getTop(self):
        return self.datas[-1]

    def empty(self):
        return self.size() == 0

    def show(self):
        print '-'*50
        print '-'*50
        print '*'*20 + '<<stack>>'+'*' *  20
        for data in self.datas:
            print data
        print '<'*50

nodenames = ['a', 'p', 'b',]
from copy import deepcopy as dc
from styletree import getTagName
import datatagextractor
class SourceParser:
    '''
    parse html source and add nodes to styletree
    '''
    def __init__(self):
        self.styletree = StyleTree()
        self.stack = Stack()
        self.datatagextractor = datatagextractor.DatatagExtractor()

    def setSource(self, source):
        self.pq = pq(source)

    def parse(self):
        body = self.pq('body')
        #init node
        self.stack.init()
        self.stack.push(
            [
                body,
                self.styletree.body
            ]
        )
        self.parseIter()

    def parseIter(self):

        def addDataNode(fnode, element):
            #print 'addDataNode'
            children = fnode.children()
            print 'fnode.children: ', children
            dn = DataNode()
            self.datatagextractor.init()
            self.datatagextractor.feed(str(fnode))
            res = self.datatagextractor.getData()
            if dn.setData(res):
                element.registerStyleNode(dn)

        def addStyleNode(node):
            #print 'addStyleNode(%s)'% node
            #clean node
            childnodes = node.children()
            stylenode = StyleNode()
            assert node != None , "addStyleNode(None)"
            stylenode.generateStyleNode(node)
            _stylenode = element.registerStyleNode(stylenode)
            j = -1
            for i in range(len(childnodes)):
                child = childnodes.eq(i)
                tag = getTagName(child)
                print '** tag:', tag
                if tag not in datanodenames:
                    j += 1
                    childnode = _stylenode.getChild(j)
                    self.stack.push([ childnodes.eq(i), childnode ])
                
        while not self.stack.empty():
            (node , element) = self.stack.pop()
            #print '.. stylenode: ', _stylenode
            addDataNode(node, element)
            addStyleNode(node)

    def _getTag(self, node):
        end = str(node).index('>')
        res = str(node)[:end+1]
        #print 'getTag: ', res
        return res


if __name__ == '__main__':
    strr = '''
<body>
    body-data
    <div id='nav'>
        nav-data
        <a href='#'>a1</a>
        <a href='#'>a2</a>
        <a href='#'>a3</a>
    </div>
</body>
    '''
    sourceparser = SourceParser()
    for i in range(1,3):
        strr = open('./test/%d'%i).read()
        print 'content', len(strr)
        #strr = open('html').read()
        sourceparser.setSource(strr)
        sourceparser.parse()
    sourceparser.styletree.cal()
    res = sourceparser.styletree.show()
    

    
