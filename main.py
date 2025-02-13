import tkinter as tk
from tkinter import messagebox
from collections import deque

knight_possible_moves = [
    (-2, -1), (-2, +1), (+2, -1), (+2, +1),
    (-1, -2), (-1, +2), (+1, -2), (+1, +2)
]

"""
Szélességi kereséssel bejárja a táblát, amíg meg nem találja a végpozíciót. Közben eltárolja a lépéseket egy listában.
Args: n, m, start, end : int
Returns: count_of_steps : int; path_list : list
"""
def breadth_first_search(n, m, start, end):
    i1, j1 = start
    i2, j2 = end

    if (i1, j1) == (i2, j2):
        return 0, [(i1, j1)]

    visited = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(False)
        visited.append(row)

    visited[i1][j1] = True
    queue = deque([(i1, j1, 0, [])])

    while queue:
        x, y, steps, path = queue.popleft()
        path.append((x, y))

        for x_val, y_val in knight_possible_moves:
            move_x, move_y = x + x_val, y + y_val

            if is_inside_board(move_x, move_y, n, m) and not visited[move_x][move_y] :
                if (move_x, move_y) == (i2, j2):
                    return steps + 1, path + [(move_x, move_y)]

                visited[move_x][move_y] = True
                queue.append((move_x, move_y, steps + 1, path.copy()))

    return -1, []

"""
Ellenőrzi, hogy a megadott pozíció a táblán belül helyezkedik-e el.
Args: x, y, n, m : int
Returns: boolean
"""
def is_inside_board(x, y, n, m):
    if 0 <= x < n and 0 <= y < m:
        return True
    else:
        return False

"""
Rögzíti a filedekbe írt értéket és elindítja a bfs algoritmust az értékekkel
Args: -
Returns: void
Exceprion: ValueError (ha invalid a bemenet)
"""
def start_algorithm():
    try:
        n = int(field_n.get())
        m = int(field_m.get())
        start_x = int(field_start_x.get()) - 1
        start_y = int(field_start_y.get()) - 1
        end_x = int(field_end_x.get()) - 1
        end_y = int(field_end_y.get()) - 1

        steps, path = breadth_first_search(n, m, (start_x, start_y), (end_x, end_y))

        if steps == -1:
            messagebox.showerror("Hiba", "Nincs útvonal!")
        else:
            result_label.config(text=f"Minimális lépések száma: {steps}")
            draw_board(n, m, path)

    except ValueError:
        messagebox.showerror("Hiba", "Érvénytelen bemenet!")

"""
Kirajzolja a táblát a canvas-ra.
Args: n, m : int; path : list
"""
def draw_board(n, m, path):
    cell_size = 30
    canvas.config(scrollregion=(0, 0, (m + 1) * cell_size, (n + 1) * cell_size))

    for j in range(m):
        x1 = (j + 1) * cell_size
        canvas.create_text(x1 + cell_size // 2, cell_size // 2, text=str(1 + j), fill="black")
    for i in range(n):
        y1 = (i + 1) * cell_size
        canvas.create_text(cell_size // 2, y1 + cell_size // 2, text=str(i + 1), fill="black")

    for i in range(n):
        for j in range(m):
            x1 = (j + 1) * cell_size
            y1 = (i + 1) * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            if (i + j) % 2 == 0:
                color = "yellow"
            else:
                color = "brown"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    for step, (x, y) in enumerate(path):
        x1 = (y + 1) * cell_size + cell_size // 4
        y1 = (x + 1) * cell_size + cell_size // 4
        x2 = x1 + cell_size // 2
        y2 = y1 + cell_size // 2

        if step == len(path) - 1:
            color = "red"
        elif step == 0:
            color = "green"
        else:
            color = "blue"

        canvas.create_oval(x1, y1, x2, y2, fill=color)
        canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=str(step), fill="white")


if __name__ == "__main__":
    # Ablak létrehozása
    window = tk.Tk()
    window.title("Sakktábla - BSF")

    # Tábla méretének beállítása
    tk.Label(window, text="Tábla mérete:").grid(row=0, column=0, columnspan=2)
    field_n = tk.Entry(window)
    field_n.grid(row=1, column=0, columnspan=2)
    field_m = tk.Entry(window)
    field_m.grid(row=2, column=0, columnspan=2)

    # Felirat és field a kezdő pozíció beállítására
    tk.Label(window, text="Kezdő pozíció:").grid(row=3, column=0, columnspan=2)
    field_start_x = tk.Entry(window)
    field_start_x.grid(row=4, column=0, columnspan=2)
    field_start_y = tk.Entry(window)
    field_start_y.grid(row=5, column=0, columnspan=2)

    # Felirat és field a cél pozició beállítására
    tk.Label(window, text="Cél pozíció: ").grid(row=6, column=0, columnspan=2)
    field_end_x = tk.Entry(window)
    field_end_x.grid(row=7, column=0, columnspan=2)
    field_end_y = tk.Entry(window)
    field_end_y.grid(row=8, column=0, columnspan=2)

    # Indítógomb
    button_start = tk.Button(window, text="Indítás", command=start_algorithm)
    button_start.grid(row=9, column=0, columnspan=2)

    # Felirat az eredményhez
    result_label = tk.Label(window, text="")
    result_label.grid(row=10, column=0, columnspan=2)

    # Vászon és görgetősáv a sakktábla megjelenítéséhez
    frame = tk.Frame(window)
    frame.grid(row=11, column=0, columnspan=2)

    # Scrollbar horizontálisan
    horizontal_scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
    horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    # Scrollbar vertikálisan
    vertical_scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
    vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Sakktábla canvas
    canvas = tk.Canvas(frame, width=300, height=300, bg="white", xscrollcommand=horizontal_scrollbar.set, yscrollcommand=vertical_scrollbar.set)
    canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    horizontal_scrollbar.config(command=canvas.xview)
    vertical_scrollbar.config(command=canvas.yview)

    window.mainloop()
