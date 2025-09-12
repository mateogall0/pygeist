#include "core/include/server/master.h"
#include "core/include/server/sessions/map.h"
#include "core/include/server/sessions/wheel.h"
#include "core/include/server/api/response.h"
#include "adapters/include/server/exceptions.h"
#include <Python.h>
#include <stddef.h>
#include <time.h>


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

    Py_INCREF(Py_None);
    return (Py_None);
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

    Py_INCREF(Py_None);
    return (Py_None);

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

    connected_session_t *session = get_connected_session(id);
    if (!session) {
        PyErr_SetString(SessionCreation, "session doesn't exist");
        return (NULL);
    }
    session->meta = (uintptr_t)value;

    Py_INCREF(value);
    return value;
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

    connected_session_t *session = get_connected_session(id);
    if (!session) {
        PyErr_SetString(SessionCreation, "session doesn't exist");
        return (NULL);
    }
    PyObject *value = (PyObject *)session->meta;

    Py_INCREF(value);
    return (value);
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

    connected_session_t *session = get_connected_session(id);
    if (!session) {
        PyErr_SetString(SessionCreation, "session doesn't exist");
        return (NULL);
    }
    size_t payload_size = (size_t)payload_len_size;

    send_unrequested_payload(id, payload, payload_size);

    Py_INCREF(Py_None);
    return (Py_None);
}
