library(XML)
library(RCurl)

# USAGE: ldply(c('9780387962406', '9780387961406', '0387981403'), function(x) ISBNdb(x, 'apikey'))

ISBNdb <- function(isbn, access_key, 
                   isbn.api='http://isbndb.com/api/books.xml?access_key=%s&index1=isbn&value1=%s') {
  isbn <- as.character(isbn)
  stopifnot(length(isbn)==1, (nchar(isbn)==10 || nchar(isbn)==13))
  stopifnot(length(access_key)==1)
  
  query <- sprintf(isbn.api, access_key, isbn)
  
  isbn.xml <- xmlParse(getURL(query))
  
  bookdata <- getNodeSet(isbn.xml, '//BookData')
  
  if (length(bookdata) == 0) {
    warning(paste('No results found for ISBN', isbn))
    return(NULL)
  }
  cbind(xmlToDataFrame(bookdata),
        as.data.frame(t(xmlAttrs(bookdata[[1]]))))
}

