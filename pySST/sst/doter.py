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
        self.index += 1

    def get_name(self):
        return "hello"

    def toFile(self, filename='tem.dot', strr=''):
        res = 'graph graphname {\n'
        res += strr 
        res += '}\n'
        open(filename, 'w').write(res)

class ElementNodeDoter(Doter):
    def __init__(self):
        Doter.__init__(self)

    def get_name(self):
        res = self.node.getName()
        return res.replace('"', "'")

class StyleNodeDoter(Doter):
    def __init__(self):
        Doter.__init__(self)

    def initDotNode(self):
        return '%s [label="%s", shape=box]' % (
            self.getDotNode(),
            self.get_name()
        )

    def get_name(self):
        res = self.node.getPreview()
        return res.replace('"', "'")

class DataNodeDoter(Doter):
    def __init__(self):
        Doter.__init__(self)

    def get_name(self):
        res = self.node.getName()
        return res.replace('"', "'")
        

    
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


