import os
from concurrent import futures
from pathlib import Path

import grpc
from proto.ripper_pb2_grpc import RipperServicer, add_RipperServicer_to_server
from rip import Ripper


class RipperServer(RipperServicer):
    def __init__(self, ripper: Ripper):
        self._ripper = ripper

    def RipDisk(self, request, context):
        self._ripper.rip()
        return super().RipDisk(request, context)


def serve():
    config_path = Path(os.getenv("AUTORIPPER_CONFIG_PATH", "/config/shows.yaml"))
    ripper = Ripper(config_path)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    add_RipperServicer_to_server(RipperServer(ripper), server)
    server.add_insecure_port("[::]:50001")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
