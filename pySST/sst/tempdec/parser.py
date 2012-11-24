import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('../../')
from config import Config

from  sst.sourceparser import Stack
from sst.styletree import StyleNode, getTagName
from sst.sourceparser import nodenames

from pyquery import PyQuery as pq


class Parser:
    def __init__(self, value):
        self.value = value
        self.stack = Stack()
        _config = Config()
        self.pageNum = len(_config.getSourcePaths())

    def setDic(self, dic):
        self.dic = dic

    def setSST(self, sst):
        self.styletree = sst

    def setSource(self, source):
        self.pq = pq(source)
        self.pq.remove('script')
        self.pq.remove('style')

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

    def markNoiseNode(self, fnode, isnoise):
        '''
        mark html node
        '''
        if isnoise:
            try:
                fnode.css('background-color', 'gray')
                #fnode.css('border', '1px solid yellow')
            except:
                print 'mark wrong!!!!'
        else:
            try:
                fnode.css('background-color', 'blue')
                #fnode.css('border', '1px solid red')
            except:
                print 'mark wrong!!!!'

    def parseIter(self):

        def scanDataNode(fnode, element):
            '''
            add datanodes
            first build a data container (DataNode)
            then for each data, create a Data and register in DataNode
            '''
            rank = element.getCompImp()
            self.markNoiseNode(fnode, rank < self.value)
            #print 'addDataNode'
            #children = fnode.children()
            #print 'fnode.children: ', children
            #dics
            #dn = element.getDataNode()
            #self.datatagextractor.setNode(str(fnode))
            #features = self.datatagextractor.getFeatures()
            #for each data add to DataNode
            #dn.addFeatures(features)

        def scanStyleNode(node):
            #print 'addStyleNode(%s)'% node
            #clean node
            childnodes = node.children()
            stylenode = StyleNode(self.dic, self.pageNum)
            assert node != None , "addStyleNode(None)"
            stylenode.generateStyleNode(node)
            print 'find stylenode:', stylenode.generatePreview()
            stylenodes = element.getChildStyleNodes()[1:]
            print '.. start stylenodes list:'
            for node in stylenodes:
                print 'stylenodes: ', node.getPreview()
            print '.. end stylenode list'
            _stylenode = element.findStyleNode(stylenode)

            print 'find _stylenode', _stylenode
            j = -1
            for i in range(len(childnodes)):
                child = childnodes.eq(i)
                tag = getTagName(child)
                #print '** tag:', tag
                if tag not in nodenames:
                    j += 1
                    childnode = _stylenode.getChild(j)
                    self.stack.push([ childnodes.eq(i), childnode ])
                
        while not self.stack.empty():
            (node , element) = self.stack.pop()
            #print '.. stylenode: ', _stylenode
            scanDataNode(node, element)
            scanStyleNode(node)

    def tofile(self, filename):
        open(filename, 'w').write(str(self.pq.html()))
        

