#coding: utf-8
from lxml import etree
from pathlib import Path

def parseDiv(dom,depth=0):
    titles=  dom.xpath("./a/text()")
    if len(titles)>0:
        print(depth* "-",titles[0])

    divs2=  dom.xpath("./div")
    if len(divs2)>0:
        for d in divs2:
            parseDiv(d,depth+1)

def genMenu(filepath):

    contents =Path(filepath).read_text()
    contents = contents.encode('utf-8')
    dom = etree.HTML(contents)
    divs = dom.xpath("./body/div")
    for d in divs:
        parseDiv(d)


def shrinkImg():
    pass


def filterContent():
    pass


def embedContent():
    pass


if __name__ == "__main__":
    genMenu("./test.html")
