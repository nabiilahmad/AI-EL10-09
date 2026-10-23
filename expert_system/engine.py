from dataclasses import dataclass
from typing import List

from search_algorithm import ALGORITHMS, SearchResult, TransitNetwork, segments, TRANSFER_MINUTES
from .rules import RULES, STATUS, Facts


@dataclass
class Diagnosis:
    status: str
    result: SearchResult
    messages: List[str]
    fired_rules: List[str]
    route_text: List[str]


def route_text(net: TransitNetwork, path) -> List[str]:
    """Ubah rute menjadi kalimat: 'Naik Jalur Merah: A -> B' dan 'Pindah ke ... di ...'."""
    lines = []
    segs = segments(path)
    for i, (lid, stops) in enumerate(segs):
        names = " -> ".join(net.stations[s].name for s in stops)
        if i > 0:
            lines.append(f"Pindah ke {net.lines[lid].name} di {net.stations[stops[0]].name} "
                         f"({TRANSFER_MINUTES:g} menit)")
        if len(stops) > 1:
            lines.append(f"Naik {net.lines[lid].name}: {names}")
    return lines


def diagnose(net: TransitNetwork, start: str, goal: str, closed_stations=(), closed_lines=(),
             algorithm: str = "UCS", rush_hour: bool = False) -> Diagnosis:
    for sid in (start, goal):
        if sid not in net.stations:
            raise KeyError(f"Stasiun tidak dikenal: {sid}")
    for sid in closed_stations:
        if sid not in net.stations:
            raise KeyError(f"Stasiun tidak dikenal: {sid}")
    for lid in closed_lines:
        if lid not in net.lines:
            raise KeyError(f"Jalur tidak dikenal: {lid}")
    if algorithm not in ALGORITHMS:
        raise KeyError(f"Algoritma tidak dikenal: {algorithm}")

    cs, cl = frozenset(closed_stations), frozenset(closed_lines)
    search = ALGORITHMS[algorithm]
    result = search(net, start, goal, cs, cl)
    baseline = search(net, start, goal, (), ())
    if start == goal and not result.found and start not in cs:
        lid = net.lines_at[start][0]
        result = SearchResult(algorithm, [(start, lid)], 0.0, 0, 0, 0)
        baseline = result
    facts = Facts(net, start, goal, cs, cl, rush_hour, result, baseline)

    fired = [r for r in RULES if r.condition(facts)]
    level = max((r.level for r in fired), default=0)
    text = route_text(net, result.path) if result.found else []
    return Diagnosis(STATUS[level], result, [r.message(facts) for r in fired],
                     [r.id for r in fired], text)
