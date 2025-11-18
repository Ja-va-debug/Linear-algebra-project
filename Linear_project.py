import tkinter as tk

def gaussian_elimination(A, b):
    n = len(b)

    augmented_matrix = [A[i] + [b[i]] for i in range(n)]

    result_text.config(state='normal')
    result_text.delete(1.0, 'end')

    def print_and_append(text, msg):
        result_text.insert('end', msg + '\n')
        text.update_idletasks()

    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j

        print_and_append(result_text, f"\nStep {i + 1}:")
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        print_and_append(result_text, f"\n(R{i + 1} <--> R{max_row + 1})")

        for row in augmented_matrix:
            print_and_append(result_text, str(row))

        pivot = augmented_matrix[i][i]
        if pivot == 0:
            # Check if there is a row with all zeros in coefficients (except last column)
            if all(x == 0 for x in augmented_matrix[i][:n]) and augmented_matrix[i][n] != 0:
                print_and_append(result_text, f"\nNo solution for this matrix.")
                result_text.config(state='disabled')
                return None

            print_and_append(result_text, f"\nInfinite solutions for this matrix.")
            result_text.config(state='disabled')
            return None

        for j in range(i, n + 1):
            augmented_matrix[i][j] /= pivot

        print_and_append(result_text, f"\n(R{i + 1} / {pivot}) --> R{i + 1}")

        for row in augmented_matrix:
            print_and_append(result_text, str(row))

        for j in range(i + 1, n):
            factor = augmented_matrix[j][i]
            for k in range(i, n + 1):
                augmented_matrix[j][k] -= factor * augmented_matrix[i][k]

            print_and_append(result_text, f"\n({factor} x R{i + 1}) - R{j + 1} --> R{j + 1}")

            for row in augmented_matrix:
                print_and_append(result_text, str(row))

    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = augmented_matrix[i][n]
        for j in range(i + 1, n):
            x[i] -= augmented_matrix[i][j] * x[j]

    print_and_append(result_text, "\nThe Final Augmented Matrix:")
    for row in augmented_matrix:
        print_and_append(result_text, str(row))

    result_text.config(state='disabled')

    return x

def calculate():
    rows = int(rows_entry.get())
    columns = int(columns_entry.get())

    A = []
    b = []

    matrix_text = matrix_textbox.get("1.0", tk.END)
    matrix_lines = matrix_text.strip().split('\n')

    for i in range(rows):
        row_values = list(map(float, matrix_lines[i].split()))
        if len(row_values) != columns + 1:
            result_text.config(state='normal')
            result_text.delete(1.0, 'end')
            result_text.insert('end', f"Error in row {i + 1}: Each row must have {columns + 1} values.")
            result_text.config(state='disabled')
            return
        A.append(row_values[:columns])
        b.append(row_values[columns])

    if len(b) != rows:
        result_text.config(state='normal')
        result_text.delete(1.0, 'end')
        result_text.insert('end', "Error: The vector constants must have the same number of rows as the matrix coefficients.")
        result_text.config(state='disabled')
    else:
        solution = gaussian_elimination(A, b)
        if solution is not None:
            result_text.config(state='normal')
            result_text.insert('end', "\nSolution: " + " ".join([f"x{i + 1} = {sol:.4f}," for i, sol in enumerate(solution)]))
            result_text.config(state='disabled')

window = tk.Tk()
window.title("Gaussian Elimination Calculator")

tk.Label(window, text="Number of Rows In Coefficient Matrix:").grid(row=0, column=0)
rows_entry = tk.Entry(window)
rows_entry.grid(row=0, column=1, pady=(10, 10))

tk.Label(window, text="Number of Columns In Coefficient Matrix:").grid(row=1, column=0)
columns_entry = tk.Entry(window)
columns_entry.grid(row=1, column=1, pady=(10, 10))

matrix_label = tk.Label(window, text="Enter the matrix")
matrix_label.grid(row=2, column=0, columnspan=2)

matrix_textbox = tk.Text(window, height=10, width=50)
matrix_textbox.grid(row=3, column=0, columnspan=2)

calculate_button = tk.Button(window, text="Calculate", command=calculate)
calculate_button.grid(row=4, column=0, columnspan=2, pady=(10, 30))

result_text = tk.Text(window, height=35, width=100, state="normal")
result_text.grid(row=5, column=0, columnspan=2)

window.mainloop()
