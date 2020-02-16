#coding: utf-8
import xml.etree.ElementTree as etree
from epub2html import DisableXmlNamespaces
from pathlib import Path
import re

def _genMemuTree(node,depth=0):
    for cc in node.findall("."):
        name = cc.find("./navLabel/text")
        link = cc.find("./content")
        attrib = link.attrib["src"]
        print(depth, name.text.strip(),attrib)
        yield depth, name.text.strip(),attrib
        
        subs =cc.findall("./navPoint")
        if len(subs)>0:
            for d in subs:
                yield from _genMemuTree(d,depth+1)

def genMemuTree(path):
    contents = Path(path).read_text()
    contents = contents
    print(type(contents))
    contents = re.sub(' xmlns="[^"]+"', '', contents, count=1)
    root = etree.fromstring(contents)
    print(root.tag)
    for c in root.findall("./navMap/navPoint"):
        yield from _genMemuTree(c,0)


def test_xml():
    full = []
    for d,n,s in genMemuTree("./b/toc.ncx"):
        full.append("-"*d+n+"\n")
        

    menu = Path("./new_menu.txt")
    menu.write_text("".join(full))

