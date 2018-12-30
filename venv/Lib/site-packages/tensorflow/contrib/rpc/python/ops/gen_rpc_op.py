"""Python wrappers around TensorFlow ops.

This file is MACHINE GENERATED! Do not edit.
"""

import collections as _collections
import six as _six

from tensorflow.python import pywrap_tensorflow as _pywrap_tensorflow
from tensorflow.python.eager import context as _context
from tensorflow.python.eager import core as _core
from tensorflow.python.eager import execute as _execute
from tensorflow.python.framework import dtypes as _dtypes
from tensorflow.python.framework import errors as _errors
from tensorflow.python.framework import tensor_shape as _tensor_shape

from tensorflow.core.framework import op_def_pb2 as _op_def_pb2
# Needed to trigger the call to _set_call_cpp_shape_fn.
from tensorflow.python.framework import common_shapes as _common_shapes
from tensorflow.python.framework import op_def_registry as _op_def_registry
from tensorflow.python.framework import ops as _ops
from tensorflow.python.framework import op_def_library as _op_def_library
from tensorflow.python.util.tf_export import tf_export


@tf_export('rpc')
def rpc(address, method, request, protocol="", fail_fast=True, timeout_in_ms=0, name=None):
  r"""Perform batches of RPC requests.

  This op asynchronously performs either a single RPC request, or a batch
  of requests.  RPC requests are defined by three main parameters:
  
    - `address` (the host+port or BNS address of the request)
    - `method` (the RPC method name for the request)
    - `request` (the serialized proto string, or vector of strings,
       of the RPC request argument).
  
  For example, if you have an RPC service running on port localhost:2345,
  and its interface is configured with the following proto declaration:
  
  ```
  service MyService {
    rpc MyMethod(MyRequestProto) returns (MyResponseProto) {
    }
  };
  ```
  
  then call this op with arguments:
  
  ```
  address = "localhost:2345"
  method = "MyService/MyMethod"
  ```
  
  The `request` tensor is a string tensor representing serialized `MyRequestProto`
  strings; and the output string tensor `response` will have the same shape
  and contain (upon successful completion) corresponding serialized
  `MyResponseProto` strings.
  
  For example, to send a single, empty, `MyRequestProto`, call
  this op with `request = ""`.  To send 5 **parallel** empty requests,
  call this op with `request = ["", "", "", "", ""]`.
  
  More generally, one can create a batch of `MyRequestProto` serialized protos
  from regular batched tensors using the `encode_proto` op, and convert
  the response `MyResponseProto` serialized protos to batched tensors
  using the `decode_proto` op.
  
  **NOTE** Working with serialized proto strings is faster than instantiating
  actual proto objects in memory, so no performance degradation is expected
  compared to writing custom kernels for this workflow.
  
  If the connection fails or the remote worker returns an error
  status, the op reraises this exception locally.
  
  See the `TryRpc` op if you prefer to handle RPC failures manually in the graph.

  Args:
    address: A `Tensor` of type `string`.
      `0-D` or `1-D`.  The address (i.e. host_name:port) of the RPC server.
      If this tensor has more than 1 element, then multiple parallel rpc requests
      are sent.  This argument broadcasts with `method` and `request`.
    method: A `Tensor` of type `string`.
      `0-D` or `1-D`.  The method address on the RPC server.
      If this tensor has more than 1 element, then multiple parallel rpc requests
      are sent.  This argument broadcasts with `address` and `request`.
    request: A `Tensor` of type `string`.
      `0-D` or `1-D`.  Serialized proto strings: the rpc request argument.
      If this tensor has more than 1 element, then multiple parallel rpc requests
      are sent.  This argument broadcasts with `address` and `method`.
    protocol: An optional `string`. Defaults to `""`.
      RPC protocol to use.  Empty string means use the default protocol.
      Options include 'grpc'.
    fail_fast: An optional `bool`. Defaults to `True`.
      `boolean`. If `true` (default), then failures to connect
      (i.e., the server does not immediately respond) cause an RPC failure.
    timeout_in_ms: An optional `int`. Defaults to `0`.
      `int`. If `0` (default), then the kernel will run the RPC
      request and only time out if the RPC deadline passes or the session times out.
      If this value is greater than `0`, then the op will raise an exception if
      the RPC takes longer than `timeout_in_ms`.
    name: A name for the operation (optional).

  Returns:
    A `Tensor` of type `string`.
  """
  _ctx = _context._context
  if _ctx is None or not _ctx._eager_context.is_eager:
    if protocol is None:
      protocol = ""
    protocol = _execute.make_str(protocol, "protocol")
    if fail_fast is None:
      fail_fast = True
    fail_fast = _execute.make_bool(fail_fast, "fail_fast")
    if timeout_in_ms is None:
      timeout_in_ms = 0
    timeout_in_ms = _execute.make_int(timeout_in_ms, "timeout_in_ms")
    _, _, _op = _op_def_lib._apply_op_helper(
        "Rpc", address=address, method=method, request=request,
        protocol=protocol, fail_fast=fail_fast, timeout_in_ms=timeout_in_ms,
        name=name)
    _result = _op.outputs[:]
    _inputs_flat = _op.inputs
    _attrs = ("protocol", _op.get_attr("protocol"), "fail_fast",
              _op.get_attr("fail_fast"), "timeout_in_ms",
              _op.get_attr("timeout_in_ms"))
    _execute.record_gradient(
      "Rpc", _inputs_flat, _attrs, _result, name)
    _result, = _result
    return _result

  else:
    try:
      _result = _pywrap_tensorflow.TFE_Py_FastPathExecute(
        _ctx._context_handle, _ctx._eager_context.device_name, "Rpc", name,
        _ctx._post_execution_callbacks, address, method, request, "protocol",
        protocol, "fail_fast", fail_fast, "timeout_in_ms", timeout_in_ms)
      return _result
    except _core._FallbackException:
      return rpc_eager_fallback(
          address, method, request, protocol=protocol, fail_fast=fail_fast,
          timeout_in_ms=timeout_in_ms, name=name, ctx=_ctx)
    except _core._NotOkStatusException as e:
      if name is not None:
        message = e.message + " name: " + name
      else:
        message = e.message
      _six.raise_from(_core._status_to_exception(e.code, message), None)


def rpc_eager_fallback(address, method, request, protocol="", fail_fast=True, timeout_in_ms=0, name=None, ctx=None):
  r"""This is the slowpath function for Eager mode.
  This is for function rpc
  """
  _ctx = ctx if ctx else _context.context()
  if protocol is None:
    protocol = ""
  protocol = _execute.make_str(protocol, "protocol")
  if fail_fast is None:
    fail_fast = True
  fail_fast = _execute.make_bool(fail_fast, "fail_fast")
  if timeout_in_ms is None:
    timeout_in_ms = 0
  timeout_in_ms = _execute.make_int(timeout_in_ms, "timeout_in_ms")
  address = _ops.convert_to_tensor(address, _dtypes.string)
  method = _ops.convert_to_tensor(method, _dtypes.string)
  request = _ops.convert_to_tensor(request, _dtypes.string)
  _inputs_flat = [address, method, request]
  _attrs = ("protocol", protocol, "fail_fast", fail_fast, "timeout_in_ms",
  timeout_in_ms)
  _result = _execute.execute(b"Rpc", 1, inputs=_inputs_flat, attrs=_attrs,
                             ctx=_ctx, name=name)
  _execute.record_gradient(
      "Rpc", _inputs_flat, _attrs, _result, name)
  _result, = _result
  return _result


_try_rpc_outputs = ["response", "status_code", "status_message"]
_TryRpcOutput = _collections.namedtuple(
    "TryRpc", _try_rpc_outputs)


@tf_export('try_rpc')
def try_rpc(address, method, request, protocol="", fail_fast=True, timeout_in_ms=0, name=None):
  r"""Perform batches of RPC requests.

  This op asynchronously performs either a single RPC request, or a batch
  of requests.  RPC requests are defined by three main parameters:
  
    - `address` (the host+port or BNS address of the request)
    - `method` (the method name for the request)
    - `request` (the serialized proto string, or vector of strings,
       of the RPC request argument).
  
  For example, if you have an RPC service running on port localhost:2345,
  and its interface is configured with the following proto declaration:
  
  ```
  service MyService {
    rpc MyMethod(MyRequestProto) returns (MyResponseProto) {
    }
  };
  ```
  
  then call this op with arguments:
  
  ```
  address = "localhost:2345"
  method = "MyService/MyMethod"
  ```
  
  The `request` tensor is a string tensor representing serialized `MyRequestProto`
  strings; and the output string tensor `response` will have the same shape
  and contain (upon successful completion) corresponding serialized
  `MyResponseProto` strings.
  
  For example, to send a single, empty, `MyRequestProto`, call
  this op with `request = ""`.  To send 5 **parallel** empty requests,
  call this op with `request = ["", "", "", "", ""]`.
  
  More generally, one can create a batch of `MyRequestProto` serialized protos
  from regular batched tensors using the `encode_proto` op, and convert
  the response `MyResponseProto` serialized protos to batched tensors
  using the `decode_proto` op.
  
  **NOTE** Working with serialized proto strings is faster than instantiating
  actual proto objects in memory, so no performance degradation is expected
  compared to writing custom kernels for this workflow.
  
  Unlike the standard `Rpc` op, if the connection fails or the remote worker
  returns an error status, this op does **not** reraise the exception.
  Instead, the `status_code` and `status_message` entry for the corresponding RPC
  call is set with the error returned from the RPC call.  The `response` tensor
  will contain valid response values for those minibatch entries whose RPCs did
  not fail; the rest of the entries will have empty strings.

  Args:
    address: A `Tensor` of type `string`.
      `0-D` or `1-D`.  The address (i.e. host_name:port) of the RPC server.
      If this tensor has more than 1 element, then multiple parallel rpc requests
      are sent.  This argument broadcasts with `method` and `request`.
    method: A `Tensor` of type `string`.
      `0-D` or `1-D`.  The method address on the RPC server.
      If this tensor has more than 1 element, then multiple parallel rpc requests
      are sent.  This argument broadcasts with `address` and `request`.
    request: A `Tensor` of type `string`.
      `0-D` or `1-D`.  Serialized proto strings: the rpc request argument.
      If this tensor has more than 1 element, then multiple parallel rpc requests
      are sent.  This argument broadcasts with `address` and `method`.
    protocol: An optional `string`. Defaults to `""`.
      RPC protocol to use.  Empty string means use the default protocol.
      Options include 'grpc'.
    fail_fast: An optional `bool`. Defaults to `True`.
      `boolean`. If `true` (default), then failures to connect
      (i.e., the server does not immediately respond) cause an RPC failure.
    timeout_in_ms: An optional `int`. Defaults to `0`.
      `int`. If `0` (default), then the kernel will run the RPC
      request and only time out if the RPC deadline passes or the session times out.
      If this value is greater than `0`, then the op will raise an exception if
      the RPC takes longer than `timeout_in_ms`.
    name: A name for the operation (optional).

  Returns:
    A tuple of `Tensor` objects (response, status_code, status_message).

    response: A `Tensor` of type `string`.
    status_code: A `Tensor` of type `int32`.
    status_message: A `Tensor` of type `string`.
  """
  _ctx = _context._context
  if _ctx is None or not _ctx._eager_context.is_eager:
    if protocol is None:
      protocol = ""
    protocol = _execute.make_str(protocol, "protocol")
    if fail_fast is None:
      fail_fast = True
    fail_fast = _execute.make_bool(fail_fast, "fail_fast")
    if timeout_in_ms is None:
      timeout_in_ms = 0
    timeout_in_ms = _execute.make_int(timeout_in_ms, "timeout_in_ms")
    _, _, _op = _op_def_lib._apply_op_helper(
        "TryRpc", address=address, method=method, request=request,
        protocol=protocol, fail_fast=fail_fast, timeout_in_ms=timeout_in_ms,
        name=name)
    _result = _op.outputs[:]
    _inputs_flat = _op.inputs
    _attrs = ("protocol", _op.get_attr("protocol"), "fail_fast",
              _op.get_attr("fail_fast"), "timeout_in_ms",
              _op.get_attr("timeout_in_ms"))
    _execute.record_gradient(
      "TryRpc", _inputs_flat, _attrs, _result, name)
    _result = _TryRpcOutput._make(_result)
    return _result

  else:
    try:
      _result = _pywrap_tensorflow.TFE_Py_FastPathExecute(
        _ctx._context_handle, _ctx._eager_context.device_name, "TryRpc", name,
        _ctx._post_execution_callbacks, address, method, request, "protocol",
        protocol, "fail_fast", fail_fast, "timeout_in_ms", timeout_in_ms)
      _result = _TryRpcOutput._make(_result)
      return _result
    except _core._FallbackException:
      return try_rpc_eager_fallback(
          address, method, request, protocol=protocol, fail_fast=fail_fast,
          timeout_in_ms=timeout_in_ms, name=name, ctx=_ctx)
    except _core._NotOkStatusException as e:
      if name is not None:
        message = e.message + " name: " + name
      else:
        message = e.message
      _six.raise_from(_core._status_to_exception(e.code, message), None)


def try_rpc_eager_fallback(address, method, request, protocol="", fail_fast=True, timeout_in_ms=0, name=None, ctx=None):
  r"""This is the slowpath function for Eager mode.
  This is for function try_rpc
  """
  _ctx = ctx if ctx else _context.context()
  if protocol is None:
    protocol = ""
  protocol = _execute.make_str(protocol, "protocol")
  if fail_fast is None:
    fail_fast = True
  fail_fast = _execute.make_bool(fail_fast, "fail_fast")
  if timeout_in_ms is None:
    timeout_in_ms = 0
  timeout_in_ms = _execute.make_int(timeout_in_ms, "timeout_in_ms")
  address = _ops.convert_to_tensor(address, _dtypes.string)
  method = _ops.convert_to_tensor(method, _dtypes.string)
  request = _ops.convert_to_tensor(request, _dtypes.string)
  _inputs_flat = [address, method, request]
  _attrs = ("protocol", protocol, "fail_fast", fail_fast, "timeout_in_ms",
  timeout_in_ms)
  _result = _execute.execute(b"TryRpc", 3, inputs=_inputs_flat, attrs=_attrs,
                             ctx=_ctx, name=name)
  _execute.record_gradient(
      "TryRpc", _inputs_flat, _attrs, _result, name)
  _result = _TryRpcOutput._make(_result)
  return _result

def _InitOpDefLibrary(op_list_proto_bytes):
  op_list = _op_def_pb2.OpList()
  op_list.ParseFromString(op_list_proto_bytes)
  _op_def_registry.register_op_list(op_list)
  op_def_lib = _op_def_library.OpDefLibrary()
  op_def_lib.add_op_list(op_list)
  return op_def_lib
# op {
#   name: "Rpc"
#   input_arg {
#     name: "address"
#     type: DT_STRING
#   }
#   input_arg {
#     name: "method"
#     type: DT_STRING
#   }
#   input_arg {
#     name: "request"
#     type: DT_STRING
#   }
#   output_arg {
#     name: "response"
#     type: DT_STRING
#   }
#   attr {
#     name: "protocol"
#     type: "string"
#     default_value {
#       s: ""
#     }
#   }
#   attr {
#     name: "fail_fast"
#     type: "bool"
#     default_value {
#       b: true
#     }
#   }
#   attr {
#     name: "timeout_in_ms"
#     type: "int"
#     default_value {
#       i: 0
#     }
#   }
#   is_stateful: true
# }
# op {
#   name: "TryRpc"
#   input_arg {
#     name: "address"
#     type: DT_STRING
#   }
#   input_arg {
#     name: "method"
#     type: DT_STRING
#   }
#   input_arg {
#     name: "request"
#     type: DT_STRING
#   }
#   output_arg {
#     name: "response"
#     type: DT_STRING
#   }
#   output_arg {
#     name: "status_code"
#     type: DT_INT32
#   }
#   output_arg {
#     name: "status_message"
#     type: DT_STRING
#   }
#   attr {
#     name: "protocol"
#     type: "string"
#     default_value {
#       s: ""
#     }
#   }
#   attr {
#     name: "fail_fast"
#     type: "bool"
#     default_value {
#       b: true
#     }
#   }
#   attr {
#     name: "timeout_in_ms"
#     type: "int"
#     default_value {
#       i: 0
#     }
#   }
#   is_stateful: true
# }
_op_def_lib = _InitOpDefLibrary(b"\n\205\001\n\003Rpc\022\013\n\007address\030\007\022\n\n\006method\030\007\022\013\n\007request\030\007\032\014\n\010response\030\007\"\026\n\010protocol\022\006string\032\002\022\000\"\025\n\tfail_fast\022\004bool\032\002(\001\"\030\n\rtimeout_in_ms\022\003int\032\002\030\000\210\001\001\n\255\001\n\006TryRpc\022\013\n\007address\030\007\022\n\n\006method\030\007\022\013\n\007request\030\007\032\014\n\010response\030\007\032\017\n\013status_code\030\003\032\022\n\016status_message\030\007\"\026\n\010protocol\022\006string\032\002\022\000\"\025\n\tfail_fast\022\004bool\032\002(\001\"\030\n\rtimeout_in_ms\022\003int\032\002\030\000\210\001\001")
