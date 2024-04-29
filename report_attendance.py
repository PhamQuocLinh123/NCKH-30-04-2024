import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_pdf import PdfPages
import mysql.connector
from datetime import datetime, timedelta

class Report:
    def __init__(self, root):
        self.root = root
        self.root.title("Thống Kê")
        self.root.geometry("1350x700")

        self.db = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "face_recognizer"
        }

        self.create_widgets()

    def create_widgets(self):
        self.tabControl = ttk.Notebook(self.root)
        self.tabControl.pack(expand=True, fill="both")

        self.tab_camera = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_camera, text="Đếm số lượng người từ camera")

        self.tab_count = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_count, text="Đếm số lượng người từ ảnh")

        self.tab_attendance = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_attendance, text="Xác nhận danh tính")

        self.create_camera_tab(self.tab_camera)
        self.create_count_tab(self.tab_count)
        self.create_attendance_tab(self.tab_attendance)

    def create_camera_tab(self, frame):
        self.label_camera = ttk.Label(frame, text="", font=("Arial", 14))
        self.label_camera.pack(pady=10)

        self.fig_camera = Figure(figsize=(6, 4), dpi=100)
        self.plot_camera = self.fig_camera.add_subplot(111)

        self.canvas_camera = FigureCanvasTkAgg(self.fig_camera, master=frame)
        self.canvas_camera.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.export_button_camera = ttk.Button(frame, text="Xuất PDF", command=lambda: self.export_to_pdf(self.fig_camera, "Thống kê đếm số lượng người từ camera.pdf"))
        self.export_button_camera.pack(pady=10)

        self.load_camera_data()

    def create_count_tab(self, frame):
        self.label_count = ttk.Label(frame, text="", font=("Arial", 14))
        self.label_count.pack(pady=10)

        self.fig_count = Figure(figsize=(6, 4), dpi=100)
        self.plot_count = self.fig_count.add_subplot(111)

        self.canvas_count = FigureCanvasTkAgg(self.fig_count, master=frame)
        self.canvas_count.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.export_button_count = ttk.Button(frame, text="Xuất PDF", command=lambda: self.export_to_pdf(self.fig_count, "Thống kê đếm số lượng người từ ảnh.pdf"))
        self.export_button_count.pack(pady=10)

        self.load_count_data()

    def create_attendance_tab(self, frame):
        self.label_attendance = ttk.Label(frame, text="", font=("Arial", 14))
        self.label_attendance.pack(pady=10)

        self.fig_attendance = Figure(figsize=(6, 4), dpi=100)
        self.plot_attendance = self.fig_attendance.add_subplot(111)

        self.canvas_attendance = FigureCanvasTkAgg(self.fig_attendance, master=frame)
        self.canvas_attendance.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.export_button_attendance = ttk.Button(frame, text="Xuất PDF", command=lambda: self.export_to_pdf(self.fig_attendance, "Thống kê xác nhận danh tính.pdf"))
        self.export_button_attendance.pack(pady=10)

        self.load_attendance_data()

    def load_camera_data(self):
        try:
            conn = mysql.connector.connect(**self.db)
            my_cursor = conn.cursor()

            query = "SELECT DATE(timestamp) AS day, COUNT(*) AS count FROM face_count_camera GROUP BY DATE(timestamp)"
            my_cursor.execute(query)
            data = my_cursor.fetchall()

            days = []
            counts = []
            for record in data:
                days.append(record[0].strftime("%Y-%m-%d"))
                counts.append(record[1])

            self.plot_camera.clear()
            self.plot_camera.bar(days, counts, color='blue')
            self.plot_camera.set_xlabel('Ngày')
            self.plot_camera.set_ylabel('Số lượng ')
            self.plot_camera.set_title('Thống kê đếm số lượng người từ camera')

            self.canvas_camera.draw()

            conn.close()
        except Exception as e:
            print("Error:", e)

    def load_count_data(self):
        try:
            conn = mysql.connector.connect(**self.db)
            my_cursor = conn.cursor()

            query = "SELECT DATE(timestamp) AS day, COUNT(*) AS count FROM face_count GROUP BY DATE(timestamp)"
            my_cursor.execute(query)
            data = my_cursor.fetchall()

            days = []
            counts = []
            for record in data:
                days.append(record[0].strftime("%Y-%m-%d"))
                counts.append(record[1])

            self.plot_count.clear()
            self.plot_count.bar(days, counts, color='green')
            self.plot_count.set_xlabel('Ngày')
            self.plot_count.set_ylabel('Số lượng ảnh')
            self.plot_count.set_title('Thống kê đếm số lượng người từ ảnh')

            self.canvas_count.draw()

            conn.close()
        except Exception as e:
            print("Error:", e)

    def load_attendance_data(self):
        try:
            conn = mysql.connector.connect(**self.db)
            my_cursor = conn.cursor()

            query = "SELECT Date, COUNT(*) FROM attendance GROUP BY Date"
            my_cursor.execute(query)
            data = my_cursor.fetchall()

            dates = []
            counts = []
            for record in data:
                dates.append(record[0])
                counts.append(record[1])

            self.plot_attendance.clear()
            self.plot_attendance.bar(dates, counts, color='red')
            self.plot_attendance.set_xlabel('Ngày')
            self.plot_attendance.set_ylabel('Số lượng danh tính')
            self.plot_attendance.set_title('Thống kê danh tính')

            self.canvas_attendance.draw()

            conn.close()
        except Exception as e:
            print("Error:", e)

    def export_to_pdf(self, fig, filename):
        try:
            filepath = r"D:\Nghiên cứu khoa học-2024\face_recognizer\Thong_Ke\\" + filename
            with PdfPages(filepath) as pdf:
                pdf.savefig(fig)
            messagebox.showinfo("Thông báo", "Xuất PDF thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Xảy ra lỗi khi xuất PDF: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Report(root)
    root.mainloop()
