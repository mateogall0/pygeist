#include <Python.h>
#include "adapters/include/server/const.h"
#include "core/include/server/api/endpoint.h"
#include "core/include/common/format.h"


void _add_methods_const(PyObject *m) {
    for (int i = 0; i < METHODS_COUNT; ++i) {
        if (PyModule_AddIntConstant(m, methods_str[i], i) < 0) {
            Py_DECREF(m);
            return;
        }
    }
}

void _add_server_version(PyObject *m) {
    if (PyModule_AddStringConstant(m,
                                   "SERVER_VERSION",
                                   ZEIT_RESPONSE_VERSION) < 0)
        Py_DECREF(m);
}

void init_consts(PyObject *m) {
    if (!m)
        return;
    _add_methods_const(m);
    _add_server_version(m);
}
