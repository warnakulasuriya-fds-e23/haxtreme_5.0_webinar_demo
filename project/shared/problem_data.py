"""Hidden problem registry — the single source of truth for all four services.

IMPORTANT: This data is deliberately NOT published in dummy_hackerrank.
Contestants only receive a problem_id and must query the gRPC services to
uncover the decisive properties (topology, constraints, oracle outputs and
approach validation).
"""

PROBLEMS = {
    # ------------------------------------------------------------------
    # Problem 1 — warm-up: a very simple problem.
    # "Sum It Up": given a sequence of integers, output their total sum.
    # ------------------------------------------------------------------
    1: {
        "title": "Sum It Up",
        "topology": {
            "data_type": "sequence",
            "directed": False,
            "weighted": False,
            "has_negative_weights": False,
            "has_cycles": False,
            "description": (
                "The input is a flat sequence of integers. There is no "
                "graph, tree or grid structure involved."
            ),
            "input_format": (
                "Line 1: integer n (the number of values).\n"
                "Next line(s): n space-separated integers a_1 ... a_n "
                "(may span multiple lines)."
            ),
        },
        "constraints": {
            "max_n": 100_000,
            "max_m": 0,
            "time_limit_ms": 1000,
            "value_range": "-10^9 <= a_i <= 10^9 (use 64-bit arithmetic)",
            "edge_case_flags": [
                "n_can_be_zero",
                "values_can_be_negative",
                "sum_may_exceed_32bit",
            ],
        },
        "validation": {
            "accepted_algorithms": {"LINEAR_SCAN", "PREFIX_SUM", "ITERATIVE_SUM"},
            "required_complexity": {"O(N)", "O(n)"},
            "hints": {
                "SORTING": "Sorting is unnecessary — the answer does not depend on order.",
                "BINARY_SEARCH": "There is nothing to search; every element contributes.",
            },
        },
    },
    # ------------------------------------------------------------------
    # Problem 2 — the Hidden Delivery Route Challenge.
    # Cheapest cost from Warehouse 1 to Warehouse N in a directed, weighted
    # graph that MAY contain negative-weight promotional routes but is
    # guaranteed acyclic  =>  DAG shortest path in O(V + E).
    # ------------------------------------------------------------------
    2: {
        "title": "Hidden Delivery Route Challenge",
        "topology": {
            "data_type": "graph",
            "directed": True,
            "weighted": True,
            "has_negative_weights": True,
            "has_cycles": False,
            "description": (
                "Warehouses form a directed weighted graph. Promotional "
                "routes may have negative cost, but the route network is "
                "guaranteed to be acyclic."
            ),
            "input_format": (
                "Line 1: two integers N M (warehouses, routes).\n"
                "Next M lines: three integers u v w — a DIRECTED route from "
                "warehouse u to warehouse v with cost w (w may be negative).\n"
                "Warehouses are numbered 1..N; source = 1, destination = N."
            ),
        },
        "constraints": {
            "max_n": 50_000,          # max_vertices
            "max_m": 200_000,         # max_edges
            "time_limit_ms": 2000,
            "value_range": "-10^4 <= w <= 10^4 per route",
            "edge_case_flags": [
                "destination_may_be_unreachable",
                "negative_edge_weights",
                "graph_is_acyclic",
                "no_negative_cycles_possible",
            ],
        },
        "validation": {
            "accepted_algorithms": {"DAG_SHORTEST_PATH"},
            "required_complexity": {"O(V+E)", "O(V + E)", "O(N+M)", "O(N + M)"},
            "hints": {
                "DIJKSTRA": "Dijkstra is incorrect here: negative edge weights exist.",
                "BELLMAN_FORD": "Bellman-Ford is correct but O(VE) is far too slow for these limits.",
                "BFS": "The graph is weighted — BFS only counts edges.",
                "FLOYD_WARSHALL": "Floyd-Warshall is O(V^3) — hopeless at this scale.",
            },
        },
    },
}
