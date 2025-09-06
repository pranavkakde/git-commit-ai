import grpc
import message_pb2_grpc as pb2_grpc
import message_pb2 as pb2
import subprocess

def get_staged_diff():
    result = subprocess.run(['git', 'diff', '--cached'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

def main():
    try:
        diff = get_staged_diff()
        channel = grpc.insecure_channel('localhost:50051')
        stub = pb2_grpc.GITCommitMessageStub(channel)
        request = pb2.Message(message=diff)
        response = stub.GetCommitMessage(request)
        print(response.message)
    except Exception as e:
        print(f"Error getting response: {e}")
        raise e

if __name__ == "__main__":
    main()
