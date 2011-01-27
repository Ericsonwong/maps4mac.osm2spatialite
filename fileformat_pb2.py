# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


DESCRIPTOR = descriptor.FileDescriptor(
  name='fileformat.proto',
  package='',
  serialized_pb='\n\x10\x66ileformat.proto\"_\n\x04\x42lob\x12\x0b\n\x03raw\x18\x01 \x01(\x0c\x12\x10\n\x08raw_size\x18\x02 \x01(\x05\x12\x11\n\tzlib_data\x18\x03 \x01(\x0c\x12\x11\n\tlzma_data\x18\x04 \x01(\x0c\x12\x12\n\nbzip2_data\x18\x05 \x01(\x0c\"@\n\x0b\x42lockHeader\x12\x0c\n\x04type\x18\x01 \x02(\t\x12\x11\n\tindexdata\x18\x02 \x01(\x0c\x12\x10\n\x08\x64\x61tasize\x18\x03 \x02(\x05\x42\x0f\n\rcrosby.binary')




_BLOB = descriptor.Descriptor(
  name='Blob',
  full_name='Blob',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='raw', full_name='Blob.raw', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='raw_size', full_name='Blob.raw_size', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='zlib_data', full_name='Blob.zlib_data', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='lzma_data', full_name='Blob.lzma_data', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='bzip2_data', full_name='Blob.bzip2_data', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=20,
  serialized_end=115,
)


_BLOCKHEADER = descriptor.Descriptor(
  name='BlockHeader',
  full_name='BlockHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='type', full_name='BlockHeader.type', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='indexdata', full_name='BlockHeader.indexdata', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='datasize', full_name='BlockHeader.datasize', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=117,
  serialized_end=181,
)



class Blob(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BLOB
  
  # @@protoc_insertion_point(class_scope:Blob)

class BlockHeader(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BLOCKHEADER
  
  # @@protoc_insertion_point(class_scope:BlockHeader)

# @@protoc_insertion_point(module_scope)
