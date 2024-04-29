import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import mysql.connector
from datetime import datetime
import os
import dlib


class Database_str:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'face_recognizer'
        self.port = '3306'


class FaceCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HỆ THỐNG ĐẾM SỐ LƯỢNG NGƯỜI TỪ ẢNH")
        self.root.geometry("1300x600")  # Set window size to 1000x600
        self.root.configure(background="#CCE5FF")  # Set background color to light blue

        self.db = Database_str()

        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#CCE5FF")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Title label
        title_label = tk.Label(main_frame, text="HỆ THỐNG ĐẾM SỐ LƯỢNG NGƯỜI TỪ ẢNH", font=("Arial", 26, "bold"), bg="#CCE5FF")
        title_label.pack(pady=10)

        # Frame for input image
        input_frame = tk.Frame(main_frame, bg="#CCE5FF")
        input_frame.pack(side="left", padx=10, pady=10)

        self.input_label = tk.Label(input_frame, text="Ảnh đầu vào:", font=("Arial", 12), bg="#CCE5FF")
        self.input_label.pack(pady=(10, 5))

        self.input_canvas = tk.Canvas(input_frame, width=400, height=300, bg="lightgray", highlightthickness=0)
        self.input_canvas.pack(padx=10, pady=10)

        # Frame for processed image
        processed_frame = tk.Frame(main_frame, bg="#CCE5FF")
        processed_frame.pack(side="right", padx=10, pady=10)

        self.processed_label = tk.Label(processed_frame, text="Ảnh sau khi xử lý:", font=("Arial", 12), bg="#CCE5FF")
        self.processed_label.pack(pady=(10, 5))

        self.processed_canvas = tk.Canvas(processed_frame, width=400, height=300, bg="lightgray", highlightthickness=0)
        self.processed_canvas.pack(padx=10, pady=10)

        # Button frame
        button_frame = tk.Frame(main_frame, bg="#CCE5FF")
        button_frame.pack(side="bottom", padx=10, pady=10)

        self.select_button = tk.Button(button_frame, text="Chọn Ảnh", command=self.select_image, font=("Arial", 10))
        self.select_button.pack(side="left", padx=10)

        self.count_button = tk.Button(button_frame, text="Bắt Đầu Đếm", command=self.count_faces, font=("Arial", 10))
        self.count_button.pack(side="left", padx=10)

        self.show_report_button = tk.Button(button_frame, text="Hiển Thị Danh Sách", command=self.open_show_face_count,
                                            font=("Arial", 10))
        self.show_report_button.pack(side="left", padx=10)

    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if hasattr(self, 'image_path'):
            self.image = cv2.imread(self.image_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.image = cv2.resize(self.image, (400, 300))
            self.display_input_image()

    def display_input_image(self):
        self.input_photo = tk.PhotoImage(data=cv2.imencode('.png', self.image)[1].tobytes())
        self.input_canvas.create_image(200, 150, anchor=tk.CENTER, image=self.input_photo)  # Center the image in canvas

    def count_faces(self):
        if hasattr(self, 'image_path'):
            num_faces, processed_image = self.count_faces_in_image(self.image_path)
            self.insert_face_count(self.image_path, num_faces)
            self.display_processed_image(processed_image, num_faces)
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn ảnh trước.")

    def count_faces_in_image(self, image_path):
        detector = dlib.get_frontal_face_detector()
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        # Draw bounding boxes around faces
        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

        return len(faces), image

    def display_processed_image(self, processed_image, num_faces):
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
        processed_image = cv2.resize(processed_image, (400, 300))
        self.processed_photo = tk.PhotoImage(data=cv2.imencode('.png', processed_image)[1].tobytes())
        self.processed_canvas.create_image(200, 150, anchor=tk.CENTER, image=self.processed_photo)  # Center the image in canvas
        self.processed_canvas.create_text(10, 10, anchor=tk.NW, text=f"Số lượng người: {num_faces}", fill="red",
                                          font=("Arial", 14, "bold"))

        # Save processed image with faces to 'img_face_count' directory
        save_dir = 'img_face_count'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_path = os.path.join(save_dir, os.path.basename(self.image_path))
        cv2.imwrite(save_path, cv2.cvtColor(processed_image, cv2.COLOR_RGB2BGR))
        print(f"Ảnh sau khi xử lý đã được lưu vào {save_path}")

    def insert_face_count(self, image_name, count):
        try:
            conn = mysql.connector.connect(
                host=self.db.host,
                user=self.db.user,
                password=self.db.password,
                database=self.db.database,
                port=self.db.port
            )
            cursor = conn.cursor()
            timestamp = datetime.now()

            # Lưu ảnh vào thư mục 'img_face_count'
            save_dir = 'img_face_count'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            save_path = os.path.join(save_dir, os.path.basename(image_name))
            cv2.imwrite(save_path, cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR))

            # Thêm bản ghi vào cơ sở dữ liệu
            cursor.execute("INSERT INTO face_count (image_name, timestamp, count) VALUES (%s, %s, %s)",
                           (save_path, timestamp, count))
            conn.commit()
            messagebox.showinfo("Thành công", "Số lượng khuôn mặt đã được thêm thành công.")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm số lượng khuôn mặt: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def open_show_face_count(self):
        # Mở cửa sổ hiển thị danh sách khuôn mặt đã đếm
        os.system("python show_face_count.py")


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceCounterApp(root)
    root.mainloop()