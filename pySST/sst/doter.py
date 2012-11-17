#to generate unique name for each node
index = 0

class Doter:
    '''
    to generate dot file for dot
    '''
    def __init__(self):
        self.node = None

    def init(self, node):
        self.node = node

    def initDotNode(self):
        return '%s [label="%s"]' % (
            self.getDotNode(),
            self.get_name()
        )

    def getDotNode(self):
        name = self.get_name()
        node =  "%s_%d" % (name , index)
        return str(hash(node))

    def incIndex(self):
        global index
        index += 1

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


