#include <Python.h>
#include "adapters/include/server/config.h"
#include "adapters/include/server/exceptions.h"
#include <stdio.h>


PyObject *ServerAlreadyStarted = NULL;
PyObject *SessionsStructureInit = NULL;
PyObject *SessionsStructureDestruct = NULL;
PyObject *EndpointsInit = NULL;
PyObject *EndpointsDestruct = NULL;
PyObject *SessionCreation = NULL;

int init_exceptions(void) {
    PyObject *exceptions_module = PyImport_ImportModule(ZSERVER_MODULE_NAME ".exceptions");
    if (!exceptions_module) {
        return 1;
    }

    ServerAlreadyStarted = PyObject_GetAttrString(exceptions_module, "ServerAlreadyStarted");
    SessionsStructureInit = PyObject_GetAttrString(exceptions_module, "SessionsStructureInit");
    SessionsStructureDestruct = PyObject_GetAttrString(exceptions_module, "SessionsStructureDestruct");
    SessionCreation = PyObject_GetAttrString(exceptions_module, "SessionCreation");
    EndpointsInit = PyObject_GetAttrString(exceptions_module, "EndpointsInit");
    EndpointsDestruct = PyObject_GetAttrString(exceptions_module, "EndpointsDestruct");



    // Done with the module
    Py_DECREF(exceptions_module);

    // Validate all
    if (!ServerAlreadyStarted ||
        !SessionsStructureInit ||
        !SessionsStructureDestruct ||
        !EndpointsInit ||
        !EndpointsDestruct ||
        !SessionCreation) {
        PyErr_SetString(PyExc_ImportError, "Failed to initialize custom exceptions");
        return 1;
    }
    return 0;
}
