#ifndef ZPYTHON_ZSERVER_API_HANDLER_H
#define ZPYTHON_ZSERVER_API_HANDLER_H

#include <Python.h>

extern PyObject *global_executor;

PyObject *
run_respond(PyObject *self, PyObject *args, PyObject *kwargs);

PyObject*
run_zeitgeist_server_adapter(PyObject *self, PyObject *args, PyObject *kwargs);

PyObject*
run_get_api_log_requests(PyObject *self);

PyObject*
run_set_api_log_requests(PyObject *self, PyObject *args, PyObject *kwargs);

#endif
