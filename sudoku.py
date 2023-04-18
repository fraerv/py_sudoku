class CellArray:
    def __init__(self, number):
        self.number = number
        self.cells = []

    def add_cell(self, cell):
        self.cells.append(cell)


class Row(CellArray):
    pass


class Column(CellArray):
    pass


class Block(CellArray):
    pass


class Cell:

    def __init__(self, board, value=None):
        self.board = board
        self.value = value
        self.possible_values = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.row = None
        self.col = None
        self.block = None
        self.number = None

    def set_value(self, value):
        self.value = value

    def solve(self):
        if self.value is not None:
            return 0
        # by difference
        row_values = {cell.value for cell in self.row.cells}
        col_values = {cell.value for cell in self.col.cells}
        block_values = {cell.value for cell in self.block.cells}
        self.possible_values = self.possible_values.difference(row_values).\
            difference(col_values).difference(block_values)

        if len(self.possible_values) == 1:
            self.set_value(list(self.possible_values)[0])
            return 0

        # by uniqueness
        for arr in ['row', 'col', 'block']:
            arr_possibles = set()
            for cell in getattr(self, arr).cells:
                if cell != self:
                    arr_possibles = arr_possibles.union(cell.possible_values)
        unique_possible_values = self.possible_values.difference(arr_possibles)

        if len(unique_possible_values) == 1:
            self.set_value(list(self.possible_values)[0])
            return 0
        return 1

    def print_possible_values(self):
        print(f"Cell {self.row.number}, {self.col.number} (block {self.block.number}). "
              f"Possible values are {self.possible_values}")

    def __str__(self):
        return str(self.value or ".")


class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rows = {}
        self.cols = {}
        self.blocks = {}
        self.cells = {}
        for i in range(0, width):
            self.rows[i] = Row(i)
        for i in range(0, height):
            self.cols[i] = Column(i)
        for i in range(0, (width // 3) * (height // 3)):
            self.blocks[i] = Block(i)
        for c in range(width):
            for r in range(height):
                self.add_cell(r, c)

    def add_cell(self, row, col, value=None):
        cell = Cell(board=self, value=value)
        block_number = 3 * (row // 3) + col // 3
        cell_number = self.width * row + col

        cell.row = self.rows[row]
        cell.col = self.cols[col]
        cell.block = self.blocks[block_number]
        cell.number = cell_number

        self.rows[row].add_cell(cell)
        self.cols[col].add_cell(cell)
        self.blocks[block_number].add_cell(cell)
        self.cells[cell_number] = cell

    def get_cell(self, row, col) -> Cell:
        return self.cells.get(self.width*row+col, None)

    def set_cell_value(self, row, col, value=None):
        cell = self.get_cell(row, col)
        cell.set_value(value)

    def print(self):
        for r in self.rows.keys():
            shift = r * self.width
            for i in range(0+shift, 3+shift):
                print(str(self.cells[i]), end=' ')
            print('|', end=' ')
            for i in range(3+shift, 6+shift):
                print(str(self.cells[i]), end=' ')
            print('|', end=' ')
            for i in range(6+shift, 9+shift):
                print(str(self.cells[i]), end=' ')
            print()
            if r % 3 == 2 and r < 8:
                print("-"*5, "+", "-"*5, "+", "-"*5)

    def print_cell_numbers(self):
        for r in self.rows.keys():
            shift = r * self.width
            for i in range(0+shift, 3+shift):
                print(str(self.cells[i].number), end=' ')
            print('|', end=' ')
            for i in range(3+shift, 6+shift):
                print(str(self.cells[i].number), end=' ')
            print('|', end=' ')
            for i in range(6+shift, 9+shift):
                print(str(self.cells[i].number), end=' ')
            print()
            if r % 3 == 2 and r < 8:
                print("-" * 5, "+", "-" * 5, "+", "-" * 5)

    def _solve(self):
        not_solved_yet = 0
        for cell in self.cells.values():
            not_solved_yet += cell.solve()
        return not_solved_yet

    def solve(self):
        cells_to_solve = self._solve()
        while cells_to_solve != 0:
            old_cells_to_solve = cells_to_solve
            cells_to_solve = self._solve()
            if cells_to_solve == old_cells_to_solve:
                print("Impossible to solve. Current board state is")
                self.print()
                break
        else:
            print("Board solved:")
            self.print()

    def print_possibilities(self):
        for cell in self.cells.values():
            if not cell.value:
                cell.print_possible_values()
