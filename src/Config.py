from matplotlib.table import Cell


class Config:



    CELL_PANEL_HEIGHT = 40


    states_count: int = 14


    class Cell:
        ACTIVE_STATE = 16
        MAX_STATES = 16


        CELL_COLOR: list[str] = [
            "#000000", "#FF4A4A", "#4CFF6A", "#4A9FFF",
            "#FFF34A", "#FF4AD9", "#35FFFF", "#FF8A32",
            "#9A55FF", "#35E69A", "#FF4A4A", "#4A9FFF",
            "#FFD43B", "#D34DFF", "#32E6D5", "#333333",
        ]

        BASE_STATE: str = CELL_COLOR[0]