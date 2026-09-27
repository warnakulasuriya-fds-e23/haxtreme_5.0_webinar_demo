"""Judge's hidden reference solutions used by OracleService.

These implementations are the ground truth. Contestants send a small custom
test input and receive the output produced by these reference solutions.
"""

import sys
from collections import deque

# Safety guards for the oracle: keep custom tests small.
MAX_INPUT_BYTES = 16 * 1024
MAX_TOKENS = 20_000


def solve_problem_1(data: str) -> str:
    """Sum It Up.

    Input:
        n
        a_1 a_2 ... a_n   (may span multiple lines)
    Output:
        sum of the n integers
    """
    tokens = data.split()
    if not tokens:
        raise ValueError("empty input")
    n = int(tokens[0])
    values = [int(t) for t in tokens[1:1 + n]]
    if len(values) < n:
        raise ValueError(f"expected {n} values, got {len(values)}")
    return str(sum(values))


def solve_problem_2(data: str) -> str:
    """Hidden Delivery Route Challenge — DAG shortest path from 1 to N.

    Input:
        N M
        u v w   (M lines, directed edge u -> v with cost w, w may be negative)
    Output:
        cheapest cost from vertex 1 to vertex N, or UNREACHABLE
    """
    tokens = data.split()
    if len(tokens) < 2:
        raise ValueError("input must start with: N M")
    n, m = int(tokens[0]), int(tokens[1])
    if n <= 0 or m < 0:
        raise ValueError("invalid N or M")
    if len(tokens) < 2 + 3 * m:
        raise ValueError(f"expected {m} edges (u v w per edge)")

    adj = [[] for _ in range(n + 1)]
    indegree = [0] * (n + 1)
    idx = 2
    for _ in range(m):
        u, v, w = int(tokens[idx]), int(tokens[idx + 1]), int(tokens[idx + 2])
        idx += 3
        if not (1 <= u <= n and 1 <= v <= n):
            raise ValueError(f"vertex out of range: {u} {v}")
        adj[u].append((v, w))
        indegree[v] += 1

    # Topological order (Kahn's algorithm).
    queue = deque(i for i in range(1, n + 1) if indegree[i] == 0)
    topo = []
    while queue:
        node = queue.popleft()
        topo.append(node)
        for nxt, _ in adj[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    if len(topo) < n:
        raise ValueError("graph contains a cycle; oracle expects a DAG")

    INF = sys.maxsize
    dist = [INF] * (n + 1)
    dist[1] = 0
    for u in topo:
        if dist[u] == INF:
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    return str(dist[n]) if dist[n] != INF else "UNREACHABLE"


SOLVERS = {
    1: solve_problem_1,
    2: solve_problem_2,
}
