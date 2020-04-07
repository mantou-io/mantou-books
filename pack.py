#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re

import delegator
import os 

from ebooklib import epub

def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

def is_alpha(uchar):
    if '0' <= uchar <= '9':
        return True
    if 'a' <= uchar <= 'z':
        return True
    if 'A' <= uchar <= 'Z':
        return True
    return False
        
def pack_all():
    for filename in os.listdir("."):
        if filename.isdigit():
            pack(filename)

def fix_toc(book_id):
    _prefixs = ["OEBPS/Text/", "/OEBPS/", "/", ]
    prefixs = []
    for _ in _prefixs:
        prefixs.append(book_id + "/" + _)

    for prefix in prefixs:
        opath = os.path.join(prefix, "toc.ncx")
        if os.path.exists(opath):
            content = ''
            index = 1
            nlines = []
            with open(opath) as f:
                content = f.read()
                lines = content.splitlines()
                for line in lines:
                    print line
                    if "playOrder" not in line:
                        nlines.append(line)
                    else:
                        nline = re.sub('playOrder="\d+"','playOrder="%s"'%index,  line)
                        nlines.append(nline)
                        index += 1
            content = "\n".join(nlines)
            with open(opath+'s', 'w') as wf:
                wf.write(content)

def process_alpha(fname):
    content = ''
    ncontent = ''

    with open(fname) as f:
        content = f.read()
        content = content.decode('utf-8')
        index = 0
        total = len(content)
        begin_it = 0
        while(index < total):
            if not begin_it and content[index:index+4].lower() == 'body':
                print "beginnnnn"
                begin_it = 1
            if not begin_it:
                ncontent += content[index]
                index += 1
                continue

            if not is_chinese(content[index]):
                ncontent += content[index]
                index += 1
            else:
                # look backward first
                if (index > 2) and is_alpha(content[index-1]):
                    pos = index - 2
                    while (pos > 0 and is_alpha(content[pos])):
                        pos -= 1
                    # eat back : it's tricky
                    ncontent = ncontent[:pos-index+1]

                    ncontent += '<span class="alpha-r alpha">'+ content[pos+1:index] + '</span>'

                ncontent += content[index]

                # look afterward then
                if is_alpha(content[index +1]):
                    pos = index+2
                    while(pos < total and is_alpha(content[pos])):
                        pos += 1
                    class_name = ''
                    if is_chinese(content[pos]):
                        class_name = 'alpha-r '
                    ncontent += '<span class="alpha-l ' + class_name + 'alpha">'+ content[index+1:pos] + '</span>'
                    if is_chinese(content[pos]):
                        index = pos
                        ncontent += content[index]
                    else:
                        index = pos - 1
                index += 1

    with open(fname, "w") as f:
        f.write(ncontent)


def fix_alpha(book_id):
    alpha_path = book_id + "-alpha"
    delegator.run('rm -rf %s' % alpha_path)
    delegator.run('cp -a %s %s' % (book_id, alpha_path))

    _prefixs = ["/OEBPS/Text/", "/OEBPS/", "/", ]
    prefixs = []

    for _ in _prefixs:
        prefixs.append(alpha_path + _)

    for prefix in prefixs:
        if os.path.exists(prefix):
            dpath = prefix
            for filename in os.listdir(dpath):
                if filename.endswith("html"):
                    fname = os.path.join(dpath, filename)
                    process_alpha(fname)

def pack(book_id, output = True):
    #fix_toc(book_id)
    fix_alpha(book_id)

    delegator.run('cd %s-alpha; zip -rX ../%s.epub *' % (book_id, book_id)) 
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
