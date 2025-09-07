#ifndef ZPYTHON_ZSERVER_ENDPOINTS_H
#define ZPYTHON_ZSERVER_ENDPOINTS_H


#include <Python.h>


PyObject*
run_init_endpoints_list(PyObject *self);

PyObject*
run_destroy_endpoints_list(PyObject *self);

PyObject*
run_create_append_endpoint(PyObject *self,
                           PyObject *args,
                           PyObject *kwargs);

#endif
