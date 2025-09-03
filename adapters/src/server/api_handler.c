#include "core/include/server/master.h"
#include "core/include/server/api/socket.h"
#include "adapters/include/server/config.h"
#include "adapters/include/server/exceptions.h"
#include <sys/prctl.h>
#include <Python.h>


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

    run_core_server_loop(server_port, 1, thread_pool_size, false);

    Py_INCREF(Py_None);
    return (Py_None);
}
