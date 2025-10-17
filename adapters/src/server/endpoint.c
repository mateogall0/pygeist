#include <Python.h>
#include "adapters/include/server/exceptions.h"
#include "adapters/include/server/classes.h"
#include "adapters/include/server/config.h"
#include "core/include/server/api/endpoint.h"
#include "core/include/debug.h"


PyObject*
run_init_endpoints_list(PyObject *self) {
    PyGILState_STATE gstate = PyGILState_Ensure();
    (void)self;
    if (endpoints) {
        PyErr_SetString(EndpointsInit,
                        "endpoints list are already initialized");
        PyGILState_Release(gstate);
        return (NULL);
    }
    if (!init_endpoints_list()) {
        PyErr_SetString(EndpointsInit,
                        "endpoints list couldn't be initialized");
        PyGILState_Release(gstate);
        return (NULL);
    }

    PyGILState_Release(gstate);
    Py_RETURN_NONE;
}

PyObject*
run_destroy_endpoints_list(PyObject *self) {
    PyGILState_STATE gstate = PyGILState_Ensure();
    (void)self;
    if (!endpoints) {
        PyErr_SetString(EndpointsDestruct,
                        "endpoints list is not initialized");
        PyGILState_Release(gstate);
        return (NULL);
    }
    destroy_endpoints();

    PyGILState_Release(gstate);
    Py_RETURN_NONE;
}

char *py_handler_wrapper(request_t *req, PyObject *py_func) {
    // Wrap raw C pointer in PyCapsule
    PyObject *capsule = PyCapsule_New((void *)req, "request_t", NULL);
    if (!capsule) {
        return (NULL);
    }

    // Call Python function with the capsule
    PyObject *result = PyObject_CallFunctionObjArgs(py_func, capsule, NULL);
    Py_DECREF(capsule);

    char *ret = NULL;
    if (result && PyUnicode_Check(result)) {
        const char *tmp = PyUnicode_AsUTF8(result);
        if (tmp) ret = strdup(tmp);  // dynamically allocate
        Py_DECREF(result);
    }
    return (ret);
}


char *_handler(request_t *r) {
    PyGILState_STATE gstate = PyGILState_Ensure();
    print_debug("Reached internal _handler\n");
    char *result_cstr = NULL;

    // Build Python Request instance
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

    // Detect if async
    PyObject *inspect = PyImport_ImportModule("inspect");
    if (!inspect) goto fail_args;

    PyObject *is_coro_func = PyObject_CallMethod(inspect, "iscoroutinefunction", "O", handler);
    Py_DECREF(inspect);
    if (!is_coro_func) goto fail_args;

    int async_func = PyObject_IsTrue(is_coro_func);
    Py_DECREF(is_coro_func);

    if (async_func) {

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
        Py_DECREF(run_handler_func);
        Py_DECREF(run_args);
        print_debug("Finished call async helper from C\n");
        // For async, run_handler usually returns None
        if (result) Py_DECREF(result);
        result_cstr = strdup("");  // return empty string for async
    } else {
        // sync function: call directly
        result = PyObject_CallObject(handler, args);
        if (!result) goto fail_args;

        PyObject *str_obj = PyObject_Str(result);
        Py_DECREF(result);
        if (!str_obj) goto fail_args;

        const char *tmp = PyUnicode_AsUTF8(str_obj);
        if (tmp) result_cstr = strdup(tmp);
        Py_DECREF(str_obj);
    }

fail_args:
    Py_DECREF(args);
    PyGILState_Release(gstate);
    return result_cstr;

fail:
    PyGILState_Release(gstate);
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
