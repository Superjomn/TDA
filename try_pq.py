from pyquery import PyQuery as pq
import  chardet as cd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

f = open('./sina.html')
c = f.read()
f.close()

root = pq(c)
root('script').remove()
root('style').remove()
ss = root.html()
f = open('./sina.clean.html', 'w')
f.write(ss)
f.close()



