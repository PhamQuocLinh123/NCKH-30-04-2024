import tkinter as tk
from tkinter import ttk
import pandas as pd

# Hàm để đọc dữ liệu từ tệp CSV và hiển thị nó trong giao diện Tkinter
def display_data():
    try:
        # Đọc dữ liệu từ tệp CSV
        df = pd.read_csv("Attendance/Attendance_16-04-2024.csv")

        # Tạo cửa sổ Tkinter
        root = tk.Tk()
        root.title("Data Display")

        # Tạo một bảng Treeview để hiển thị dữ liệu
        tree = ttk.Treeview(root)
        tree["columns"] = tuple(df.columns)
        tree.heading("#0", text="Index")
        for col in df.columns:
            tree.heading(col, text=col)

        # Thêm dữ liệu vào bảng Treeview
        for i, row in df.iterrows():
            tree.insert("", "end", text=i, values=tuple(row))

        # Định cấu hình cửa sổ
        tree.pack(expand=True, fill=tk.BOTH)

        # Chạy ứng dụng
        root.mainloop()
    except FileNotFoundError:
        print("File not found.")

# Gọi hàm để hiển thị dữ liệu
display_data()
