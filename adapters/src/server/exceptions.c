#include <Python.h>
#include "adapters/include/server/config.h"
#include "adapters/include/server/exceptions.h"


PyObject *ServerAlreadyStarted = NULL;

void init_exceptions(void) {
    PyObject *exceptions_module = PyImport_ImportModule(ZSERVER_MODULE_NAME ".exceptions");
    if (!exceptions_module) return;

    ServerAlreadyStarted = PyObject_GetAttrString(exceptions_module, "ServerAlreadyStarted");
    Py_DECREF(exceptions_module);
    if (!ServerAlreadyStarted) return;
}
