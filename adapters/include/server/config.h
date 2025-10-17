#ifndef ZPYTHON_ZSERVER_CONFIG_H
#define ZPYTHON_ZSERVER_CONFIG_H

#include <Python.h>

#ifdef DEBUG
    #define ZSERVER_SYSTEM_VERBOSE true
#else
    #define ZSERVER_SYSTEM_VERBOSE false
#endif

#define ZSERVER_MODULE_NAME "pygeist"

#ifndef ZSERVER_SYSTEM_BATCH_SIZE
#define ZSERVER_SYSTEM_BATCH_SIZE 1
#endif


#endif
