#coding: utf-8
import argparse
from lxml import etree
from pathlib import Path
import re
import zipfile
import os
import sys
import html
from os.path import dirname,basename,join

class Epub2Html(): 
    def __init__(self,epubpath,outputdir):
        self.epubpath = epubpath 

        script_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(script_dir,"template.html")

        self.template =Path(template_path).read_text()
        (only_name,ext)=  os.path.splitext(basename(self.epubpath))
        self.only_name = only_name

        self.filedir = join(dirname(self.epubpath),only_name)
        self.absfiledir = os.path.abspath(self.filedir)
        self.outputdir =outputdir
        self.textdir = os.path.join(outputdir,only_name ,"text")

    
    def parseDiv(self,dom,depth=0):
        titles=  dom.xpath("./a/text()")
        if len(titles)>0:
            print(depth* "---",titles[0])

        divs2=  dom.xpath("./div")
        if len(divs2)>0:
            for d in divs2:
                self.parseDiv(d,depth+1)

    def genMenuTree(self,filepath):
        contents =Path(filepath).read_text()
        contents = contents.encode('utf-8')
        dom = etree.HTML(contents)
        divs = dom.xpath("./body/div")
        for d in divs:
            self.parseDiv(d)

    def unzip(self):

        with zipfile.ZipFile(self.epubpath,'r') as zip_ref:
            zip_ref.extractall(os.path.join(self.outputdir,f"{self.only_name}"))


    def genContent(self):
        content_list = []
        print("self.textdir",self.textdir)
        for text in  self.traverse(self.textdir):
            if text in  ["part0000.html"]:
                continue
            text = os.path.join(self.textdir,text)
            print(text)
            raw_menu = Path(text).read_text()
            raw_menu = raw_menu.encode('utf-8')
            raw_menu_dom = etree.HTML(raw_menu)
            # parts = raw_menu_dom.xpath("//body")[0]
            # for p in parts:
            raw_menu = etree.tostring(raw_menu_dom.xpath("//body")[0],pretty_print=True).decode('utf-8')
            content_list.append(raw_menu)

        full_content = "".join(content_list)
        full_content=re.sub(r"\.\.\/images","./images",full_content)
        return full_content
        
    def traverse(self,rootdir):
        for cdirname, dirnames, filenames in os.walk(rootdir):
            if rootdir ==  cdirname:
                return filenames 


    def genMenu(self,menuhtmlname):
        # self.genMenuTree("./a/text/part0000.html")
        raw_menu =Path(join(self.textdir,menuhtmlname)).read_text()
        raw_menu = raw_menu.encode('utf-8')
        raw_menu_dom = etree.HTML(raw_menu)
        parts = raw_menu_dom.xpath("//body/*")
        raw_menus = []
        for p in parts:
            raw_menu = etree.tostring(p,pretty_print=True).decode('utf-8')
            raw_menus.append(raw_menu)
        raw_menus = "".join(raw_menus)
        raw_menu=re.sub(r"part\w+\.html","",raw_menus)
        return raw_menu

    
    def gen(self):
        self.unzip()
        full_content = self.genContent()
        menu = self.genMenu("part0000.html")
        menu =menu + self.genMenu("part0001.html")
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
