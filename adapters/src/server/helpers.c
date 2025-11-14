#include "adapters/include/server/helpers.h"
#include "adapters/include/server/config.h"

PyObject *run_handler_func = NULL;

int
init_helpers() {
    PyObject *helpers = PyImport_ImportModule(ZSERVER_MODULE_NAME ".concurrency.helpers");
    if (!helpers) {
        return 1;
    }

    run_handler_func = PyObject_GetAttrString(helpers, "run_handler");
    if (!run_handler_func)
        return 1;
    Py_DECREF(helpers);
    return 0;
}
