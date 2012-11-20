import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
from sst.dic.dic import Dic
from sst.datatagextractor import FeatureExtrator
from config import Config
from pyquery import PyQuery as pq

class CentreDicBuilder:
    def __init__(self):
        self.dic = Dic()
        self.feature_extrator = FeatureExtrator()
        self.config = Config()

    def buildPath(self):
        basepath = self.config.get('path', 'source')
        for path in os.listdir(basepath):
            yield basepath + path

    def run(self):
        fi = open('CentreDicBuilder.log', 'a')
        for path in self.buildPath():
            c = open(path).read()
            self.feature_extrator.setSource(c)
            features = self.feature_extrator.getFeatures()
            for f in features:
                print f
                self.dic.add(f)
                fi.write(f + '\n')
        self.dic.done()
        self._tofile()
        fi.close()

    def _tofile(self, filename='features.dic'):
        self.dic.tofile(filename)
    
def createCentreDic():
    cdic = CentreDicBuilder()
    cdic.run()

from sst.sourceparser import SourceParser

def createStyletree():
    sourceparser = SourceParser()
    centre = CentreDicBuilder()
    for path in centre.buildPath():
        c = open(path).read()
        sourceparser.setSource(c)
        sourceparser.parse()
    #sourceparser.styletree.cal()
    res = sourceparser.styletree.show()

#createCentreDic()
createStyletree()

    
    