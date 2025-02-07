"""
Copyright (c) 2025 ANSYS, Inc.

This program is commercial software: you can use it under the terms of the
Ansys License Agreement as published by ANSYS, Inc.

Except as expressly permitted in the Ansys License Agreement, you may not
modify or redistribute this program.
"""

import sys
if not sys.maxsize > 2**32:
    print("Error: 32-bit Python is not supported.")
    sys.exit()

from ctypes import Structure, Union, POINTER, CDLL, c_char, c_int, c_uint, c_ulonglong, c_double, c_char_p, c_void_p, \
    byref, memmove, addressof
import inspect
import json
import os
import platform
import re
import weakref
import numpy as np
import warnings
import collections
import types

from .configure import environ, initLib, Session, Any, LumString, LumMat, LumNameValuePair, LumStruct, LumList, ValUnion, InteropPaths, remoteModuleOn

class LumApiSession:
    def __init__(self, iapiArg, handleArg):
        self.iapi = iapiArg
        self.handle = handleArg
        self.__doc__ = "handle to the session"


def lumWarning(message):
    print("{!!}")
    warnings.warn(message)
    print("")


class LumApiError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def verifyConnection(handle):
    try:
        if isinstance(handle, LumApiSession) and handle.handle is not None:
            return handle.iapi.appOpened(handle.handle)
    except:
            raise LumApiError("Error validating the connection")


biopen = open

def extractsHostnameAndPort(remoteArgs):
    hostname_key = "hostname"
    port_key = "port"
    hostname = "localhost"
    port = 8989 # default port

    if hostname_key in remoteArgs:
        hostname = remoteArgs[hostname_key]
        
        if port_key in remoteArgs:
            port = remoteArgs[port_key]

    return hostname + ":" + str(port)


def open(product, key=None, hide=False, serverArgs={}, remoteArgs={}):
    '''
    Adds a key/value 'keepCADOpened'=False to achieve the same behaviour we had before the remote API.
    Previously, when the user called open() the CAD would be opened and a handle to it returned also 
    the CAD would run until closed by the user or the Python interpreter shutdown.
    We weren't instantiating a Lumerical object subclass but now we are and the instance is deleted once 
    it goes out of scope or the Python interpreter is terminated.
    '''
    serverArgs['keepCADOpened'] = True 
    if product == "interconnect":
        return INTERCONNECT(None, key, hide, serverArgs, remoteArgs)
    elif product == "fdtd":
        return FDTD(None, key, hide, serverArgs, remoteArgs)
    elif product == "mode":
        return MODE(None, key, hide, serverArgs, remoteArgs)
    elif product == "device":
        return DEVICE(None, key, hide, serverArgs, remoteArgs)
    else:
        raise LumApiError("Product [" + product + "] is not available")

def close(handle):
    try:
        if isinstance(handle, Lumerical):
            handle.close()
        else:
            if isinstance(handle, LumApiSession) and handle.handle is not None:
                handle.iapi.appClose(handle.handle)
                handle = None
    except:
        raise LumApiError("Error closing a connection")


def _evalScriptInternal(handle, code):
    ec = handle.iapi.appEvalScript(handle.handle, code.encode())
    if ec < 0:
        raise LumApiError("Failed to evaluate code")


def evalScript(handle, code, verifyConn = False):
    if isinstance(handle, Lumerical):
        s = handle.handle
    else:
        s = handle

    if verifyConn is True: 
        verifyConnection(s)

    _evalScriptInternal(s, code)


def _getVarInternal(s, varname):
    value = POINTER(Any)()

    ec = s.iapi.appGetVar(s.handle, varname.encode(), byref(value))
    if ec < 0:
        raise LumApiError("Failed to get variable")

    r = 0.
    valType = value[0].type

    if valType < 0:
        raise LumApiError("Failed to get variable")

    if valType == 0:
        ls = value[0].val.strVal
        r = ''
        rawData = bytearray()
        for i in range(ls.len): rawData += ls.str[i]
        r = rawData.decode()
    elif valType == 1:
        r = float(value[0].val.doubleVal)
    elif valType == 2:
        r = unpackMatrix(s, value[0].val.matrixVal)
    elif valType == 4:
        r = GetTranslator.getStructMembers(s, value[0])
    elif valType == 5:
        r = GetTranslator.getListMembers(s, value[0])

    s.iapi.freeAny(value)

    return r


def getVar(handle, varname, verifyConn = False):
    if isinstance(handle, Lumerical):
        s = handle.handle
    else:
        s = handle

    if verifyConn is True: 
        verifyConnection(s)

    return _getVarInternal(s, varname)


def putString(handle, varname, value, verifyConn = False):
    if isinstance(handle, Lumerical):
        s = handle.handle
    else:
        s = handle

    if verifyConn is True: 
        verifyConnection(s)
    try:
        v = str(value).encode()
    except:
        raise LumApiError("Unsupported data type")

    a = s.iapi.allocateLumString(len(v), v)
    ec = s.iapi.appPutVar(s.handle, varname.encode(), a)

    if ec < 0: raise LumApiError("Failed to put variable")


def putMatrix(handle, varname, value, verifyConn = False):
    if isinstance(handle, Lumerical):
        s = handle.handle
    else:
        s = handle

    if verifyConn is True: 
        verifyConnection(s)
    a = packMatrix(s, value)

    ec = s.iapi.appPutVar(s.handle, varname.encode(), a)

    if ec < 0: raise LumApiError("Failed to put variable")


def putDouble(handle, varname, value, verifyConn = False):
    if isinstance(handle, Lumerical):
        s = handle.handle
    else:
        s = handle

    if verifyConn is True: 
        verifyConnection(s)
    try:
        v = float(value)
    except:
        raise LumApiError("Unsupported data type")

    a = s.iapi.allocateLumDouble(v)

    ec = s.iapi.appPutVar(s.handle, varname.encode(), a)

    if ec < 0: raise LumApiError("Failed to put variable")


def putStruct(handle, varname, values, verifyConn = False):
    if isinstance(handle, Lumerical):
        s = handle.handle
    else:
        s = handle
        
    if verifyConn is True: 
        verifyConnection(s)
    nvlist = 0
    try:
        nvlist = PutTranslator.putStructMembers(s, values)
    except LumApiError as e:
        raise
    except:
        raise LumApiError("Unknown exception")

    a = PutTranslator.translateStruct(s, nvlist)

    ec = s.iapi.appPutVar(s.handle, varname.encode(), a)

    if ec < 0: raise LumApiError("Failed to put variable")


def _putListInternal(s, varname, values):
    llist = 0
    try:
        llist = PutTranslator.putListMembers(s, values)
    except LumApiError as e:
        raise
    except:
        raise LumApiError("Unknown exception")

    a = PutTranslator.translateList(s, llist)

    ec = s.iapi.appPutVar(s.handle, varname.encode(), a)

    if ec < 0: raise LumApiError("Failed to put variable")


def putList(handle, varname, values, verifyConn = False):
    if isinstance(handle, Lumerical):
        s = handle.handle
    else:
        s = handle
   
    if verifyConn is True: 
        verifyConnection(s)

    _putListInternal(s, varname, values)



#### Support classes and functions ####
def packMatrix(handle, value):
    try:
        if 'numpy.ndarray' in str(type(value)):
            v = value
        else:
            v = np.array(value, order='F')

        if v.dtype != complex and "float" not in str(v.dtype):
            v = v.astype(dtype="float64", casting="unsafe", order='F')
    except:
        raise LumApiError("Unsupported data type")

    dim = c_ulonglong(v.ndim)
    dimlist = c_ulonglong * v.ndim
    dl = dimlist()
    for i in range(v.ndim):
        dl[i] = v.shape[i]
    v = np.asfortranarray(v)

    srcPtr = v.ctypes.data_as(POINTER(c_double))
    if v.dtype == complex:
        a = handle.iapi.allocateComplexLumMatrix(dim, dl)
        destPtr = a[0].val.matrixVal.data
        handle.iapi.memmovePackComplexLumMatrix(destPtr, srcPtr, v.size)
    else:
        a = handle.iapi.allocateLumMatrix(dim, dl)
        destPtr = a[0].val.matrixVal.data
        memmove(destPtr, srcPtr, 8 * v.size)

    return a


def unpackMatrix(handle, value):
    lumatrix = value
    l = 1
    dl = [0] * lumatrix.dim
    for i in range(lumatrix.dim):
        l *= lumatrix.dimlst[i]
        dl[i] = lumatrix.dimlst[i]

    if lumatrix.mode == 1:
        r = np.empty(l, dtype="float64", order='F')
        destPtr = r.ctypes.data_as(POINTER(c_double))
        memmove(destPtr, lumatrix.data, l * 8)
        r = r.reshape(dl, order='F')
    else:
        r = np.empty(l, dtype=complex, order='F')
        destPtr = r.ctypes.data_as(POINTER(c_double))
        handle.iapi.memmoveUnpackComplexLumMatrix(destPtr, lumatrix.data, l)
        r = r.reshape(dl, order='F')

    return r

class MatrixDatasetTranslator:
    @staticmethod
    def _applyConventionToStructAttribute(d, attribName):
        # [1, ncomp, npar_1, npar_2, ...] -> [npar_1, npar_2, ..., ncomp]
        if (d[attribName].shape[0] != 1) or (d[attribName].ndim < 2):
            raise LumApiError("Inconsistency between dataset metadata and attribute dimension")
        desiredShape = list(np.roll(d[attribName].shape[1:], -1))
        if desiredShape[-1] == 1:
            del desiredShape[-1]
        d[attribName] = np.reshape(np.rollaxis(d[attribName], 1, d[attribName].ndim), desiredShape)

    @staticmethod
    def applyConventionToStruct(d):
        for attribName in d["Lumerical_dataset"].get("attributes", []):
            MatrixDatasetTranslator._applyConventionToStructAttribute(d, attribName)

    @staticmethod
    def createStructMemberPreTranslators(d):
        metaData = d["Lumerical_dataset"]
        numParamDims = len(metaData.get("parameters", []))

        # [npar_1, npar_2, ..., ncomp]
        ncomp = lambda v: v.shape[-1] if (v.ndim > numParamDims) else 1

        if numParamDims:
            # [...] -> [1, ncomp, npar_1, npar_2, ...]
            attribPreTranslator = lambda v: np.rollaxis(np.reshape(v, [1] + list(v.shape[:numParamDims]) + [ncomp(v)]), -1, 1)
        else:
            # [...] -> [1, ncomp]
            attribPreTranslator = lambda v: np.reshape(v, [1, ncomp(v)])
        return dict([(attribName, attribPreTranslator) for attribName in metaData.get("attributes", [])]) 


class PointDatasetTranslator:
    @staticmethod
    def _applyConventionToStructAttribute(d, attribName, geometryShape, paramShape, removeScalarDim):
        # [npts, ncomp, npar_1, npar_2, ...] -> [npts_x, npts_y, npts_z, npar_1, npar_2, ..., ncomp]
        #                                        or               [npts, npar_1, npar_2, ..., ncomp]
        interimShape = list(geometryShape)
        interimShape.append(d[attribName].shape[1])
        interimShape.extend(paramShape)
        desiredShape = list(geometryShape)
        desiredShape.extend(paramShape)
        desiredShape.append(d[attribName].shape[1])
        if (desiredShape[-1] == 1) and removeScalarDim:
            del desiredShape[-1]
        d[attribName] = np.reshape(
            np.rollaxis(np.reshape(d[attribName], interimShape, order='F'), len(geometryShape), len(interimShape)),
            desiredShape)

    @staticmethod
    def _applyConventionToStructCellAttribute(d, attribName):
        # [ncell, ncomp, 1] -> [ncell, ncomp]
        d[attribName] = np.reshape(d[attribName], d[attribName].shape[:2])

    @staticmethod
    def applyConventionToStruct(d, geometryShape, paramShape, removeScalarDim):
        for attribName in d["Lumerical_dataset"].get("attributes", []):
            PointDatasetTranslator._applyConventionToStructAttribute(d, attribName, geometryShape, paramShape,
                                                                     removeScalarDim)
        for attribName in d["Lumerical_dataset"].get("cell_attributes", []):
            PointDatasetTranslator._applyConventionToStructCellAttribute(d, attribName)

    @staticmethod
    def createStructMemberPreTranslators(d, numGeomDims):
        metaData = d["Lumerical_dataset"]
        numParamDims = len(metaData.get("parameters", []))

        # [npts_x, npts_y, npts_z, npar_1, npar_2, ..., ncomp]
        # or               [npts, npar_1, npar_2, ..., ncomp]
        wrongNumberDims = lambda v: (v.ndim < (numGeomDims + numParamDims) or v.ndim > (numGeomDims + numParamDims + 1))
        npts = lambda v: np.prod(v.shape[:numGeomDims])
        nparList = lambda v: list(v.shape[numGeomDims:numGeomDims + numParamDims])
        ncomp = lambda v: v.shape[-1] if (v.ndim > numGeomDims + numParamDims) else 1

        if numParamDims:
            # [...] -> [npts, ncomp, npar_1, npar_2, ...]
            attribPreTranslator = lambda v: np.rollaxis(np.reshape(v, [npts(v)] + nparList(v) + [ncomp(v)], order='F'),
                                                        -1, 1)
        else:
            # [...] -> [npts, ncomp]
            attribPreTranslator = lambda v: np.reshape(v, [npts(v), ncomp(v)], order='F')

        # [ncell, ncomp] -> [ncell, ncomp, 1]
        cellWrongNumberDims = lambda v: (v.ndim != 2)
        cellPreTranslator = lambda v: np.reshape(v, list(v.shape) + [1])

        preTransDict = {}
        for attribName in metaData.get("attributes", []):
            if wrongNumberDims(d[attribName]):
                raise LumApiError("Inconsistency between dataset metadata and attribute data shape")
            preTransDict[attribName] = attribPreTranslator
        for attribName in metaData.get("cell_attributes", []):
            if cellWrongNumberDims(d[attribName]):
                raise LumApiError("Inconsistency between dataset metadata and attribute data shape")
            preTransDict[attribName] = cellPreTranslator
        return preTransDict


class RectilinearDatasetTranslator:
    @staticmethod
    def applyConventionToStruct(d):
        metaData = d["Lumerical_dataset"]
        geometryShape = [d["x"].size, d["y"].size, d["z"].size]
        paramShape = []
        for param in metaData.get("parameters", []):
           paramShape.append((d[param[0]]).size if hasattr(d[param[0]], 'size') else len(d[param[0]]))
        removeScalarDim = True
        PointDatasetTranslator.applyConventionToStruct(d, geometryShape, paramShape, removeScalarDim)

    @staticmethod
    def createStructMemberPreTranslators(d):
        return PointDatasetTranslator.createStructMemberPreTranslators(d, numGeomDims=3)


class UnstructuredDatasetTranslator:
    @staticmethod
    def applyConventionToStruct(d):
        metaData = d["Lumerical_dataset"]
        geometryShape = [d["x"].size]  # == [d["y"].size] == [d["z"].size]
        paramShape=[]
        for param in metaData.get("parameters", []):
           paramShape.append((d[param[0]]).size if hasattr(d[param[0]], 'size') else len(d[param[0]]))
        removeScalarDim = False
        PointDatasetTranslator.applyConventionToStruct(d, geometryShape, paramShape, removeScalarDim)

    @staticmethod
    def createStructMemberPreTranslators(d):
        return PointDatasetTranslator.createStructMemberPreTranslators(d, numGeomDims=1)


class PutTranslator:
    @staticmethod
    def translateStruct(handle, value):
        return handle.iapi.allocateLumStruct(len(value), value)

    @staticmethod
    def translateList(handle, values):
        return handle.iapi.allocateLumList(len(values), values)

    @staticmethod
    def translate(handle, value):
        strTypes = [bytes, str]
        if type(value) in strTypes:
            v = str(value).encode()
            return handle.iapi.allocateLumString(len(v), v)
        elif type(value) is float or type(value) is int or type(value) is bool:
            return handle.iapi.allocateLumDouble(float(value))
        elif 'numpy.ndarray' in str(type(value)):
            return packMatrix(handle, value)
        elif 'numpy.float' in str(type(value)):
            value = float(value)
            return handle.iapi.allocateLumDouble(value)
        elif 'numpy.int' in str(type(value)) or 'numpy.uint' in str(type(value)):
            value=int(value)
            return handle.iapi.allocateLumDouble(float(value))
        elif type(value) is dict:
            return PutTranslator.translateStruct(handle, PutTranslator.putStructMembers(handle, value))
        elif type(value) is list:
            return PutTranslator.translateList(handle, PutTranslator.putListMembers(handle, value))
        else:
            raise LumApiError("Unsupported data type")

    @staticmethod
    def createStructMemberPreTranslators(value):
        try:
            metaData = value["Lumerical_dataset"]
        except KeyError:
            return {}
        metaDataGeometry = metaData.get("geometry", None)
        try:
            if metaDataGeometry == None:
                return MatrixDatasetTranslator.createStructMemberPreTranslators(value)
            elif metaDataGeometry == 'rectilinear':
                return RectilinearDatasetTranslator.createStructMemberPreTranslators(value)
            elif metaDataGeometry == 'unstructured':
                return UnstructuredDatasetTranslator.createStructMemberPreTranslators(value)
            else:
                raise LumApiError("Unsupported dataset geometry")
        except LumApiError:
            raise
        except AttributeError:
            raise LumApiError("Inconsistency between dataset metadata and available attributes")

    @staticmethod
    def putStructMembers(handle, value):
        preTranslatorDict = PutTranslator.createStructMemberPreTranslators(value)
        nvlist = (POINTER(Any) * len(value))()
        index = 0
        for key in value:
            preTranslator = preTranslatorDict.get(key, lambda v: v)
            nvlist[index] = handle.iapi.allocateLumNameValuePair(len(key), key.encode(),
                                                          PutTranslator.translate(handle, preTranslator(value[key])))
            index += 1
        return nvlist

    @staticmethod
    def putListMembers(handle, value):
        llist = (POINTER(Any) * len(value))()
        index = 0
        for v in value:
            llist[index] = PutTranslator.translate(handle, v)
            index += 1
        return llist


class GetTranslator:
    @staticmethod
    def translateString(strVal):
        ls = strVal
        rawData = bytearray()
        for i in range(ls.len): rawData += ls.str[i]
        return rawData.decode()

    @staticmethod
    def recalculateSize(size, elements):
        if size == 0:
            return list()
        ptr = Any.from_address(addressof(elements[0]))
        return (POINTER(Any) * size).from_address(addressof(elements[0]))

    @staticmethod
    def translate(handle, d, element):
        if element.type == 0:
            return GetTranslator.translateString(element.val.strVal)
        elif element.type == 1:
            return element.val.doubleVal
        elif element.type == 2:
            return unpackMatrix(handle, element.val.matrixVal)
        elif element.type == 3:
            name = GetTranslator.translateString(element.val.nameValuePairVal.name)
            d[name] = GetTranslator.translate(handle, d, element.val.nameValuePairVal.value[0])
            return d
        elif element.type == 4:
            return GetTranslator.getStructMembers(handle, element)
        elif element.type == 5:
            return GetTranslator.getListMembers(handle, element)
        else:
            raise LumApiError("Unsupported data type")

    @staticmethod
    def applyLumDatasetConventions(d):
        try:
            metaData = d["Lumerical_dataset"]
        except KeyError:
            return
        metaDataGeometry = metaData.get("geometry", None)
        try:
            if metaDataGeometry == None:
                MatrixDatasetTranslator.applyConventionToStruct(d)
            elif metaDataGeometry == 'rectilinear':
                RectilinearDatasetTranslator.applyConventionToStruct(d)
            elif metaDataGeometry == 'unstructured':
                UnstructuredDatasetTranslator.applyConventionToStruct(d)
            else:
                raise LumApiError("Unsupported dataset geometry")
        except LumApiError:
            raise
        except AttributeError:
            raise LumApiError("Inconsistency between dataset metadata and available attributes")
        except IndexError:
            raise LumApiError("Inconsistency between dataset metadata and attribute data")

    @staticmethod
    def getStructMembers(handle, value):
        elements = GetTranslator.recalculateSize(value.val.structVal.size,
                                                 value.val.structVal.elements)
        d = {}
        for index in range(value.val.structVal.size):
            d.update(GetTranslator.translate(handle, d, Any.from_address(addressof(elements[index][0]))))
        GetTranslator.applyLumDatasetConventions(d)
        return d

    @staticmethod
    def getListMembers(handle, value):
        d = []
        elements = GetTranslator.recalculateSize(value.val.listVal.size,
                                                 value.val.listVal.elements)
        for index in range(value.val.listVal.size):
            s = []
            e = GetTranslator.translate(handle, s, Any.from_address(addressof(elements[index][0])))
            if len(s):
                d.append(s)
            else:
                d.append(e)
        return d


# helper function
def removePromptLineNo(strval):
    message = strval
    first = message.find(':')
    second = message.find(':', first + 1, len(message) - 1)
    if (first != -1) and (second != -1):
        substr = message[first:second]
        if 'prompt line ' in substr:
            message = message[:first] + message[second:]
    return message


def appCallWithConstructor(self, funcName, *args, **kwargs):
    appCall(self, funcName, *args)
    if "properties" in kwargs:
        if not isinstance(kwargs["properties"], collections.OrderedDict):
            lumWarning("It is recommended to use an ordered dict for properties,"
                            "as regular dict elements can be re-ordered by Python")
        for key, value in kwargs["properties"].items():
            try:
                self.set(key, value)
            except LumApiError as e:
                if "inactive" in str(e):
                    raise AttributeError("In '%s', '%s' property is inactive" % (funcName, key))
                else:
                    raise AttributeError("Type added by '%s' doesn't have '%s' property" % (funcName, key))
    for key, value in kwargs.items():
        if key == "properties":
            pass
        else:
            try:
                self.set(key.replace('_', ' '),value)
            except LumApiError as e:
                try:
                    key = key.replace(' ', '_')
                    self.set(key, value)
                except LumApiError as e:
                    if "inactive" in str(e):
                        raise AttributeError("In '%s', '%s' property is inactive" % (funcName, key))
                    else:
                        raise AttributeError("Type added by '%s' doesn't have '%s' property" % (funcName, key))
    return self.getObjectBySelection()


def appCall(self, name, *args):
    """Calls a function in Lumerical script

    This function calls the named Lumerical script function passing
    all the positional arguments. If the Lumerical script function
    raises an error, this will raise a Python exception. Otherwise the return
    value of the Lumerical script function is returned
    """
    verifyConnection(self.handle)

    vname = 'internal_lum_script_' + str(np.random.randint(10000, 100000))
    vin = vname + 'i'
    vout = vname + 'o'
    _putListInternal(self.handle, vin, list(args[0]))

    code = '%s = cell(3);\n' % vout
    code += 'try{\n'
    code += '%s{1} = %s' % (vout, name)

    first = True
    for i in range(len(args[0])):
        if first:
            code += '('
        else:
            code += ','
        code += '%s{%d}' % (vin, i + 1)
        first = False

    if len(args[0]) > 0: code += ')'
    code += ';\n%s{2} = 1;\n' % vout
    # API doesn't support NULL. Use a random string to represent NULL
    # chance that this string ever collides with a real string is nil
    code += 'if(isnull(%s{1})){%s{1}="d6d8d1b2c083c251";}' % (vout, vout)
    code += '}catch(%s{3});' % vout

    try:
        _evalScriptInternal(self.handle, code)
    except LumApiError:
        pass
    rvals = _getVarInternal(self.handle, vout)
    _evalScriptInternal(self.handle, 'clear(%s,%s);' % (vin, vout))

    if rvals[1] < 0.9:
        message = re.sub(r'^(Error:)\s(prompt line)\s[0-9]+:', '', str(rvals[2])).strip()
        if "argument" in message and ("must be one of" in message or "type is not supported" in message or "is incorrect" in message):
            argLumTypes = lumTypes(list(args[0]))
            message += (" - " + name + " arguments were converted to (" + ", ".join(argLumTypes) + ")")
        raise LumApiError(message)
    if isinstance(rvals[0], str) and (rvals[0] == "d6d8d1b2c083c251"):
        rvals[0] = None
    return rvals[0]


def lumTypes(argList):
    if type(argList) is not list:
        return

    converted = list()
    for arg in argList:
        if "numpy" in str(type(arg)):
            converted.append("matrix")
        elif type(arg) is list:
            converted.append("cell array")
        else:
            converted.append(str(type(arg))[7:-2])
    return converted


class SimObjectResults(object):
    """An object containing all the results of a simulation objects

    This object has attributes that match each of the results of the simulation
    object in the Lumerical application. The attribute names are the same as
    the result names, except underscore characters are replaced with spaces if the
    original attribute name is not found in the results.

    Attributes can be read and result data is retrieved each time the attribute
    is read. For results with a large amount of data you should avoid repeatedly
    accessing the attribute. Instead, store the result of the attribute in
    a local variable.

    Writing to results is not supported and will have no effect on the result
    of the simulation object.
    """

    def __init__(self, parent):
        self._parent = weakref.ref(parent)

    def __dir__(self):
        try:
            gparent = self._parent()._parent
            resultNames = gparent.getresult(self._parent()._id.name).split("\n")
        except LumApiError:
            resultNames = list()
        return dir(super(SimObjectResults, self)) + resultNames

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __setitem__(self, name, value):
        self.__setattr__(name, value)

    def __getattr__(self, name):
        try:
            gparent = self._parent()._parent
            # build a name map to handle names with spaces
            nList = gparent.getresult(self._parent()._id.name).split("\n")

            nDict = dict()
            for x in nList: nDict[x] = x

            return gparent.getresult(self._parent()._id.name, nDict.get(name, name))
        except LumApiError:
            try:
                name = name.replace('_', ' ')
                return gparent.getresult(self._parent()._id.name, nDict.get(name, name))

            except LumApiError:
                raise AttributeError("'SimObjectResults' object has no attribute '%s'" % name)

    def __setattr__(self, name, value):
        if (name[0] == '_'):
            return object.__setattr__(self, name, value)

        gparent = self._parent()._parent
        nList = gparent.getresult(self._parent()._id.name).split("\n")
        nList = [x for x in nList]
        if (name in nList):
            raise LumApiError("Attribute '%s' can not be set" % name)
        else:
            return object.__setattr__(self, name, value)


class GetSetHelper(dict):
    """Object that allows chained [] and . statements"""

    def __init__(self, owner, name, **kwargs):
        super(GetSetHelper, self).__init__(**kwargs)
        self._owner = weakref.proxy(owner)
        self._name = name

    def __getitem__(self, key):
        try:
            val = dict.__getitem__(self, key)
        except KeyError:
            raise AttributeError("'%s' property has no '%s' sub-property" % (self._name, key))
        if isinstance(val, GetSetHelper):
            return val
        else:
            return self._owner._parent.getnamed(self._owner._id.name, val, self._owner._id.index)

    def __setitem__(self, key, val):
        try:
            location = dict.__getitem__(self, key)
        except KeyError:
            raise AttributeError("'%s' property has no '%s' sub-property" % (self._name, key))
        self._owner._parent.setnamed(self._owner._id.name, location, val, self._owner._id.index)

    def __getattr__(self, key):
        try:
            val = dict.__getitem__(self,key)
        except KeyError:
            key = key.replace('_', ' ')
            try:
                val = dict.__getitem__(self, key)
            except KeyError:
                raise AttributeError("'%s' property has no '%s' sub-property" % (self._name, key))
        if isinstance(val, GetSetHelper):
            return val
        else:
            return self._owner._parent.getnamed(self._owner._id.name, val, self._owner._id.index)

    def __setattr__(self, key, val):
        if (key[0] == '_'):
            return object.__setattr__(self, key, val)
        else:
            try:
                location = dict.__getitem__(self, key)
            except KeyError:
                key = key.replace('_', ' ')
                try:
                    location = dict.__getitem__(self, key)
                except KeyError:
                    raise AttributeError("'%s' property has no '%s' sub-property" % (self._name, key))
            self._owner._parent.setnamed(self._owner._id.name, location, val, self._owner._id.index)

    def __repr__(self):
        dictrepr = dict.__repr__(self)
        return '%s<%s>(%s)' % (type(self).__name__, self._name, dictrepr)


class SimObjectId(object):
    """Object respresenting a weak reference to a simulation object"""

    def __init__(self, id):
        idParts = id.rsplit('#', 1)
        self.name = idParts[0]
        self.index = int(idParts[1]) if len(idParts) > 1 else 1


class SimObject(object):
    """An object representing simulation objects in the object tree

    The object has attributes that match the properties of the simulation
    object. The attribute names are the same as the property names in the
    Lumerical application, except underscore characters are replaced with
    spaces if the original attribute name is not found in the object.

    Attributes can be read and set. Attributes that are set will immediately
    update the object in the Lumerical application

    The 'results' attribute is an object that contains all the results of the
    object
    """

    def __init__(self, parent, id):
        self._parent = parent
        self._id = SimObjectId(id)

        count = parent.getnamednumber(self._id.name)
        if self._id.index > count: raise LumApiError("Object %s not found" % id)
        if count > 1:
            lumWarning("Multiple objects named '%s'. Use of this object may "
                          "give unexpected results." % self._id.name)

        # getnamed doesn't support index, so property names may be wrong
        # if multiple objects with same name but different types
        propNames = parent.getnamed(self._id.name).split("\n")
        self._nameMap = self.build_nested(propNames)
        self.results = SimObjectResults(self)

    def build_nested(self, properties):
        tree = dict()
        for item in properties:
            t = tree
            for part in item.split('.')[:-1]:
                t = t.setdefault(part, GetSetHelper(self, part))
            t = t.setdefault(item.split('.')[-1], item)
        return tree

    def __dir__(self):
        return dir(super(SimObject, self)) + list(self._nameMap)

    def __getitem__(self, key):
        if key not in self._nameMap:
            raise AttributeError("'SimObject' object has no attribute '%s'" % key)
        if isinstance(self._nameMap[key], GetSetHelper):
            return self._nameMap[key]
        else:
            return getattr(self, key)

    def __setitem__(self, key, item):
        setattr(self, key, item)

    def __getattr__(self, name):
        if name not in self._nameMap:
            name = name.replace('_', ' ')
            if name not in self._nameMap:
                raise AttributeError("'SimObject' object has no attribute '%s'" % name)
        if isinstance(self._nameMap[name], GetSetHelper):
            return self._nameMap[name]
        else:
            return self._parent.getnamed(self._id.name, self._nameMap[name], self._id.index)

    def __setattr__(self, name, value):
        if (name[0] == '_') or (name == "results"):
            return object.__setattr__(self, name, value)

        if name not in self._nameMap:
            name = name.replace('_', ' ')
            if name not in self._nameMap:
                raise AttributeError("'SimObject' object has no attribute '%s'" % name)

        id = self._id
        if name == "name":
            self._id = SimObjectId('::'.join(self._id.name.split('::')[:-1]) + '::' + value)
            # changing name could lead to non-unique ID since no way to detect
            # the new index
            if self._parent.getnamednumber(self._id.name) > 0:
                lumWarning("New object name '%s' results in name duplication. Use of "
                              "this object may give unexpected results." % self._id.name)
        return self._parent.setnamed(id.name, self._nameMap[name], value, id.index)

    def getParent(self):
        # Save selection state
        try:
            currentlySelected = self._parent.getid().split("\n")
        except LumApiError as e:
            if "in getid, no items are currently selected" in str(e):
                currentlySelected = []
            else:
                raise e
        currScope = self._parent.groupscope()

        self._parent.select(self._id.name)
        name = self._parent.getObjectBySelection()._id.name
        parentName = name.split("::")
        parentName = "::".join(parentName[:-1])
        parent = self._parent.getObjectById(parentName)

        # Restore selection state
        self._parent.groupscope(currScope)
        for obj in currentlySelected:
            self._parent.select(obj)
        return parent

    def getChildren(self):
        # Save selection state
        try:
            currentlySelected = self._parent.getid().split("\n")
        except LumApiError as e:
            if "in getid, no items are currently selected" in str(e):
                currentlySelected = []
            else:
                raise e
        currScope = self._parent.groupscope()

        self._parent.groupscope(self._id.name)
        self._parent.selectall()
        children = self._parent.getAllSelectedObjects()

        # Restore selection state
        self._parent.groupscope(currScope)
        for obj in currentlySelected:
            self._parent.select(obj)
        return children


class Lumerical(object):
    def __init__(self, product, filename, key, hide, serverArgs, remoteArgs, **kwargs):
        """Keyword Arguments:
                script: A single string containing a script filename, or a collection of strings
                        that are filenames. Preffered types are list and tuple, dicts are not
                        supported. These scripts will run after the project specified by the
                        project keyword is opened. If no project is specified, they will run
                        in a new blank project.

                project: A single string containing a project filename. This project will be
                         opened before any scripts specified by the script keyword are run.
        """
         # this is to keep backward compatibility with applications that need a CAD running until the 
         # Python interpreter shuts down
        self.keepCADOpened = self.__extractKeepCADOpenedArgument__(serverArgs)
        iapi = initLib(remoteArgs)
        handle = self.__open__(iapi, product, key, hide, serverArgs, remoteArgs)
        self.handle = LumApiSession(iapi, handle)

        self.syncUserFunctionsFlag = False
        self.userFunctions = set() # variable to keep track of all added user methods

        # get a list of commands from script interpreter and register them
        # an error here is a constructor failure to populate class methods
        try:
            self.eval('api29538 = getcommands;')
            commands = self.getv('api29538').split("\n")
            commands = [x for x in commands if len(x) > 0 and x[0].isalpha()]
            self.eval('clear(api29538);')
        except:
            close(self.handle)
            raise

        try:
            with biopen(InteropPaths.INTEROPLIBDIR + '/docs.json') as docFile:
                docs = json.load(docFile)
        except:
            docs = {}

        # add methods to class corresponding to Lumerical script
        # use lambdas to create closures on the name argument.
        keywordsLumerical = ['for', 'if', 'else', 'exit', 'break', 'del', 'eval', 'try', 'catch', 'assert', 'end',
                             'true', 'false', 'isnull']
        deprecatedScriptCommands = ['addbc', 'addcontact', 'addeigenmode', 'addpropagator', 'deleteallbc', 'deletebc',
                                    'getasapdata', 'getbc', 'getcompositionfraction', 'getcontact', 'getglobal',
                                    'importdoping', 'lum2mat', 'monitors', 'new2d', 'new3d', 'newmode', 'removepropertydependency',
                                    'setbc', 'setcompositionfraction', 'setcontact', 'setglobal', 'setsolver', 'setparallel',
                                    'showdata', 'skewness', 'sources', 'structures']
        functionsToExclude = keywordsLumerical + deprecatedScriptCommands + ['h5info', 'pearson4pdf', 'fitnormpdf']

        addScriptCommands =    ['add2drect', 'add2dpoly', 'addabsorbing', 'addanalysisgroup', 'addanalysisprop',
                                'addanalysisresult', 'addbandstructuremonitor', 'addbulkgen', 'addchargemesh',
                                'addchargemonitor', 'addchargesolver', 'addcircle', 'addconvectionbc',
                                'addctmaterialproperty', 'addcustom', 'adddeltachargesource', 'addelectricalcontact',
                                'addelement', 'addemabsorptionmonitor', 'addemfieldmonitor', 'addemfieldtimemonitor',
                                'addemmaterialproperty', 'adddevice', 'adddgtdmesh', 'adddgtdsolver', 'adddiffusion',
                                'addimplant', 'adddipole', 'adddope', 'addeffectiveindex', 'addefieldmonitor',
                                'addelectricalcontact', 'addelement', 'addeme', 'addemeindex', 'addemeport',
                                'addemeprofile', 'addfde', 'addfdtd', 'addfeemsolver', 'addfeemmesh', 'addgaussian',
                                'addgridattribute', 'addgroup', 'addheatfluxbc', 'addheatfluxmonitor', 'addheatmesh',
                                'addheatsolver', 'addhtmaterialproperty', 'addimport', 'addimportdope',
                                'addimportedsource', 'addimportgen', 'addimportheat', 'addimporttemperature',
                                'addindex', 'addjfluxmonitor', 'addlayer', 'addlayerbuilder',
                                'addimportnk', 'addmesh', 'addmode', 'addmodeexpansion', 'addmodelmaterial',
                                'addmodesource', 'addmovie', 'addobject', 'addparameter', 'addpath', 'addpec',
                                'addperiodic', 'addplane', 'addplanarsolid', 'addpmc', 'addpml', 'addpoly', 'addpower',
                                'addprofile', 'addproperty', 'addpyramid', 'addradiationbc', 'addrect',
                                'addring', 'addsimulationregion', 'addsphere', 'addstructuregroup', 'addsurface',
                                'addsurfacerecombinationbc', 'addtemperaturebc', 'addtemperaturemonitor', 'addtfsf',
                                'addthermalinsulatingbc', 'addthermalpowerbc', 'addtime', 'addtriangle',
                                'adduniformheat', 'adduserprop', 'addvarfdtd', 'addvoltagebc', 'addwaveguide']

        for name in [n for n in commands if n not in functionsToExclude]:
            if name in addScriptCommands:
                method = (lambda x: lambda self, *args, **kwargs:
                appCallWithConstructor(self, x, args, **kwargs))(name)
            else:
                method = (lambda x: lambda self, *args: appCall(self, x, args))(name)
            method.__name__ = str(name)
            try:
                method.__doc__ = docs[name]['text'] + "\n" + docs[name]['link']
            except:
                pass
            setattr(Lumerical, name, method)

        # change the working directory to match Python program
        # load or run any file provided as argument
        # an error here is a constructor failure due to invalid user argument
        try:
            if not remoteModuleOn(remoteArgs): # we are not on remote mode
                self.cd(os.getcwd())
            if filename is not None:
                if filename.endswith('.lsf'):
                    self.feval(filename)
                elif filename.endswith('.lsfx'):
                    self.eval(filename[:-5] + ';')
                else:
                    self.load(filename)

            if kwargs is not None:
                if 'project' in kwargs:
                    self.load(kwargs['project'])
                if 'script' in kwargs:
                    if type(kwargs['script']) is not str:
                        for script in kwargs['script']:
                            if script.endswith('.lsfx'):
                                self.eval(script[:-5] + ';')
                            else:
                                self.feval(script)
                    else:
                        if kwargs['script'].endswith('.lsfx'):
                            self.eval(kwargs['script'][:-5] + ';')
                        else:
                            self.feval(kwargs['script'])
        except:
            close(self.handle)
            raise

    def __extractKeepCADOpenedArgument__(self, serverArgs):
        keepOpened = False
        if type(serverArgs) is not dict:
            raise LumApiError("Server arguments must be in dict format")
        else:
            if 'keepCADOpened' in serverArgs.keys():
                keepOpened = serverArgs['keepCADOpened']
                del serverArgs['keepCADOpened']
        return keepOpened

    def __del__(self):
        self.syncUserFunctionsFlag = False
        try:
            if self.keepCADOpened is False:
                if(hasattr(self, 'handle')) is True:
                    close(self.handle)
        except AttributeError:
            pass #< occurs if open() failed in __init__ or if __exit__ already called

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.syncUserFunctionsFlag = False
        try:
            if(hasattr(self, 'handle')) is True:
                close(self.handle)
        except AttributeError:
            pass #< occurs if open() failed in __init__

    def _addUserFunctions(self):
        """adds all current 'User Functions' into the current object
        
        User Functions are usually loaded in by using eval()
        Allowing to call those functions as they were defined within the API.
        """
        workspace = self.workspace().strip().split('\n')
        try:    
            i =  workspace.index('User Functions:')+1
            names = workspace[i].strip().split()
        except ValueError : 
            return    
        except IndexError : 
            return   

        for name in names:
            method = (lambda x: lambda self, *args: appCall(self, x, args))(name)
            setattr(self, name, types.MethodType(method, self))
            self.userFunctions.add(name)

    def _deleteUserFunctions(self):
        """deletes all previously added methods"""
        for currFunction in self.userFunctions:
            if hasattr(self, currFunction) is True:
                delattr(self, currFunction)
        self.userFunctions.clear()        

    def _syncUserFunctions(self):
        """synchronizes 'User Functions' into the current object
        
        'User Functions' will be available from the Python interpreter
        """
        if self.syncUserFunctionsFlag is True:
            self._deleteUserFunctions()
            self._addUserFunctions()
            self.syncUserFunctionsFlag = False

    def __getattr__(self, name):
        self._syncUserFunctions()
        # Default behaviour
        return self.__getattribute__(name)        

    def __open__(self, iapi, product, key=None, hide=False, serverArgs={}, remoteArgs={}):
        additionalArgs=""
        if type(serverArgs) is not dict:
            raise LumApiError("Server arguments must be in dict format")
        else:
            for argument in serverArgs.keys():
                additionalArgs = additionalArgs + "&" + argument + "=" + str(serverArgs[argument])

        remoteServerFlag = "?server=true"
        hostnameAndPort = "localhost"
        if remoteModuleOn(remoteArgs):
            hostnameAndPort = extractsHostnameAndPort(remoteArgs)
            remoteServerFlag = "?remote-server=true"

        url = ""
        if product == "interconnect":
            url = b"interconnect://" + hostnameAndPort.encode() + remoteServerFlag.encode() + additionalArgs.encode()
        elif product == "fdtd":
            url = b"fdtd://" + hostnameAndPort.encode() + remoteServerFlag.encode() + additionalArgs.encode()
        elif product == "mode":
            url = b"mode://" + hostnameAndPort.encode() + remoteServerFlag.encode() + additionalArgs.encode()
        elif product == "device":
            url = b"device://" + hostnameAndPort.encode() + remoteServerFlag.encode() + additionalArgs.encode()

        if len(url) == 0:
            raise LumApiError("Invalid product name")

        KeyType = c_ulonglong * 2
        k = KeyType()
        k[0] = 0
        k[1] = 0

        if key:
            url += b"&feature=" + str(key[0]).encode()
            k[0] = c_ulonglong(key[1])
            k[1] = c_ulonglong(key[2])

        if hide:
            url += b"&hide"

        with environ({"PATH":InteropPaths.ENVIRONPATH}):
            h = iapi.appOpen(url, k)
            if not iapi.appOpened(h):
                error = iapi.appGetLastError()
                error = error.contents.str[:error.contents.len].decode('utf-8')
                raise LumApiError(error)

        return h
        

    def close(self):
        """close will call appClose on the the object handle and destroy the session"""
        self.syncUserFunctionsFlag = False
        if isinstance(self.handle, LumApiSession) and self.handle.handle is not None:
            close(self.handle)
            self.handle = None

    def eval(self, code):
        """eval will evaluate the given script code as a string"""
        self.syncUserFunctionsFlag = True
        evalScript(self.handle, code, True)

    def getv(self, varname):
        """getv is a wrapper around getVar for the session"""
        return getVar(self.handle, varname, True)

    def putv(self, varname, value):
        """putv is a wrapper around the various put calls for the session"""

        if isinstance(value, float):
            putDouble(self.handle, varname, value, True)
            return

        if isinstance(value, str):
            putString(self.handle, varname, value, True)
            return

        if isinstance(value, np.ndarray):
            putMatrix(self.handle, varname, value, True)
            return

        if isinstance(value, list):
            putList(self.handle, varname, value, True)
            return

        if isinstance(value, dict):
            putStruct(self.handle, varname, value, True)
            return

        try:
            v = float(value)
            putDouble(self.handle, varname, v, True)
            return
        except TypeError:
            pass
        except ValueError:
            pass

        try:
            v = list(value)
            putList(self.handle, varname, v, True)
            return
        except TypeError:
            pass

        try:
            v = dict(value)
            putStruct(self.handle, varname, v, True)
            return
        except TypeError:
            pass
        except ValueError:
            pass

        try:
            v = str(value)
            putString(self.handle, varname, v, True)
            return
        except ValueError:
            pass

        raise LumApiError("Unsupported data type")

    def getObjectById(self, id):
        """returns the simulation object identified by ID

        The object ID is the fully distinguished name of the object. Eg:

        ::model::group::rectangle

        If a duplicate names exist, you should append #N to the name to
        unambiguously identify a single object. N is an integer identifing
        the Nth object in the tree with the given name. Eg:

        ::model::group::rectangle#3

        If an unqualified name is given, the group scope will be prepended to
        the name
        """
        i = id if id.startswith("::") else self.groupscope() + '::' + id
        return SimObject(self, i)

    def getObjectBySelection(self):
        """returns the currently selected simulation objects

        If multiple objects are selected the first object is returned
        """
        idToGet = self.getid().split("\n")
        return self.getObjectById(idToGet[0])

    def getAllSelectedObjects(self):
        """returns a list of all currently selected simulation objects"""
        listOfChildren = list()
        toGet = self.getid().split("\n")
        for i in toGet:
            listOfChildren.append(self.getObjectById(i))
        return listOfChildren
    
    
    def h5info(self, filename):
        """
        Retrieves information about the contents of an HDF5 file.

        Parameters:
        filename (str): The path to the HDF5 file.

        Returns:
        dict: A dictionary containing information about the HDF5 file.
        """
        return appCall(self, 'h5info', [filename])

    def pearson4pdf(self, x, mean, variance, skewness, kurtosis):
        """
        Computes the Pearson type IV probability density function.

        Parameters:
        x (float): The value at which to evaluate the PDF.
        mean (float): The mean of the distribution.
        variance (float): The variance of the distribution.
        skewness (float): The skewness of the distribution.
        kurtosis (float): The kurtosis of the distribution.

        Returns:
        float: The value of the PDF at x.
        """
        return appCall(self, 'pearson4pdf', [x, mean, variance, skewness, kurtosis])

    def fitnormpdf(self, x, y, normalize=0, fit_threshold=2e-8, max_iter=400):
        """
        Fits data with the normal (Gaussian) probability density function.

        Parameters:
        x (list): The x values of the data.
        y (list): The y values of the data.
        normalize (int, optional): If set to 1, the fit amplitude is relative to a distribution with a unit maximum (A = 1). Default is 0.
        fit_threshold (float, optional): Relative tolerance for the fitting convergence. Default is 2e-8.
        max_iter (int, optional): Maximum number of iterations for the fitting process. Default is 400.

        Returns:
        list: The values for A, µ, and σ.
        """
        return appCall(self, 'fitnormpdf', [x, y, normalize, fit_threshold, max_iter])



class INTERCONNECT(Lumerical):
    def __init__(self, filename=None, key=None, hide=False, serverArgs={}, remoteArgs={}, **kwargs):
        super(INTERCONNECT, self).__init__('interconnect', filename, key, hide, serverArgs, remoteArgs, **kwargs)


class DEVICE(Lumerical):
    def __init__(self, filename=None, key=None, hide=False, serverArgs={}, remoteArgs={}, **kwargs):
        super(DEVICE, self).__init__('device', filename, key, hide, serverArgs, remoteArgs, **kwargs)


class FDTD(Lumerical):
    def __init__(self, filename=None, key=None, hide=False, serverArgs={}, remoteArgs={}, **kwargs):
        super(FDTD, self).__init__('fdtd', filename, key, hide, serverArgs, remoteArgs, **kwargs)


class MODE(Lumerical):
    def __init__(self, filename=None, key=None, hide=False, serverArgs={}, remoteArgs={}, **kwargs):
        super(MODE, self).__init__('mode', filename, key, hide, serverArgs, remoteArgs, **kwargs)

