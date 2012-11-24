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

sys.path.append('../')
from config import Config

import math

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
    t = re.compile("<[\s]*(\S*)[\s]*[>]*")
    res = t.findall(str(node))
    res = res[0]
    t = []
    t.append(res.find('>'))
    t.append(res.find('/'))
    t = [i for i in t if i>0]
    if t:
        t = min(t)
        res = res[:t]
    if res.find('!--') != -1: return False
    return res

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
    def __init__(self, name, dic, pageNum):
        #print ">>> construct ElementNode: %s" % name
        self._name = name
        self._childStyleNodes = []
        self._count = 1
        self._imp = 0
        self._nodeimp = 0
        self.type = 'elementnode'
        self.doter = ElementNodeDoter()
        self.doter.init(self)
        #set DataNode default pos 0
        _datanode = DataNode(self, dic)
        self._childStyleNodes.append(_datanode)
        self.pageNum = pageNum

        self._is_nodeimp = False
        self._is_comimp = False

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

    def findStyleNode(self, stylenode):
        '''
        only find the stylenode
        '''
        return self._searchStyleNode(stylenode.getPreview())

    def incCount(self):
        '''
        count pages that contain node
        '''
        self._count += 1

    def getCount(self):
        return self._count

    def getP(self):
        return self._count / self.pageNum

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

    def getNodeImp(self):
        '''
        if len(self.getChildStyleNodes()) == 1:
            return 1
        '''
        if self._is_nodeimp:
            return self._nodeimp
        m = self.getCount()
        res = 0
        if m == 1:
            res = 1
        else:
            for stylenode in self.getChildStyleNodes()[1:]:
                pi = stylenode.getCount() / self.getCount()
                res -= pi * math.log(pi, m)
                print '>>> pi: %f' % pi
                print '@'*50
            print 'nodeimp res is: %f' % res
            #res += self.getDataNode().getCompImp()
        self._nodeimp = res
        self._is_nodeimp = True
        return res

    def getCompImp(self):
        r = 0.9
        if self._is_comimp:
            return self._imp
        if len(self.getChildStyleNodes()) == 1:
            self._imp = self.getDataNode().getCompImp()
            self._is_comimp = True
            return self._imp
        #else
        res = 0
        res += (1 - r) * self.getNodeImp()
        tem = 0
        tem += r * sum([
            #pi
            stylenode.getP() * stylenode.getCompImp()
                for stylenode in self.getChildStyleNodes()[1:]
        ])
        tem /= self.pageNum
        res += tem
        self._imp = res
        self._is_comimp = True
        return res


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
    def __init__(self, dic, pageNum):
        #print "construct StyleNode: ",
        self._preview = ''
        self._imp = 0
        self._count = 1
        self._children = []
        self.type = 'stylenode'
        self.doter = StyleNodeDoter()
        self.doter.init(self)
        self.dic = dic
        self.pageNum = pageNum

        self._is_comimp = False

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
            element = ElementNode(self._getTag(childnode), self.dic, self.pageNum)
            #print '.. Element : ',element
            self.addChildElement(element)

    def getPreview(self):
        #return self._preview
        return trim(self.generatePreview())


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

    def getP(self):
        return self._count / self.pageNum

    def getCompImp(self):
        if self._is_comimp:
            return self._imp

        k = len(self._children)
        if not k:
            self._is_comimp = True
            return 9

        res = sum(child.getCompImp() for child in self._children)
        self._imp = res / k
        self._is_comimp = True
        return self._imp
    
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
    def __init__(self, fatherElement, centralDic):
        #print '>> construct DataNode'
        self.doter = DataNodeDoter()
        self.doter.init(self)
        #text content of a tag
        self.type = 'datanode'
        self.setName('datas')
        #data dic
        self.dic = centralDic
        self.datadic = Datas(centralDic)
        #data container for each page
        self.pagedatas = []
        self._imp = 0
        self.fatherElement = fatherElement

        self._is_comimp = False

    def addFeatures(self, features):
        features = [f for f in features]
        self.datadic.addFeatures(features)
        _dic = Datas(self.dic)
        _dic.addFeatures(features)
        #print 'pagedic', _dic.list.datas
        self.pagedatas.append(_dic)

    def setName(self, data):
        self._name = str(data)

    def hasData(self):
        return self.datadic.hasData()

    def getName(self):
        return self._name

    def getP(self):
        '''
        get frequency
        '''
        #return self.fatherElement.getP()
        return 1

    def getCompImp(self):
        if self._is_comimp:
            return self._imp

        m = len(self.pagedatas)
        l = self.datadic.size()
        if not l: 
            self._is_comimp = True
            return 0
        '''
        print '-' * 50
        print 'm: dicsize: ', m
        print 'nodedic: ', self.datadic.list.datas
        print 'pagedatas:'
        '''
        '''
        for p in self.pagedatas:
            print p.list.datas
        '''

        def P(i):
            '''
            print '-' * 50
            print 'P(i): ' + '-'*30
            print 'm: ', m
            '''
            n = 0
            data_index = self.datadic[i]
            print 'data_index: ', data_index

            li = []
            for page in self.pagedatas:
                #print 'find pageindex in page', data_index, page.list.datas
                res = np.where(page.list.datas == data_index )
                #print 'find res:', res
                try:
                    i = res[0][0]
                    li.append(1)
                except:
                    li.append(0)
                    pass
            n = sum(li)
            if not n: n=1
            print 'n, m : %d, %d' %  (n, m)
            return [i/n for i in li]

        def H(i):
            if m == 1: return 0
            res = 0
            for p in P(i):
                if not p: continue
                res -= p * math.log(p, m)
            return res

        if m ==1: 
            self._is_comimp = True
            return 1
        res = sum(
            [H(i) for i in range(l)]
        )
        #res = 1 - res / l
        res = 1 - res/l
        self._imp = res
        print 'H(i): ', self._imp
        self._is_comimp = True
        return res

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
    def __init__(self, dic):
        _config = Config()
        self.pageNum = len(_config.getSourcePaths())
        self.body = ElementNode('body', dic, self.pageNum)

    def cal(self):
        #print '#'*50 
        #print '>>> cal..'
        self.calCompImp(self.body)

    def calNodeImp(self, element):
        '''
        calcuate the node importance
        @ element : ElementNode
        '''
        #print '>'*30
        #print '>>> calNodeImp'
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
                res -= pi * math.log(pi, m)
        element.setImp(res)
        return res

    def calCompImp(self, node):
        '''
        calculate the composite importance
        @ node : StyleNode or ElementNode
        '''
        print '>'*30
        print '>>> calCompImp'
        self.body.getCompImp()

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





