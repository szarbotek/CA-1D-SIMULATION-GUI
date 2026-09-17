import tkinter as tk
from fontTools.misc import configTools
from src.Config import Config

class Pallet:

    class Tool:
        activeTool: str = "pencil"

        PENCIL = "pencil"
        ERASER = "eraser"
        FILL = "fill"

        configTool = {
            "pencil": {
                "brush_size": 1,
            },
            "eraser": {
                "brush_size": 1,
            },
            "fill": {
                "pattern": "1-1",
            },
        }

        @classmethod
        def pencil(clsTool, pallet: "Pallet", index, state):
            """
                Change color of clicet rectengel in canvas.
            :param index:
            :param state:
            :return:
            """

            size = clsTool.configTool["pencil"]["brush_size"]
            start = index - size // 2
            end = start + size  # zakres wyłączny

            for pos in range(start, end):
                if 0 <= pos < pallet.width_canvas:
                    pallet.cells[pos] = state

        @classmethod
        def eraser(clsTool, pallet: "Pallet", index, state):
            """
                Erase cells in canvas (set state to 0 using brush size).
            :param index:
            :param state:
            :return:
            """
            size = clsTool.configTool["eraser"]["brush_size"]
            start = index - size // 2
            end = start + size  # zakres wyłączny

            for pos in range(start, end):
                if 0 <= pos < pallet.width_canvas:
                    pallet.cells[pos] = 0

        @classmethod
        def fill(clsTool, pallet: "Pallet", index, state):
            """
                Fill continuous area of same state with k-n pattern.
            :param index:
            :param state:
            :return:
            """
            old_state = pallet.cells[index]
            new_state = state

            if old_state == new_state:
                return

            # wyznaczenie ciągłego obszaru o tym samym stanie (w lewo i w prawo od kliknięcia)
            left_bound = index
            while left_bound - 1 >= 0 and pallet.cells[left_bound - 1] == old_state:
                left_bound -= 1

            right_bound = index
            while right_bound + 1 < pallet.width_canvas and pallet.cells[right_bound + 1] == old_state:
                right_bound += 1

            raw_pattern = clsTool.configTool["fill"].get("pattern", "1-1")
            try:
                k_str, n_str = raw_pattern.split("-")
                k = int(k_str)
                n = int(n_str)
                if k < 1 or n < 1:
                    raise ValueError
            except (ValueError, AttributeError):
                k, n = 1, 1

            period = max(1, k * n)

            for pos in range(left_bound, right_bound + 1):
                offset = pos - left_bound
                if (offset % period) < k:
                    pallet.cells[pos] = new_state
                else:
                    pallet.cells[pos] = 0

    CELL_PANEL_HEIGHT = 50

    def __init__(self, root, app_controller):
        self.app_controller = app_controller

        # --- ROOT --- =============================================================
        frame = tk.Frame(
            root, bg="white", bd=1, highlightthickness=1,  highlightbackground = "#888888"
        )
        frame.grid(
            row=0, column=0, columnspan=2,
            sticky="ew",
            padx=10, pady=10,
        )
        # --- ROOT: label --- =============================================================
        tk.Label(
            frame, text="Base state Q(0)", font=("Arial", 10, "bold"),  highlightthickness=1,  highlightbackground = "#888888", bg="white"
        ).pack( anchor='w', padx=5, pady=5)

        # --- ROOT: canvas --- =============================================================
        self.colors: list[str] = Config.Cell.CELL_COLOR
        self.height_canvas = 1
        self.width_canvas = 60

        self.cell_canvas = tk.Canvas(
            frame,
            height = 50,
            highlightthickness = 1,  highlightbackground = "#888888", bg = Config.Cell.BASE_STATE
        )
        self.cell_canvas.pack( fill='x', expand=True, padx=5, pady=5)

        self.cell_canvas.bind( "<Configure>", self.redraw_cell_canvas )
        self.cell_canvas.bind( "<Button-1>",  self.on_canvas_click)

        self.cell_rects: list = []

        self.cells = [0] * self.width_canvas

        # =============================================================
        # addon
        # =============================================================
        self.tool = Pallet.Tool
        self.current_state = 1


    # =============================================================
    #
    # =============================================================
    def redraw_cell_canvas(self, event=None):

        canvas_width = event.width if event is not None and hasattr(event, 'width') else self.cell_canvas.winfo_width()

        if canvas_width <= 1:
            return

        self.cell_canvas.delete("all")
        self.cell_rects = []

        cell_w = canvas_width / self.width_canvas

        for i in range(self.width_canvas):
            x0 = i * cell_w
            x1 = x0 + cell_w
            state_idx = self.cells[i]
            color = self.colors[state_idx] if state_idx < len(self.colors) else self.colors[0]
            rect = self.cell_canvas.create_rectangle(
                x0, 0, x1, self.CELL_PANEL_HEIGHT,
                fill = color, outline="#555555", width=0.5
            )
            self.cell_rects.append(rect)

    def on_canvas_click(self, event):

        canvas_width = self.cell_canvas.winfo_width()

        if canvas_width <= 1 or self.width_canvas == 0:
            return

        cell_w = canvas_width / self.width_canvas
        index = int(event.x // cell_w)
        index = max(0, min(self.width_canvas - 1, index))
        self.cell_clicked(index)

    def cell_clicked(self, index):
        if self.tool.activeTool == Pallet.Tool.PENCIL:
            self.tool.pencil(self, index, self.current_state)
        elif self.tool.activeTool == Pallet.Tool.ERASER:
            self.tool.eraser(self, index, 0)
        elif self.tool.activeTool == Pallet.Tool.FILL:
            self.tool.fill(self, index, self.current_state)

        self.update_cell_visuals()
        self.app_controller.plot_panel.update_plot()

    def update_cell_visuals(self):
        """
            Update visual representation of cells on canvas without full redraw.
        """
        for i, rect in enumerate(self.cell_rects):
            state_idx = self.cells[i]
            color = self.colors[state_idx] if state_idx < len(self.colors) else self.colors[0]
            self.cell_canvas.itemconfig(rect, fill=color)