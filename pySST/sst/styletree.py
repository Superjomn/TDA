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
from doter import ElementNodeDoter, StyleNodeDoter, DataNodeDoter
import math
def getTag(node):
    end = str(node).index('>')
    res = str(node)[:end+1]
    #print "** getTag: ", res
    return res


datanodenames = ['a', 'p', 'b',]
#help to generate a unique name for each node
print_index = 0

def trim(text):
    return text.lstrip().rstrip()

import re
def getTagName(node):
    t = re.compile("^<[\s]*(\S*)[\s>]")
    res = t.findall(str(node))[0]
    if res: return res
    return False

from lxml import etree
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
        #print ">>> construct ElementNode: %s" % name
        self._name = name
        self._childStyleNodes = []
        self._count = 1
        self._imp = 0
        self.type = 'elementnode'
        self.doter = ElementNodeDoter()
        self.doter.init(self)

    def setName(self, name):
        self._name =  str(name)

    def getName(self):
        return self._name

    def getChildStyleNodes(self):
        return self._childStyleNodes

    def getImp(self):
        return self._imp

    def setImp(self, imp):
        self._imp = imp

    def addDataNode(self, node):
        '''
        add text img a p b 
        '''
        nodenames = [
            'img', 'IMG', 'P', 'p', 'b', 'B', ]
        datanode = DataNode()
        #use lxml to parse html and get text data
        root = etree.XML( str(node))
        tagname = root.tag
        if tagname in nodenames:
            datanode.setTagNode(node)
            self.addChildStyleNode(datanode)
        elif datanode.setTextNode(node):
            self.addChildStyleNode(datanode)
        
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
        if not trim(stylenode.getPreview()):
            return
        node = self._searchStyleNode(stylenode.getPreview())
        if node:
            node.incCount()
            #print '.. return node ', node
            return node
        else:
            self.addChildStyleNode(stylenode)
            #print '.. return stylenode ', 
            #print str(stylenode)
            return stylenode

    def __str__(self):
        '''
        use dot to generate structure
        '''
        #create dot node 
        res = ''
        res += self.doter.initDotNode() + '\n'
        for i,e in enumerate(self.getChildStyleNodes()):
            e.doter.initIndex(self.doter.index+i)
            res += '%s -- %s;\n' % (
                self.doter.getDotNode(),
                e.doter.getDotNode() 
            )
            res += str(e)
        #self.doter.incIndex()
        return res

class StyleNode:
    def __init__(self):
        #print "construct StyleNode: ",
        self._preview = ''
        self._imp = 0
        self._count = 1
        self._children = []
        self.type = 'stylenode'
        self.doter = StyleNodeDoter()
        self.doter.init(self)

    def generateStyleNode(self, node):
        '''
        @node : PyQuery
        '''
        childnodes = node.children()
        for i in range(len(childnodes)):
            childnode = childnodes.eq(i)
            #skip data nodes
            tagname = getTagName(childnode)
            if tagname in datanodenames: continue
            #generate ...
            element = ElementNode(self._getTag(childnode))
            #print '.. Element : ',element
            self.addChildElement(element)

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

    def getChild(self, i):
        return self._children[i]

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
        res = ''
        res += self.doter.initDotNode() + '\n'
        for i,e in enumerate(self.getChildrenElements()):
            e.doter.initIndex(self.doter.index)
            e.doter.incIndex()
            res += '%s -- %s;\n' % (
                self.doter.getDotNode(),
                e.doter.getDotNode() 
            )
            res += str(e)
        self.doter.incIndex()
        return res

    def _getTag(self, node):
        end = str(node).index('>')
        res = str(node)[:end+1]
        #print "** tag: ", res
        return res

#from copy import deepcopy as dc
class DataNode(StyleNode):
    '''
    DataNode is a special StyleNode
    for nodes like b p img a
    '''
    def __init__(self, data = ''):
        #print '>> construct DataNode'
        StyleNode.__init__(self)
        self.doter = DataNodeDoter()
        self.doter.init(self)
        #text content of a tag
        self._nodedata = ''

    def setName(self, data):
        self._name = str(data)

    def getName(self):
        return self._name

    def getPreview(self):
        return self._name

    def setData(self, data):
        if data:
            res = hash(data)
            #res = data
            self.setName(res)
            return True
        return False

    def __str__(self):
        res = ''
        res += self.doter.initDotNode() + '\n'
        self.doter.incIndex()
        return res

class StyleTree:
    def __init__(self):
        self.body = ElementNode('body')
        #num of sitepages
        self.pageNum = 0

    def calNodeImp(self, element):
        '''
        calcuate the node importance
        @ element : ElementNode
        '''
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
        '''
        calculate the composite importance
        @ node : StyleNode or ElementNode
        '''
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

    def show(self):
        '''
        show structure
        '''
        res = str(self.body)
        #print res
        self.body.doter.initIndex(0)
        self.body.doter.toFile(strr=res)
        return res

if __name__ == '__main__':
    body = ElementNode('body')
    stylenode = StyleNode()
    p = ElementNode('p')
    b = ElementNode('b')
    stylenode.addChildElement(p)
    stylenode.addChildElement(b)
    print stylenode
    body.registerStyleNode(stylenode)
    q = ElementNode('q')
    c = ElementNode('c')
    stylenode2 = StyleNode()
    stylenode2.addChildElement(q)
    stylenode2.addChildElement(c)
    b.registerStyleNode(stylenode2)
    print 'body', body
