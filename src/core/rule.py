from src.Config import Config
# =============================================================
# CELLULAR AUTOMATON RULE
# =============================================================
def rule(cells: list[int], index: int) -> int:
    """
        Calculate the next state of a single cell.

        The cell is evaluated using two neighbours on each side.

        :param cells: Orginal cell list
        :param index: The index of the cell in the original cell list.
        :return: The calculated state of the cell in the next generation.
    """
    highest_state = Config.Cell.ACTIVE_STATE - 1
    radius = 2

    # Extend the list by repeating the boundary values.
    # This allows the neighbourhood to be calculated for cells
    # located at the beginning and at the end of the list.
    resized_cells = (
            [cells[0]] * radius
            + cells
            + [cells[-1]] * radius
    )
    index = index + radius

    # Select the cell's neighbourhood.
    neighbors = resized_cells[
        index - radius: index + radius + 1
    ]
    cl2 = resized_cells[index - 2]
    cl1 = resized_cells[index - 1]
    cc = resized_cells[index]
    cr1 = resized_cells[index + 1]
    cr2 = resized_cells[index + 2]

    ret_cc = None
    # =============================================================
    # LIVING CELL
    # =============================================================
    if cc > 0:

        if neighbors.count(cc) >= 3:
            ret_cc = cc
        elif cc == highest_state:
            if neighbors.count(cc) + neighbors.count(0) >= 3:
                ret_cc = cc
            else:
                ret_cc = 0
        else:
            ret_cc = 0
    # =============================================================
    # DEAD CELL
    # =============================================================
    else:
        if neighbors.count(0) + neighbors.count(highest_state) >= 4:
            ret_cc = highest_state
        else:
            if cr2 == cr1 and (cr1 != 0):
                ret_cc = cr1
            elif cl2 == cl1 and (cl1 != 0):
                ret_cc = cl1
            else:
                ret_cc = 0
    # =============================================================
    return ret_cc