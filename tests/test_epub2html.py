
# -*- coding: utf-8 -*-

from epub2html import Epub2Html


def test_opf():
    e= Epub2Html("/Users/zk/Downloads/隐性逻辑：教你快速切换思考方式-卡尔•诺顿.epub","./")
    a, b = e.readOpf()
    print(a,b)
