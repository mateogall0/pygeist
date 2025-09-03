#include <Python.h>
#include "adapters/include/server/api_handler.h"


static PyMethodDef AdapterMethods[] = {
    {"_run_server",
     (PyCFunction)run_zeitgeist_server_adapter,
     METH_VARARGS | METH_KEYWORDS,
     "Initialize and run server"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef adaptermodule = {
    PyModuleDef_HEAD_INIT,
    "_adapter",
    "Example adapter",  // docstring
    -1,                 // per-interpreter state (or -1 if not needed)
    AdapterMethods
};

// Module init function (entry point for import)
PyMODINIT_FUNC PyInit__adapter(void) {
    return PyModule_Create(&adaptermodule);
}
