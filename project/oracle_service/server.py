"""OracleService — runs the hidden reference solution on a small custom input."""

import os
from concurrent import futures

import grpc

import challenge_pb2
import challenge_pb2_grpc
from problem_data import PROBLEMS
from reference_solutions import MAX_INPUT_BYTES, MAX_TOKENS, SOLVERS

PORT = os.environ.get("PORT", "50053")


class OracleService(challenge_pb2_grpc.OracleServiceServicer):
    def RunTest(self, request, context):
        if request.problem_id not in PROBLEMS:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"Unknown problem_id: {request.problem_id}",
            )

        # The oracle is for small hypothesis tests only — guard the input.
        if len(request.input.encode("utf-8", errors="replace")) > MAX_INPUT_BYTES:
            return challenge_pb2.OracleResponse(
                problem_id=request.problem_id,
                status="ERROR",
                message=(
                    "Input too large. The oracle only answers small custom "
                    "tests; the real limits are revealed by ConstraintService."
                ),
            )
        if len(request.input.split()) > MAX_TOKENS:
            return challenge_pb2.OracleResponse(
                problem_id=request.problem_id,
                status="ERROR",
                message="Too many tokens for an oracle test. Keep it small.",
            )

        solver = SOLVERS[request.problem_id]
        try:
            output = solver(request.input)
        except Exception as exc:  # malformed input -> helpful error, not a crash
            return challenge_pb2.OracleResponse(
                problem_id=request.problem_id,
                status="ERROR",
                message=f"Invalid input: {exc}",
            )

        return challenge_pb2.OracleResponse(
            problem_id=request.problem_id,
            status="OK",
            output=output,
            message="Reference output for your custom test.",
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    challenge_pb2_grpc.add_OracleServiceServicer_to_server(OracleService(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    print(f"OracleService listening on port {PORT}", flush=True)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
