# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pyquery import PyQuery as pq
from styletree import StyleTree, ElementNode, StyleNode

class Stack:
    def __init__(self):
        self.datas = []
    def push(self, data):
        self.datas.append(data)
    def pop(self):
        return self.datas.pop()
    def size(self):
        return len(self.datas)
    def getTop(self):
        return self.datas[-1]
    def empty(self):
        return self.size() == 0

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

    def _getTag(self, node):
        end = str(node).index('>')
        return str(node)[:end+1]

    def parseIter(self):
        if not self.stack.empty():
            (node , element) = self.stack.pop()
            stylenode = StyleNode()
            childnodes = node.children()
            for i in range(len(childnodes)):
                childnode = childnodes.eq(i)
                html = childnodes
                element = ElementNode(self._getTag(childnode))
                stylenode.addChildElement(element)
            element.registerStyleNode(stylenode)

