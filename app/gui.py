"""Antarmuka Tkinter untuk MetroRoute AI."""
import tkinter as tk
from tkinter import ttk

from expert_system import diagnose
from search_algorithm import ALGORITHMS, TransitNetwork

COLOR_STATUS = {"LANCAR": "#1b873f", "PERHATIAN": "#b7791f", "TERGANGGU": "#c53030"}
SCALE, MARGIN_X, MARGIN_Y = 42, 60, 40
KM_X0, KM_Y_MAX = 1, 10


class App(tk.Tk):
    def __init__(self, net: TransitNetwork):
        super().__init__()
        self.title("MetroRoute AI - Perencana Rute Transportasi Umum")
        self.net = net
        self.name_to_id = {s.name: i for i, s in net.stations.items()}
        self._build_controls()
        self._build_canvas()
        self._build_output()
        self.draw()

    # ---------- tata letak ----------
    def _build_controls(self):
        f = ttk.Frame(self, padding=8)
        f.pack(fill="x")
        names = list(self.name_to_id)
        ttk.Label(f, text="Asal:").grid(row=0, column=0, sticky="w")
        self.from_var = tk.StringVar(value="Sekolah")
        ttk.Combobox(f, textvariable=self.from_var, values=names, state="readonly", width=20).grid(row=0, column=1, padx=6)
        ttk.Label(f, text="Tujuan:").grid(row=1, column=0, sticky="w", pady=3)
        self.to_var = tk.StringVar(value="Bandara")
        ttk.Combobox(f, textvariable=self.to_var, values=names, state="readonly", width=20).grid(row=1, column=1, padx=6)
        ttk.Label(f, text="Algoritma:").grid(row=2, column=0, sticky="w")
        self.algo_var = tk.StringVar(value="UCS")
        ttk.Combobox(f, textvariable=self.algo_var, values=list(ALGORITHMS), state="readonly", width=20).grid(row=2, column=1, padx=6)

        ttk.Label(f, text="Stasiun ditutup\n(pilih lebih dari satu\nboleh, tahan Ctrl):").grid(row=0, column=2, rowspan=3, padx=10)
        self.closed_list = tk.Listbox(f, selectmode=tk.MULTIPLE, height=5, exportselection=False, width=20)
        for n in names:
            self.closed_list.insert(tk.END, n)
        self.closed_list.grid(row=0, column=3, rowspan=3)
        sb = ttk.Scrollbar(f, command=self.closed_list.yview)
        self.closed_list.config(yscrollcommand=sb.set)
        sb.grid(row=0, column=4, rowspan=3, sticky="ns")

        lf = ttk.LabelFrame(f, text="Jalur gangguan", padding=4)
        lf.grid(row=0, column=5, rowspan=3, padx=10)
        self.line_vars = {}
        for lid, line in self.net.lines.items():
            v = tk.BooleanVar(value=False)
            tk.Checkbutton(lf, text=line.name, variable=v, fg=line.color, anchor="w").pack(anchor="w")
            self.line_vars[lid] = v
        self.rush_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(f, text="Jam sibuk", variable=self.rush_var).grid(row=0, column=6, padx=10)
        ttk.Button(f, text="Cari Rute", command=self.run).grid(row=1, column=6, padx=10)
        ttk.Button(f, text="Reset", command=self.reset).grid(row=2, column=6, padx=10)

    def _build_canvas(self):
        w = 13 * SCALE + 2 * MARGIN_X
        h = 10 * SCALE + 2 * MARGIN_Y
        self.canvas = tk.Canvas(self, width=w, height=h, bg="white", highlightthickness=1,
                                highlightbackground="#999")
        self.canvas.pack(padx=8, pady=4)
        ttk.Label(self, font=("Arial", 8),
                  text="Garis tebal gelap = rute | Cincin biru = asal | Cincin hijau = tujuan | "
                       "Merah + X = stasiun tutup").pack()

    def _build_output(self):
        f = ttk.Frame(self, padding=8)
        f.pack(fill="both", expand=True)
        self.status_lbl = tk.Label(f, text="Status: -", font=("Arial", 14, "bold"))
        self.status_lbl.pack(anchor="w")
        self.output = tk.Text(f, height=10, width=100, wrap="word", state="disabled")
        self.output.pack(fill="both", expand=True)

    # ---------- aksi ----------
    def _closed_stations(self):
        return {self.name_to_id[self.closed_list.get(i)] for i in self.closed_list.curselection()}

    def _closed_lines(self):
        return {lid for lid, v in self.line_vars.items() if v.get()}

    def run(self):
        start, goal = self.name_to_id[self.from_var.get()], self.name_to_id[self.to_var.get()]
        cs, cl = self._closed_stations(), self._closed_lines()
        d = diagnose(self.net, start, goal, cs, cl, self.algo_var.get(), self.rush_var.get())
        self.status_lbl.config(text=f"Status: {d.status}", fg=COLOR_STATUS[d.status])
        lines = []
        if d.result.found:
            r = d.result
            lines.append(f"Waktu: {r.minutes} menit | Pindah stasiun: {r.rides}x | Pindah jalur: {r.transfers}x | "
                         f"Keadaan diekspansi: {r.expanded} ({r.algorithm})")
            lines += [f"  * {t}" for t in d.route_text]
        else:
            lines.append("Rute: tidak ditemukan")
        lines += ["", "Saran / hasil aturan:"] + [f"- {m}" for m in d.messages]
        self._write("\n".join(lines))
        self.draw(d, start, goal, cs)

    def reset(self):
        self.closed_list.selection_clear(0, tk.END)
        for v in self.line_vars.values():
            v.set(False)
        self.rush_var.set(False)
        self.status_lbl.config(text="Status: -", fg="black")
        self._write("")
        self.draw()

    def _write(self, text):
        self.output.config(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)
        self.output.config(state="disabled")

    # ---------- gambar peta ----------
    def _pos(self, sid):
        s = self.net.stations[sid]
        return MARGIN_X + (s.x - KM_X0) * SCALE, MARGIN_Y + (KM_Y_MAX - s.y) * SCALE

    def draw(self, d=None, start=None, goal=None, closed=()):
        cv = self.canvas
        cv.delete("all")
        used = set()
        if d and d.result.found:
            for (s1, l1), (s2, l2) in zip(d.result.path, d.result.path[1:]):
                if l1 == l2:
                    used.add((l1, frozenset((s1, s2))))
        for lid, line in self.net.lines.items():
            for a, b in zip(line.stations, line.stations[1:]):
                p, q = self._pos(a), self._pos(b)
                if (lid, frozenset((a, b))) in used:
                    cv.create_line(*p, *q, fill="#1a202c", width=9)
                cv.create_line(*p, *q, fill=line.color, width=4)
        for sid, s in self.net.stations.items():
            x, y = self._pos(sid)
            fill = "#e53e3e" if sid in closed else "white"
            outline, width = "#4a5568", 2
            if sid == start:
                outline, width = "#2b6cb0", 4
            if sid == goal and sid != start:
                outline, width = "#2f855a", 4
            cv.create_oval(x - 9, y - 9, x + 9, y + 9, fill=fill, outline=outline, width=width)
            if sid in closed:
                cv.create_text(x, y, text="X", fill="white", font=("Arial", 9, "bold"))
            cv.create_text(x, y + 20, text=s.name, font=("Arial", 8))


def launch(net: TransitNetwork):
    App(net).mainloop()
