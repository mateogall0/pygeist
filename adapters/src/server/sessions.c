#include "core/include/server/master.h"
#include "core/include/server/sessions/map.h"
#include "core/include/server/sessions/wheel.h"
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

    static char *kwlist[] = {"idle_timout", "map_size", NULL};
    time_t idle_timout = 300;
    size_t map_size = 512;

    if (!PyArg_ParseTupleAndKeywords(
            args, kwargs,
            "|II",
            kwlist,
            &idle_timout,
            &map_size))
        return (NULL);


    initialize_sessions_structure(idle_timout, map_size);
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

    destroy_connected_sessions_wheel();

    Py_INCREF(Py_None);
    return (Py_None);

}
