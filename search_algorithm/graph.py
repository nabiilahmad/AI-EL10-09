"""Model jaringan transportasi umum.

Kota punya beberapa STASIUN dan beberapa JALUR (line). Satu stasiun bisa dilayani
lebih dari satu jalur, dan penumpang boleh PINDAH JALUR di stasiun itu.

Karena pindah jalur memakan waktu, "keadaan" pencarian bukan hanya stasiun,
tetapi pasangan (stasiun, jalur yang sedang dinaiki).
"""
import json
import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

MIN_PER_KM = 2.0          # menit per km (kecepatan rata-rata 30 km/jam)
DWELL_MINUTES = 1.0       # waktu berhenti di tiap stasiun
TRANSFER_MINUTES = 5.0    # waktu pindah jalur

State = Tuple[str, str]   # (id stasiun, id jalur)


@dataclass(frozen=True)
class Station:
    id: str
    name: str
    x: float   # km
    y: float   # km


@dataclass(frozen=True)
class Line:
    id: str
    name: str
    color: str
    stations: Tuple[str, ...]


class TransitNetwork:
    def __init__(self, stations: List[Station], lines: List[Line]):
        self.stations: Dict[str, Station] = {s.id: s for s in stations}
        self.lines: Dict[str, Line] = {l.id: l for l in lines}
        self.lines_at: Dict[str, List[str]] = {s.id: [] for s in stations}
        self.ride: Dict[str, Dict[str, List[Tuple[str, float]]]] = {l.id: {} for l in lines}
        self.edge_minutes: Dict[Tuple[str, str, str], float] = {}
        for line in lines:
            for sid in line.stations:
                if sid not in self.stations:
                    raise ValueError(f"Stasiun tidak dikenal di {line.id}: {sid}")
                self.lines_at[sid].append(line.id)
            for a, b in zip(line.stations, line.stations[1:]):
                m = self._minutes(self.stations[a], self.stations[b])
                self.ride[line.id].setdefault(a, []).append((b, m))
                self.ride[line.id].setdefault(b, []).append((a, m))
                self.edge_minutes[(line.id, a, b)] = m
                self.edge_minutes[(line.id, b, a)] = m

    @staticmethod
    def _minutes(a: Station, b: Station) -> float:
        return round(MIN_PER_KM * math.hypot(a.x - b.x, a.y - b.y) + DWELL_MINUTES, 1)

    @classmethod
    def from_json(cls, path: str) -> "TransitNetwork":
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        stations = [Station(s["id"], s["name"], s["x"], s["y"]) for s in data["stations"]]
        lines = [Line(l["id"], l["name"], l["color"], tuple(l["stations"])) for l in data["lines"]]
        return cls(stations, lines)

    # ---- dipakai oleh algoritma pencarian ----
    def start_states(self, station: str, closed_stations=(), closed_lines=()) -> List[State]:
        """Keadaan awal: naik jalur mana pun yang melayani stasiun asal (tanpa biaya pindah)."""
        if station in closed_stations:
            return []
        return [(station, l) for l in self.lines_at[station] if l not in closed_lines]

    def neighbors(self, state: State, closed_stations=(), closed_lines=()):
        """Keadaan berikutnya + biaya (menit): lanjut satu stasiun di jalur yang sama,
        atau pindah ke jalur lain di stasiun yang sama. Stasiun/jalur tertutup dilewati."""
        sid, lid = state
        out = []
        for nbr, m in self.ride[lid].get(sid, []):
            if nbr not in closed_stations:
                out.append(((nbr, lid), m))
        for other in self.lines_at[sid]:
            if other != lid and other not in closed_lines:
                out.append(((sid, other), TRANSFER_MINUTES))
        return out

    def heuristic(self, station: str, goal: str) -> float:
        """Perkiraan waktu minimum ke tujuan: jarak garis lurus x 2 menit/km.
        Tidak pernah melebihi waktu sebenarnya, karena waktu naik >= 2 menit/km."""
        a, b = self.stations[station], self.stations[goal]
        return MIN_PER_KM * math.hypot(a.x - b.x, a.y - b.y)

    def path_minutes(self, path: List[State]) -> float:
        total = 0.0
        for (s1, l1), (s2, l2) in zip(path, path[1:]):
            total += self.edge_minutes[(l1, s1, s2)] if l1 == l2 else TRANSFER_MINUTES
        return round(total, 1)
