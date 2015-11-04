import pyPdf
import optparse
from pyPdf import PdfFileReader
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

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

    if fileName == None:
        print parser.usage
        exit(0)
    else:
        printMeta('/home/eltonr/Downloads/'+fileName)

if __name__ == '__main__':
    main()