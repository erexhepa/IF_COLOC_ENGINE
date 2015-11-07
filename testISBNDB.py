__author__ = 'eltonr'

from initISNDB import ISBNdbException
from models  import *
from client  import ISBNdbClient
from catalog import *


ACCESS_KEY = "LW3LP8ZB"


if __name__ == "__main__":
    client = ISBNdbClient( access_key=ACCESS_KEY )
    catalog = BookCollection(client)
    result  = catalog.isbn('1429216220', results='details')
    #print result
    binfo = result.__getitem__(0)


    print 'end'