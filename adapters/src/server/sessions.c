#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "core/include/server/master.h"
#include "core/include/server/sessions/map.h"
#include "core/include/server/sessions/wheel.h"
#include "core/include/server/api/response.h"
#include "adapters/include/server/exceptions.h"
#include <stddef.h>
#include <time.h>
#include "core/include/debug.h"


PyObject*
run_initialize_sessions_structure(PyObject *self,
                                  PyObject *args,
                                  PyObject *kwargs) {
    (void)self;
    if (connected_sessions_map || connected_sessions_wheel) {
        PyErr_SetString(SessionsStructureInit, "sessions structure already initialized");
        return (NULL);
    }

    static char *kwlist[] = {"idle_timeout", "map_size", NULL};
    time_t idle_timeout = 300;
    size_t map_size = 512;

    if (!PyArg_ParseTupleAndKeywords(
            args, kwargs,
            "|II",
            kwlist,
            &idle_timeout,
            &map_size))
        return (NULL);


    initialize_sessions_structure(idle_timeout, map_size);
    if (!connected_sessions_map || !connected_sessions_wheel) {
        PyErr_SetString(SessionsStructureInit, "sessions structure didn't start correctly");
        return (NULL);
    }

    Py_RETURN_NONE;
}

PyObject*
run_destroy_sessions_structure(PyObject *self) {
    (void)self;
    if (!connected_sessions_map || !connected_sessions_wheel) {
        PyErr_SetString(SessionsStructureDestruct, "sessions struture not initialized");
        return (NULL);
    }

    destroy_connected_sessions_map();
    destroy_connected_sessions_wheel();

    Py_RETURN_NONE;
}

PyObject*
run_set_session_object(PyObject *self, PyObject *args, PyObject *kwargs) {
    (void)self;
    if (!connected_sessions_map || !connected_sessions_wheel) {
        PyErr_SetString(SessionsStructureInit, "sessions structure not initialized");
        return (NULL);
    }

    static char *kwlist[] = {"id", "value", NULL};
    int id;
    PyObject *value = NULL;

    if (!PyArg_ParseTupleAndKeywords(
            args, kwargs,
            "iO",
            kwlist,
            &id, &value))
        return (NULL);

    connected_session_t *session = NULL;
    /* Py_BEGIN_ALLOW_THREADS */
    session = get_connected_session(id);
    /* Py_END_ALLOW_THREADS */
    if (!session) {
        PyErr_SetString(SessionCreation, "session doesn't exist");
        return (NULL);
    }
    PyGILState_STATE gstate = PyGILState_Ensure();

    PyObject *old = (PyObject*)session->meta;
    if (old)
        Py_DECREF(old);

    Py_INCREF(value);
    session->meta = (uintptr_t)value;
    PyGILState_Release(gstate);
    return (value);
}

PyObject*
run_get_session_object(PyObject *self, PyObject *args, PyObject *kwargs) {
    (void)self;
    if (!connected_sessions_map || !connected_sessions_wheel) {
        PyErr_SetString(SessionsStructureInit, "sessions structure not initialized");
        return (NULL);
    }

    static char *kwlist[] = {"id", NULL};
    int id;

    if (!PyArg_ParseTupleAndKeywords(
            args, kwargs,
            "i",
            kwlist,
            &id))
        return (NULL);

    connected_session_t *session = NULL;
    /* Py_BEGIN_ALLOW_THREADS */
    session = get_connected_session(id);
    /* Py_END_ALLOW_THREADS */

    PyObject *value = NULL;
    PyGILState_STATE gstate = PyGILState_Ensure();
    value = (PyObject*)session->meta;
    if (!value) {
        Py_INCREF(Py_None);
        value = Py_None;
    } else {
        Py_INCREF(value);
    }
    PyGILState_Release(gstate);
    return value;
}

PyObject *
run_send_unrequested_payload(PyObject *self, PyObject *args, PyObject *kwargs) {
    (void)self;
    if (!connected_sessions_map || !connected_sessions_wheel) {
        PyErr_SetString(SessionsStructureInit, "sessions structure not initialized");
        return (NULL);
    }

    static char *kwlist[] = {"id", "payload", NULL};
    int id;
    char *payload = NULL;
    Py_ssize_t payload_len_size;

    if (!PyArg_ParseTupleAndKeywords(
            args, kwargs,
            "is#",
            kwlist,
            &id, &payload, &payload_len_size))
        return (NULL);

    if (payload_len_size < 0) {
        PyErr_SetString(PyExc_ValueError, "negative string length");
        return (NULL);
    }

    connected_session_t *session = NULL;
    /* Py_BEGIN_ALLOW_THREADS */
    session = get_connected_session(id);
    /* Py_END_ALLOW_THREADS */
    if (!session) {
        PyErr_SetString(SessionCreation, "session doesn't exist");
        return (NULL);
    }
    print_debug("Sending the payload from Python: %s\n", payload);
    /* Py_BEGIN_ALLOW_THREADS */
    size_t payload_size = (size_t)payload_len_size;
    send_unrequested_payload(id, payload, payload_size);
    /* Py_END_ALLOW_THREADS */

    print_debug("Sent the payload from Python: %s\n", payload);

    Py_RETURN_NONE;
}
