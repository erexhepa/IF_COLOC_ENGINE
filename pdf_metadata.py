import pyPdf
import optparse
from pyPdf import PdfFileReader
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

import zipfile
from lxml import etree

def get_epub_info(fname):
    ns = {
        'n':'urn:oasis:names:tc:opendocument:xmlns:container',
        'pkg':'http://www.idpf.org/2007/opf',
        'dc':'http://purl.org/dc/elements/1.1/'
    }

    # prepare to read from the .epub file
    zip = zipfile.ZipFile(fname)

    # find the contents metafile
    txt = zip.read('META-INF/container.xml')
    tree = etree.fromstring(txt)
    cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path',namespaces=ns)[0]

    # grab the metadata block from the contents metafile
    cf = zip.read(cfname)
    tree = etree.fromstring(cf)
    p = tree.xpath('/pkg:package/pkg:metadata',namespaces=ns)[0]

    # repackage the data
    res = {}
    for s in ['title','language','creator','date','identifier']:
        res[s] = p.xpath('dc:%s/text()'%(s),namespaces=ns)[0]

    return res

def get_toc(pdf_path):
    infile = open(pdf_path, 'rb')
    parser = PDFParser(infile)
    document = PDFDocument(parser)

    toc = list()
    for (level,title,dest,a,structelem) in document.get_outlines():
        toc.append((level, title))

    return toc

def printMeta(fileName):
    pdfFile = PdfFileReader(file(fileName,'rb'))
    docInfo = pdfFile.getDocumentInfo()
    pginput = pdfFile.getPage(1)

    print "title = %s" % (pdfFile.getDocumentInfo().title)
    print '[*] PDF MetaData For: '+ str(fileName)

    tocfilepdf = get_toc(fileName)

    for metaItem in docInfo:
        print '[+]' + metaItem + ':' + docInfo[metaItem]

def main():

    parser = optparse.OptionParser('usage %prog "+\"-F ')
    parser.add_option('-F', dest='fileName', type='string',help='specify PDF file name')

    (options, args) = parser.parse_args()
    fileName = options.fileName

    #fmeta = get_epub_info('/home/eltonr/Downloads/'+fileName)

    if fileName == None:
        print parser.usage
        exit(0)
    else:
        printMeta('/home/eltonr/Downloads/'+fileName)

if __name__ == '__main__':
    main()