
# -*- coding: utf-8 -*-

from epub2html import Epub2Html


def test_opf():
    e= Epub2Html("/Users/zk/git/jsPrj/epub2html/a.epub","./")
    print(e.readMeta())
