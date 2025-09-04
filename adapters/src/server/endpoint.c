#include "adapters/include/server/exceptions.h"
#include "core/include/server/api/endpoint.h"
#include <Python.h>

PyObject*
run_init_endpoints_list(PyObject *self) {
    (void)self;
    if (endpoints) {
        PyErr_SetString(EndpointsInit,
                        "endpoints list are already initialized");
        return (NULL);
    }
    if (!init_endpoints_list()) {
        PyErr_SetString(EndpointsInit,
                        "endpoints list couldn't be initialized");
        return (NULL);
    }

    Py_INCREF(Py_None);
    return (Py_None);
}


PyObject*
run_destroy_endpoints_list(PyObject *self) {
    (void)self;
    if (!endpoints) {
        PyErr_SetString(SessionsStructureDestruct,
                        "endpoints list is not initialized");
        return (NULL);
    }
    destroy_endpoints();

    Py_INCREF(Py_None);
    return (Py_None);
}
