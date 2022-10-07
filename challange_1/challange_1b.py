from typing import Tuple, List


class DirectedGraph:
    """
    A Directed Graph with Adjacency list
    It can have maximum nodes 6
    """

    max_routers = 6

    def __init__(self, edges: List[Tuple[int, int]]) -> None:
        self.data = [[] for _ in range(self.max_routers + 1)]
        for n1, n2 in edges:
            self.data[n1].append(n2)

    def __repr__(self) -> str:
        return "\n".join(["{}: {}".format(v, i) for v, i in enumerate(self.data)])

    def __str__(self) -> str:
        return self.__repr__()


def identify_router(edges: List[Tuple[int, int]]) -> Tuple[int]:
    """
    Identifies the nodes with the most number of connections

    Args
        - edges

    Returns
        - list of routes with max connections

    Examples
        -   1 -> 2 -> 3 -> 5 -> 2 -> 1 = 2 *since router 2 has 2 inbound links and 2 outbound links
        -   1 -> 3 -> 5 -> 6 -> 4 -> 5 -> 2 -> 6 = 5 * since router 5 has 2 inbound links and 2 outbound link

    Time Complexity - O(n), we are applying BFS, then every node visited atleast once. also where `n` denoting the number of edges

    """

    graph = DirectedGraph(edges=edges)
    root = edges[0][0]

    routers_total_inbound_outbound_links = [0 for _ in range(graph.max_routers + 1)]
    visited = [False] * len(graph.data)

    queue = []
    visited[root] = True

    queue.append(root)
    idx = 0

    while idx < len(queue):
        # dequeue
        current = queue[idx]
        idx += 1

        routers_total_inbound_outbound_links[current] += len(graph.data[current])
        # chcek for all the outbound links
        # and push the nodes into queue
        for node in graph.data[current]:
            routers_total_inbound_outbound_links[node] += 1
            if not visited[node]:
                visited[node] = True
                queue.append(node)

    max_connections = max(routers_total_inbound_outbound_links)
    return [
        route
        for route, links in enumerate(routers_total_inbound_outbound_links)
        if links == max_connections
    ]
