#include "adapters/include/server/api_handler.h"
#include "adapters/include/server/sessions.h"
#include "adapters/include/server/exceptions.h"
#include "adapters/include/server/endpoint.h"
#include <Python.h>


static PyMethodDef AdapterMethods[] = {
    {"_run_server",
     run_zeitgeist_server_adapter,
     METH_VARARGS | METH_KEYWORDS,
     "Initialize and run server"},
    {"_init_sessions_structure",
     run_initialize_sessions_structure,
     METH_VARARGS | METH_KEYWORDS,
     "Initialize sessions wheel and map"},
    {"_destroy_sessions_structure",
     run_destroy_sessions_structure,
     METH_VARARGS | METH_KEYWORDS,
     "Destroy sessions wheel and map"},
    {"_init_endpoints_list",
     run_init_endpoints_list,
     METH_VARARGS | METH_KEYWORDS,
     "Initialize endpoints list"},
    {"_destroy_endpoints_list",
     run_destroy_endpoints_list,
     METH_VARARGS | METH_KEYWORDS,
     "Destroy endpoints list"},
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
    PyObject *m = PyModule_Create(&adaptermodule);
    if (!m)
        return (NULL);
    init_exceptions();
    return (m);
}
