from sudoku import Board

if __name__ == '__main__':
    board = Board(9, 9)

    # print("Board created. Input data as row, column, value")
    # print("Then type \"solve\"")

    with open(r"C:\Users\VLADIMIR\Desktop\sudoku_2.txt", 'r') as f:
        data = f.readlines()

    row_cnt = 0
    for line in data:
        col_cnt = 0
        for c in line[:-1]:
            if c != "*" and c != "":
                try:
                    board.set_cell_value(row_cnt, col_cnt, int(c))
                except Exception as e:
                    raise e
            col_cnt += 1
        row_cnt += 1

    while True:
        s = input()
        if s == "solve":
            board.solve()
        elif s == "poss":
            board.print_possibilities()
        elif s == "board":
            board.print()
        elif s == "exit":
            break
        else:
            try:
                row, col, value = (int(i) for i in input().split())
            except Exception as e:
                print("failed to parse: ", e)
            else:
                print(f"you entered {row}, {col}, {value}")
                board.set_cell_value(row=row, col=col, value=value)
