#include <Python.h>
#include "adapters/include/server/exceptions.h"
#include "adapters/include/server/classes.h"
#include "adapters/include/server/config.h"
#include "core/include/server/api/endpoint.h"


PyObject*
run_init_endpoints_list(PyObject *self) {
    PyGILState_STATE gstate = PyGILState_Ensure();
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

    PyObject *args = PyTuple_New(1);
    if (!args) {
        Py_DECREF(req_inst);
        goto fail;
    }
    Py_INCREF(req_inst);
    PyTuple_SetItem(args, 0, req_inst);

    PyObject *handler = (PyObject *)r->endpoint->meta;
    PyObject *result = NULL;

    // Import inspect module to detect async functions
    PyObject *inspect = PyImport_ImportModule("inspect");
    if (!inspect) {
        PyErr_Print();
        goto fail_args;
    }

    PyObject *is_coro_func = PyObject_CallMethod(inspect, "iscoroutinefunction", "O", handler);
    Py_DECREF(inspect);
    if (!is_coro_func) {
        PyErr_Print();
        goto fail_args;
    }

    int async_func = PyObject_IsTrue(is_coro_func);
    Py_DECREF(is_coro_func);

    if (async_func) {
        // async function: create coroutine
        PyObject *coro = PyObject_CallObject(handler, args);
        if (!coro) {
            PyErr_Print();
            goto fail_args;
        }
        PyObject *queue_helper = PyImport_ImportModule(ZSERVER_MODULE_NAME ".concurrency.queue");
        if (!queue_helper) {
            PyErr_Print();
            goto fail_args;
        }


        PyObject *res = PyObject_CallMethod(queue_helper, "push_async", "O", coro);
        if (!res) {
            PyErr_Print();
        } else {
            Py_DECREF(res);
        }
        Py_XDECREF(coro);

        Py_XDECREF(args);
        Py_XDECREF(req_inst);
        goto fail;
    } else {
        // sync function: call directly
        result = PyObject_CallObject(handler, args);
    }

fail_args:
    Py_DECREF(args);
    Py_DECREF(req_inst);

    if (!result) {
        PyErr_Print();
        goto fail;
    }

    // convert result to C string
    PyObject *str_obj = PyObject_Str(result);
    Py_DECREF(result);
    if (!str_obj)
        goto fail;

    const char *tmp = PyUnicode_AsUTF8(str_obj);
    if (tmp)
        result_cstr = strdup(tmp);
    Py_DECREF(str_obj);

    return (result_cstr);

fail:
    return (NULL);
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
    Py_INCREF(py_handler);
    e->meta = (uintptr_t)py_handler;

    Py_RETURN_NONE;
}

PyObject*
run_print_all_endpoints(PyObject *self) {
    (void)self;

    pall_endpoints();

    Py_RETURN_NONE;
}
