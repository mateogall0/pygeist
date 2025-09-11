#ifndef ZPYTHON_ZSERVER_SESSIONS_H
#define ZPYTHON_ZSERVER_SESSIONS_H


PyObject*
run_initialize_sessions_structure(PyObject *self, PyObject *args, PyObject *kwargs);

PyObject*
run_destroy_sessions_structure(PyObject *self);

PyObject*
run_set_session_object(PyObject *self, PyObject *args, PyObject *kwargs);

PyObject*
run_get_session_object(PyObject *self, PyObject *args, PyObject *kwargs);

PyObject *
run_send_unrequested_payload(PyObject *self, PyObject *args, PyObject *kwargs);

#endif
