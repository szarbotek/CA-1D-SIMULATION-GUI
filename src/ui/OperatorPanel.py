import tkinter as tk
from src.Config import Config
from src.ui.Pallet import Pallet

class OperatorPanel:

    MAX_STATES = Config.Cell.MAX_STATES

    def __init__(self, root, app_controller):
        self.app_controller = app_controller

        self.colors = Config.Cell.CELL_COLOR

        self.left_panel = tk.Frame(root)
        self.left_panel.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

        # > =============================================================
        frame_001 = tk.Frame(self.left_panel, highlightthickness=1,  highlightbackground = "#888888")
        frame_001.pack()
        # >> =============================================================
        width_frame = tk.Frame(frame_001, highlightthickness=1,  highlightbackground = "#888888")
        width_frame.grid(row=0, column=0,)
        tk.Label(width_frame, text="Stimulate cells size:", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.width_entry = tk.Entry(width_frame, width=6)
        self.width_entry.insert(0, str(app_controller.pallet.width_canvas ))
        self.width_entry.grid(row=1, column=0, padx=10, pady=10)
        tk.Button(width_frame, text="SET", command=self.set_width, bg="#84EB73").grid(row=1, column=1, padx=10, pady=10)
        # >> =============================================================
        tk.Button(
            frame_001, text="Clear all", command=self.clear_all, width=10, height=3, font=("Arial", 10, "bold"), bg="#84EB73"
        ).grid(row=0, column=1,)
        # $ =============================================================

        # > =============================================================
        frame_002 = tk.Frame(self.left_panel, highlightthickness=1, highlightbackground="#888888")
        frame_002.pack()
        # >> =============================================================
        tk.Label(frame_002 , text="Pick Color:", font=("Arial", 12, "bold")).grid( row=0, column=0, padx=10, pady=10)
        self.current_color_label = tk.Label(
            frame_002, text="State", bg=self.colors[1], fg="black", width=15, height=4
        )
        self.current_color_label.grid( row=1, column=0, padx=10, pady=10)
        # >> =============================================================
        tk.Label(frame_002 , text="Tools:", font=("Arial", 12, "bold")).grid( row=0, column=1, padx=10, pady=10)
        self.tool_var = tk.StringVar(value="pencil")
        # >> =============================================================
        tools_frame = tk.Frame(frame_002, highlightthickness=1, highlightbackground="#888888" )
        tools_frame.grid( row=1, column=1, padx=10, pady=10)
        # >>> =============================================================
        tk.Radiobutton(tools_frame, text="pencil", variable=self.tool_var, value="pencil", command=self.change_tool).grid(row=0, column=0, pady=5)
        tk.Radiobutton(tools_frame, text="fill", variable=self.tool_var, value="fill", command=self.change_tool).grid(row=1, column=0, pady=5)
        tk.Radiobutton(tools_frame, text="eraser", variable=self.tool_var, value="eraser", command=self.change_tool).grid(row=2, column=0, pady=5)
        # $ =============================================================

        # > =============================================================
        frame_003 = tk.Frame(self.left_panel, highlightthickness=1, highlightbackground="#888888")
        frame_003.pack()
        # >> =============================================================
        tk.Label(frame_003, text="Pencil size:", font=("Arial", 12, "bold")).pack()
        self.brush_size_var = tk.IntVar(value=1)
        self.brush_size_spinbox = tk.Spinbox(
            frame_003, from_=1, to=999, width=10, textvariable=self.brush_size_var, justify=tk.CENTER,
            command=self.update_brush_size
        )
        self.brush_size_spinbox.pack()
        self.brush_size_spinbox.bind("<KeyRelease>", self.update_brush_size)
        # >> =============================================================
        tk.Label(frame_003, text="Fill pattern (k-n):", font=("Arial", 12, "bold")).pack()
        self.fill_pattern_entry = tk.Entry(frame_003, width=10, justify=tk.CENTER)
        self.fill_pattern_entry.insert(0, "1-1")
        self.fill_pattern_entry.pack()
        self.fill_pattern_entry.bind("<KeyRelease>", self.update_fill_pattern)
        # $ =============================================================

        # tk.Label(self.left_panel, text="Liczba stanów:", font=("Arial", 11, "bold")).pack(pady=(15, 3))
        # states_frame = tk.Frame(self.left_panel)
        # states_frame.pack()
        #
        # self.states_entry = tk.Entry(states_frame, width=10)
        # self.states_entry.insert(0, "4")
        # self.states_entry.pack(side=tk.LEFT)
        # tk.Button(states_frame, text="Ustaw", command=self.set_states).pack(side=tk.LEFT, padx=5)

        # > =============================================================
        frame_004 = tk.Frame(self.left_panel, highlightthickness=1, highlightbackground="#888888")
        frame_004.pack()
        # >> =============================================================
        tk.Label(frame_004, text="Colors:", font=("Arial", 12, "bold")).pack()
        self.palette_frame = tk.Frame(frame_004)
        self.palette_frame.pack()
        self.palette_buttons = []
        self.create_palette(16)
        # $ =============================================================

        # > =============================================================
        frame_005 = tk.Frame(self.left_panel, highlightthickness=1, highlightbackground="#888888")
        frame_005.pack()
        # >> =============================================================
        tk.Label(frame_005, text="Time steps:", font=("Arial", 12, "bold")).pack()
        step_frame = tk.Frame(frame_005)
        step_frame.pack()
        # >> =============================================================
        self.step_entry = tk.Entry(step_frame, width=10)
        self.step_entry.insert(0, str(app_controller.plot_panel.step))
        self.step_entry.pack(side=tk.LEFT)
        tk.Button(step_frame, text="SET", command=self.app_controller.plot_panel.set_step, bg="#84EB73" ).pack(side=tk.LEFT)
        # >> =============================================================
        tk.Button(
            frame_005, text="▶ START", command=self.app_controller.plot_panel.simulate,
            bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=20, height=2
        ).pack()
        # >> =============================================================
        step_control_frame = tk.Frame(frame_005)
        step_control_frame.pack(pady=5)
        # >>> =============================================================
        tk.Button(step_control_frame, text="STEP", command=self.app_controller.plot_panel.advance_step, width=11, bg="#F2A746").grid(row=0, column=0, padx=3)
        tk.Button(step_control_frame, text="RESET", command=self.app_controller.plot_panel.reset_step, width=11, bg="#F27A46").grid(row=0, column=1, padx=3)
        # >> =============================================================
        self.progress_label = tk.Label(frame_005, text=f"Progres: 1 / {app_controller.plot_panel.step}")
        self.progress_label.pack(pady=(8, 0))

    def change_tool(self):
        tool_val = self.tool_var.get()
        Pallet.Tool.activeTool = tool_val

    def update_brush_size(self, event=None):
        try:
            size = int(self.brush_size_var.get())
            Pallet.Tool.configTool["pencil"]["brush_size"] = size
            Pallet.Tool.configTool["eraser"]["brush_size"] = size
        except (ValueError, tk.TclError):
            pass

    def update_fill_pattern(self, event=None):
        Pallet.Tool.configTool["fill"]["pattern"] = self.fill_pattern_entry.get().strip()

    def create_palette(self, states_count):
        for widget in self.palette_frame.winfo_children():
            widget.destroy()

        self.palette_buttons = []

        for state in range(self.MAX_STATES):
            row = state // 4
            column = state % 4
            active = state < states_count

            button = tk.Button(
                self.palette_frame,
                text=str(state) if active else "",
                width=5,
                height=1,
                bg=self.colors[state] if active else "#dddddd",
                fg=("black" if state in (12, 13) else "white") if active else "#dddddd",
                state=tk.NORMAL if active else tk.DISABLED,
                relief=tk.RAISED if active else tk.FLAT,
                command=(lambda s=state: self.select_color(s)) if active else None,
            )
            button.grid(row=row, column=column, padx=2, pady=2)
            self.palette_buttons.append(button)

    def update_current_color_display(self, state):
        self.current_color_label.config(text=f"Stan {state}", bg=self.colors[state])
        self.current_color_label.config(fg="black" if state in (12, 13) else "white")

    def update_progress(self, current, total):
        self.progress_label.config(text=f"Progres: {current} / {total}")

    # --- Przeniesione metody operacyjne ---

    def set_width(self):
        try:
            new_width = int(self.width_entry.get())
            if new_width < 1 or new_width > 500:
                raise ValueError

            pallet = self.app_controller.pallet
            old_cells = pallet.cells
            current_width = pallet.width_canvas

            if new_width >= current_width:
                pallet.cells = old_cells + [0] * (new_width - current_width)
            else:
                pallet.cells = old_cells[:new_width]

            pallet.width_canvas = new_width

            pallet.redraw_cell_canvas()
            self.app_controller.plot_panel.update_plot()
        except ValueError:
            print("Szerokość musi być liczbą całkowitą od 1 do 500.")

    def clear_all(self):
        pallet = self.app_controller.pallet
        pallet.cells = [0] * self.app_controller.pallet.width_canvas
        pallet.update_cell_visuals()
        self.app_controller.plot_panel.update_plot()

    def select_color(self, state):
        pallet = self.app_controller.pallet
        pallet.current_state = state
        self.update_current_color_display(state)

    def set_states(self):
        try:
            count = int(self.states_entry.get())
            if count < 1 or count > 20:
                raise ValueError

            self.app_controller.states_count = count
            pallet = self.app_controller.pallet
            if pallet.current_state >= count:
                pallet.current_state = 0

            for i in range(self.app_controller.pallet.width_canvas ):
                if pallet.cells[i] >= count:
                    pallet.cells[i] = 0

            self.create_palette(count)
            pallet.update_cell_visuals()
            self.select_color(pallet.current_state)
            self.app_controller.plot_panel.update_plot()
        except ValueError:
            print("Liczba stanów musi być liczbą od 1 do 20.")