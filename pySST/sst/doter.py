import random
#to generate unique name for each node
class Doter:
    '''
    to generate dot file for dot
    '''
    def __init__(self):
        self.node = None
        self.index = 0

    def init(self, node):
        self.node = node

    def initIndex(self, index):
        self.index = index

    def initDotNode(self):
        return '%s [label="%s"]' % (
            self.getDotNode(),
            self.get_name()
        )

    def getDotNode(self):
        name = self.get_name()
        node =  "%s_%d" % (name , self.index)
        return str(hash(node))

    def incIndex(self):
        self.index += random.randint(1, 100000)

    def get_name(self):
        return "hello"

    def toFile(self, filename='tem.dot', strr=''):
        res = 'graph graphname {\n'
        res += 'graph [ dpi = 300 ];\n' 
        res += strr 
        res += '}\n'
        open(filename, 'w').write(res)

class ElementNodeDoter(Doter):
    def __init__(self):
        Doter.__init__(self)

    def get_name(self):
        res = self.node.getName()
        res = res.replace('"', "'")
        res += '{%f}' % self.node.getP()
        res += ' child_len: %d' % len(self.node.getChildStyleNodes())
        res += '[%f-%f]' % (self.node.getNodeImp(),self.node.getCompImp())
        return res

class StyleNodeDoter(Doter):
    def __init__(self):
        Doter.__init__(self)

    def initDotNode(self):
        return '%s [label="%s", shape=box, style=filled, color=lightblue]' % (
            self.getDotNode(),
            self.get_name()
        )

    def get_name(self):
        res = self.node.getPreview()
        res = res.replace('"', "'")
        res += "_%d" % self.node.getCount()
        res += "_%f" % self.node.getP()
        res += '[%f]' % self.node.getCompImp()
        return res

class DataNodeDoter(Doter):
    def __init__(self):
        Doter.__init__(self)

    def initDotNode(self):
        return '%s [label="%s",style=filled, color=".7 .3 1.0"]' % (
            self.getDotNode(),
            self.get_name()
        )

    def get_name(self):
        res = self.node.getName()
        res = res.replace('"', "'")
        res += '{%d}' % self.node.datadic.size()
        res += '[%f]' % self.node.getCompImp()
        '''
        tem = ''
        for s in self.node.pagedatas:
            tem += str(s)
        res += 'L:%s' % tem +  str(self.node.datadic)
        '''
        return res
        
    
if __name__ == '__main__':
    doter = Doter()
    print doter.initDotNode()
    print doter.getDotNode()
    from styletree import ElementNode
    e = ElementNode('<body>')
    edoter = ElementNodeDoter()
    edoter.init(e)
    print edoter.getDotNode()
    print edoter.initDotNode()


