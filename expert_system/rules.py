"""Basis aturan (sistem pakar) untuk menafsirkan hasil pencarian rute.

Setiap aturan: JIKA <kondisi pada fakta> MAKA <tingkat status + saran>.
Tingkat status: 0 = LANCAR, 1 = PERHATIAN, 2 = TERGANGGU.
"""
from dataclasses import dataclass
from typing import Callable, List

from search_algorithm import SearchResult, TransitNetwork

STATUS = {0: "LANCAR", 1: "PERHATIAN", 2: "TERGANGGU"}
BANYAK_PINDAH = 2       # pindah jalur >= 2 kali dianggap merepotkan
PERJALANAN_LAMA = 40.0  # menit
FAKTOR_JAM_SIBUK = 1.3  # waktu bertambah ~30% saat jam sibuk


@dataclass
class Facts:
    net: TransitNetwork
    start: str
    goal: str
    closed_stations: frozenset
    closed_lines: frozenset
    rush_hour: bool
    result: SearchResult
    baseline: SearchResult   # hasil jika tidak ada gangguan

    def name(self, sid: str) -> str:
        return self.net.stations[sid].name

    @property
    def same_place(self) -> bool:
        return self.start == self.goal

    @property
    def start_closed(self) -> bool:
        return self.start in self.closed_stations

    @property
    def goal_closed(self) -> bool:
        return self.goal in self.closed_stations

    @property
    def disrupted(self) -> bool:
        return bool(self.closed_stations or self.closed_lines)

    @property
    def detour(self) -> float:
        if not (self.result.found and self.baseline.found):
            return 0.0
        return round(self.result.minutes - self.baseline.minutes, 1)


@dataclass
class Rule:
    id: str
    level: int
    condition: Callable[[Facts], bool]
    message: Callable[[Facts], str]


RULES: List[Rule] = [
    Rule("R1", 2, lambda f: f.start_closed or f.goal_closed,
         lambda f: "Stasiun asal atau tujuan sedang ditutup, jadi Anda tidak bisa naik atau turun di sana. "
                   "Pilih stasiun terdekat lain."),
    Rule("R2", 2, lambda f: not f.result.found and not f.same_place and not (f.start_closed or f.goal_closed),
         lambda f: "Tidak ada rute yang bisa dipakai. Pertimbangkan bus, ojek online, atau tunggu jalur dibuka lagi."),
    Rule("R3", 1, lambda f: f.result.found and (f.result.transfers or 0) >= BANYAK_PINDAH,
         lambda f: f"Anda harus pindah jalur {f.result.transfers} kali. "
                   "Perhatikan waktu pindah di tiap stasiun dan jaga barang bawaan."),
    Rule("R4", 1, lambda f: f.result.found and f.disrupted and f.detour > 0,
         lambda f: f"Ada gangguan di jaringan. Perjalanan lebih lama +{f.detour} menit dari kondisi normal."),
    Rule("R5", 1, lambda f: f.result.found and (f.result.minutes or 0) > PERJALANAN_LAMA,
         lambda f: f"Perjalanan cukup lama ({f.result.minutes} menit). Siapkan waktu lebih."),
    Rule("R6", 1, lambda f: f.result.found and f.rush_hour and not f.same_place,
         lambda f: f"Jam sibuk: kereta padat. Perkirakan waktu sekitar "
                   f"{round((f.result.minutes or 0) * FAKTOR_JAM_SIBUK, 1)} menit."),
    Rule("R7", 0, lambda f: f.result.found and (f.result.transfers or 0) == 0 and not f.same_place,
         lambda f: "Perjalanan langsung tanpa pindah jalur."),
    Rule("R8", 0, lambda f: f.same_place and not f.start_closed,
         lambda f: "Asal dan tujuan sama. Anda sudah berada di tujuan."),
    Rule("R9", 0, lambda f: f.result.found and not f.disrupted and not f.same_place,
         lambda f: "Jaringan normal, tidak ada gangguan. Rute di bawah adalah rute terbaik."),
    Rule("R10", 1, lambda f: len(f.closed_stations) >= 2,
         lambda f: f"{len(f.closed_stations)} stasiun ditutup sekaligus. Cek informasi petugas sebelum berangkat."),
]
