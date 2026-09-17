import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator
from src.Config import Config
import importlib
from src.core import rule

class SymulationPlot:

    MAX_STATES = Config.Cell.MAX_STATES

    def __init__(self, root, app_controller):
        self.app_controller = app_controller
        self.rule = rule

        self.colors = Config.Cell.CELL_COLOR
        self.step = 8

        self.right_panel = tk.Frame(root)
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=10, pady=(5, 10))

        self.figure = Figure(figsize=(10, 7), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.cmap = ListedColormap(self.colors)
        self.norm = BoundaryNorm(
            boundaries=np.arange(self.MAX_STATES + 1) - 0.5,
            ncolors=self.MAX_STATES
        )

    def next_generation(self, rule, cells, width ):
        try:
            importlib.reload(rule)

            new_cells = [0] * width
            for i in range(0, width - 1):
                new_cells[i] = rule.rule(cells, i)

            new_cells[0] = cells[0]
            new_cells[-1] = cells[-1]
            return new_cells

        except Exception as e:
            print("Error in rule.py file")

    def draw_plot(self, data):
        self.ax.clear()
        arr = np.array(data, dtype=int)

        self.ax.imshow(
            arr,
            cmap=self.cmap,
            norm=self.norm,
            interpolation="nearest",
            aspect="auto",
        )

        self.ax.set_xlabel("Cell position")
        self.ax.set_ylabel("Time steps")
        self.ax.set_title("1D Cellular Automaton")

        n_rows = len(data)
        n_cols = len(data[0]) if n_rows > 0 else 0

        if n_cols > 0:
            self.ax.set_box_aspect( n_rows / n_cols)

        tick_step = max(1, n_rows // 20)
        ticks = list(range(0, n_rows, tick_step))

        self.ax.set_yticks(ticks)
        self.ax.set_yticklabels(ticks)

        self.ax.xaxis.set_major_locator(MultipleLocator(10))
        self.ax.yaxis.set_major_locator(MultipleLocator(4))

        self.ax.set_yticks(np.arange(-0.5, n_rows, 1), minor=True)
        self.ax.set_xticks(np.arange(-0.5, n_cols, 1), minor=True)

        self.ax.grid(which="minor", color="gray", linewidth=0.5, alpha=0.5)
        self.ax.grid(which="major", visible=False)
        self.ax.tick_params(which="minor", length=0)

        self.canvas.draw_idle()

    def set_step(self):
        try:
            value = int(self.app_controller.operator_panel.step_entry.get())
            if value < 1 or value > 5000:
                raise ValueError
            self.step = value
            self.init_simulation_buffer()
        except ValueError:
            print("STEP musi być liczbą całkowitą od 1 do 5000.")

    def init_simulation_buffer(self):
        width = self.app_controller.pallet.width_canvas
        initial_cells = self.app_controller.pallet.cells.copy()

        self.simulation_buffer = [initial_cells] + [[0] * width for _ in range(self.step - 1)]
        self.current_rows = 1

        self.app_controller.operator_panel.update_progress(self.current_rows, self.step)
        self.draw_plot(self.simulation_buffer)

    def advance_step(self):
        if self.simulation_buffer is None or self.current_rows >= self.step:
            return

        width = self.app_controller.pallet.width_canvas

        prev_row = self.simulation_buffer[self.current_rows - 1]
        new_row = self.next_generation(self.rule, prev_row , width)

        self.simulation_buffer[self.current_rows] = new_row
        self.current_rows += 1

        self.app_controller.operator_panel.update_progress(self.current_rows, self.step)
        self.draw_plot(self.simulation_buffer)

    def reset_step(self):
        if self.simulation_buffer is None:
            return

        width = self.app_controller.pallet.width_canvas
        for i in range(1, self.step):
            self.simulation_buffer[i] = [0] * width

        self.current_rows = 1
        self.app_controller.operator_panel.update_progress(self.current_rows, self.step)
        self.draw_plot(self.simulation_buffer)

    def simulate(self):
        if self.simulation_buffer is None:
            return

        width = self.app_controller.pallet.width_canvas

        row = self.simulation_buffer[0]
        for i in range(1, self.step):
            row = self.next_generation( self.rule, row, width)
            self.simulation_buffer[i] = row

        self.current_rows = self.step
        self.app_controller.operator_panel.update_progress(self.current_rows, self.step)
        self.draw_plot(self.simulation_buffer)

    def update_plot(self):
        self.init_simulation_buffer()