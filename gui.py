import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def calculate_sum():
    try:
        num1 = float(sum_entry1.get())
        num2 = float(sum_entry2.get())
        result = num1 + num2
        sum_output_label.config(text=f"Sum: {result}")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers")

def calculate_product():
    try:
        num1 = float(product_combobox.get())
        num2 = float(product_entry2.get())
        result = num1 * num2
        product_output_label.config(text=f"Product: {result}")
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid numbers")

# 创建主窗口
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("400x300")

# 创建 Notebook
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# 创建第一个标签页（计算和）
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text="Sum")

sum_label1 = tk.Label(frame1, text="Number 1:")
sum_label1.pack(pady=10)
sum_entry1 = tk.Entry(frame1, font=("Helvetica", 14))
sum_entry1.pack(pady=5)

sum_label2 = tk.Label(frame1, text="Number 2:")
sum_label2.pack(pady=10)
sum_entry2 = tk.Entry(frame1, font=("Helvetica", 14))
sum_entry2.pack(pady=5)

sum_button = tk.Button(frame1, text="Calculate", command=calculate_sum, font=("Helvetica", 14))
sum_button.pack(pady=20)

sum_output_label = tk.Label(frame1, text="Sum: ", font=("Helvetica", 14))
sum_output_label.pack(pady=10)

# 创建第二个标签页（计算积）
frame2 = ttk.Frame(notebook)
notebook.add(frame2, text="Product")

product_label1 = tk.Label(frame2, text="Number 1:")
product_label1.pack(pady=10)

product_combobox = ttk.Combobox(frame2, values=[1, 10, 100, 1000], font=("Helvetica", 14))
product_combobox.pack(pady=5)
product_combobox.current(0)  # 设置默认值

product_label2 = tk.Label(frame2, text="Number 2:")
product_label2.pack(pady=10)
product_entry2 = tk.Entry(frame2, font=("Helvetica", 14))
product_entry2.pack(pady=5)

product_button = tk.Button(frame2, text="Calculate", command=calculate_product, font=("Helvetica", 14))
product_button.pack(pady=20)

product_output_label = tk.Label(frame2, text="Product: ", font=("Helvetica", 14))
product_output_label.pack(pady=10)

# 运行主循环
root.mainloop()
