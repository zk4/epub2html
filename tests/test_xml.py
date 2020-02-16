#coding: utf-8
import xml.etree.ElementTree as etree
from pathlib import Path
import re

def _genMemuTree(node,ulist,depth=0):
    for cc in node.findall("."):
        name = cc.find("./navLabel/text").text.strip()
        link = cc.find("./content")
        attrib = link.attrib["src"]
        print(depth, name,attrib)
        ulist.append(f"<li><a href=\"{attrib}\">{name}</a></li>")
        yield depth, name,attrib
        
        subs =cc.findall("./navPoint")
        if len(subs)>0:
            for d in subs:
                ulist.append("<ul>")
                yield from _genMemuTree(d,ulist,depth+1)
                ulist.append("</ul>")
def genMemuTree(path):
    contents = Path(path).read_text()
    contents = contents
    print(type(contents))
    contents = re.sub(' xmlns="[^"]+"', '', contents, count=1)
    root = etree.fromstring(contents)
    print(root.tag)
    ulist =[]
    ulist.append("<ul class=\"nav nav-sidebar \">")
    for c in root.findall("./navMap/navPoint"):
        yield from _genMemuTree(c,ulist,0)
    ulist.append("</ul>")
    print("\n".join(ulist))
    diskulist = Path("ullist.html")
    diskulist.write_text("\n".join(ulist))


# <ul class="nav nav-sidebar noSelect">
# <li id="__origin" url="4,5,6"><a>item2</a></li>
# <ul>
#     <li id="__origin" url="4,5,6"><a>item2</a></li>
#     <li id="__origin" url="4,5,6"><a>item2</a></li>
#     <li id="__origin" url="4,5,6"><a>item2</a></li>
# </ul>
# </ul>

def test_xml():
    li ="""<li><a href="$hash$">$name$</a></li>"""
    sub=f"""<ul>
            $li$ 
    </ul>"""

    full = []

    od = -99

    for d,n,s in genMemuTree("./b/toc.ncx"):
        # same level 
        if d == od:
            pass
        else:
            pass



            


        full.append("-"*d+n+"\n")

    menu = Path("./new_menu.txt")
    menu.write_text("".join(full))

