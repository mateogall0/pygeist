#include <Python.h>
#include "adapters/include/server/response.h"
#include "core/include/server/api/endpoint.h"


/* PyObject * */
/* run_send_response_payload(PyObject *self, PyObject *args, PyObject *kwagrs) { */
/*     (void)self; */

/*     static char *kwlist[] = {"payload", NULL}; */

/*     char *result = NULL; */

/*     if (!PyArg_ParseTupleAndKeywords( */
/*             args, kwagrs, */
/*             "s", */
/*             kwlist, */
/*             &result)) */
/*         return (NULL); */

/*     if (!result) */
/*         return (NULL); */

/*     PyObject *str_obj = PyObject_Str(result); */
/*     Py_DECREF(result); */
/*     if (!str_obj) */
/*         return (NULL); */

/*     const char *tmp = PyUnicode_AsUTF8(str_obj); */
/*     if (tmp) */
/*         result_cstr = strdup(tmp); */
/*     Py_DECREF(str_obj); */

/*     PyGILState_Release(gstate); */
/*     return (result_cstr); */
/* } */
