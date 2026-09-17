import tkinter as tk
## project
from src.core.rule import rule
from src.Config import Config
# --- GUI ---
from src.ui.Pallet import Pallet
from src.ui.OperatorPanel import OperatorPanel
from src.ui.SimulationPlot import SymulationPlot


class SimulationGUI:

    def __init__(self):
        root = tk.Tk()
        root.title("1D Cellular Automaton")
        root.geometry("1500x1000")

        root.columnconfigure(0, weight=1, minsize=340)
        root.columnconfigure(1, weight=5)
        root.rowconfigure(0, weight=0)
        root.rowconfigure(1, weight=1)

        self.pallet = Pallet( root, self )
        self.plot_panel = SymulationPlot( root, self)

        self.operator_panel = OperatorPanel(root, self)

        self.plot_panel.init_simulation_buffer()
        root.mainloop()

if __name__ == "__main__":
    app = SimulationGUI()