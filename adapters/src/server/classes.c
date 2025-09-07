#include "adapters/include/server/classes.h"
#include "adapters/include/server/config.h"
#include <Python.h>


PyObject *RequestClass = NULL;


void import_classes() {
    PyObject *request_py = PyImport_ImportModule(ZSERVER_MODULE_NAME ".request");
    if (!request_py) return;

    PyObject *RequestClass = PyObject_GetAttrString(request_py, "Request");

    Py_DECREF(request_py);
    if (!RequestClass) return;
}
