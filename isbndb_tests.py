from initISNDB import ISBNdbException
from models  import *
from client  import ISBNdbClient
from catalog import *


ACCESS_KEY = "LW3LP8ZB"


if __name__ == "__main__":
    client = ISBNdbClient( access_key=ACCESS_KEY )
    catalog = BookCollection(client)
    result  = catalog.isbn('0210406240', results='authors')