#coding: utf-8

import argparse
from lxml import etree
import xmltodict
from pathlib import Path
import re
import zipfile
import subprocess
import webbrowser
import os
import tempfile
import sys
import shutil
import html
from os.path import dirname,basename,join,splitext,abspath
import html.parser as htmlparser
parser = htmlparser.HTMLParser()

class Epub2Html():
    def __init__(self,epubpath,outputdir):
        self.epubpath = epubpath

        script_dir    = dirname(abspath(__file__))
        template_path = join(script_dir,"template.html")

        self.template              = Path(template_path).read_text(encoding='utf-8')
        (epub_name_without_ext,_)  = splitext(basename(self.epubpath))
        self.epub_name_without_ext = epub_name_without_ext
        self.outputdir             = outputdir
        self.root_a_path           = join(outputdir,epub_name_without_ext)

        self.unzip()

        opf_r_root_path   = self.get_opf_r_root_path()
        self.index_a_path = join(self.root_a_path,"index.html")
        self.opf_a_path   = join(self.root_a_path,opf_r_root_path)
        self.opf_a_dir    = dirname(join(self.root_a_path,opf_r_root_path))

        self.ncx_r_opf_path,self.css_r_opf_path = self.paths_from_opf()

        self.ncx_a_path = join(self.opf_a_dir,self.ncx_r_opf_path)
        self.css_a_path = join(self.opf_a_dir,self.css_r_opf_path)

        # save the only name html that alredy parsed
        self.alread_gen_html = set()

        print("self.ncx_a_path",self.ncx_a_path)
        print("self.css_a_path",self.css_a_path)

    def get_xml_root(self,path):
        contents    = Path(path).read_text(encoding='utf-8')
        contents = re.sub(' xmlns="[^"]+"', '', contents, count=1)
        contents = contents.encode('utf-8')
        root     = etree.fromstring(contents)
        return root

    def get_opf_r_root_path(self):
        meta_a_path = (join(self.root_a_path,"META-INF/container.xml"))
        root     = self.get_xml_root(meta_a_path)

        for item in root.findall(".//rootfiles/"):
            return item.attrib["full-path"]

    def read_xml(self,path):
        pass

    def paths_from_opf(self):

        ncx_r_opf_path   = None
        css_r_opf_path   = None
        root             = self.get_xml_root(self.opf_a_path)

        for item in root.findall(".//manifest/"):
            href = item.attrib["href"]

            if "ncx" in item.attrib["media-type"]:
                ncx_r_opf_path = href

            if "css" in item.attrib["media-type"]:
                css_r_opf_path = href

        return  ncx_r_opf_path, css_r_opf_path

    def getIndexLoc(self):
        return self.index_a_path


    def _gen_menu_content(self,node,menus,contents,depth=0):
        for cc in node.findall("."):
            name = cc.find("./navLabel/text").text.strip()
            link = cc.find("./content")
            src = link.attrib["src"]
            unified_src = src

            # extract only name
            no_hash_name = src
            if src.find('#') != -1:
                no_hash_name = src[:src.find("#")]

            if '#' not in src:
                # check if need manually add hash tag
                unified_src = "#"+self.hash(src)
                # content need to add id to response hash tag
                anchor = f"<div id=\"{self.hash(src)}\"></div>"
                contents.append(anchor)
            else:
                # only need hash tag
                unified_src=re.sub(r".+html","",src)


            menus.append(f"<li><a href=\"{unified_src}\">{name}</a></li>")

            if no_hash_name  in self.alread_gen_html:
                continue

            self.alread_gen_html.add(no_hash_name)

            washed_content = self.gen_content(join(dirname(self.ncx_a_path),no_hash_name))

            contents.append(washed_content)

            subs =cc.findall("./navPoint")
            if len(subs)>0:
                for d in subs:
                    menus.append("<ul>")
                    self._gen_menu_content(d,menus,contents,depth+1)
                    menus.append("</ul>")

    def gen_menu_content(self):
        menus      = []
        contents   = []
        root       = self.get_xml_root(self.ncx_a_path)

        menus.append("<ul class=\"nav nav-sidebar \">")

        for c in root.findall("./navMap/navPoint"):
            self._gen_menu_content(c,menus,contents,0)

        menus.append("</ul>")

        return "\n".join(menus),"".join(contents)

    def unzip(self):
        with zipfile.ZipFile(self.epubpath,'r') as zip_ref:
            zip_ref.extractall(self.root_a_path)


    def gen_content(self,path):
        raw_text_content = Path(path).read_text(encoding='utf-8')
        raw_text_content = raw_text_content.encode('utf-8')
        raw_content_dom = etree.HTML(raw_text_content)
        content = etree.tostring(raw_content_dom.xpath("//body")[0],method='html').decode('utf-8')
        washed_content = self.wash_body(content)
        washed_content = self.wash_img_link(path,washed_content)
        return washed_content

    def wash_body(self,sub_content):
        tmp = sub_content.replace("<body","<div")
        tmp = tmp.replace("</body>","</div>")
        return tmp

    def wash_img_link(self,content_path,content):
        content =  re.sub("(?<=src=\")(.*)(?=\")",lambda match: os.path.relpath(join(dirname(content_path),match.group(1)),self.root_a_path),content)

        return content


    def hash(self, s):
        import base64
        tag                 = base64.b64encode(s.encode('ascii'))
        tag                 = tag.decode("ascii")
        return tag.rstrip('=')

    def gen_r_css(self):
        css_r_path=os.path.relpath(self.css_a_path,self.root_a_path)
        return f'<link rel="stylesheet" href="{css_r_path}" />'


    def gen(self):
        menu, full_content = self.gen_menu_content()
        self.template = self.template.replace("${menu}$",menu)
        self.template = self.template.replace("${title}$",self.epub_name_without_ext)
        self.template = self.template.replace("${content}$",full_content)
        self.template = self.template.replace("${css}$",self.gen_r_css())
        Path(join(self.outputdir, self.epub_name_without_ext,"./index.html")).write_text(self.template,encoding='utf-8')
        self.gen_jquery_js()

    def gen_jquery_js(self):
        script_dir = dirname(abspath(__file__))
        shutil.copy(join(script_dir,"jquery.min.js"),self.root_a_path)
        shutil.copy(join(script_dir,"leader-line.min.js"),self.root_a_path)


def main(args):
    filepath = args.filepath
    if filepath[0]!="." and filepath[0]!="/":
        filepath= "./"+filepath
    filepath = abspath(filepath)

    outputdir =tempfile.gettempdir()
    if args.outputdir:
        outputdir = abspath(args.outputdir)

    e = Epub2Html(filepath,outputdir)
    e.gen()
    print("converted! "+ e.getIndexLoc())
    if sys.platform == "win32":
        webbrowser.open(e.getIndexLoc(), new=2)  # open in new tab
    else:
        bashCommand = "open '" + e.getIndexLoc() +"'"
        subprocess.check_call(bashCommand,shell=True)



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



