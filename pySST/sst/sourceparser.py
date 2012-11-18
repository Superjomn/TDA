# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pyquery import PyQuery as pq
from styletree import StyleTree, ElementNode, StyleNode, DataNode

class Stack:
    def __init__(self):
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

nodenames = ['a', 'p', 'b',]
from copy import deepcopy as dc
from styletree import getTagName
class SourceParser:
    '''
    parse html source and add nodes to styletree
    '''
    def __init__(self):
        self.styletree = StyleTree()
        self.stack = Stack()

    def setSource(self, source):
        self.pq = pq(source)

    def parse(self):
        body = self.pq('body')
        #init node
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
            for i in range(len(children)):
                child = children.eq(i)
                if getTagName(child) in nodenames:
                    dn.addNodeTag(child)
                    #element.registerStyleNode(dn)
            #add text node
            dn.addTextNode(node)
            if dn.closeNode():
                element.registerStyleNode(dn)

        def addStyleNode(node):
            #print 'addStyleNode(%s)'% node
            #clean node
            childnodes = node.children()
            stylenode = StyleNode()
            stylenode.generateStyleNode(node)
            _stylenode = element.registerStyleNode(stylenode)
            try:
                for i in range(len(childnodes)):
                    childnode = _stylenode.getChild(i)
                    self.stack.push([ childnodes.eq(i), childnode ])
            except:
                pass
                
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
    strr = open('./test/2').read()
    print 'content', len(strr)
    #strr = open('html').read()
    sourceparser = SourceParser()
    sourceparser.setSource(strr)
    sourceparser.parse()
    res = sourceparser.styletree.show()

    
