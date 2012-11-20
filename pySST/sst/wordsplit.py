#encoding=utf-8
import sys
sys.path.append("../")
import jieba

default_encoding='utf-8'

def split(data):
    return jieba.cut(data)

