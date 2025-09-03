#include <Python.h>


// Example function
static PyObject* hello(PyObject *self, PyObject *args) {
    return Py_BuildValue("s", "Hello from C!");
}

// Method table
static PyMethodDef AdapterMethods[] = {
    {"hello", hello, METH_NOARGS, "Say hello"},
    {NULL, NULL, 0, NULL}
};

// Module definition
static struct PyModuleDef adaptermodule = {
    PyModuleDef_HEAD_INIT,
    "_adapter",         // module name
    "Example adapter",  // docstring
    -1,
    AdapterMethods
};

// Module init function
PyMODINIT_FUNC PyInit__adapter(void) {
    return PyModule_Create(&adaptermodule);
}
