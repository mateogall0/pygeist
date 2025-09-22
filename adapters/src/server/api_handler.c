#include <Python.h>
#include "core/include/server/master.h"
#include "core/include/server/static.h"
#include "core/include/server/api/socket.h"
#include "core/include/server/api/response.h"
#include "adapters/include/server/config.h"
#include "adapters/include/server/api_handler.h"
#include "adapters/include/server/exceptions.h"
#include <sys/prctl.h>
#include <stdbool.h>


PyObject *
_handle_input_py(PyObject *self,
                 PyObject *args) {
    (void)self;
    int client_fd;
    if (!PyArg_ParseTuple(args, "i", &client_fd))
        return NULL;

    respond(client_fd);

    Py_RETURN_NONE;
}

void _handle_input(int client_fd) {
    PyGILState_STATE gstate = PyGILState_Ensure();

    // Import our Python helper module that defines run()
    PyObject *helpers = PyImport_ImportModule(ZSERVER_MODULE_NAME ".concurrency.helpers");
    if (!helpers) {
        PyErr_Print();
        PyGILState_Release(gstate);
        return;
    }

    PyObject *run_func = PyObject_GetAttrString(helpers, "run_handler");
    Py_DECREF(helpers);
    if (!run_func) {
        PyErr_Print();
        PyGILState_Release(gstate);
        return;
    }

    PyMethodDef method_def = {
        "_handle_input_py_temp",
        _handle_input_py,
        METH_VARARGS,
        NULL
    };

    PyObject *py_handler = PyCFunction_New(&method_def, NULL);
    if (!py_handler) {
        PyGILState_Release(gstate);
        return;
    }

    // Then pack it into args
    PyObject *args = PyTuple_Pack(2, py_handler, PyLong_FromLong(client_fd));
    Py_DECREF(py_handler);
    if (!args) {
        PyErr_Print();
        Py_DECREF(run_func);
        PyGILState_Release(gstate);
        return;
    }

    PyObject *res = PyObject_CallObject(run_func, args);
    Py_DECREF(args);
    Py_DECREF(run_func);

    if (!res)
        PyErr_Print();
    else
        Py_XDECREF(res);

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

    static char *kwlist[] = {"port", NULL};
    uint32_t server_port = 4000;

    if (!PyArg_ParseTupleAndKeywords(
            args, kwargs,
            "|I",
            kwlist,
            &server_port))
        return (NULL);

    run_core_server_loop(server_port,
                         ZSERVER_SYSTEM_BATCH_SIZE,
                         ZSERVER_SYSTEM_VERBOSE,
                         _handle_input);

    Py_RETURN_NONE;
}

PyObject*
run_get_api_log_requests(PyObject *self) {
    (void)self;

    bool b = get_log_requests();

    Py_INCREF(b ? Py_True : Py_False);
    return (b ? Py_True : Py_False);
}

PyObject*
run_set_api_log_requests(PyObject *self, PyObject *args, PyObject *kwargs) {
    (void)self;
    static char *kwlist[] = {"value", NULL};
    PyObject *py_enabled = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", kwlist, &py_enabled))
        return (NULL);

    if (!PyBool_Check(py_enabled)) {
        PyErr_SetString(PyExc_TypeError, "Argument 'enabled' must be a boolean");
        return (NULL);
    }

    bool v = (py_enabled == Py_True);
    set_log_requests(v);

    Py_RETURN_NONE;
}
