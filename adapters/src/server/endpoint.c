#include <Python.h>
#include "adapters/include/server/exceptions.h"
#include "adapters/include/server/classes.h"
#include "adapters/include/server/config.h"
#include "core/include/server/api/endpoint.h"
#include "core/include/debug.h"


PyObject*
run_init_endpoints_list(PyObject *self) {
    (void)self;
    if (endpoints) {
        PyErr_SetString(EndpointsInit,
                        "endpoints list are already initialized");
        return (NULL);
    }
    if (!init_endpoints_list()) {
        PyErr_SetString(EndpointsInit,
                        "endpoints list couldn't be initialized");
        return (NULL);
    }

    Py_RETURN_NONE;
}

PyObject*
run_destroy_endpoints_list(PyObject *self) {
    (void)self;
    if (!endpoints) {
        PyErr_SetString(EndpointsDestruct,
                        "endpoints list is not initialized");
        return (NULL);
    }
    destroy_endpoints();

    Py_RETURN_NONE;
}

char *_handler(request_t *r) {
    print_debug("Internal handler before getting the GIL\n");
    PyGILState_STATE gstate = PyGILState_Ensure();
    print_debug("Reached internal _handler\n");

    PyObject *req_inst_args = Py_BuildValue("(isssik)",
                                            r->method,
                                            r->target,
                                            r->body,
                                            r->headers,
                                            r->client_fd,
                                            r->id);
    if (!req_inst_args)
        goto fail;

    if (!RequestClass) {
        PyErr_SetString(PyExc_RuntimeError, "RequestClass not initialized!");
        goto fail;
    }

    PyObject *req_inst = PyObject_CallObject(RequestClass, req_inst_args);
    Py_DECREF(req_inst_args);
    if (!req_inst)
        goto fail;

    PyObject *args = PyTuple_Pack(1, req_inst);
    Py_DECREF(req_inst);
    if (!args)
        goto fail;

    PyObject *handler = (PyObject *)r->endpoint->meta;
    PyObject *result = NULL;

    PyObject *helpers = PyImport_ImportModule(ZSERVER_MODULE_NAME ".concurrency.helpers");
    if (!helpers) {
        goto fail_args;
    }

    PyObject *run_handler_func = PyObject_GetAttrString(helpers, "run_handler");
    Py_DECREF(helpers);
    if (!run_handler_func) {
        goto fail_args;
    }
    PyObject *run_args = Py_BuildValue("(OO)", handler, req_inst);
    if (!run_args) {
        Py_DECREF(run_handler_func);
        goto fail_args;
    }

    print_debug("About to call async helper from C\n");
    result = PyObject_CallObject(run_handler_func, run_args);
    if (result) Py_DECREF(result);
    Py_DECREF(run_handler_func);
    Py_DECREF(run_args);
    print_debug("Finished call async helper from C\n");

fail_args:
    Py_DECREF(args);
    PyGILState_Release(gstate);
    print_debug("Finished internal endpoint process\n");
    return NULL;

fail:
    PyGILState_Release(gstate);
    print_debug("(fail) Finished internal endpoint process\n");
    return NULL;
}

PyObject*
run_create_append_endpoint(PyObject *self,
                           PyObject *args,
                           PyObject *kwargs) {
    (void)self;
    if (!endpoints) {
        if (!init_endpoints_list()) {
            PyErr_SetString(EndpointsInit,
                            "endpoints list couldn't be initialized");
            return (NULL);
        }
    }

    static char *kwlist[] = {"method", "target", "handler", NULL};
    int method;
    PyObject *py_handler;
    char *target = NULL;

    if (!PyArg_ParseTupleAndKeywords(
            args, kwargs,
            "isO",
            kwlist,
            &method,
            &target,
            &py_handler))
        return (NULL);
    if (!PyCallable_Check(py_handler)) {
        PyErr_SetString(PyExc_TypeError, "handler must be a callable");
        return (NULL);
    }

    if (method < 0 || method >= METHODS_COUNT) {
        PyErr_SetString(PyExc_ValueError, "invalid method enum value");
        return (NULL);
    }

    endpoint_t *e = set_endpoint_va(4, method, target, _handler, true);

    e->meta = (uintptr_t)py_handler;
    Py_INCREF(py_handler);

    Py_RETURN_NONE;
}

PyObject*
run_print_all_endpoints(PyObject *self) {
    (void)self;

    pall_endpoints();

    Py_RETURN_NONE;
}
