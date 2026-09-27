# gRPC Tutorial (grpcurl)

Run all commands from the directory containing `challenge.proto` (in this repo: `cd protos`).
Install grpcurl: https://github.com/fullstorydev/grpcurl/releases (or `brew install grpcurl`).

| Service | Port | Reveals |
|---|---|---|
| TopologyService | 50051 | Input structure and exact input format |
| ConstraintService | 50052 | Limits, time budget, edge-case flags |
| OracleService | 50053 | Correct output for your own small test |
| ValidationService | 50054 | Coarse feedback on algorithm + complexity |

## List services and methods

```bash
grpcurl -import-path . -proto challenge.proto list
grpcurl -import-path . -proto challenge.proto describe challenge.TopologyService
```

## 1. Topology: input structure

```bash
grpcurl -plaintext -emit-defaults -import-path . -proto challenge.proto -d '{"problem_id": 1}' 54.37.231.25:50051 challenge.TopologyService/DescribeStructure
```

## 2. Constraints: limits

```bash
grpcurl -plaintext -emit-defaults -import-path . -proto challenge.proto -d '{"problem_id": 1}' 54.37.231.25:50052 challenge.ConstraintService/GetConstraints
```

## 3. Oracle: test your own small input

Write newlines in the input as `\n`.

```bash
grpcurl -plaintext -emit-defaults -import-path . -proto challenge.proto -d '{"problem_id": 1, "input": "3\n1 2 3\n"}' 54.37.231.25:50053 challenge.OracleService/RunTest
```

## 4. Validation: check your approach

```bash
grpcurl -plaintext -emit-defaults -import-path . -proto challenge.proto -d '{"problem_id": 1, "algorithm": "LINEAR_SCAN", "complexity": "O(N)"}' 54.37.231.25:50054 challenge.ValidationService/ValidateApproach
```

Results: `COMPLEXITY_MATCHES`, `COMPLEXITY_MISMATCH`, `ALGORITHM_REJECTED` (read `message`), `UNKNOWN_PROBLEM`.

For other problems, change `problem_id` (e.g. `2`) and use your own input and algorithm.

## Notes

- Keep `-emit-defaults`: without it, fields that are `false` or `0` are hidden from the output.
- `server does not support the reflection API`: you forgot `-import-path . -proto challenge.proto`.
- `open challenge.proto: no such file`: run from the directory containing the file.
- `first record does not look like a TLS handshake`: add `-plaintext`.
- `int64` values are printed as strings (e.g. `"maxN": "123"`); this is normal.
