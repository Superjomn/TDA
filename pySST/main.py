import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from sst.dic.dic import Dic
from sst.datatagextractor import FeatureExtrator
from config import Config
from pyquery import PyQuery as pq

open('status.log', 'w').write(' ')
ci = open('status.log', 'w')

class CentreDicBuilder:
    def __init__(self):
        self.dic = Dic()
        self.feature_extrator = FeatureExtrator()
        self.config = Config()

    def buildPath(self):
        basepath = self.config.get('path', 'source')
        return [basepath + path for path in os.listdir(basepath)]

    def run(self):
        #log
        open('CentreDicBuilder.log', 'w').write(' ')
        fi = open('CentreDicBuilder.log', 'a')
        ci.write( 'CentreDicBuilder:!!!' + '-'*30 )
        for path in self.buildPath():
            ci.write(path + '\n') 
            c = open(path).read()
            self.feature_extrator.setSource(c)
            features = self.feature_extrator.getFeatures()
            for f in features:
                #print f
                self.dic.add(f)
                fi.write(f + '\n')
        self.dic.done()
        self._tofile()
        ci.write( 'CentreDicBuilder:!!!' + '-'*30 )
        fi.close()

    def _tofile(self, filename='features.dic'):
        self.dic.tofile(filename)
    
def createCentreDic():
    cdic = CentreDicBuilder()
    cdic.run()

from sst.sourceparser import SourceParser

def createStyletree(ci):  
    ci.write('-' * 30)
    ci.write('createCentreDic!!!' + '\n')
    #dic
    dic = Dic()
    dic.fromfile()

    sourceparser = SourceParser(dic)
    centre = CentreDicBuilder()
    paths = centre.buildPath()
    for path in paths:
        ci.write(path + '\n')
        c = open(path).read()
        sourceparser.setSource(c)
        sourceparser.parse()
    sourceparser.styletree.cal()
    res = sourceparser.styletree.show()
    ci.write('-' * 30)
    return (dic, sourceparser.styletree)

from sst.tempdec.parser import Parser
def markNoise(sst, ci):
    values = [0.33, 0.2, 0.4, 0.1]
    for value in values:
        #create path
        try:
            os.mkdir('resource/%f' % value)
        except:
            print 'wrong make dir'
        ci.write('-' * 30)
        ci.write('markNoise!!!' + '\n')
        p = Parser(value)
        p.setDic(sst[0])
        p.setSST(sst[1])
        centre = CentreDicBuilder()
        paths = centre.buildPath()
        for i,path in enumerate(paths):
            ci.write(path + '\n')
            c = open(path).read()
            p.setSource(c)
            p.parse()
            print 'parse Wrong!!!!'
            p.tofile('resource/%f/%d' % (value,i))

createCentreDic()
sst = createStyletree(ci)
markNoise(sst,ci)

    
    
