#include "core/include/server/master.h"
#include "core/include/server/static.h"
#include "core/include/server/api/socket.h"
#include "core/include/server/api/response.h"
#include "adapters/include/server/config.h"
#include "adapters/include/server/api_handler.h"
#include "adapters/include/server/exceptions.h"
#include <sys/prctl.h>
#include <Python.h>
#include <stdbool.h>


PyObject *
_handle_input_py(PyObject *self,
                 PyObject *args) {
    (void)self;
    int client_fd;
    if (!PyArg_ParseTuple(args, "i", &client_fd))
        return NULL;

    respond(client_fd);

    Py_INCREF(Py_None);
    return (Py_None);
}

void _handle_input(int client_fd) {
    PyGILState_STATE gstate = PyGILState_Ensure();

    PyMethodDef method_def = {
        "_handle_input_py_temp",
        _handle_input_py,
        METH_VARARGS,
        NULL
    };
    PyObject *py_func = PyCFunction_New(&method_def, NULL);

    PyObject *args_tuple = Py_BuildValue("(i)", client_fd);

    PyObject *res = PyObject_CallObject(py_func, args_tuple);
    if (!res) {
        PyErr_Print();
    }

    Py_XDECREF(res);
    Py_DECREF(args_tuple);
    Py_DECREF(py_func);

    PyGILState_Release(gstate);
}

PyObject*
run_zeitgeist_server_adapter(PyObject *self,
                             PyObject *args,
                             PyObject *kwargs) {
    (void)self;
    if (ssc) {
        PyErr_SetString(ServerAlreadyStarted, "server already initialized");
        return (NULL);
    }

    static char *kwlist[] = {"port", "thread_pool_size", NULL};
    uint32_t server_port = 4000;
    size_t thread_pool_size = 2;

    if (!PyArg_ParseTupleAndKeywords(
            args, kwargs,
            "|Ik",
            kwlist,
            &server_port,
            &thread_pool_size))
        return (NULL);

    run_core_server_loop(server_port,
                         ZSERVER_SYSTEM_BATCH_SIZE,
                         ZSERVER_SYSTEM_VERBOSE,
                         _handle_input);

    Py_INCREF(Py_None);
    return (Py_None);
}

PyObject*
run_get_api_log_requests(PyObject *self) {
    (void)self;

    bool b = get_log_requests();

    Py_INCREF(b ? Py_True : Py_False);
    return b ? Py_True : Py_False;
}

PyObject*
run_set_api_log_requests(PyObject *self, PyObject *args, PyObject *kwargs) {
    (void)self;
    static char *kwlist[] = {"value", NULL};
    PyObject *py_enabled = NULL;


    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", kwlist, &py_enabled))
        return NULL;


    if (!PyBool_Check(py_enabled)) {
        PyErr_SetString(PyExc_TypeError, "Argument 'enabled' must be a boolean");
        return NULL;
    }

    bool v = (py_enabled == Py_True);

    set_log_requests(v);

    Py_INCREF(Py_None);
    return Py_None;

}
