import grpc
from concurrent import futures
import sys
import os
import message_pb2_grpc as pb2_grpc
import message_pb2 as pb2


current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to 
# the sys.path.
sys.path.append(parent)
from agent import get_response
from config import GRPC_SERVER_PORT

class GITMessageService(pb2_grpc.GITCommitMessageServicer):

    def __init__(self, *args, **kwargs):
        pass

    def GetCommitMessage(self, request, context):
        message = request.message
        result = get_response(message)
        result = {'message': result, 'received': True}
        return pb2.MessageResponse(**result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_GITCommitMessageServicer_to_server(GITMessageService(),server)
    server.add_insecure_port(f'[::]:{GRPC_SERVER_PORT}')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()