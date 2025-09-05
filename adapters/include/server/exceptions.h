#ifndef ZPYTHON_ZSERVER_EXCEPTIONS_H
#define ZPYTHON_ZSERVER_EXCEPTIONS_H

#include <Python.h>

extern PyObject *ServerAlreadyStarted;
extern PyObject *SessionsStructureInit;
extern PyObject *SessionsStructureDestruct;
extern PyObject *EndpointsInit;
extern PyObject *EndpointsDestruct;


void init_exceptions(void);


#endif
