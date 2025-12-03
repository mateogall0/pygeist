#include "adapters/include/server/helpers.h"
#include "adapters/include/server/config.h"

PyObject *run_handler_func = NULL;

int
init_helpers() {
    PyObject *helpers = PyImport_ImportModule(ZSERVER_MODULE_NAME ".concurrency.helpers");
    if (!helpers) {
        return 1;
    }

    PyObject *workers_queue = PyObject_GetAttrString(helpers, "workers_queue");
    Py_DECREF(helpers);
    if (!workers_queue)
        return 1;
    run_handler_func = PyObject_GetAttrString(workers_queue, "run_handler");
    Py_DECREF(workers_queue);
    Py_INCREF(run_handler_func);

    return 0;
}
