class ZeitgeistServerException(Exception):
    pass

class ServerAlreadyStarted(ZeitgeistServerException):
    pass

class SessionsStructureInit(ZeitgeistServerException):
    pass

class SessionsStructureDestruct(ZeitgeistServerException):
    pass

class SessionCreation(ZeitgeistServerException):
    pass

class EndpointsInit(ZeitgeistServerException):
    pass

class EndpointsDestruct(ZeitgeistServerException):
    pass
