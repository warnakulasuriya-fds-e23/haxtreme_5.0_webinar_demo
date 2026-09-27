FROM python:3.11-slim

WORKDIR /app

COPY constraint_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Generate gRPC stubs from the shared contract.
COPY protos/ ./protos/
RUN python -m grpc_tools.protoc -Iprotos \
    --python_out=. --grpc_python_out=. \
    protos/challenge.proto

# Shared hidden problem registry + this service's code.
COPY shared/problem_data.py .
COPY constraint_service/server.py .

EXPOSE 50052
CMD ["python", "server.py"]
