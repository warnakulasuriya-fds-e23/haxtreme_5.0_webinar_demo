"""Example investigation client.

Demonstrates the reconnaissance workflow a contestant would follow:

    Phase 1  -> Query TopologyService + ConstraintService
    Phase 2  -> Form a hypothesis (done by the human, not this script)
    Phase 3  -> Test the hypothesis with OracleService
    Phase 4  -> Validate the approach with ValidationService

Usage (from the project/ directory, services running):

    python -m grpc_tools.protoc -Iprotos --python_out=client --grpc_python_out=client protos/challenge.proto
    python client/investigate.py --problem-id 2
"""

import argparse
import sys
import textwrap

import grpc

try:
    import challenge_pb2
    import challenge_pb2_grpc
except ImportError:
    sys.exit(
        "gRPC stubs not found. Generate them first:\n"
        "  python -m grpc_tools.protoc -Iprotos "
        "--python_out=client --grpc_python_out=client protos/challenge.proto"
    )

HOSTS = {
    "topology": "localhost:50051",
    "constraint": "localhost:50052",
    "oracle": "localhost:50053",
    "validation": "localhost:50054",
}


def query_topology(problem_id: int):
    with grpc.insecure_channel(HOSTS["topology"]) as channel:
        stub = challenge_pb2_grpc.TopologyServiceStub(channel)
        return stub.DescribeStructure(challenge_pb2.ProblemRequest(problem_id=problem_id))


def query_constraints(problem_id: int):
    with grpc.insecure_channel(HOSTS["constraint"]) as channel:
        stub = challenge_pb2_grpc.ConstraintServiceStub(channel)
        return stub.GetConstraints(challenge_pb2.ProblemRequest(problem_id=problem_id))


def query_oracle(problem_id: int, test_input: str):
    with grpc.insecure_channel(HOSTS["oracle"]) as channel:
        stub = challenge_pb2_grpc.OracleServiceStub(channel)
        return stub.RunTest(challenge_pb2.OracleRequest(problem_id=problem_id, input=test_input))


def query_validation(problem_id: int, algorithm: str, complexity: str):
    with grpc.insecure_channel(HOSTS["validation"]) as channel:
        stub = challenge_pb2_grpc.ValidationServiceStub(channel)
        return stub.ValidateApproach(
            challenge_pb2.ValidationRequest(
                problem_id=problem_id, algorithm=algorithm, complexity=complexity
            )
        )


def main():
    parser = argparse.ArgumentParser(description="Investigate a hidden problem.")
    parser.add_argument("--problem-id", type=int, required=True)
    args = parser.parse_args()
    pid = args.problem_id

    print("=" * 64)
    print(f"PHASE 1 — INVESTIGATE (problem_id={pid})")
    print("=" * 64)
    topo = query_topology(pid)
    print("\nTopologyService.DescribeStructure:")
    print(
        textwrap.indent(
            "{\n"
            f'  "data_type": "{topo.data_type}",\n'
            f'  "directed": {str(topo.directed).lower()},\n'
            f'  "weighted": {str(topo.weighted).lower()},\n'
            f'  "has_negative_weights": {str(topo.has_negative_weights).lower()},\n'
            f'  "has_cycles": {str(topo.has_cycles).lower()}\n'
            "}",
            "  ",
        )
    )
    print(f"  note: {topo.description}")
    print("  input_format:")
    print(textwrap.indent(topo.input_format, "    "))

    cons = query_constraints(pid)
    print("\nConstraintService.GetConstraints:")
    print(
        textwrap.indent(
            "{\n"
            f'  "max_n": {cons.max_n},\n'
            f'  "max_m": {cons.max_m},\n'
            f'  "time_limit_ms": {cons.time_limit_ms},\n'
            f'  "value_range": "{cons.value_range}",\n'
            f'  "edge_case_flags": {list(cons.edge_case_flags)}\n'
            "}",
            "  ",
        )
    )

    print("\n" + "=" * 64)
    print("PHASE 3 — TEST WITH ORACLE (example small test)")
    print("=" * 64)
    if pid == 2:
        test_input = "3 3\n1 2 -3\n2 3 5\n1 3 10\n"
    else:
        test_input = "5\n4 8 2 7 1\n"
    print(f"\nOracleService.RunTest input:\n{textwrap.indent(test_input, '  ')}")
    oracle = query_oracle(pid, test_input)
    print(f"  status: {oracle.status}")
    print(f"  output: {oracle.output}")
    print(f"  message: {oracle.message}")

    print("\n" + "=" * 64)
    print("PHASE 4 — VALIDATE APPROACH (example candidates)")
    print("=" * 64)
    candidates = (
        [("DIJKSTRA", "O((V+E) log V)"), ("BELLMAN_FORD", "O(VE)"), ("DAG_SHORTEST_PATH", "O(V+E)")]
        if pid == 2
        else [("SORTING", "O(N log N)"), ("LINEAR_SCAN", "O(N)")]
    )
    for algorithm, complexity in candidates:
        resp = query_validation(pid, algorithm, complexity)
        print(f"\n  {algorithm} / {complexity}")
        print(f"    result : {resp.result}")
        print(f"    message: {resp.message}")


if __name__ == "__main__":
    main()
