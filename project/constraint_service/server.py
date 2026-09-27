"""ConstraintService — reveals scale limits, time budget and edge-case flags."""

import os
from concurrent import futures

import grpc

import challenge_pb2
import challenge_pb2_grpc
from problem_data import PROBLEMS

PORT = os.environ.get("PORT", "50052")


class ConstraintService(challenge_pb2_grpc.ConstraintServiceServicer):
    def GetConstraints(self, request, context):
        problem = PROBLEMS.get(request.problem_id)
        if problem is None:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"Unknown problem_id: {request.problem_id}",
            )
        c = problem["constraints"]
        return challenge_pb2.ConstraintResponse(
            problem_id=request.problem_id,
            max_n=c["max_n"],
            max_m=c["max_m"],
            time_limit_ms=c["time_limit_ms"],
            value_range=c["value_range"],
            edge_case_flags=c["edge_case_flags"],
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    challenge_pb2_grpc.add_ConstraintServiceServicer_to_server(ConstraintService(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    print(f"ConstraintService listening on port {PORT}", flush=True)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
