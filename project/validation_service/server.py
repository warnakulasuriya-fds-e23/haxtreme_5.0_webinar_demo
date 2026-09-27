"""ValidationService — gives only coarse feedback about a candidate approach."""

import os
from concurrent import futures

import grpc

import challenge_pb2
import challenge_pb2_grpc
from problem_data import PROBLEMS

PORT = os.environ.get("PORT", "50054")


def _normalize(text: str) -> str:
    return "".join(text.upper().split())


class ValidationService(challenge_pb2_grpc.ValidationServiceServicer):
    def ValidateApproach(self, request, context):
        problem = PROBLEMS.get(request.problem_id)
        if problem is None:
            return challenge_pb2.ValidationResponse(
                problem_id=request.problem_id,
                result="UNKNOWN_PROBLEM",
                message=f"Unknown problem_id: {request.problem_id}",
            )

        rules = problem["validation"]
        algorithm = _normalize(request.algorithm)
        complexity = _normalize(request.complexity)
        accepted = {_normalize(a) for a in rules["accepted_algorithms"]}
        required = {_normalize(c) for c in rules["required_complexity"]}
        hints = {_normalize(k): v for k, v in rules["hints"].items()}

        if algorithm in accepted:
            if complexity in required:
                return challenge_pb2.ValidationResponse(
                    problem_id=request.problem_id,
                    result="COMPLEXITY_MATCHES",
                    message=(
                        f"Approach '{request.algorithm}' with complexity "
                        f"'{request.complexity}' fits the hidden constraints."
                    ),
                )
            return challenge_pb2.ValidationResponse(
                problem_id=request.problem_id,
                result="COMPLEXITY_MISMATCH",
                message=(
                    f"'{request.algorithm}' is the right family, but "
                    f"'{request.complexity}' does not match the required "
                    "complexity class."
                ),
            )

        if algorithm in hints:
            message = hints[algorithm]
        else:
            message = (
                "This approach does not fit the hidden problem properties. "
                "Re-check TopologyService and ConstraintService evidence."
            )
        return challenge_pb2.ValidationResponse(
            problem_id=request.problem_id,
            result="ALGORITHM_REJECTED",
            message=message,
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    challenge_pb2_grpc.add_ValidationServiceServicer_to_server(ValidationService(), server)
    server.add_insecure_port(f"[::]:{PORT}")
    server.start()
    print(f"ValidationService listening on port {PORT}", flush=True)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
