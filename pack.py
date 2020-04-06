#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re

import delegator
import os 

from ebooklib import epub


def pack_all():
    for filename in os.listdir("."):
        if filename.isdigit():
            pack(filename)

def pack(book_id, output = True):
    delegator.run('cd %s; zip -rX ../%s.epub *' % (book_id, book_id)) 
    if output:
        print book_id, "packed"


if __name__ =="__main__":
    if len(sys.argv) < 2:
        print "usage: pack.py all|book_id"
        sys.exit()

    if sys.argv[1].lower() == "all":
        pack_all()
        sys.exit()

    if not "".join(sys.argv[1:]).isdigit():
        print "usage: pack.py all|book_id"
        sys.exit()

    for book_id in sys.argv[1:]:
        if os.path.exists(book_id):
            try:
                pack(book_id)
            except:
                import traceback
                traceback.print_exc()
        else:
            print "%s not exist" % (book_id)
