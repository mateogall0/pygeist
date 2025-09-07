#include "adapters/include/server/exceptions.h"
#include "adapters/include/server/classes.h"
#include "core/include/server/api/endpoint.h"
#include <Python.h>


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

    Py_INCREF(Py_None);
    return (Py_None);
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

    Py_INCREF(Py_None);
    return (Py_None);
}

char *py_handler_wrapper(request_t *req, PyObject *py_func) {
    PyGILState_STATE gstate = PyGILState_Ensure();

    // Wrap raw C pointer in PyCapsule
    PyObject *capsule = PyCapsule_New((void *)req, "request_t", NULL);
    if (!capsule) {
        PyGILState_Release(gstate);
        return NULL;
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

    PyGILState_Release(gstate);
    return ret;
}

char *_handler(request_t *r) {
    PyGILState_STATE gstate = PyGILState_Ensure();  // acquire GIL
    char *result_cstr = NULL;

    PyObject *req_inst_args = Py_BuildValue("(is)", r->method, r->target);
    if (!req_inst_args)
        goto fail;

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

    if (PyCoro_CheckExact(handler)) {
        // async function: call with args first to get coroutine
        PyObject *coro = PyObject_CallObject(handler, args);
        if (!coro) {
            PyErr_Print();
            goto fail;
        }

        PyObject *asyncio = PyImport_ImportModule("asyncio"); // cached
        if (!asyncio) {
            Py_DECREF(coro);
            goto fail;
        }

        PyObject *loop = PyObject_CallMethod(asyncio, "get_event_loop", NULL);
        Py_DECREF(asyncio);
        if (!loop) {
            Py_DECREF(coro);
            goto fail;
        }

        result = PyObject_CallMethod(loop, "run_until_complete", "O", coro);
        Py_DECREF(loop);
        Py_DECREF(coro);
    } else // sync function: call directly with args
        result = PyObject_CallObject(handler, args);

    Py_DECREF(args);
    Py_DECREF(req_inst);

    if (!result) {
        PyErr_Print();
        goto fail;
    }

    // convert result to C string
    PyObject *str_obj = PyObject_Str(result);
    Py_DECREF(result);
    if (!str_obj) goto fail;

    const char *tmp = PyUnicode_AsUTF8(str_obj);
    if (tmp)
        result_cstr = strdup(tmp);  // allocate copy for C
    Py_DECREF(str_obj);

    PyGILState_Release(gstate);
    return (result_cstr);

fail:
    PyGILState_Release(gstate);
    return (NULL);
}

PyObject*
run_create_append_endpoint(PyObject *self,
                           PyObject *args,
                           PyObject *kwargs) {
    (void)self;
    if (!endpoints) {
        PyErr_SetString(EndpointsInit,
                        "endpoints list is not initialized");
        return (NULL);
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
        return NULL;
    }

    if (method < 0 || method >= METHODS_COUNT) {
        PyErr_SetString(PyExc_ValueError, "invalid method enum value");
        return NULL;
    }

    endpoint_t *e = set_endpoint_va(3, method, target, _handler);
    Py_INCREF(py_handler);
    e->meta = (uintptr_t)py_handler;

    Py_INCREF(Py_None);
    return (Py_None);
}

PyObject*
run_print_all_endpoints(PyObject *self) {
    (void)self;

    pall_endpoints();

    Py_INCREF(Py_None);
    return (Py_None);
}
