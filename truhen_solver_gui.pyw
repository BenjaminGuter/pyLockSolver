import tkinter as tk
from collections import deque

def apply_move(state, hinge, direction, matrix, num_pins):
    new_state = list(state)
    for j in range(len(state)):
        influence = 1 if j == hinge else matrix[hinge][j]
        if influence == 0:
            continue
        new_pos = new_state[j] + direction * influence
        if new_pos < 0 or new_pos >= num_pins:
            return None
        new_state[j] = new_pos
    return tuple(new_state)


def solve(start, goal, matrix, num_pins):
    start = tuple(start)
    goal  = tuple(goal)
    if start == goal:
        return []
    visited = {start: (-1, 0, None)}
    queue   = deque([start])
    while queue:
        state = queue.popleft()
        for hinge in range(len(start)):
            for direction in [1, -1]:
                new_state = apply_move(state, hinge, direction, matrix, num_pins)
                if new_state is None or new_state in visited:
                    continue
                visited[new_state] = (hinge, direction, state)
                if new_state == goal:
                    return _reconstruct_path(visited, new_state)
                queue.append(new_state)
    return None


def _reconstruct_path(visited, goal_state):
    path = []
    current = goal_state
    while True:
        hinge, direction, previous = visited[current]
        if previous is None:
            break
        path.append((hinge, direction, previous))
        current = previous
    path.reverse()
    return path

BG       = "#f5f5f2"
BG_WHITE = "#ffffff"
BORDER   = "#dddddd"
FONT     = "Helvetica"

GREEN_BG = "#c0dd97"
GREEN_FG = "#3b6d11"
RED_BG   = "#f5c4b3"
RED_FG   = "#993c1d"
GRAY_BG  = "#eeeeee"
GRAY_FG  = "#888888"
BLUE_BG  = "#b5d4f4"
BLUE_FG  = "#0c447c"

ACCORDION_BG     = "#ececea"
ACCORDION_HEADER = "#ddddd9"

class Accordion(tk.Frame):

    def __init__(self, parent, title, expanded=True, **kwargs):
        super().__init__(parent, bg=BG, **kwargs)

        self._expanded = expanded
        self._title    = title

        self.header = tk.Frame(self, bg=ACCORDION_HEADER,
                               highlightthickness=1, highlightbackground=BORDER,
                               cursor="hand2")
        self.header.pack(fill="x")

        self._arrow = tk.Label(self.header, text="▾" if expanded else "▸",
                               font=(FONT, 11), bg=ACCORDION_HEADER, fg="#555",
                               width=2)
        self._arrow.pack(side="left", padx=(8, 0), pady=6)

        tk.Label(self.header, text=title, font=(FONT, 11, "bold"),
                 bg=ACCORDION_HEADER, fg="#333").pack(side="left", pady=6)

        for widget in (self.header, self._arrow):
            widget.bind("<Button-1>", self._toggle)

        self.body = tk.Frame(self, bg=BG_WHITE,
                             highlightthickness=1, highlightbackground=BORDER)
        if expanded:
            self.body.pack(fill="x")

    def _toggle(self, event=None):
        if self._expanded:
            self.body.pack_forget()
            self._arrow.configure(text="▸")
        else:
            self.body.pack(fill="x")
            self._arrow.configure(text="▾")
        self._expanded = not self._expanded

    def expand(self):
        if not self._expanded:
            self._toggle()

    def collapse(self):
        if self._expanded:
            self._toggle()

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Truhen-Scharnier-Solver")
        self.resizable(True, True)
        self.configure(bg=BG)

        self.num_hinges  = tk.IntVar(value=6)
        self.num_pins    = tk.IntVar(value=7)
        self.matrix_vars = []
        self.start_vars  = []
        self.goal_vars   = []

        self._build_header()
        self._build_input_accordion()
        self._build_solve_button()
        self._build_result_accordion()
        self._rebuild()

    def _build_header(self):
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=16, pady=(14, 8))

        tk.Label(bar, text="Truhen-Scharnier-Solver",
                 font=(FONT, 15, "bold"), bg=BG, fg="#111").pack(side="left")

        cfg = tk.Frame(bar, bg=BG)
        cfg.pack(side="right")

        tk.Label(cfg, text="Scharniere:", bg=BG, fg="#555",
                 font=(FONT, 10)).pack(side="left")
        tk.Spinbox(cfg, from_=1, to=10, textvariable=self.num_hinges,
                   width=3, font=(FONT, 10)).pack(side="left", padx=(2, 10))

        tk.Label(cfg, text="Löcher:", bg=BG, fg="#555",
                 font=(FONT, 10)).pack(side="left")
        tk.Spinbox(cfg, from_=2, to=12, textvariable=self.num_pins,
                   width=3, font=(FONT, 10)).pack(side="left", padx=(2, 10))

        tk.Button(cfg, text="Aufbauen", command=self._rebuild,
                  font=(FONT, 10), relief="groove",
                  cursor="hand2").pack(side="left")

    def _build_input_accordion(self):
        self._input_accordion = Accordion(self, title="Eingabe", expanded=True)
        self._input_accordion.pack(fill="x", padx=16, pady=(0, 6))

        self.state_holder  = tk.Frame(self._input_accordion.body, bg=BG_WHITE)
        self.state_holder.pack(fill="x")

        self.matrix_holder = tk.Frame(self._input_accordion.body, bg=BG_WHITE)
        self.matrix_holder.pack(fill="x")

    def _build_solve_button(self):
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", padx=16, pady=(0, 6))
        tk.Button(bar, text="Lösung berechnen", command=self._solve,
                  font=(FONT, 11, "bold"), relief="groove",
                  bg="#e8e8e8", cursor="hand2",
                  padx=12, pady=6).pack(side="left")

    def _build_result_accordion(self):
        self._result_accordion = Accordion(self, title="Lösung", expanded=True)
        self._result_accordion.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        container = tk.Frame(self._result_accordion.body, bg=BG)
        container.pack(fill="both", expand=True)

        self._result_canvas = tk.Canvas(container, bg=BG,
                                        highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical",
                                 command=self._result_canvas.yview)

        self._result_canvas.configure(yscrollcommand=scrollbar.set)
        self._result_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.result_frame = tk.Frame(self._result_canvas, bg=BG)
        self._result_window = self._result_canvas.create_window(
            (0, 0), window=self.result_frame, anchor="nw"
        )

        self.result_frame.bind("<Configure>", self._on_result_resize)
        self._result_canvas.bind("<Configure>", self._on_canvas_resize)
        self._result_canvas.bind_all("<MouseWheel>",
            lambda e: self._result_canvas.yview_scroll(
                -1 * (e.delta // 120), "units"))

    def _on_result_resize(self, event):
        self._result_canvas.configure(
            scrollregion=self._result_canvas.bbox("all"))

    def _on_canvas_resize(self, event):
        self._result_canvas.itemconfig(self._result_window, width=event.width)

    def _rebuild(self):
        H = self.num_hinges.get()
        P = self.num_pins.get()

        for holder in (self.state_holder, self.matrix_holder, self.result_frame):
            for widget in holder.winfo_children():
                widget.destroy()

        self.start_vars = [tk.IntVar(value=1) for _ in range(H)]
        self.goal_vars  = [tk.IntVar(value=1) for _ in range(H)]

        self._build_state_section(H, P)
        self._build_matrix_section(H)

    def _build_state_section(self, H, P):
        sec = tk.Frame(self.state_holder, bg=BG_WHITE)
        sec.pack(fill="x", padx=12, pady=(8, 4))

        tk.Label(sec, text="Start & Ziel", font=(FONT, 10, "bold"),
                 bg=BG_WHITE, fg="#444").grid(
                     row=0, column=0, columnspan=H + 1,
                     sticky="w", pady=(0, 6))

        for row_idx, (label, variables) in enumerate(
                [("Start", self.start_vars), ("Ziel", self.goal_vars)]):
            base_row = 1 + row_idx * 2

            tk.Label(sec, text=label, font=(FONT, 9, "bold"),
                     bg=BG_WHITE, fg="#888").grid(
                         row=base_row, column=0, padx=(0, 8), sticky="e")

            for i, var in enumerate(variables):
                tk.Spinbox(sec, from_=1, to=P, textvariable=var,
                           width=3, font=(FONT, 10)).grid(
                               row=base_row, column=i + 1, padx=3, pady=3)
                tk.Label(sec, text=f"S{i+1}", font=(FONT, 8),
                         bg=BG_WHITE, fg="#aaa").grid(
                             row=base_row + 1, column=i + 1)

        sec.grid_columnconfigure(0, minsize=40)

    def _build_matrix_section(self, H):
        tk.Frame(self.matrix_holder, bg=BORDER, height=1).pack(fill="x")

        sec = tk.Frame(self.matrix_holder, bg=BG_WHITE)
        sec.pack(fill="x", padx=12, pady=(8, 12))

        tk.Label(sec, text="Einfluss-Matrix", font=(FONT, 10, "bold"),
                 bg=BG_WHITE, fg="#444").grid(
                     row=0, column=0, columnspan=H + 1, sticky="w", pady=(0, 2))

        tk.Label(sec,
                 text="Zeile = bewegtes Scharnier   |   + gleiche Richtung   − entgegen   0 kein Einfluss",
                 font=(FONT, 8), bg=BG_WHITE, fg="#999").grid(
                     row=1, column=0, columnspan=H + 1, sticky="w", pady=(0, 6))

        self.matrix_vars = []

        for i in range(H):
            row_vars = []
            tk.Label(sec, text=f"S{i+1} bewegen →",
                     font=(FONT, 9), bg=BG_WHITE, fg="#555").grid(
                         row=i + 2, column=0, padx=(0, 6), sticky="e")

            for j in range(H):
                if i == j:
                    tk.Label(sec, text="•", bg=BG_WHITE, fg="#ccc",
                             font=(FONT, 12)).grid(
                                 row=i + 2, column=j + 1, padx=4, pady=2)
                    row_vars.append(None)
                else:
                    var = tk.IntVar(value=0)
                    btn = tk.Button(sec, width=3, font=(FONT, 10),
                                    relief="groove", cursor="hand2")
                    btn._var    = var
                    btn._strvar = tk.StringVar(value="0")
                    btn.configure(textvariable=btn._strvar,
                                  command=lambda b=btn, v=var: self._toggle_cell(b, v))
                    self._style_matrix_btn(btn, 0)
                    btn.grid(row=i + 2, column=j + 1, padx=3, pady=2)
                    row_vars.append((var, btn))

            self.matrix_vars.append(row_vars)

        for j in range(H):
            tk.Label(sec, text=f"S{j+1}", font=(FONT, 8),
                     bg=BG_WHITE, fg="#aaa").grid(
                         row=H + 2, column=j + 1, pady=(0, 4))

    def _toggle_cell(self, btn, var):
        current = var.get()
        new_val = 1 if current == 0 else (-1 if current == 1 else 0)
        var.set(new_val)
        self._style_matrix_btn(btn, new_val)

    def _style_matrix_btn(self, btn, val):
        if val == 1:
            btn.configure(bg=GREEN_BG, fg=GREEN_FG, activebackground="#a8cc7a")
            btn._strvar.set("+")
        elif val == -1:
            btn.configure(bg=RED_BG, fg=RED_FG, activebackground="#e8a898")
            btn._strvar.set("−")
        else:
            btn.configure(bg=GRAY_BG, fg=GRAY_FG, activebackground="#e0e0e0")
            btn._strvar.set("0")

    def _solve(self):
        H = self.num_hinges.get()
        P = self.num_pins.get()

        start  = [v.get() - 1 for v in self.start_vars]
        goal   = [v.get() - 1 for v in self.goal_vars]
        matrix = self._read_matrix(H)

        self._clear_result()
        tk.Label(self.result_frame, text="Suche läuft...",
                 font=(FONT, 10), bg=BG, fg="#888").pack(anchor="w", padx=8, pady=4)
        self.update()

        path = solve(start, goal, matrix, P)

        self._clear_result()
        self._result_accordion.expand()
        self._show_result(path)

    def _read_matrix(self, H):
        matrix = []
        for i in range(H):
            row = []
            for j in range(H):
                if i == j:
                    row.append(1)
                else:
                    entry = self.matrix_vars[i][j]
                    row.append(entry[0].get() if entry else 0)
            matrix.append(row)
        return matrix

    def _show_result(self, path):
        if path is None:
            tk.Label(self.result_frame,
                     text="Keine Lösung gefunden — Ziel nicht erreichbar ohne Wand zu treffen.",
                     font=(FONT, 10), bg=BG, fg="#c0392b",
                     wraplength=500, justify="left").pack(anchor="w", padx=8, pady=8)
            return

        if len(path) == 0:
            tk.Label(self.result_frame, text="Bereits am Ziel! Keine Züge nötig.",
                     font=(FONT, 10, "bold"), bg=BG, fg="#27ae60").pack(
                         anchor="w", padx=8, pady=8)
            return

        tk.Label(self.result_frame,
                 text=f"{len(path)} Züge gefunden — kein Zug trifft eine Wand:",
                 font=(FONT, 10), bg=BG, fg="#777").pack(
                     anchor="w", padx=8, pady=(8, 4))

        for i, (hinge, direction, before) in enumerate(path):
            from_pin = before[hinge] + 1
            to_pin   = from_pin + direction
            arrow    = "→" if direction == 1 else "←"

            row = tk.Frame(self.result_frame, bg=BG)
            row.pack(fill="x", padx=8, pady=2)

            tk.Label(row, text=str(i + 1), width=3,
                     font=(FONT, 9, "bold"),
                     bg=BLUE_BG, fg=BLUE_FG).pack(side="left", padx=(0, 8))

            key = "D" if direction == -1 else "A"

            tk.Label(row,
                     text=f"Scharnier {hinge+1}:  Loch {from_pin}  {arrow}  Loch {to_pin}",
                     font=(FONT, 10), bg=BG, fg="#222").pack(side="left")

            tk.Label(row, text=f"S{hinge+1} – {key}",
                     font=(FONT, 9, "bold"), bg=BG, fg="#888").pack(side="left", padx=(12, 0))

        tk.Frame(self.result_frame, bg=BG, height=8).pack()

    def _clear_result(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()