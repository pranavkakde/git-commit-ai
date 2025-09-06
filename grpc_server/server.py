import grpc
from concurrent import futures
import sys
import os
import message_pb2_grpc as pb2_grpc
import message_pb2 as pb2
from grpc_reflection.v1alpha import reflection

current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to 
# the sys.path.
sys.path.append(parent)
from llm_client import get_response
from config import GRPC_SERVER_PORT

class GITMessageService(pb2_grpc.GITCommitMessageServicer):
    """
    Service to get the commit message from the LLM model.
    """
    def __init__(self, *args, **kwargs):
        pass

    def GetCommitMessage(self, request, context):
        """
        Function to get the commit message from the LLM model.

        Returns:
        MessageResponse: MessageResponse object containing the commit message and a boolean indicating if the message was received.
        """
        message = request.message
        result = get_response(message)
        result = {'message': result, 'received': True}
        return pb2.MessageResponse(**result)


def serve():
    """
    Function to start the GRPC server.
    """
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_GITCommitMessageServicer_to_server(GITMessageService(),server)
        reflection.enable_server_reflection(pb2._descriptor.__name__, server)
        server.add_insecure_port(f'[::]:{GRPC_SERVER_PORT}')
        server.start()
        server.wait_for_termination()
        print(f"Server started on port {GRPC_SERVER_PORT}")        
    except Exception as e:
        print(f"Error starting the GRPC server: {e}")
        raise e


if __name__ == '__main__':
    serve()