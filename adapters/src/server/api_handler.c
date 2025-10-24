#include <Python.h>
#include "core/include/server/master.h"
#include "core/include/debug.h"
#include "core/include/server/static.h"
#include "core/include/server/api/socket.h"
#include "core/include/server/api/response.h"
#include "adapters/include/server/config.h"
#include "adapters/include/server/api_handler.h"
#include "adapters/include/server/exceptions.h"
#include <sys/prctl.h>
#include <stdbool.h>

PyObject *
run_respond(PyObject *self, PyObject *args, PyObject *kwargs) {
    (void)self;
    int client_fd;

    static char *kwlist[] = {"fd", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "i", kwlist, &client_fd)) {
        return NULL;
    }
    Py_BEGIN_ALLOW_THREADS

    respond(client_fd);

    Py_END_ALLOW_THREADS
    Py_RETURN_NONE;
}

void _handle_input(int client_fd) {
    print_debug("Reached _handle_input\n");

    PyGILState_STATE gstate = PyGILState_Ensure();
    print_debug("_handle_input: grabbed GIL\n");

    PyObject *helpers = PyImport_ImportModule(ZSERVER_MODULE_NAME ".concurrency.helpers");
    if (!helpers) {
        PyErr_Print();
        PyGILState_Release(gstate);
        return;
    }

    PyObject *enqueue_fd_func = PyObject_GetAttrString(helpers, "enqueue_fd");
    Py_DECREF(helpers);
    if (!enqueue_fd_func || !PyCallable_Check(enqueue_fd_func)) {
        Py_XDECREF(enqueue_fd_func);
        PyGILState_Release(gstate);
        return;
    }

    PyObject *module = PyImport_ImportModule(ZSERVER_MODULE_NAME "._adapter");
    if (!module) {
        PyErr_Print();
        Py_DECREF(enqueue_fd_func);
        PyGILState_Release(gstate);
        return;
    }

    PyObject *py_respond_func = PyObject_GetAttrString(module, "_respond");
    Py_DECREF(module);
    if (!py_respond_func || !PyCallable_Check(py_respond_func)) {
        Py_XDECREF(py_respond_func);
        Py_DECREF(enqueue_fd_func);
        PyGILState_Release(gstate);
        return;
    }

    PyObject *args = Py_BuildValue("(iO)", client_fd, py_respond_func);
    Py_DECREF(py_respond_func);
    if (!args) {
        Py_DECREF(enqueue_fd_func);
        PyGILState_Release(gstate);
        return;
    }

    print_debug("Before calling enqueue_fd\n");
    PyObject *result = PyObject_CallObject(enqueue_fd_func, args);
    if (!result) {
        PyErr_Print();

    } else {
        Py_DECREF(result);
    }
    print_debug("After calling enqueue_fd\n");
    Py_DECREF(args);
    Py_DECREF(enqueue_fd_func);

    print_debug("Exiting _handle_input\n");
    PyGILState_Release(gstate);
}

PyObject*
run_zeitgeist_server_adapter(PyObject *self,
                             PyObject *args,
                             PyObject *kwargs) {
    (void)self;
    if (!Py_IsInitialized()) {
        Py_Initialize();
    }

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
        &server_port)) {
        return (NULL);
    }

    Py_BEGIN_ALLOW_THREADS
    run_core_server_loop(server_port,
                         ZSERVER_SYSTEM_BATCH_SIZE,
                         ZSERVER_SYSTEM_VERBOSE,
                         _handle_input);
    Py_END_ALLOW_THREADS

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
