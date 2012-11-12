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

class StyleTree:
    def __init__(self):
        self.nodelist = Nodelist()
        self.stack = Stack()

    def registerChildTag(self, hash_tag, index_father):
        '''
         * given father node, if find the matching child, then add it's count
         * if cannot find the matching one, then create a new child.
        '''
        lastBrother = None
        child = None
        if child == self.searchChild(hash_tag, index_father, lastBrother):
            self.nodelist[child].count += 1
        else:
            self.addChildTag(hash_tag, index_father, lastBrother)
    
    def searchChild(self, hash_child, index_father, list_lastBrother):
        child = None
        brother = None
        child = self.nodelist[index_father].child
        if child == 0:
            return False
        else:
            if not self.nodelist[child].hash == hash_child:
                brother = self.nodelist[child].brother
            while brother != 0:
                if self.nodelist[brother].hash == hash_child:
                    child = brother
                list_lastBrother[0] = brother
                brother = self.nodelist[brother].brother
        return child
    
    def addChildTag(self, hash_data, index_father, index_lastBrother):
        node = Node()
        node.hash = hash_data
        node.brother = index_lastBrother
        self.nodelist.append(node)
        self.nodelist[index_father].child = len(self.nodelist) - 1


