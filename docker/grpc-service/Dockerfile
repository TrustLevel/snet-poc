# Use an official Python image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the dependencies file to the working directory
COPY src/requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install gRPC tools
RUN pip install grpcio-tools

# Copy the content of the local src directory to the working directory
COPY src/ .

# Generate Python gRPC code from the .proto file
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./example.proto

# Specify the command to run on container start
CMD [ "python", "./server.py" ]

# Expose the port the server is running on
EXPOSE 8010
