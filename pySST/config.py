import ConfigParser
import os

class Config:
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        _path = os.path.abspath(__file__)
        _path = os.path.dirname(_path)
        _path = os.path.join(_path+'/', "conf.ini")
        self.config.read(_path)

    def get(self, section, key):
        return self.config.get(section, key)

    def getint(self, section, key):
        return self.config.getint(section, key)

    def getfloat(self, section, key):
        return self.config.getfloat(section, key)

    def getbool(self, section, key):
        return self.config.getbool(section, key)


if __name__ == '__main__':
    config = Config()
    print config.getpath('indexer', 'idxs_num_path')

    
    
