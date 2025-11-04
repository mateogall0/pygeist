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
        "I",
        kwlist,
        &server_port)) {
        return (NULL);
    }
    print_debug("Selected server port: %u\n", server_port);

    Py_BEGIN_ALLOW_THREADS
    run_core_server_loop(server_port,
                         ZSERVER_SYSTEM_BATCH_SIZE,
                         ZSERVER_SYSTEM_VERBOSE,
                         respond);
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
