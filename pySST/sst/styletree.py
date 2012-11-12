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

class Nodelist:
    def __init__(self):
        self.datas = []
    def push(self, node):
        self.datas.append(node)
    def size(self):
        return len(self.datas)
    def latestIndex(self):
        return self.size() - 1

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

class _Tag:
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
    def __init__(self):
        self._datas = []
        #attributes
        tagname = ''
        childtags = []
        count = 1
        imp = 0
        #init
        self._datas.append(tagname)
        self._datas.append(childtags)
        self._datas.append(count)
        self._datas.append(imp)

    def getTagname(self):
        return self._datas[0]

    def getChildTags(self):
        return self._datas[1]

    def getCount(self):
        return self._datas[2]

    def getImp(self):
        return self._datas[3]

    def setTagname(self, name):
        self._datas[0] = name

    def addChildTag(self, childtag):
        '''
        @childtag : Tag
        '''
        self.getChildTags().append(childtag)

    def incCount(self):
        self._datas[2] += 1

    def setImp(self, imp):
        self._datas[3] = imp

    def __str__(self):
        res = '(tagname: ' + str(self.getTagname())
        res += ' count: ' + str(self.getCount()) + '\n'
        res += '['
        for child in self.getChildTags():
            res += str(child)
        res += '])'
        return res
        
class Tag(_Tag):
    def __init__(self):
        _Tag.__init__(self)

    def _searchChilds(self, tagname):
        for childtag in self.getChildTags():
            if childtag.getTagname() == tagname:
                return childtag
        return False

    def registerChild(self, tagname):
        child = self._searchChilds(tagname)
        if child:
            child.incCount()
        else:
            child = Tag()
            child.setTagname(tagname)
            self.addChildTag(child)
        return child


if __name__ == '__main__':
    tag = Tag()
    tag.setTagname('body')
    p = tag.registerChild('p')
    tag.registerChild('p')
    tag.registerChild('b')
    p.registerChild('table')
    print tag
