#coding: utf-8

import argparse
from lxml import etree
import xmltodict
from pathlib import Path
import re
import zipfile
import subprocess
import os
import tempfile
import sys
import shutil
import html
from os.path import dirname,basename,join
import html.parser as htmlparser
parser = htmlparser.HTMLParser()

class Epub2Html(): 
    def __init__(self,epubpath,outputdir):
        self.epubpath = epubpath 

        script_dir    = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(script_dir,"template.html")

        self.template              = Path(template_path).read_text()
        (epub_name_without_ext,_)  = os.path.splitext(basename(self.epubpath))
        self.epub_name_without_ext = epub_name_without_ext
        self.outputdir             = outputdir
        self.root_a_path           = os.path.join(outputdir,epub_name_without_ext)

        self.unzip()

        opf_r_root_path   = self.get_opf_r_root_path()
        self.index_a_path = os.path.join(self.root_a_path,"index.html")
        self.opf_a_path   = join(self.root_a_path,opf_r_root_path)
        self.opf_a_dir    = dirname(join(self.root_a_path,opf_r_root_path))

        self.image_r_opf_path, self.text_r_opf_path ,self.ncx_r_opf_path = self.paths_from_opf()

        self.text_a_path = os.path.join(self.opf_a_dir, self.text_r_opf_path)

        print("self.image_r_opf_path:",
                self.image_r_opf_path,
                "\nself.text_r_opf_path:",
                self.text_r_opf_path,
                "\nself.ncx_r_opf_path:",
                self.ncx_r_opf_path) 


    def get_opf_r_root_path(self):
        meta_a_path= (os.path.join(self.root_a_path,"META-INF/container.xml"))
        contents = Path(meta_a_path).read_text()
        contents = re.sub(' xmlns="[^"]+"', '', contents, count=1)
        
        contents = contents.encode('utf-8')
        root = etree.fromstring(contents)
        for item in root.findall(".//rootfiles/"):
            return item.attrib["full-path"]

    def read_xml(self,path):
        pass

    def paths_from_opf(self):
        opf_a_path               = self.opf_a_path
        image_r_opf_path         = None
        text_r_opf_path          = None
        ncx_path_relative_to_opf = None
        css_path_relative_to_opf = None
        contents                 = Path(opf_a_path).read_text()

        contents = re.sub(' xmlns="[^"]+"', '', contents, count=1)
        contents = contents.encode('utf-8')

        root = etree.fromstring(contents)
        for item in root.findall(".//manifest/"):

            href = item.attrib["href"]

            if image_r_opf_path == None \
            and re.search('image', href, re.IGNORECASE):
                image_r_opf_path = os.path.dirname(href)

            if text_r_opf_path == None \
            and re.search('text', href, re.IGNORECASE):
                text_r_opf_path = os.path.dirname(href)

            if "ncx" in item.attrib["media-type"]:
                ncx_path_relative_to_opf = href

            if "css" in item.attrib["media-type"]:
                css_path_relative_to_opf = href

            if image_r_opf_path != None \
            and text_r_opf_path != None \
            and ncx_path_relative_to_opf != None:
                break

        return image_r_opf_path, text_r_opf_path, ncx_path_relative_to_opf

    def getIndexLoc(self):
        return self.index_a_path

    
    def _genMemuTree(self,node,need_hash_names,menu_names,ulist,depth=0): 
        for cc in node.findall("."):
            name = cc.find("./navLabel/text").text.strip()
            link = cc.find("./content")
            attrib = link.attrib["src"]
            
            htmlpath  = re.findall(".+html",attrib)
            if len(htmlpath)> 0:
                n = htmlpath[0]
                n = n.split("/")[-1]
                if n not in menu_names:
                    menu_names.append(n)

            # only page link, no hash jump
            if '#' not in attrib:
                short_link = attrib.split('/')[-1]
                need_hash_names.append(short_link)
                attrib = "#"+self.hash(short_link)
            else:
                attrib=re.sub(r".+html","",attrib)
            print("attrib",attrib)

            

            ulist.append(f"<li><a href=\"{attrib}\">{name}</a></li>")

            subs =cc.findall("./navPoint")
            if len(subs)>0:
                for d in subs:
                    ulist.append("<ul>")
                    self._genMemuTree(d,need_hash_names,menu_names,ulist,depth+1)
                    ulist.append("</ul>")

    def genMemuTree(self,path):
        print("path",path)
        contents = Path(path).read_text()
        contents = re.sub(' xmlns="[^"]+"', '', contents, count=1)
        contents = contents.encode('utf-8')
        root = etree.fromstring(contents)
        ulist =[]
        need_hash_names = []
        menu_names = []
        ulist.append("<ul class=\"nav nav-sidebar \">")
        for c in root.findall("./navMap/navPoint"):
            self._genMemuTree(c,need_hash_names,menu_names,ulist,0)
        ulist.append("</ul>")
        return "\n".join(ulist),need_hash_names,menu_names

    def unzip(self):
        with zipfile.ZipFile(self.epubpath,'r') as zip_ref:
            zip_ref.extractall(self.root_a_path)



    def genContent(self,hash_files,menu_names):
        content_list = []
        for epub_name_without_ext in  menu_names:
            if epub_name_without_ext in  ["part0000.html","part0001.html"]:
                continue

            full_path = os.path.join(self.text_a_path,epub_name_without_ext)
            raw_content = Path(full_path).read_text()

            raw_content = raw_content.encode('utf-8')
            raw_content_dom = etree.HTML(raw_content)
            raw_content = etree.tostring(raw_content_dom.xpath("//body")[0],method='html').decode('utf-8')
            raw_content = self.washBody(raw_content)

            # ad slef generated hash
            short_link = os.path.basename(full_path)
            if short_link in hash_files:
                anhor = f"<div id=\"{self.hash(short_link)}\"></div>"
                content_list.append(anhor)

            content_list.append(raw_content)

        full_content = "".join(content_list)
        full_content = self.washImageLink(full_content)
        return full_content

    def washBody(self,sub_content):
        tmp = sub_content.replace("<body","<div")
        tmp = tmp.replace("</body>","</div>")
        return tmp

    def washImageLink(self,full_content):
        return re.sub(r"\.\.\/images","./"+self.image_r_opf_path,full_content)
        
    def traverse(self,rootdir):
        for cdirname, _, filenames in os.walk(rootdir):
            if rootdir ==  cdirname:
                return filenames 
    def hash(self, s):
        import base64
        tag                 = base64.b64encode(s.encode('ascii'))
        tag                 = tag.decode("ascii")
        return tag.rstrip(' = ')


    
    def gen(self):
        menu, hash_files, menu_names = self.genMemuTree(os.path.join(self.opf_a_dir,"toc.ncx"))

        full_content = self.genContent(hash_files,menu_names)

        self.template = self.template.replace("${menu}$",menu)
        self.template = self.template.replace("${title}$",self.epub_name_without_ext)
        self.template = self.template.replace("${content}$",full_content)
        Path(join(self.outputdir, self.epub_name_without_ext,"./index.html")).write_text(self.template)
        self.copyJs()

    def copyJs(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        shutil.copy(os.path.join(script_dir,"jquery.min.js"),self.root_a_path)
        shutil.copy(os.path.join(script_dir,"leader-line.min.js"),self.root_a_path)


def main(args):
    filepath = args.filepath
    if filepath[0]!="." and filepath[0]!="/":
        filepath= "./"+filepath
    filepath = os.path.abspath(filepath)

    outputdir =tempfile.gettempdir()
    if args.outputdir:
        outputdir = os.path.abspath(args.outputdir)

    e = Epub2Html(filepath,outputdir)
    e.gen()
    print("converted! "+ e.getIndexLoc())
    if sys.platform == 'darwin':
        bashCommand = "open '" + e.getIndexLoc() +"'"
        subprocess.check_call(bashCommand,
                              shell=True)



def entry_point():
    parser = createParse()
    mainArgs=parser.parse_args()
    main(mainArgs)


def createParse():
    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="")
    parser.add_argument("filepath",  help="filepath" )
    parser.add_argument("-o",'--outputdir', type=str,  required=False, help='output dir')
    # parser.add_argument("outputdir",  help="outputdir" )
    return parser
    


