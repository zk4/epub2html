#coding: utf-8
from lxml import etree
from pathlib import Path
import zipfile

def parseDiv(dom,depth=0):
    titles=  dom.xpath("./a/text()")
    if len(titles)>0:
        print(depth* "---",titles[0])

    divs2=  dom.xpath("./div")
    if len(divs2)>0:
        for d in divs2:
            parseDiv(d,depth+1)

def genMenuTree(filepath):
    contents =Path(filepath).read_text()
    contents = contents.encode('utf-8')
    dom = etree.HTML(contents)
    divs = dom.xpath("./body/div")
    for d in divs:
        parseDiv(d)

def unzipFile(filepath):
    tokens =filepath.split(".")
    only_name = filepath+".unzip"
    if len(tokens)>0:
        only_name= tokens[-2] 
    else:
        print("can`t extract name!")


    with zipfile.ZipFile(filepath,'r') as zip_ref:
        zip_ref.extractall(f"./{only_name}")

def shrinkImg():
    pass


def filterContent():
    pass


def embedContent():
    pass


if __name__ == "__main__":
    unzipFile("./a.epub")

    genMenuTree("./a/text/part0000.html")

