import tkinter as tk

def gaussian_elimination(A, b, result_text):
    rows = len(A)
    cols = len(A[0])
    augmented = [A[i] + [b[i]] for i in range(rows)]

    result_text.config(state='normal')
    result_text.delete(1.0, 'end')

    def print_and_append(msg):
        result_text.insert('end', msg + '\n')
        result_text.update_idletasks()

    pivot_positions = []
    current_row = 0
    step = 0

    for col in range(cols):
        if current_row >= rows:
            break

        max_row = current_row
        for r in range(current_row, rows):
            if abs(augmented[r][col]) > abs(augmented[max_row][col]):
                max_row = r

        step += 1
        print_and_append(f"\nStep {step}:")

        if abs(augmented[max_row][col]) < 1e-12:
            print_and_append(f"No pivot found in column {col+1}, continue")
            for row_view in augmented:
                print_and_append(str(row_view))
            continue

        if max_row != current_row:
            augmented[current_row], augmented[max_row] = augmented[max_row], augmented[current_row]
            print_and_append(f"Swap R{current_row + 1} with R{max_row + 1}")
            for row_view in augmented:
                print_and_append(str(row_view))
        else:
            print_and_append(f"Swap R{current_row + 1} with R{max_row + 1}")
            for row_view in augmented:
                print_and_append(str(row_view))

        pivot = augmented[current_row][col]

        print_and_append(f"R{current_row + 1} = R{current_row + 1} / {pivot}")
        for j in range(col, cols + 1):
            augmented[current_row][j] /= pivot
        for row_view in augmented:
            print_and_append(str(row_view))

        for r in range(rows):
            if r != current_row:
                factor = augmented[r][col]
                if abs(factor) > 1e-12:
                    for c in range(col, cols + 1):
                        augmented[r][c] -= factor * augmented[current_row][c]
                    print_and_append(f"Eliminate R{r + 1}: R{r + 1} = R{r + 1} - {factor} * R{current_row + 1}")
                    for row_view in augmented:
                        print_and_append(str(row_view))

        pivot_positions.append((current_row, col))
        current_row += 1

    inconsistent = False
    for r in range(rows):
        if all(abs(augmented[r][c]) < 1e-12 for c in range(cols)) and abs(augmented[r][cols]) > 1e-12:
            inconsistent = True
            break

    if inconsistent:
        print_and_append("\nFinal Augmented Matrix:")
        for row_view in augmented:
            print_and_append(str(row_view))
        print_and_append("\nNo solution exists for this system.")
        result_text.config(state='disabled')
        return None

    pivot_cols = [col for (_, col) in pivot_positions]
    free_vars = [c for c in range(cols) if c not in pivot_cols]

    if len(free_vars) == 0:
        print_and_append("\nUnique solution exists for this system.")
        x = [0.0] * cols
        for (r, c) in pivot_positions:
            x[c] = augmented[r][cols]
        print_and_append("\nFinal Augmented Matrix:")
        for row_view in augmented:
            print_and_append(str(row_view))
        print_and_append("\nSolution:")
        for i, val in enumerate(x):
            result_text.insert('end', f"x{i+1} = {val:.4f}\n")
        result_text.config(state='disabled')
        return x
    else:
        print_and_append("\nInfinite solutions exist for this system.")
        col_to_row = {col: row for (row, col) in pivot_positions}
        params = [f"t{i+1}" for i in range(len(free_vars))]
        free_map = dict(zip(free_vars, params))
        solution_expr = ["0"] * cols

        for col in range(cols):
            if col in free_vars:
                solution_expr[col] = free_map[col]
            else:
                r = col_to_row[col]
                expr = f"{augmented[r][cols]:.4f}"
                for j in free_vars:
                    coeff = -augmented[r][j]
                    if abs(coeff) > 1e-12:
                        expr += f" + ({coeff:.4f})*{free_map[j]}"
                solution_expr[col] = expr

        print_and_append("\nFinal Augmented Matrix:")
        for row_view in augmented:
            print_and_append(str(row_view))

        print_and_append("\nSolution:")
        for i, expr in enumerate(solution_expr):
            result_text.insert('end', f"x{i+1} = {expr}\n")
        result_text.config(state='disabled')
        return solution_expr

def generate_matrix():
    global entries, matrix_frame
    rows = int(rows_entry.get())
    cols = int(cols_entry.get())
    for widget in matrix_frame.winfo_children():
        widget.destroy()
    entries = []
    tk.Label(matrix_frame, text="Enter the augmented matrix:").grid(row=0, column=0, columnspan=cols+1)
    for i in range(rows):
        row_entries = []
        for j in range(cols + 1):
            entry = tk.Entry(matrix_frame, width=8)
            entry.grid(row=i+1, column=j, padx=5, pady=5)
            row_entries.append(entry)
        entries.append(row_entries)

def solve():
    rows = len(entries)
    cols = len(entries[0]) - 1
    A = []
    b = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(float(entries[i][j].get()))
        A.append(row)
        b.append(float(entries[i][cols].get()))
    gaussian_elimination(A, b, result_text)

window = tk.Tk()
window.title("Gaussian Elimination Calculator")

tk.Label(window, text="Number of rows:").grid(row=0, column=0)
rows_entry = tk.Entry(window)
rows_entry.grid(row=0, column=1)

tk.Label(window, text="Number of columns:").grid(row=1, column=0)
cols_entry = tk.Entry(window)
cols_entry.grid(row=1, column=1)

generate_button = tk.Button(window, text="Generate Matrix", command=generate_matrix)
generate_button.grid(row=2, column=0, columnspan=2, pady=10)

matrix_frame = tk.Frame(window)
matrix_frame.grid(row=3, column=0, columnspan=2)

solve_button = tk.Button(window, text="Solve", command=solve)
solve_button.grid(row=4, column=0, columnspan=2, pady=10)

result_frame = tk.Frame(window)
result_frame.grid(row=5, column=0, columnspan=2)

scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.Text(result_frame, height=30, width=100, yscrollcommand=scrollbar.set)
result_text.pack(side=tk.LEFT)

scrollbar.config(command=result_text.yview)

window.mainloop()
import tkinter as tk

def gaussian_elimination(A, b, result_text):
    rows = len(A)
    cols = len(A[0])
    augmented = [A[i] + [b[i]] for i in range(rows)]

    result_text.config(state='normal')
    result_text.delete(1.0, 'end')

    def print_and_append(msg):
        result_text.insert('end', msg + '\n')
        result_text.update_idletasks()

    pivot_positions = []
    current_row = 0
    step = 0

    for col in range(cols):
        if current_row >= rows:
            break

        max_row = current_row
        for r in range(current_row, rows):
            if abs(augmented[r][col]) > abs(augmented[max_row][col]):
                max_row = r

        step += 1
        print_and_append(f"\nStep {step}:")

        if abs(augmented[max_row][col]) < 1e-12:
            print_and_append(f"No pivot found in column {col+1}, continue")
            for row_view in augmented:
                print_and_append(str(row_view))
            continue

        if max_row != current_row:
            augmented[current_row], augmented[max_row] = augmented[max_row], augmented[current_row]
            print_and_append(f"Swap R{current_row + 1} with R{max_row + 1}")
            for row_view in augmented:
                print_and_append(str(row_view))
        else:
            print_and_append(f"Swap R{current_row + 1} with R{max_row + 1}")
            for row_view in augmented:
                print_and_append(str(row_view))

        pivot = augmented[current_row][col]

        print_and_append(f"R{current_row + 1} = R{current_row + 1} / {pivot}")
        for j in range(col, cols + 1):
            augmented[current_row][j] /= pivot
        for row_view in augmented:
            print_and_append(str(row_view))

        for r in range(rows):
            if r != current_row:
                factor = augmented[r][col]
                if abs(factor) > 1e-12:
                    for c in range(col, cols + 1):
                        augmented[r][c] -= factor * augmented[current_row][c]
                    print_and_append(f"Eliminate R{r + 1}: R{r + 1} = R{r + 1} - {factor} * R{current_row + 1}")
                    for row_view in augmented:
                        print_and_append(str(row_view))

        pivot_positions.append((current_row, col))
        current_row += 1

    inconsistent = False
    for r in range(rows):
        if all(abs(augmented[r][c]) < 1e-12 for c in range(cols)) and abs(augmented[r][cols]) > 1e-12:
            inconsistent = True
            break

    if inconsistent:
        print_and_append("\nFinal Augmented Matrix:")
        for row_view in augmented:
            print_and_append(str(row_view))
        print_and_append("\nNo solution exists for this system.")
        result_text.config(state='disabled')
        return None

    pivot_cols = [col for (_, col) in pivot_positions]
    free_vars = [c for c in range(cols) if c not in pivot_cols]

    if len(free_vars) == 0:
        print_and_append("\nUnique solution exists for this system.")
        x = [0.0] * cols
        for (r, c) in pivot_positions:
            x[c] = augmented[r][cols]
        print_and_append("\nFinal Augmented Matrix:")
        for row_view in augmented:
            print_and_append(str(row_view))
        print_and_append("\nSolution:")
        for i, val in enumerate(x):
            result_text.insert('end', f"x{i+1} = {val:.4f}\n")
        result_text.config(state='disabled')
        return x
    else:
        print_and_append("\nInfinite solutions exist for this system.")
        col_to_row = {col: row for (row, col) in pivot_positions}
        params = [f"t{i+1}" for i in range(len(free_vars))]
        free_map = dict(zip(free_vars, params))
        solution_expr = ["0"] * cols

        for col in range(cols):
            if col in free_vars:
                solution_expr[col] = free_map[col]
            else:
                r = col_to_row[col]
                expr = f"{augmented[r][cols]:.4f}"
                for j in free_vars:
                    coeff = -augmented[r][j]
                    if abs(coeff) > 1e-12:
                        expr += f" + ({coeff:.4f})*{free_map[j]}"
                solution_expr[col] = expr

        print_and_append("\nFinal Augmented Matrix:")
        for row_view in augmented:
            print_and_append(str(row_view))

        print_and_append("\nSolution:")
        for i, expr in enumerate(solution_expr):
            result_text.insert('end', f"x{i+1} = {expr}\n")
        result_text.config(state='disabled')
        return solution_expr

def generate_matrix():
    global entries, matrix_frame
    rows = int(rows_entry.get())
    cols = int(cols_entry.get())
    for widget in matrix_frame.winfo_children():
        widget.destroy()
    entries = []
    tk.Label(matrix_frame, text="Enter the augmented matrix:").grid(row=0, column=0, columnspan=cols+1)
    for i in range(rows):
        row_entries = []
        for j in range(cols + 1):
            entry = tk.Entry(matrix_frame, width=8)
            entry.grid(row=i+1, column=j, padx=5, pady=5)
            row_entries.append(entry)
        entries.append(row_entries)

def solve():
    rows = len(entries)
    cols = len(entries[0]) - 1
    A = []
    b = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(float(entries[i][j].get()))
        A.append(row)
        b.append(float(entries[i][cols].get()))
    gaussian_elimination(A, b, result_text)

window = tk.Tk()
window.title("Gaussian Elimination Calculator")

tk.Label(window, text="Number of equations:").grid(row=0, column=0)
rows_entry = tk.Entry(window)
rows_entry.grid(row=0, column=1)

tk.Label(window, text="Number of unknowns:").grid(row=1, column=0)
cols_entry = tk.Entry(window)
cols_entry.grid(row=1, column=1)

generate_button = tk.Button(window, text="Generate Matrix", command=generate_matrix)
generate_button.grid(row=2, column=0, columnspan=2, pady=10)

matrix_frame = tk.Frame(window)
matrix_frame.grid(row=3, column=0, columnspan=2)

solve_button = tk.Button(window, text="Solve", command=solve)
solve_button.grid(row=4, column=0, columnspan=2, pady=10)

result_frame = tk.Frame(window)
result_frame.grid(row=5, column=0, columnspan=2)

scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.Text(result_frame, height=30, width=100, yscrollcommand=scrollbar.set)
result_text.pack(side=tk.LEFT)

scrollbar.config(command=result_text.yview)

window.mainloop()
