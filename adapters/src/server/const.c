#include "adapters/include/server/const.h"
#include "core/include/server/api/endpoint.h"
#include <Python.h>


void _add_methods_const(PyObject *m) {
    for (int i = 0; i < METHODS_COUNT; ++i) {
        if (PyModule_AddIntConstant(m, methods_str[i], i) < 0) {
            Py_DECREF(m);
            return;
        }
    }
}

void init_consts(PyObject *m) {
    _add_methods_const(m);
}
