#coding: utf-8

import argparse
from lxml import etree
import xmltodict
from pathlib import Path
import re
import zipfile
import os
import sys
import html
from os.path import dirname,basename,join
import html.parser as htmlparser
parser = htmlparser.HTMLParser()

class Epub2Html(): 
    def __init__(self,epubpath,outputdir):
        self.epubpath = epubpath 

        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(script_dir,"template.html")

        self.template =Path(template_path).read_text()
        (only_name,_)=  os.path.splitext(basename(self.epubpath))
        self.only_name = only_name

        self.filedir = join(dirname(self.epubpath),only_name)
        self.absfiledir = os.path.abspath(self.filedir)
        self.outputdir =outputdir
        self.textdir = os.path.join(outputdir,only_name ,"text")

    
    def _genMemuTree(self,node,need_hash_names,ulist,depth=0):
        for cc in node.findall("."):
            name = cc.find("./navLabel/text").text.strip()
            link = cc.find("./content")
            attrib = link.attrib["src"]
            # only page link, no hash jump
            if '#' not in attrib:
                short_link = attrib.split('/')[-1]
                attrib = "#"+self.hash(short_link)
                need_hash_names.append(short_link)
            else:
                attrib=re.sub(r"text\/part\w+\.html","index.html",attrib)

            ulist.append(f"<li><a href=\"{attrib}\">{name}</a></li>")

            subs =cc.findall("./navPoint")
            if len(subs)>0:
                for d in subs:
                    ulist.append("<ul>")
                    self._genMemuTree(d,need_hash_names,ulist,depth+1)
                    ulist.append("</ul>")

    def genMemuTree(self,path):
        contents = Path(path).read_text()
        contents = contents
        contents = re.sub(' xmlns="[^"]+"', '', contents, count=1)
        contents = contents.encode('utf-8')
        root = etree.fromstring(contents)
        ulist =[]
        need_hash_names = []
        ulist.append("<ul class=\"nav nav-sidebar \">")
        for c in root.findall("./navMap/navPoint"):
            self._genMemuTree(c,need_hash_names,ulist,0)
        ulist.append("</ul>")
        return "\n".join(ulist),need_hash_names

    def unzip(self):
        with zipfile.ZipFile(self.epubpath,'r') as zip_ref:
            zip_ref.extractall(os.path.join(self.outputdir,f"{self.only_name}"))



    def genContent(self,hash_files):
        content_list = []
        print("self.textdir",self.textdir)
        for only_name in  self.traverse(self.textdir):
            if only_name in  ["part0000.html","part0001.html"]:
                continue

            full_path = os.path.join(self.textdir,only_name)
            raw_content = Path(full_path).read_text()


            raw_content = raw_content.encode('utf-8')
            raw_content_dom = etree.HTML(raw_content)
            raw_content = etree.tostring(raw_content_dom.xpath("//body")[0],method='html').decode('utf-8')
            raw_content = self.washBody(raw_content)

            # debug
            # if only_name in  ["part0004_split_001.html"]:
            #     print(parser.unescape(raw_content))

            # ad slef generated hash
            short_link = os.path.basename(full_path)
            if short_link in hash_files:
                anhor = f"<div id=\"{self.hash(short_link)}\"></div>"
                content_list.append(anhor)

            # content_list.append(parser.unescape(raw_content))
            content_list.append(raw_content)

        full_content = "".join(content_list)
        full_content = self.washImageLink(full_content)
        return full_content

    def washBody(self,sub_content):
        tmp = sub_content.replace("<body","<div")
        tmp = tmp.replace("</body>","</div>")
        return tmp

    def washImageLink(self,full_content):
        return re.sub(r"\.\.\/images","./images",full_content)
        
    def traverse(self,rootdir):
        for cdirname, _, filenames in os.walk(rootdir):
            if rootdir ==  cdirname:
                return filenames 
    def hash(self, s):
        import base64
        tag = base64.b64encode(s.encode('ascii'))
        tag = tag.decode("ascii")
        return tag

    def genMenu(self,menuhtmlname):
        raw_menu =Path(join(self.textdir,menuhtmlname)).read_text()
        raw_menu = raw_menu.encode('utf-8')
        raw_menu_dom = etree.HTML(raw_menu)
        parts = raw_menu_dom.xpath("//body/*")
        raw_menus = []
        need_hash_names = []
        for p in parts:
            raw_menu = etree.tostring(p,method='html').decode('utf-8')
            # only page link, no hash jump
            a = re.search("\"part\d+.html\"",raw_menu)
            if a:
                need_hash_names.append(a.group())
                raw_menu = re.sub("(part\d+.html)","#"+self.hash(a.group()),raw_menu)
            else:
                raw_menu=re.sub(r"part\w+\.html","",raw_menu)
            
            raw_menus.append(raw_menu) 
        return "".join(raw_menus),need_hash_names

    
    def gen(self):
        self.unzip()
        menu, hash_files= self.genMemuTree(os.path.join(self.filedir,"toc.ncx"))

        full_content = self.genContent(hash_files)

        self.template = self.template.replace("${menu}$",menu)
        self.template = self.template.replace("${content}$",full_content)
        Path(join(self.outputdir, self.only_name,"./index.html")).write_text(self.template)
        self.copyJs()

    def copyJs(self):
        import shutil
        dest = join(self.outputdir, self.only_name,"./jquery.min.js")
        print("dest:",dest)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        jquery_path = os.path.join(script_dir,"jquery.min.js")
        shutil.copy(jquery_path,dest)


def main(args):
    filepath = args.filepath
    if filepath[0]!="." and filepath[0]!="/":
        filepath= "./"+filepath
    filepath = os.path.abspath(filepath)
    outputdir = os.path.abspath(args.outputdir)

    e = Epub2Html(filepath,outputdir)
    e.gen()

def entry_point():
    parser = createParse()
    mainArgs=parser.parse_args()
    main(mainArgs)


def createParse():
    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="")
    parser.add_argument("filepath",  help="filepath" )
    parser.add_argument("outputdir",  help="outputdir" )
    return parser
