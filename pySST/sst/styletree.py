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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from doter import ElementNodeDoter, StyleNodeDoter, DataNodeDoter
import math
def getTag(node):
    end = str(node).index('>')
    res = str(node)[:end+1]
    #print "** getTag: ", res
    return res

#from sourceparser import nodenames 
nodenames = ['a', 'img']
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
        #set DataNode default pos 0
        self._childStyleNodes.append(DataNode())

    def setName(self, name):
        self._name =  str(name)

    def getName(self):
        return self._name

    def getChildStyleNodes(self):
        # maybe should return _childStyleNodes[1:]
        return self._childStyleNodes

    def getDataNode(self):
        #default: the first element is DataNode
        return self._childStyleNodes[0]

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
        #skip DataNode defaut first pos
        for node in self.getChildStyleNodes()[1:]:
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
            if tagname in nodenames: continue
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



from dic.nodedatas import Datas
import numpy as np
#from copy import deepcopy as dc
class DataNode:
    '''
    DataNode is a special StyleNode
    a container for nodes like b p img a and text
    '''
    def __init__(self):
        #print '>> construct DataNode'
        self.doter = DataNodeDoter()
        self.doter.init(self)
        #text content of a tag
        self.type = 'datanode'
        self.setName('datas')
        #data dic
        self.datadic = Datas()
        #data container for each page
        self.pagedatas = []
        self._imp = 0

    def addPage(self, page):
        self.pagedatas.append(page)

    def setName(self, data):
        self._name = str(data)

    def hasData(self):
        return bool(self.datas)

    def getName(self):
        return self._name

    def cal(self):
        pagenum = len(self.pagedatas)
        m = np.size(self.datadic)

        def P(i):
            n = 0
            data_index = self.datadic[i]
            for page in self.pagedatas:
                res = np.where( page == data_index )
                if res[0]:
                    n += 1
            return n / pagenum

        def H(i):
            res = 0
            for i in range(m):
                pi = P(i)
                res -= pi * math.log( m, pi)
            return res

        if m ==1: return 1
        res = sum(
            [H(i) for i in range(m)]
        )
        res = 1 - res / m
        self._imp = res
        return res

    def getImp(self):
        return self._imp

    def _addData(self, data):
        self.datas.append(data)
        self.nums.append(1)

    def _incNum(self, pos):
        self.nums[pos] += 1

    def __str__(self):
        res = ''
        res += self.doter.initDotNode() + '\n'
        self.doter.incIndex()
        return res




class StyleTree:
    def __init__(self):
        self.body = ElementNode('body')
        #num of sitepages
        self.pageNum = 3

    def cal(self):
        print '#'*50 
        print '>>> cal..'
        self.calCompImp(self.body)

    def calNodeImp(self, element):
        '''
        calcuate the node importance
        @ element : ElementNode
        '''
        print '>'*30
        print '>>> calNodeImp'
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
        print '>'*30
        print '>>> calCompImp'
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
        elif node.type == 'datanode':
            res = node.cal()
        node.setImp(res)
        print '>>> imp: ', res
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
    '''
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
    '''
    
    print '-'*50
    print '-'*50
    print '-'*50
    '''
    dn = DataNode()
    print dn.datas
    print dn.nums
    '''





