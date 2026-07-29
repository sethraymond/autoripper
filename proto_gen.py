import shlex
from pathlib import Path

from grpc_tools import protoc


def build():
    proto_dir = Path("./proto")
    common_dir = proto_dir / "common"
    common_flags = "grpc_tools.protoc -Iproto --python_out=autoripper/proto --pyi_out=autoripper/proto --grpc_python_out=autoripper/proto"
    for common_proto_file in common_dir.glob("*.proto"):
        command = f"{common_flags} proto/common/{common_proto_file.name}"
        protoc.main(shlex.split(command))
    interface_flags = "grpc_tools.protoc -Iproto --python_out=autoripper/proto --pyi_out=autoripper/proto --grpc_python_out=autoripper/proto"
    for interface_proto_file in proto_dir.glob("*.proto"):
        command = f"{interface_flags} proto/{interface_proto_file.name}"
        protoc.main(shlex.split(command))

if __name__ == "__main__":
    build()
