"""Algoritma pencarian rute transportasi umum: BFS, UCS, A*.

Semua menerima: jaringan, stasiun asal, stasiun tujuan, stasiun tertutup, jalur tertutup.
"""
import heapq
from collections import deque
from dataclasses import dataclass
from itertools import count
from typing import List, Optional, Tuple

from .graph import State, TransitNetwork


@dataclass
class SearchResult:
    algorithm: str
    path: Optional[List[State]]   # None jika tidak ada rute
    minutes: Optional[float]      # total waktu tempuh
    rides: Optional[int]          # berapa kali pindah stasiun (naik antar stasiun)
    transfers: Optional[int]      # berapa kali pindah jalur
    expanded: int                 # jumlah keadaan yang diekspansi

    @property
    def found(self) -> bool:
        return self.path is not None


def _build_path(parent, state):
    path = [state]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    return path[::-1]


def _result(name, net, parent, state, expanded):
    path = _build_path(parent, state)
    pairs = list(zip(path, path[1:]))
    transfers = sum(1 for a, b in pairs if a[1] != b[1])
    return SearchResult(name, path, net.path_minutes(path), len(pairs) - transfers, transfers, expanded)


def _none(name, expanded):
    return SearchResult(name, None, None, None, None, expanded)


def segments(path: List[State]) -> List[Tuple[str, List[str]]]:
    """Kelompokkan rute menjadi bagian per jalur: [(id_jalur, [stasiun...]), ...]."""
    segs: List[Tuple[str, List[str]]] = []
    for sid, lid in path:
        if not segs or segs[-1][0] != lid:
            segs.append((lid, [sid]))
        elif segs[-1][1][-1] != sid:
            segs[-1][1].append(sid)
    return segs


def bfs(net: TransitNetwork, start: str, goal: str, closed_stations=(), closed_lines=()) -> SearchResult:
    """Breadth-First Search: rute dengan langkah paling sedikit
    (pindah stasiun dan pindah jalur dihitung sama-sama 1 langkah)."""
    cs, cl = set(closed_stations), set(closed_lines)
    starts = net.start_states(start, cs, cl)
    frontier = deque(starts)
    parent = {s: None for s in starts}
    expanded = 0
    while frontier:
        state = frontier.popleft()
        expanded += 1
        if state[0] == goal:
            return _result("BFS", net, parent, state, expanded)
        for nxt, _ in net.neighbors(state, cs, cl):
            if nxt not in parent:
                parent[nxt] = state
                frontier.append(nxt)
    return _none("BFS", expanded)


def ucs(net: TransitNetwork, start: str, goal: str, closed_stations=(), closed_lines=()) -> SearchResult:
    """Uniform-Cost Search: rute dengan waktu tempuh (menit) tercepat."""
    cs, cl = set(closed_stations), set(closed_lines)
    tie = count()
    starts = net.start_states(start, cs, cl)
    frontier = [(0.0, next(tie), s) for s in starts]
    heapq.heapify(frontier)
    parent = {s: None for s in starts}
    best = {s: 0.0 for s in starts}
    done = set()
    expanded = 0
    while frontier:
        g, _, state = heapq.heappop(frontier)
        if state in done:
            continue
        done.add(state)
        expanded += 1
        if state[0] == goal:
            return _result("UCS", net, parent, state, expanded)
        for nxt, cost in net.neighbors(state, cs, cl):
            ng = g + cost
            if nxt not in best or ng < best[nxt]:
                best[nxt] = ng
                parent[nxt] = state
                heapq.heappush(frontier, (ng, next(tie), nxt))
    return _none("UCS", expanded)


def astar(net: TransitNetwork, start: str, goal: str, closed_stations=(), closed_lines=()) -> SearchResult:
    """A*: seperti UCS, dipandu perkiraan waktu sisa (jarak garis lurus ke tujuan)."""
    cs, cl = set(closed_stations), set(closed_lines)
    tie = count()
    starts = net.start_states(start, cs, cl)
    frontier = [(net.heuristic(s[0], goal), next(tie), 0.0, s) for s in starts]
    heapq.heapify(frontier)
    parent = {s: None for s in starts}
    best = {s: 0.0 for s in starts}
    done = set()
    expanded = 0
    while frontier:
        _, _, g, state = heapq.heappop(frontier)
        if state in done:
            continue
        done.add(state)
        expanded += 1
        if state[0] == goal:
            return _result("A*", net, parent, state, expanded)
        for nxt, cost in net.neighbors(state, cs, cl):
            ng = g + cost
            if nxt not in best or ng < best[nxt]:
                best[nxt] = ng
                parent[nxt] = state
                heapq.heappush(frontier, (ng + net.heuristic(nxt[0], goal), next(tie), ng, nxt))
    return _none("A*", expanded)


ALGORITHMS = {"BFS": bfs, "UCS": ucs, "A*": astar}
