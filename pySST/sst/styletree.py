from __future__ import division
'''
Created on Nov 11, 2012

@author: chunwei
'''
##################################################
# structure of StyleTree:
# a static linked list:
# * <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# * array:
# * hash     child   brother  imp  count
# * ---------------------------------------
# *  hash = hash(tagname)
# *  child always link to the latest added child 
# *  brother always link to the last brother found
# *  imp is finally calculated value using count
# *#################################################*/
from type import Node

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

class ElementNode:
    '''
    base tag class
    data structure:
        [
            tagname,
            childtags: [],
            count = 1,
            imp = 0,
        ]
    '''
    def __init__(self, name = ''):
        self._name = name
        self._childStyleNodes = []

    def getName(self):
        return self._name

    def getChildStyleNodes(self):
        return self._childStyleNodes

    def addChildStyleNode(self, node):
        '''
        @ node : StyleNode
        '''
        self._childStyleNodes.append(node)

    def _searchStyleNode(self, stylenodename):
        for node in self.getChildStyleNodes():
            if node.getPreview() == stylenodename:
                return node
        return False

    def registerStyleNode(self, stylenode):
        node = self._searchStyleNode(stylenode.getPreview())
        if node:
            node.incCount()
            return node
        else:
            self.addChildStyleNode(stylenode)

    def __str__(self):
        res = '(tagname: ' + str(self.getName()) + '\n'
        res += '['
        for child in self.getChildStyleNodes():
            res += str(child)
        res += '])'
        return res
        

class StyleNode:
    def __init__(self):
        self._preview = ''
        self._imp = 0
        self._count = 1
        self._children = []

    def getPreview(self):
        #return self._preview
        return self.generatePreview()

    def getImp(self):
        return self._imp

    def getCount(self):
        return self._count

    def _setPreview(self, s):
        self._preview = s

    def addChildElement(self, childElement):
        self._children.append(childElement)

    def generatePreview(self):
        res = ''
        for child in self.getChildrenElements():
            res += child.getName()
            res += ' '
        #self._setPreview(res)
        return res
            
    def getChildrenElements(self):
        return self._children

    def incCount(self):
        self._count += 1

    def setImp(self, imp):
        self._imp  = imp

    def __str__(self):
        res = 'stylenode:'
        res += self.getPreview()
        res += '['
        for child in self.getChildrenElements():
            res += str(child)
        res += ']'
        return res

class StyleTree:
    def __init__(self):
        self.body = ElementNode()

    def cal(self):
        pass
        



if __name__ == '__main__':
    ele = ElementNode('body')
    p = ElementNode('p')
    b = ElementNode('b')
    stylenode = StyleNode()
    stylenode.addChildElement(p)
    stylenode.addChildElement(b)
    ele.registerStyleNode(stylenode)
    print ele
