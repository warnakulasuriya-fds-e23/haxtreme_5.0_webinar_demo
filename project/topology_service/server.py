"""TopologyService — reveals the hidden structure of a problem's input."""

import os
from concurrent import futures

import grpc

import challenge_pb2
import challenge_pb2_grpc
from problem_data import PROBLEMS

PORT = os.environ.get("PORT", "50051")


class TopologyService(challenge_pb2_grpc.TopologyServiceServicer):
    def DescribeStructure(self, request, context):
        problem = PROBLEMS.get(request.problem_id)
        if problem is None:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"Unknown problem_id: {request.problem_id}",
            )
        topo = problem["topology"]
        return challenge_pb2.TopologyResponse(
            problem_id=request.problem_id,
            data_type=topo["data_type"],
            directed=topo["directed"],
            weighted=topo["weighted"],
            has_negative_weights=topo["has_negative_weights"],
            has_cycles=topo["has_cycles"],
            description=topo["description"],
            input_format=topo["input_format"],
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    challenge_pb2_grpc.add_TopologyServiceServicer_to_server(TopologyService(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    print(f"TopologyService listening on port {PORT}", flush=True)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
