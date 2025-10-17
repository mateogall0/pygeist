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
_handle_input_py(PyObject *self,
                 PyObject *args) {
    (void)self;
    int client_fd;
    if (!PyArg_ParseTuple(args, "i", &client_fd))
        return NULL;

    Py_BEGIN_ALLOW_THREADS
    respond(client_fd);
    Py_END_ALLOW_THREADS

    Py_RETURN_NONE;
}

void _handle_input(int client_fd) {
    PyGILState_STATE gstate = PyGILState_Ensure();
    print_debug("Reached _handle_input\n");

    PyObject *args = PyTuple_Pack(1, PyLong_FromLong(client_fd));
    if (!args) {
        PyErr_Print();
        PyGILState_Release(gstate);
        return;
    }

    // Call the C Python function directly
    PyObject *res = _handle_input_py(NULL, args);
    Py_DECREF(args);

    if (!res) PyErr_Print();
    else Py_DECREF(res);

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
        &server_port)) {
        return (NULL);
    }

    /* Py_BEGIN_ALLOW_THREADS */
    run_core_server_loop(server_port,
                         ZSERVER_SYSTEM_BATCH_SIZE,
                         ZSERVER_SYSTEM_VERBOSE,
                         _handle_input);
    /* Py_END_ALLOW_THREADS */

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
