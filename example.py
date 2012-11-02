import sys,BodyTextExtractor
from Cleaner import Cleaner

# Usage: python example.py html_file
filename = sys.argv[1]
html = open(filename).read()
cleaner = Cleaner()
cleaner.init(html)
cleaner.clean()
html = cleaner.toString()
open(filename+'.clean', 'w').write(html)


p = BodyTextExtractor.HtmlBodyTextExtractor()
p.feed(html)
p.close()
x = p.body_text()
s = p.summary()
t = p.full_text()
#print "\n\nSummary:\n",s
print "\nBodytext:\n",x
#print "\nFulltext:\n",t
