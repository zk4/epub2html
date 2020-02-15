
# -*- coding: utf-8 -*-

from epub2html import epub2html

def test_run_openssl_command() -> None:
    assert 1 == 1


def test_feed():
    assert 4 == epub2html.feed(2)
