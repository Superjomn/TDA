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
#from type import Node
import math

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
        self._count = 1
        self._imp = 0
        self.type = 'elementnode'

    def getName(self):
        return self._name

    def getChildStyleNodes(self):
        return self._childStyleNodes

    def getImp(self):
        return self._imp

    def setImp(self, imp):
        self._imp = imp
        
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

    def incCount(self):
        '''
        count pages that contain node
        '''
        self._count += 1

    def getCount(self):
        return self._count

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
        self.type = 'stylenode'

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
        for element in self.getChildrenElements():
            element.incCount()

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
        #num of sitepages
        self.pageNum = 0

    def calNodeImp(self, element):
        if element.getImp():
            return element.getImp()
        #else
        res = 0
        m = element.getCount()
        if m == 1:
            res = 1
        else:
            for stylenode in element.getChildStyleNodes():
                pi = stylenode.getCount() / self.pageNum
                res -= pi * math.log(m, pi)
        element.setImp(res)
        return res

    def calCompImp(self, node):
        r = 0.1
        if node.getImp():
            return node.getImp()
        #else
        res = 0
        if node.type == 'elementnode':
            res += (1 - r) * self.calNodeImp(node)
            tem = 0
            for stylenode in node.getChildStyleNodes():
                pi = stylenode.getCount() / self.pageNum
                tem += pi * self.calCompImp(stylenode)
            res += r * tem
        elif node.type == 'stylenode':
            children = node.getChildrenElements()
            k = len(children)
            for element in children:
                res += self.calCompImp(element)
            res /= k
        node.setImp(res)
        return res

if __name__ == '__main__':
    ele = ElementNode('body')
    p = ElementNode('p')
    b = ElementNode('b')
    stylenode = StyleNode()
    stylenode.addChildElement(p)
    stylenode.addChildElement(b)
    ele.registerStyleNode(stylenode)
    print ele
