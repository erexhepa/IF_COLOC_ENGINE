class ISBNdbException(Exception):
    pass

class ISBNdbHttpException(ISBNdbException):
    
    def __init__(self, status, uri, msg=""):
        self.uri    = uri
        self.msg    = msg
        self.status = status

    def __str__(self):
        return "HTTP ERROR %s: %s \n %s" % (self.status, self.msg, self.uri)
