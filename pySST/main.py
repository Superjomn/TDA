import os
from sst.dic.dic import Dic
from sst.datatagextractor import FeatureExtrator
from sst.wordsplit import split
from config import Config

class CentreDicBuilder:
    def __init__(self):
        self.dic = Dic()
        self.feature_extrator = FeatureExtrator()
        self.config = Config()

    def _buildPath(self):
        basepath = self.config.get('path', 'source')
        return os.listdir(basepath)

    def run(self):
        for path in self._buildPath():
            self.feature_extrator.fromfile(path)
            features = self.feature_extrator.getFeatures()
            for f in features:
                self.dic.add(f)
        self.dic.done()
        self._tofile()

    def _tofile(self, filename='features.dic'):
        self.dic.tofile(filename)
    
def createCentreDic():
    cdic = CentreDicBuilder()
    cdic.run()


createCentreDic()

    
    
