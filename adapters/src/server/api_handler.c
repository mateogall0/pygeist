#include <Python.h>
#include "core/include/server/master.h"
#include <sys/prctl.h>


PyObject*
run_zeitgeist_server_adapter(PyObject *self,
                             PyObject *args,
                             PyObject *kwargs) {
    (void)self;
    static char *kwlist[] = {"port", "batch_size", "thread_pool_size", NULL};
    uint32_t server_port = 4000;
    uint64_t batch_size = 4;
    size_t thread_pool_size = 2;

    if (!PyArg_ParseTupleAndKeywords(
            args, kwargs,
            "|IKk",
            kwlist,
            &server_port,
            &batch_size,
            &thread_pool_size))
        return NULL; // raise exception

    run_core_server_loop(server_port, batch_size, thread_pool_size, false);

    Py_INCREF(Py_None);
    return Py_None;
}
