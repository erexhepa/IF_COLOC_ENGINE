import os
import sys
import logging
import time
import datetime
import pickle


from metasearch import BookMeta

logger = logging.getLogger('metasearch')
IGNORE_PREFIX = ['EMANER_', 'DELIAF_', 'NRAW_', 'TSIXE-NUM', 'RORREPTTH_', 'YNAMOOT_']

def searchisbnmeta_fileindex(fileindx):
    fileindxMeta = {}

    newBooks = {}

    path = '/home/eltonr/Downloads/'
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.setLevel(logging.DEBUG)
    t = time.time()
    logname = datetime.datetime.fromtimestamp(t).strftime('%Y_%m_%d_%H_%M_%S')
    fh = logging.FileHandler(logname + '.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    recorder = open(logname + '_Rename.log', 'w')
    logging.debug('filesystemencoding = ' + sys.getfilesystemencoding())

    for filename in fileindx:
        logger.debug('====== ====== ====== ====== ====== ======')
        logger.debug('Processing ' + filename)
        bookmeta = BookMeta(filename, recorder, 'goob', 'Publisher:Author:Year:Title:Language:ISBN-13')

        newName = bookmeta.rename()
        print newName
        newBooks[filename] = [newName]

    recorder.close()

    return fileindxMeta

def build_fileindex(path):

    fileindx = []

    for root, dirs, files in os.walk(unicode(path, sys.getfilesystemencoding())):
        for f in files:
            if f.endswith(('.pdf', '.epub')) and not f.startswith('EMANER_') and not f.startswith(
                'DELIAF_') and not f.startswith('NRAW_') and not f.startswith('TSIXE-NUM') and not f.startswith(
                'RORREPTTH_') and not f.startswith('YNAMOOT_'):
                filename = os.path.join(root, f)
                fileindx.append(filename)


    pickle.dump(fileindx, open("saveLibrayFileindx.pkl", "wb"))
    print 'END'
    return fileindx

if __name__ == '__main__':
        path = '/home/eltonr/Downloads/'
        # if index has to be intialised
        # fileIndx = build_fileindex(path)
        fileIndx = pickle.load(open("saveLibrayFileindx.pkl", "rb"))
        booksMeta = searchisbnmeta_fileindex(fileIndx)
        pickle.dump(booksMeta, open("saveLibrayISBNnew.pkl", "wb"))
        print 'END'