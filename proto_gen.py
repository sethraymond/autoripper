import shlex
import subprocess
from pathlib import Path

from grpc_tools import protoc


def build():
    proto_dir = Path("./proto")
    common_dir = proto_dir / "common"
    common_flags = "--python_out=autoripper/proto/common --pyi_out=autoripper/proto/common --grpc_python_out=autoripper/proto/common"
    for common_proto_file in common_dir.glob("*.proto"):
        command = f"grpc_tools.protoc {common_flags} proto/common/{common_proto_file.name}"
        protoc.main(command)
    interface_flags = "-Iproto/common --python_out=autoripper/proto --pyi_out=autoripper/proto --grpc_python_out=autoripper/proto"
    for interface_proto_file in proto_dir.glob("*.proto"):
        command = f"grpc_tools.protoc {interface_flags} proto/{interface_proto_file.name}"
        protoc.main(command)

if __name__ == "__main__":
    build()
