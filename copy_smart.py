#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re

import delegator
import os 

from ebooklib import epub
DEST_PATH = "~/mantou-reader/reader/book/"

def copy(book):
    mtime1 = os.path.getmtime(book)
    #print mtime1
    dest = os.path.join(DEST_PATH, book)
    dest = os.path.expanduser(dest)
    mtime2 = os.path.getmtime(dest)
    #print mtime2
    if mtime1 > mtime2:
        cmd = 'cp %s %s' % (book, dest)
        print cmd
        delegator.run(cmd) 

def copy_all():
    for filename in os.listdir("."):
        if filename.endswith(".epub"):
            copy(filename)

if __name__ =="__main__":
    if len(sys.argv) < 2:
        print "usage: pack.py all|book"
        sys.exit()

    if sys.argv[1].lower() == "all":
        copy_all()
        sys.exit()

    for book in sys.argv[1:]:
        if os.path.exists(book):
            copy(book)
