import time
import logging
from concurrent import futures
import grpc
import example_pb2
import example_pb2_grpc

# Implement the Example service
class ExampleServicer(example_pb2_grpc.ExampleServicer):
    def call(self, request, context):
        # Your logic here. For example, a simple echo response:
        response = f"Received: {request.query}"
        return example_pb2.Answer(answer=response, answer2=response, answer3=response)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_ExampleServicer_to_server(ExampleServicer(), server)
    server.add_insecure_port('[::]:8010')
    server.start()
    print('Server running on port 8010')
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    serve()
