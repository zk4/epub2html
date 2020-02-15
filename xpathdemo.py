
from lxml import etree
from pathlib import Path
contents =Path('./part0000.html').read_text()
contents = contents.encode('utf-8')
dom = etree.HTML(contents)
divs = dom.xpath("./body/div")

def parseDiv(dom,depth=0):
    titles=  dom.xpath("./a/text()")
    if len(titles)>0:
        print(depth* "-",titles[0])

    divs2=  dom.xpath("./div")
    if len(divs2)>0:
        for d in divs2:
            parseDiv(d,depth+1)

for d in divs:
    parseDiv(d)



