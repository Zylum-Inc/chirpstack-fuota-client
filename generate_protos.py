import os
from grpc_tools import protoc

proto_files = [
    'src/chirpstack_fuota_client/proto/fuota/fuota.proto'
]

# Path to the google/protobuf directory
proto_include = os.path.join(os.path.dirname(protoc.__file__), '_proto')

output_dir = 'src/chirpstack_fuota_client/proto/fuota'

for proto_file in proto_files:
    protoc.main((
        '',
        f'-I{os.path.dirname(proto_file)}',
        f'-I{proto_include}',
        f'--python_out={output_dir}',
        f'--grpc_python_out={output_dir}',
        proto_file,
    ))