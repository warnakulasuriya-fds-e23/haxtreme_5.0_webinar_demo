# Multi-Service Algorithm Identification Challenge

Four gRPC microservices that hide the decisive details of competitive-programming
problems. Contestants see only the public statements (in `../dummy_hackerrank`)
and must interrogate these services to deduce the correct algorithm.

## Services

| Service            | Port  | Reveals                                                        |
|--------------------|-------|----------------------------------------------------------------|
| TopologyService    | 50051 | Input structure: sequence/graph, directed, weighted, negative weights, cycles, exact input format |
| ConstraintService  | 50052 | Scale limits, time budget, value ranges, edge-case flags       |
| OracleService      | 50053 | Correct output for a small custom test input                   |
| ValidationService  | 50054 | Coarse feedback on a candidate (algorithm, complexity) pair    |

## Registered problems

| problem_id | Title                          | Hidden truth (never published)                                   |
|------------|--------------------------------|------------------------------------------------------------------|
| 1          | Sum It Up                      | Sequence, N ≤ 100000, 1s → linear scan O(N)                      |
| 2          | Hidden Delivery Route Challenge| Directed weighted **DAG with negative edges**, V ≤ 50000, E ≤ 200000, 2s → **DAG shortest path O(V+E)** |

## Run everything

```bash
cd project
docker compose up --build
```

## Try the investigation workflow

```bash
pip install grpcio grpcio-tools
python -m grpc_tools.protoc -Iprotos --python_out=client --grpc_python_out=client protos/challenge.proto
python client/investigate.py --problem-id 2
```

## Dummy contest page

The public, HackerRank-style problem statements live in `../dummy_hackerrank`.
It is plain static HTML/CSS/JS — open `dummy_hackerrank/index.html` directly, or:

```bash
cd ../dummy_hackerrank && python3 -m http.server 8080   # http://localhost:8080
```

The page only shows the story, the output format and the `problem_id`. The input
format/shape (TopologyService), constraints (ConstraintService), worked examples
(OracleService) and the expected complexity (ValidationService) appear **only**
through the services.

## Layout

```
project/
├── docker-compose.yml          # single-command deployment of all 4 services
├── protos/challenge.proto      # the shared gRPC contract
├── shared/problem_data.py      # hidden problem registry (source of truth)
├── client/investigate.py       # example reconnaissance client
├── topology_service/           # Dockerfile + server.py + requirements.txt
├── constraint_service/
├── oracle_service/             # also holds the hidden reference solutions
└── validation_service/
```
