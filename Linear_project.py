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

    pivot_columns = []
    row = 0
    for col in range(cols):
        max_row = row
        for r in range(row, rows):
            if abs(augmented[r][col]) > abs(augmented[max_row][col]):
                max_row = r

        if abs(augmented[max_row][col]) < 1e-12:
            continue

        augmented[row], augmented[max_row] = augmented[max_row], augmented[row]
        pivot_columns.append(col)

        pivot_val = augmented[row][col]
        for c in range(col, cols + 1):
            augmented[row][c] /= pivot_val

        for r in range(rows):
            if r != row and abs(augmented[r][col]) > 1e-12:
                factor = augmented[r][col]
                for c in range(col, cols + 1):
                    augmented[r][c] -= factor * augmented[row][c]
        row += 1

    inconsistent = False
    for r in range(rows):
        if all(abs(augmented[r][c]) < 1e-12 for c in range(cols)) and abs(augmented[r][cols]) > 1e-12:
            inconsistent = True
            break

    if inconsistent:
        print_and_append("No solution exists for this system.")
        result_text.config(state='disabled')
        return None

    free_vars = [i for i in range(cols) if i not in pivot_columns]
    solution = ["0"] * cols

    if len(free_vars) == 0:
        for i, col in enumerate(pivot_columns):
            solution[col] = f"{augmented[i][cols]:.4f}"
        print_and_append("Unique solution:")
        for i, val in enumerate(solution):
            print_and_append(f"x{i+1} = {val}")
    else:
        print_and_append("Infinite solutions exist. Parametric form:")
        params = [f"t{i+1}" for i in range(len(free_vars))]
        free_map = dict(zip(free_vars, params))

        # Back-substitution for dependent variables
        for i in range(len(pivot_columns)-1, -1, -1):
            col = pivot_columns[i]
            val_expr = f"{augmented[i][cols]:.4f}"
            for j in range(col+1, cols):
                if j in free_vars:
                    coeff = -augmented[i][j]
                    if abs(coeff) > 1e-12:
                        sign = "+" if coeff >= 0 else "-"
                        val_expr += f" {sign} {abs(coeff):.4f}*{free_map[j]}"
            solution[col] = val_expr

        for idx in range(cols):
            if idx in free_vars:
                solution[idx] = free_map[idx]
            print_and_append(f"x{idx+1} = {solution[idx]}")

    print_and_append("\nFinal Augmented Matrix:")
    for row in augmented:
        print_and_append(str(row))

    result_text.config(state='disabled')
    return solution

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
