"""MetroRoute AI - titik masuk program.

    python main.py                       -> buka GUI (Tkinter)
    python main.py --list                -> daftar id stasiun dan jalur
    python main.py --cli --from sekolah --to bandara --algo "A*"
    python main.py --cli --from pasar_barat --to bandara --closed-stations pusat --rush
"""
import argparse
import os

from expert_system import diagnose
from search_algorithm import ALGORITHMS, TransitNetwork

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "jaringan.json")


def split(value):
    return [v for v in value.split(",") if v]


def main():
    p = argparse.ArgumentParser(description="MetroRoute AI: perencana rute transportasi umum.")
    p.add_argument("--cli", action="store_true", help="jalankan tanpa GUI")
    p.add_argument("--list", action="store_true", help="tampilkan id stasiun dan jalur")
    p.add_argument("--from", dest="start", default="sekolah", help="id stasiun asal")
    p.add_argument("--to", dest="goal", default="bandara", help="id stasiun tujuan")
    p.add_argument("--closed-stations", default="", help="id stasiun tertutup, pisahkan dengan koma")
    p.add_argument("--closed-lines", default="", help="id jalur gangguan, pisahkan dengan koma")
    p.add_argument("--algo", default="UCS", choices=list(ALGORITHMS))
    p.add_argument("--rush", action="store_true", help="anggap jam sibuk")
    a = p.parse_args()

    net = TransitNetwork.from_json(DATA)
    if a.list:
        print("Stasiun:")
        for i, s in net.stations.items():
            print(f"  {i:<16} {s.name}")
        print("Jalur:")
        for i, l in net.lines.items():
            print(f"  {i:<8} {l.name}")
        return
    if a.cli:
        d = diagnose(net, a.start, a.goal, split(a.closed_stations), split(a.closed_lines), a.algo, a.rush)
        print(f"Status : {d.status}")
        if d.result.found:
            r = d.result
            print(f"Waktu  : {r.minutes} menit | pindah stasiun {r.rides}x | pindah jalur {r.transfers}x "
                  f"| diekspansi {r.expanded} ({r.algorithm})")
            for line in d.route_text:
                print(f"  * {line}")
        else:
            print("Rute   : tidak ditemukan")
        print("Saran  :")
        for m in d.messages:
            print(f"  - {m}")
        return
    from app.gui import launch
    launch(net)


if __name__ == "__main__":
    main()
