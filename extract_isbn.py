__author__ = 'rexhepaj'

#!/usr/bin/env python

## Extract isbn from pdf files contained in a specified directory
## - Depends upon code written by Osvaldo Santana Neto (https://code.google.com/p/osantana-code/)
## Copyright (C) 2012  Harshit Mittal <priv8code [at] gmail.com>
##
## This library is free software; you can redistribute it and/or
## modify it under the terms of the GNU Lesser General Public
## License as published by the Free Software Foundation; either
## version 2.1 of the License, or (at your option) any later version.
##
## This library is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public
## License along with this library; if not, write to the Free Software
## Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import sys
import os
import glob
import re
import pickle

from optparse import OptionParser

[OK, INVALID, ERROR] = range(3)

use = "Usage: %prog [Option] argument"
desc = '''This script %prog is used to extract isbn from pdfs'''

parser = OptionParser(usage = use, description=desc)
parser.add_option("-d", "--string", dest="dir", help="Location of the directory containing pdfs")

def strip(isbn):
    """Strip whitespace, hyphens, etc. from an ISBN number and return the result."""
    return filter(lambda x: str.isdigit(x) or x.upper() == "X", isbn)

def valid(isbn):
    """Check the validity of an ISBN. Works for either ISBN-10 or ISBN-13."""

    short = strip(isbn)
    if len(short) == 10:
        return valid_isbn10(short)
    if len(short) == 13:
        return valid_isbn13(short)
    return False

def check(stem):
    """Compute the check digit for the stem of an ISBN. Works with either the
    first 9 digits of an ISBN-10 or the first 12 digits of an ISBN-13."""

    short = strip(stem)
    if len(short) == 9:
        return check_isbn10(short)
    if len(short) == 12:
        return check_isbn13(short)
    return False

def check_isbn10(stem):
    """Computes the ISBN-10 check digit based on the first 9 digits of a
    stripped ISBN-10 number."""

    check = 11 - sum( (x+2) * int(y) for x,y in enumerate(reversed(stem)) ) % 11
    if check == 10:
        return "X"
    elif check == 11:
        return "0"

    return str(check)

def valid_isbn10(isbn):
    """Checks the validity of an ISBN-10 number."""

    short = strip(isbn)
    if len(short) != 10:
        return False

    digits = [ (10 if x.upper() == "X" else int(x)) for x in short ]
    return (sum( (x+1)*y for x,y in enumerate(reversed(digits)) ) % 11) == 0

def check_isbn13(stem):
    """Compute the ISBN-13 check digit based on the first 12 digits of a
    stripped ISBN-13 number. """

    check = 10 - sum( (x%2*2+1) * int(y) for x,y in enumerate(stem) ) % 10
    if check == 10:
        return "0"

    return str(check)

def valid_isbn13(isbn):
    """Checks the validity of an ISBN-13 number."""

    short = strip(isbn)
    if len(short) != 13:
        return False

    digits = [ (10 if x.upper() == "X" else int(x)) for x in short ]
    return (sum( (x%2*2+1) * y for x,y in enumerate(digits) ) % 10) == 0

def format(isbn, sep=""):
    s = strip(isbn)

    if len(s) == 10:
        return s[0] + sep + s[1:6] + sep + s[6:9] + sep + s[9]

    if len(s) == 13:
        return s[0:3] + sep + s[3:9] + sep + s[9:12] + sep + s[12]

    return isbn

def addBook(isbn, filename):
    newBooks[isbn] = [filename]


def get_isbn(path):
    regex = re.compile('(?:[0-9]{3}-)?[0-9]{1,5}-[0-9]{1,7}-[0-9]{1,6}-[0-9]')
    for infile in glob.glob(os.path.join(path, '*.pdf')):
        os.system('pdftotext -f 1 -l 100 "' + infile + '"')
        txtfile = infile[:-3] + 'txt'
        afile = open(txtfile, "r")
        isbn_valid = []
        for line in afile:
            isbn_candidates = regex.findall(line)
            for candidate in isbn_candidates:
                modified_candidate = strip(candidate)
                if valid(modified_candidate): isbn_valid.append(candidate)
        if len(isbn_valid) >= 1 :
            deleteBooks.append(txtfile)
            addBook(isbn_valid[0], infile)
    for db in deleteBooks:
        os.remove(db)
    for isbn, bookName in newBooks.iteritems() :
        print isbn + " >> " + ''.join(bookName)

    pickle.dump(newBooks, open("saveLibrayISBN.p", "wb"))

    return newBooks


def get_isbnrecords(isbnBooks):
    isbnRec = {}

    print 'debug'

    return  isbnRec


if __name__=='__main__':
    newBooks = {}
    deleteBooks = []
    path = ''
    path = '/archives/biocomp/rexhepaj/Telechargement/'

    #newBooksISBNs = get_isbn(path)
    newBooksISBNs = pickle.load('saveLibraryISBN.p',"rb")
    newBooksRec   = get_isbnrecords(newBooksISBNs)

    print 'END'